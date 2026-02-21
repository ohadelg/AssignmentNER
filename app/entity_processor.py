"""
entity_processor.py
────────────────────
Pure data-transformation layer: converts raw NER output into a structured
DataFrame and provides filtering utilities.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

import pandas as pd

from config import ENTITY_META

_MIN_ENTITY_LENGTH = 2
_MERGE_GAP = 3

# Entities whose class implies no internal spaces (IDs, hashes, filenames).
_COLLAPSE_SPACE_CLASSES = {"VULID", "SHA1", "SHA2", "MD5", "FILE", "URL", "EMAIL", "IP", "DOM"}

# Classes where two-part CamelCase words are almost always a single compound
# name (e.g. "Power Sploit" → "PowerSploit", "Hyper Bro" → "HyperBro").
_CAMELCASE_COLLAPSE_CLASSES = {"TOOL", "MAL", "APT", "ENCR"}

# Regex for IOB tag labels that leak into entity text.
_IOB_TAG_RE = re.compile(
    r"\s*[BI]-(?:SecTeam|Sec|HackOrg|Org|Mal|Tool|Act|Apt|Time|Loc|"
    r"Idty|Encr|File|Prot|VulName|VulId|Os|Sha2|Sha1|Md5|Url|Ip|Dom|Email)"
    r"\s*",
    re.IGNORECASE,
)


# ── Internal helpers ───────────────────────────────────────────────────────────

def _merge_adjacent(raw_entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Merge consecutive raw entity dicts that share the same entity_group and
    whose character spans are adjacent.
    """
    if not raw_entities:
        return []

    merged: list[dict[str, Any]] = []
    current = dict(raw_entities[0])

    for nxt in raw_entities[1:]:
        same_group = nxt.get("entity_group") == current.get("entity_group")
        gap = nxt.get("start", 0) - current.get("end", 0)
        adjacent = gap <= _MERGE_GAP

        if same_group and adjacent:
            current["word"] = current.get("word", "") + " " + nxt.get("word", "")
            current["end"] = nxt.get("end", current.get("end"))
            current["score"] = min(
                current.get("score", 1.0), nxt.get("score", 1.0)
            )
        else:
            merged.append(current)
            current = dict(nxt)

    merged.append(current)
    return merged


def _clean_word(word: str, entity_class: str) -> str:
    """
    Normalise a raw pipeline word. Steps:
    1. Remove BPE prefix markers (Ġ, ▁, ##).
    2. Strip leaked IOB tag labels (B-SecTeam, I-Sec, etc.).
    3. Collapse BPE-inserted spaces for structured classes (CVE IDs, files, hashes).
    4. Remove duplicated entity text ("GandCrab GandCrab" → "GandCrab").
    5. Strip isolated single-letter fragments.
    6. Strip outer punctuation junk.
    7. Normalise trailing possessive/fragment suffixes (" 's", " '").
    """
    # 1. BPE prefix markers
    word = re.sub(r"^[Ġ▁#]+", "", word)
    word = re.sub(r"\s+", " ", word).strip()

    # 2. Remove IOB tag labels that leaked into entity text
    word = _IOB_TAG_RE.sub(" ", word).strip()

    # 3. For structured classes, collapse all internal spaces
    if entity_class in _COLLAPSE_SPACE_CLASSES:
        word = re.sub(r"\s+", "", word)
    else:
        # Collapse BPE-fragmented words back together.
        parts = word.split()
        if len(parts) >= 3 and all(len(p) <= 3 for p in parts[1:]):
            # "PR OM ET HI UM" → "PROMETHIUM"
            word = "".join(parts)
        elif len(parts) == 2:
            p0, p1 = parts
            if p1[0].islower():
                # Second part starts lowercase → mid-word split
                # "Turkmen istan" → "Turkmenistan"
                word = p0 + p1
            elif len(p1) <= 2:
                # Short second fragment: "C 2" → "C2"
                word = p0 + p1
            elif p0.isupper() and p1.isupper():
                # Both all-uppercase → likely one word
                word = p0 + p1
            elif entity_class in _CAMELCASE_COLLAPSE_CLASSES:
                # Software/malware/APT names are usually single compound words
                # "Power Sploit" → "PowerSploit", "Hyper Bro" → "HyperBro"
                word = p0 + p1

    # 4. De-duplicate ("GandCrab GandCrab" → "GandCrab", "APT 10 APT 10" → "APT 10")
    word = re.sub(r"\s+", " ", word).strip()
    half = len(word)
    if half >= 4 and half % 2 == 0:
        mid = half // 2
        if word[:mid].strip() == word[mid:].strip():
            word = word[:mid].strip()
    # Also try with a space in the middle (odd-length due to separator)
    parts = word.split()
    if len(parts) >= 2 and len(parts) % 2 == 0:
        half_p = len(parts) // 2
        if parts[:half_p] == parts[half_p:]:
            word = " ".join(parts[:half_p])

    # 5. Remove isolated single-letter fragments (only if surrounded by spaces,
    #    not when the letter is the entire word or attached to digits like "C2")
    word = re.sub(r"(?<=\s)[A-Z](?=\s)", "", word)
    word = re.sub(r"\s+", " ", word).strip()

    # 6. Strip outer punctuation junk and stray hyphens/dashes
    word = word.strip("\"'`.,;:!?()[]{}|\\/@#$%^&*+=~<>- ")
    word = re.sub(r"[–—]+$", "", word).strip()

    # 7. Remove possessive artifacts
    word = re.sub(r"\s*'s?$", "", word).strip()

    # 8. Remove trailing lone " Exp" suffix that comes from the dataset labels
    word = re.sub(r"\s*-?\s*Exp$", "", word).strip()

    # Final whitespace normalisation
    word = re.sub(r"\s+", " ", word).strip()

    return word


