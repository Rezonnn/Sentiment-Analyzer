"""
Lexicon loading utilities.

By default, loads positive/negative word lists from data/*.txt in the package.
"""
from __future__ import annotations

from importlib import resources
from typing import Set, Tuple


def _load_wordlist(name: str) -> Set[str]:
    try:
        data = resources.files("sentiment_analyzer.data").joinpath(name).read_text(encoding="utf-8")
    except Exception:
        # Fallback for older Python, though this code is mainly for 3.9+
        with resources.open_text("sentiment_analyzer.data", name, encoding="utf-8") as f:  # type: ignore[arg-type]
            data = f.read()
    words = set()
    for line in data.splitlines():
        line = line.strip().lower()
        if not line or line.startswith("#"):
            continue
        words.add(line)
    return words


def load_default_lexicon() -> Tuple[Set[str], Set[str]]:
    positive = _load_wordlist("positive_words.txt")
    negative = _load_wordlist("negative_words.txt")
    return positive, negative
