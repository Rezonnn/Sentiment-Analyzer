import json
import re
from collections import Counter
from pathlib import Path

POSITIVE_WORDS = {"good","great","awesome","amazing","love","excellent","happy","fantastic","nice","positive"}
NEGATIVE_WORDS = {"bad","terrible","awful","hate","poor","sad","horrible","negative","worst","angry"}

def clean_text(text):
    return re.sub(r"[^a-zA-Z ]","", text).lower().split()

def analyze_sentiment(text):
    words = clean_text(text)
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    return {
        "positive": pos,
        "negative": neg,
        "sentiment": "positive" if pos>neg else "negative" if neg>pos else "neutral"
    }

def analyze_file(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    return analyze_sentiment(text)

def main():
    print("=== Simple Sentiment Analyzer ===")
    print("1. Analyze custom text")
    print("2. Analyze a text file")
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        text = input("Enter text: ")
        result = analyze_sentiment(text)
    elif choice == "2":
        path = input("Enter file path: ").strip()
        if not Path(path).exists():
            print("File not found.")
            return
        result = analyze_file(path)
    else:
        print("Invalid choice.")
        return

    print("\n--- Result ---")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