def _is_valid(word: str) -> bool:
    if len(word) < _MIN_ENTITY_LENGTH:
        return False
    if not re.search(r"[A-Za-z0-9]", word):
        return False
    return True


# ── Public API ─────────────────────────────────────────────────────────────────

def aggregate(raw_entities: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Merge adjacent spans, clean entity text, then collapse into a
    deduplicated summary DataFrame with one row per (class, entity) pair.
    Case-insensitive deduplication: keeps the most common casing.
    """
    merged = _merge_adjacent(raw_entities)

    # First pass: count with original casing
    raw_counter: dict[tuple[str, str], int] = defaultdict(int)
    for ent in merged:
        group = ent.get("entity_group", "")
        word = _clean_word(ent.get("word", ""), group)
        if group and _is_valid(word):
            raw_counter[(group, word)] += 1

    # Second pass: case-insensitive merge (keep the casing with highest count)
    canonical: dict[tuple[str, str], str] = {}  # (class, lower) → best casing
    counter: dict[tuple[str, str], int] = defaultdict(int)  # (class, lower) → total count
    for (cls, word), cnt in raw_counter.items():
        key = (cls, word.lower())
        counter[key] += cnt
        if key not in canonical or cnt > raw_counter.get((cls, canonical[key]), 0):
            canonical[key] = word

    rows = [
        {
            "Class":       cls,
            "Description": ENTITY_META.get(cls, {}).get("label", cls),
            "Entity":      canonical[(cls, lower)],
            "Count":       count,
        }
        for (cls, lower), count in sorted(counter.items(), key=lambda x: -x[1])
    ]
    return pd.DataFrame(rows, columns=["Class", "Description", "Entity", "Count"])


def filter_by_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Case-insensitive substring search across Class, Description, and Entity.
    """
    query = query.strip()
    if not query:
        return df

    mask = (
        df["Class"].str.contains(query, case=False, na=False)
        | df["Description"].str.contains(query, case=False, na=False)
        | df["Entity"].str.contains(query, case=False, na=False)
    )
    return df[mask]


def summary_stats(df: pd.DataFrame) -> dict[str, int]:
    return {
        "unique_classes":  int(df["Class"].nunique()),
        "unique_entities": len(df),
        "total_mentions":  int(df["Count"].sum()),
    }
