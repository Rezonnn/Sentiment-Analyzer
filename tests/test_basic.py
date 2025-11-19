from sentiment_analyzer.analyzer import SentimentAnalyzer

def test_simple_positive():
    sa = SentimentAnalyzer()
    doc = sa.analyze_document("test", "I love this. It is awesome and amazing!")
    assert doc.overall_sentiment == "positive"
    assert doc.positive_total > doc.negative_total

def test_simple_negative():
    sa = SentimentAnalyzer()
    doc = sa.analyze_document("test", "This is terrible. I hate it. Worst ever.")
    assert doc.overall_sentiment == "negative"
    assert doc.negative_total > doc.positive_total
