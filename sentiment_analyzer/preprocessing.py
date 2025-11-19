"""
Text cleaning and sentence/token utilities.
"""
from __future__ import annotations

import re
from typing import Iterable, List

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_TOKEN_RE = re.compile(r"[^a-zA-Z']+")


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    parts = _SENTENCE_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def tokenize(text: str) -> List[str]:
    text = text.lower()
    text = _TOKEN_RE.sub(" ", text)
    tokens = [t for t in text.split() if t]
    return tokens


def iter_tokens(texts: Iterable[str]) -> Iterable[str]:
    for t in texts:
        for token in tokenize(t):
            yield token
