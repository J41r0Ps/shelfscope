# Data Dictionary — ShelfScope

## Source

All data scraped from [books.toscrape.com](https://books.toscrape.com) — a sandbox site built
for scraping practice. 1000 books, 50 categories, collected in two passes (50 listing pages +
1000 detail pages).

**Critical caveat**: the site states that prices and ratings are randomly generated. This was
confirmed quantitatively in the analysis (see `04_exploration.ipynb`). No finding from the
numeric fields transfers to the real book market.

---

## `data/raw/books_raw.csv` — 1000 × 13

Direct scraper output. All values are unmodified strings as they appeared on the page.

| Column | Type | Source | Example | Notes |
|---|---|---|---|---|
| `title` | str | listing card, `h3 > a[title]` | `A Light in the Attic` | Full title from the attribute, not the truncated visible text |
| `price_raw` | str | listing card, `p.price_color` | `£51.77` | Currency symbol included |
| `availability_raw` | str | listing card, `p.instock.availability` | `In stock` | **Constant** across all 1000 rows |
| `star_rating_word` | str | listing card, `p.star-rating` 2nd CSS class | `Three` | Rating encoded as an English word in the class name |
| `detail_url` | str | listing card, `h3 > a[href]`, normalised | `https://books.toscrape.com/catalogue/...` | Join key between the two scraping passes |
| `category` | str | detail page breadcrumb, 3rd `<a>` | `Poetry` | Only available on the detail page |
| `description` | str | detail page, `<p>` after `#product_description` | `It's hard to imagine...` | 2 missing; text is duplicated on-page and ends with `...more` |
| `upc` | str | detail page product table | `a897fe39b1053632` | **1000 unique — the true primary key** |
| `price_excl_tax_raw` | str | detail page product table | `£51.77` | Identical to `price_raw` |
| `price_incl_tax_raw` | str | detail page product table | `£51.77` | Identical to `price_raw` |
| `tax_raw` | str | detail page product table | `£0.00` | **Constant** |
| `availability_detail_raw` | str | detail page product table | `In stock (22 available)` | Contains the actual stock count |
| `num_reviews_raw` | int | detail page product table | `0` | **Constant** — the site records no reviews |

---

## `data/processed/books_clean.csv` — 1000 × 8

Also available as `books_clean.json` (records-oriented).

| Column | Type | Derived from | Range / values | Transformation |
|---|---|---|---|---|
| `upc` | str | `upc` | 1000 unique | Unchanged — primary key |
| `title` | str | `title` | 999 unique | Unchanged |
| `category` | str | `category` | 50 values | Unchanged |
| `price` | float | `price_raw` | 10.00 – 59.99 | Regex `(\d+\.\d+)` |
| `rating` | int | `star_rating_word` | 1 – 5 | Dictionary lookup (`One`→1 … `Five`→5) |
| `stock` | int | `availability_detail_raw` | 1 – 22 | Regex `\((\d+)\s+available\)` |
| `description` | str | `description` | 998 present, 2 null | Unchanged |
| `detail_url` | str | `detail_url` | 1000 unique | Unchanged |

### Dropped columns and why

| Column | Reason |
|---|---|
| `availability_raw` | Constant (`In stock`) — 1 unique value |
| `tax_raw` | Constant (`£0.00`) — 1 unique value |
| `num_reviews_raw` | Constant (`0`) — 1 unique value |
| `price_excl_tax_raw` | Identical to `price_raw` (tax is always zero) |
| `price_incl_tax_raw` | Identical to `price_raw` |

All three regex/lookup parsers succeeded on all 1000 rows — **zero nulls introduced**.
**No rows were dropped.** Row count is 1000 at every stage.

---

## Known data quality issues

| Issue | Detail | Handling |
|---|---|---|
| Non-genre categories | `Default` (152 books) and `Add a comment` (67) are not genres. `Add a comment` is a UI element captured as a breadcrumb — a site-side error. 219 books / 22% of the dataset. | Retained and documented. Excluded from genre-level conclusions. |
| Long-tailed categories | 25 of 50 categories contain fewer than 10 books; several contain exactly 1. | Category analysis restricted to categories with n ≥ 10. |
| Duplicate title | *The Star-Touched Queen* appears twice, with different UPCs (`1528279aec1f3dce` / `4a7a25be293ad678`) and prices (£46.02 / £32.30). | Both kept — genuine separate catalogue entries. `upc` used as key instead of `title`. |
| Missing descriptions | 2 books have no description on the site. | Kept as `NaN`, not imputed. Not used in quantitative analysis. |
| Duplicated description text | Descriptions repeat their first ~250 characters and end with `...more`. | Not cleaned — descriptions are not analysed in this project. Would need handling for any text analysis. |
| Synthetic numeric data | Price, rating and stock are randomly generated. | Treated as the central caveat throughout; the analysis is framed as a methodological exercise. |