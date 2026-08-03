# 📚 ShelfScope — Scraped & API-Enriched Book Market Analysis

> A Data Science pipeline that scrapes a live book-catalog site, enriches it with real-world
> metadata from a public API, and runs a full OSEMN cycle (Obtain → Scrub → Explore → Interpret)
> to uncover patterns in pricing, ratings, and publication data.

**Status**: 🚧 In progress.

## 🎯 Project goal

Most course-level data projects use a single, ready-made CSV. ShelfScope instead builds the
entire data pipeline from scratch, using two different acquisition methods:

1. **Scrape** ~1000 books from [books.toscrape.com](https://books.toscrape.com) (title, price,
   star rating, stock, category, description).
2. **Enrich** that data via the [Open Library API](https://openlibrary.org/developers/api) to pull
   real-world metadata (author, original publish year, page count, subjects).
3. **Merge, clean, explore** the combined dataset with Pandas/NumPy, visualize with
   Matplotlib/Seaborn, and document every finding in narrated Jupyter notebooks.

## 🗂️ Data sources

| Source | Type | What it provides | Notes |
|---|---|---|---|
| books.toscrape.com | Web scraping | title, price, rating, stock, category, UPC, description | Sandbox site — prices/ratings are placeholder data |
| Open Library API | Public REST API | real author, publish year, page count, subjects | Free, no key; not every title matches |

## 🧬 Pipeline (OSEMN)

| Stage | Notebook | Output |
|---|---|---|
| Obtain (scrape) | `01_scraping.ipynb` | `data/raw/books_raw.csv` |
| Obtain (API) | `02_api_enrichment.ipynb` | `data/raw/books_enriched_raw.csv` |
| Scrub | `03_cleaning.ipynb` | `data/processed/books_clean.csv` |
| Explore | `04_exploration.ipynb` | charts + findings |

## 📁 Structure

```
shelfscope/
├── data/raw/
├── data/processed/
├── notebooks/
├── src/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Setup

```
python3 -m venv venv
source venv/bin/activate      # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
jupyter notebook
```

## 🛣️ Roadmap
- [x] Repo scaffolding
- [ ] Scraper built + tested
- [ ] API enrichment + match-rate report
- [ ] Cleaning & merge
- [ ] Exploratory analysis
- [ ] Findings write-up

## ⚠️ Limitations
- books.toscrape.com prices/ratings are placeholder, not real market data.
- Open Library matches aren't guaranteed exact; unmatched rows are flagged, not dropped.
