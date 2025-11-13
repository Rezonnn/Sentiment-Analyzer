# 🧠 Advanced Python Sentiment Analyzer

A more **complete and structured** sentiment analysis project in Python – great for your GitHub portfolio.

This version goes beyond a tiny script and includes:

- A reusable **package** (`sentiment_analyzer/`)
- Sentence-level and document-level sentiment
- Batch analysis over a directory of `.txt` files
- JSON and CSV **reports**
- A proper **CLI** built with `argparse`
- Small but extendable **lexicon files**
- Basic **unit tests**

---

## 📂 Project Structure

```text
python_sentiment_analyzer_advanced/
├─ main.py                      # Simple entrypoint: python main.py --text "..."
├─ sentiment_analyzer/
│  ├─ __init__.py
│  ├─ analyzer.py               # Core sentiment logic + dataclasses
│  ├─ preprocessing.py          # Sentence splitting & tokenization
│  ├─ lexicon.py                # Lexicon loading utilities
│  └─ data/
│     ├─ positive_words.txt
│     └─ negative_words.txt
├─ tests/
│  └─ test_basic.py             # Small pytest-style tests
└─ README.md
```

---

## ✨ Features

- **Sentence-level sentiment** with:
  - positive / negative word counts
  - per-sentence sentiment label
  - per-sentence score `(pos - neg) / (pos + neg)`
- **Document-level sentiment** with:
  - overall positive / negative totals
  - overall label and score
  - token count & unique token count
  - top positive / negative words
- **Batch mode**:
  - Analyze all `.txt` files in a folder
  - Export JSON and CSV summaries

---

## ▶️ How to Run

From the project root:

```bash
python3 main.py --text "I love this project, but the docs are a bit poor."
```

Analyze a **single file**:

```bash
python3 main.py --file path/to/file.txt
```

Analyze a **directory** of `.txt` files:

```bash
python3 main.py --dir path/to/texts/ --json report.json --csv summary.csv
```

---

## 🧪 Running Tests

Tests are simple `pytest`-style functions. If you have `pytest` installed:

```bash
pytest
```

(If you don't want tests, you can still run the project fine without `pytest`.)

---

## 🧩 Extending the Project

Ideas to grow it further:

- Add a larger lexicon (e.g., from external sources)
- Add **negation handling** ("not good", "no fun")
- Build a tiny **Flask** or **FastAPI** web API using this package
- Add a **Jupyter notebook** that visualizes results

This project is already “portfolio-ready” as a **modular Python codebase** that shows structure, CLI design, text processing, and simple NLP.
