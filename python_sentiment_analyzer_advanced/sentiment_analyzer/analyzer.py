"""
Core sentiment analysis logic.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Iterable, Optional
from collections import Counter

from . import preprocessing
from .lexicon import load_default_lexicon


@dataclass
class SentenceSentiment:
    sentence: str
    positive_count: int
    negative_count: int
    sentiment: str  # "positive", "negative", "neutral"
    score: float    # (pos - neg) / max(1, (pos+neg))


@dataclass
class DocumentSentiment:
    doc_id: str
    text: str
    sentences: List[SentenceSentiment]
    overall_sentiment: str
    overall_score: float
    positive_total: int
    negative_total: int
    token_count: int
    unique_token_count: int
    top_positive_words: List[Tuple[str, int]]
    top_negative_words: List[Tuple[str, int]]

    def to_dict(self) -> Dict:
        d = asdict(self)
        return d


class SentimentAnalyzer:
    """
    Simple lexicon-based sentiment analyzer.

    Attributes
    ----------
    positive_words : set[str]
    negative_words : set[str]
    """

    def __init__(self, positive_words: Iterable[str] | None = None, negative_words: Iterable[str] | None = None):
        if positive_words is None or negative_words is None:
            pos, neg = load_default_lexicon()
        else:
            pos, neg = set(positive_words), set(negative_words)
        self.positive_words = pos
        self.negative_words = neg

    def analyze_sentence(self, sentence: str) -> SentenceSentiment:
        tokens = preprocessing.tokenize(sentence)
        pos = sum(1 for t in tokens if t in self.positive_words)
        neg = sum(1 for t in tokens if t in self.negative_words)
        if pos > neg:
            label = "positive"
        elif neg > pos:
            label = "negative"
        else:
            label = "neutral"
        denom = max(1, pos + neg)
        score = (pos - neg) / denom
        return SentenceSentiment(
            sentence=sentence.strip(),
            positive_count=pos,
            negative_count=neg,
            sentiment=label,
            score=score,
        )

    def analyze_document(self, doc_id: str, text: str, top_n: int = 10) -> DocumentSentiment:
        sentences = preprocessing.split_sentences(text)
        sent_results = [self.analyze_sentence(s) for s in sentences]

        pos_total = sum(s.positive_count for s in sent_results)
        neg_total = sum(s.negative_count for s in sent_results)

        if pos_total > neg_total:
            overall_label = "positive"
        elif neg_total > pos_total:
            overall_label = "negative"
        else:
            overall_label = "neutral"

        denom = max(1, pos_total + neg_total)
        overall_score = (pos_total - neg_total) / denom

        tokens = list(preprocessing.iter_tokens([text]))
        token_count = len(tokens)
        freqs = Counter(tokens)

        pos_words = [(w, c) for w, c in freqs.items() if w in self.positive_words]
        neg_words = [(w, c) for w, c in freqs.items() if w in self.negative_words]

        pos_words.sort(key=lambda x: x[1], reverse=True)
        neg_words.sort(key=lambda x: x[1], reverse=True)

        return DocumentSentiment(
            doc_id=doc_id,
            text=text,
            sentences=sent_results,
            overall_sentiment=overall_label,
            overall_score=overall_score,
            positive_total=pos_total,
            negative_total=neg_total,
            token_count=token_count,
            unique_token_count=len(freqs),
            top_positive_words=pos_words[:top_n],
            top_negative_words=neg_words[:top_n],
        )

    def batch_analyze(
        self,
        documents: Iterable[Tuple[str, str]],
        top_n: int = 10,
    ) -> List[DocumentSentiment]:
        results: List[DocumentSentiment] = []
        for doc_id, text in documents:
            results.append(self.analyze_document(doc_id, text, top_n=top_n))
        return results
