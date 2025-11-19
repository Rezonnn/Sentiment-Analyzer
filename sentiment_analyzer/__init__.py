"""
Advanced sentiment analyzer package.

Provides tools to:
- Clean and tokenize text
- Analyze sentiment at sentence and document level
- Run batch analyses over directories of .txt files
"""
from .analyzer import SentimentAnalyzer, DocumentSentiment, SentenceSentiment  # noqa: F401
