"""
Command-line interface for the sentiment analyzer.

Supports:
- Analyzing raw text via --text
- Analyzing a single file via --file
- Analyzing all .txt files in a directory via --dir
- Exporting results to JSON and/or CSV
"""
from __future__ import annotations

import argparse
import json
import csv
from pathlib import Path
from typing import Iterable, Tuple, List

from .analyzer import SentimentAnalyzer, DocumentSentiment


def _iter_directory(dir_path: Path) -> Iterable[Tuple[str, str]]:
    for p in sorted(dir_path.glob("*.txt")):
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="latin-1")
        yield p.name, text


def _single_document(doc_id: str, text: str) -> Iterable[Tuple[str, str]]:
    yield doc_id, text


def run_cli(args: argparse.Namespace) -> List[DocumentSentiment]:
    analyzer = SentimentAnalyzer()
    docs: Iterable[Tuple[str, str]]

    if args.text:
        docs = _single_document("input_text", args.text)
    elif args.file:
        path = Path(args.file)
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        text = path.read_text(encoding="utf-8")
        docs = _single_document(path.name, text)
    elif args.dir:
        dir_path = Path(args.dir)
        if not dir_path.exists() or not dir_path.is_dir():
            raise SystemExit(f"Not a directory: {dir_path}")
        docs = _iter_directory(dir_path)
    else:
        raise SystemExit("You must specify one of --text, --file, or --dir")

    results = analyzer.batch_analyze(docs)

    # Console summary
    for doc in results:
        print("=" * 72)
        print(f"Document: {doc.doc_id}")
        print(f"Overall sentiment: {doc.overall_sentiment} (score={doc.overall_score:.3f})")
        print(f"Tokens: {doc.token_count}  Unique: {doc.unique_token_count}")
        print(f"Positive words: {doc.positive_total}  Negative words: {doc.negative_total}")
        print("-" * 72)
        print("Top positive words:")
        if doc.top_positive_words:
            for w, c in doc.top_positive_words:
                print(f"  {w:<15} {c}")
        else:
            print("  (none)")
        print("Top negative words:")
        if doc.top_negative_words:
            for w, c in doc.top_negative_words:
                print(f"  {w:<15} {c}")
        else:
            print("  (none)")
        print()

    # Export JSON
    if args.json:
        out_path = Path(args.json)
        payload = [doc.to_dict() for doc in results]
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"JSON report written to {out_path}")

    # Export CSV (per-document summary)
    if args.csv:
        out_path = Path(args.csv)
        fieldnames = [
            "doc_id",
            "overall_sentiment",
            "overall_score",
            "positive_total",
            "negative_total",
            "token_count",
            "unique_token_count",
        ]
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for doc in results:
                writer.writerow({
                    "doc_id": doc.doc_id,
                    "overall_sentiment": doc.overall_sentiment,
                    "overall_score": f"{doc.overall_score:.3f}",
                    "positive_total": doc.positive_total,
                    "negative_total": doc.negative_total,
                    "token_count": doc.token_count,
                    "unique_token_count": doc.unique_token_count,
                })
        print(f"CSV report written to {out_path}")

    return results


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentiment-analyzer",
        description="Lexicon-based sentiment analyzer (sentence + document level)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Raw text to analyze")
    group.add_argument("--file", type=str, help="Path to a text file to analyze")
    group.add_argument("--dir", type=str, help="Directory of .txt files to analyze in batch")

    parser.add_argument("--json", type=str, help="Optional path to write JSON report")
    parser.add_argument("--csv", type=str, help="Optional path to write CSV summary report")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    run_cli(args)


if __name__ == "__main__":
    main()
