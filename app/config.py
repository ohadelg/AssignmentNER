"""
config.py
─────────
Single source of truth for all application-level constants.

To add a new entity class: add one entry to ENTITY_META.
To change the NER model:   update MODEL_PATH.
To tweak theming colors:   update BADGE_PALETTE or individual "color" values in ENTITY_META.
"""

import os

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_PATH: str = os.path.join(os.path.dirname(__file__), "SecureBert-NER")

# ── Text chunking ──────────────────────────────────────────────────────────────
# Conservative character limit per chunk so that the model's 512-token window
# is never exceeded (assumes ~3–4 chars per token on average).
MAX_CHUNK_CHARS: int = 1800

# ── Entity metadata registry ───────────────────────────────────────────────────
# Each key is the raw entity_group returned by the HuggingFace pipeline.
# "label"  → human-readable description shown in the UI table.
# "color"  → hex accent color used in charts and badges.
# Adding a new class: insert a new entry here — nothing else needs to change.
ENTITY_META: dict[str, dict[str, str]] = {
    "TIME":    {"label": "Time Reference",             "color": "#60a5fa"},
    "LOC":     {"label": "Location",                   "color": "#34d399"},
    "SECTEAM": {"label": "Security Team",              "color": "#f472b6"},
    "TOOL":    {"label": "Tool / Software",            "color": "#fb923c"},
    "IDTY":    {"label": "Identity / Person",          "color": "#a78bfa"},
    "MAL":     {"label": "Malware",                    "color": "#f87171"},
    "APT":     {"label": "Advanced Persistent Threat", "color": "#ef4444"},
    "VULNAME": {"label": "Vulnerability Name",         "color": "#facc15"},
    "VULID":   {"label": "Vulnerability ID",           "color": "#fbbf24"},
    "ENCR":    {"label": "Encryption Method",          "color": "#818cf8"},
    "FILE":    {"label": "File",                       "color": "#94a3b8"},
    "SHA2":    {"label": "SHA-256 Hash",               "color": "#22d3ee"},
    "URL":     {"label": "URL",                        "color": "#4ade80"},
    "IP":      {"label": "IP Address",                 "color": "#2dd4bf"},
    "ACT":     {"label": "Action / Activity",          "color": "#c084fc"},
    "MD5":     {"label": "MD5 Hash",                   "color": "#38bdf8"},
    "DOM":     {"label": "Domain",                     "color": "#86efac"},
    "OS":      {"label": "Operating System",           "color": "#fdba74"},
    "SHA1":    {"label": "SHA-1 Hash",                 "color": "#67e8f9"},
    "EMAIL":   {"label": "Email Address",              "color": "#d946ef"},
    "PROT":    {"label": "Protocol",                   "color": "#a3e635"},
}

# Fallback color when an entity class is not in ENTITY_META.
FALLBACK_COLOR: str = "#00d4ff"

# ── Badge palette ──────────────────────────────────────────────────────────────
# (foreground, background) pairs cycled deterministically by class name hash.
BADGE_PALETTE: list[tuple[str, str]] = [
    ("#00d4ff", "rgba(0,212,255,0.12)"),
    ("#7c3aed", "rgba(124,58,237,0.15)"),
    ("#00ff88", "rgba(0,255,136,0.12)"),
    ("#f59e0b", "rgba(245,158,11,0.12)"),
    ("#ef4444", "rgba(239,68,68,0.12)"),
    ("#a855f7", "rgba(168,85,247,0.12)"),
    ("#06b6d4", "rgba(6,182,212,0.12)"),
    ("#ec4899", "rgba(236,72,153,0.12)"),
]

# ── Page settings ──────────────────────────────────────────────────────────────
PAGE_TITLE: str = "Secure Entity Extractor"
PAGE_ICON:  str = "🔐"
