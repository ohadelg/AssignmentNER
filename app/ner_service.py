"""
ner_service.py
──────────────
Defines the NER abstraction layer and provides both Local and Remote implementations.

SOLID notes
───────────
S – Single Responsibility: this module owns only model loading and inference.
O – Open / Closed: to add a new model (e.g. CyNER), subclass NERProvider and
    register it — existing code stays untouched.
L – Liskov Substitution: any NERProvider subclass can replace another without
    the caller noticing.
D – Dependency Inversion: app.py depends on NERProvider (the abstraction),
    not on SecureBertNERProvider (the concrete implementation).
"""

from __future__ import annotations

import abc
from collections.abc import Callable
from typing import Any

import torch
import requests
import streamlit as st
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from config import MAX_CHUNK_CHARS, MODEL_PATH, BACKEND_URL


# ── Abstract interface ─────────────────────────────────────────────────────────

class NERProvider(abc.ABC):
    """Contract that every NER back-end must satisfy."""

    @abc.abstractmethod
    def extract(
        self,
        text: str,
        on_chunk: Callable[[int, int], None] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Run named-entity recognition on *text* and return a list of entity
        dicts, each containing at least:
            - "entity_group" (str)
            - "word"         (str)
            - "score"        (float)

        *on_chunk(current, total)* is called after each chunk is processed so
        callers can drive a progress bar without knowing about chunking internals.
        """


# ── Text chunking helper (shared by any provider that needs it) ────────────────

def _chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """
    Split *text* into chunks that stay within *max_chars* so that the model's
    512-token context window is never exceeded.

    Strategy: greedily accumulate sentences (split on '. ') until the next
    sentence would overflow, then start a new chunk.
    """
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current = ""
    for sentence in text.replace("\n", " \n ").split(". "):
        candidate = current + sentence + ". "
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence + ". "
    if current.strip():
        chunks.append(current.strip())

    return chunks or [text[:max_chars]]


# ── SecureBERT implementation (Local) ──────────────────────────────────────────

class SecureBertNERProvider(NERProvider):
    """
    NER provider backed by the local SecureBERT-NER model.
    Used by the backend server.
    """

    def __init__(self, model_path: str = MODEL_PATH) -> None:
        self._model_path = model_path
        self._pipeline = self._load_pipeline()

    def _load_pipeline(self) -> Any:
        device = 0 if torch.cuda.is_available() else -1
        tokenizer = AutoTokenizer.from_pretrained(self._model_path)
        model = AutoModelForTokenClassification.from_pretrained(self._model_path)
        return pipeline(
            "ner",
            model=model,
            tokenizer=tokenizer,
            aggregation_strategy="simple",
            device=device,
        )

    def extract(
        self,
        text: str,
        on_chunk: Callable[[int, int], None] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Chunk *text* into model-safe pieces, run the pipeline on each, and
        return the concatenated list of raw entity dicts.
        """
        chunks = _chunk_text(text)
        total = len(chunks)
        results: list[dict[str, Any]] = []
        for i, chunk in enumerate(chunks, start=1):
            try:
                results.extend(self._pipeline(chunk))
            except Exception:
                pass
            if on_chunk:
                on_chunk(i, total)
        return results


# ── Remote implementation (Frontend) ───────────────────────────────────────────

class RemoteNERProvider(NERProvider):
    """
    NER provider that communicates with a remote FastAPI backend.
    Used by the Streamlit frontend.
    """
    def __init__(self, backend_url: str = BACKEND_URL) -> None:
        self._backend_url = backend_url

    def extract(
        self,
        text: str,
        on_chunk: Callable[[int, int], None] | None = None,
    ) -> list[dict[str, Any]]:
        chunks = _chunk_text(text)
        total = len(chunks)
        results: list[dict[str, Any]] = []
        
        for i, chunk in enumerate(chunks, start=1):
            try:
                response = requests.post(
                    f"{self._backend_url}/extract",
                    json={"text": chunk},
                    timeout=60
                )
                response.raise_for_status()
                results.extend(response.json()["entities"])
            except Exception as e:
                # We use st.error here as it's intended for the Streamlit UI
                st.error(f"Error communicating with backend: {e}")
            
            if on_chunk:
                on_chunk(i, total)
                
        return results
