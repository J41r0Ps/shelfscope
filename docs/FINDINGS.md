# Findings — ShelfScope

A standalone summary of results. Full working in `notebooks/04_exploration.ipynb`.

---

## Headline

The numeric data on books.toscrape.com is synthetic, and five independent lines of evidence
confirm it. The analytically interesting findings are in the **category** field — the only
variable reflecting genuine editorial decisions — where 22% of entries turned out to be
unusable non-genres.

---

## Evidence that the numeric data is generated

| Test | Result | Interpretation |
|---|---|---|
| Price distribution | Flat, £10.00–£59.99, skew −0.037 | Uniform; real prices are right-skewed and cluster at price points |
| Rating distribution | 226/196/203/179/196 across 1–5 | Near-uniform; real ratings skew toward 4–5 |
| Pearson correlations | price↔rating +0.028, price↔stock −0.011, rating↔stock +0.016 | No linear relationship anywhere |
| Category price effect | Permutation test, p = 0.977 | Genre does not influence price |
| Outlier detection | 0 outliers by IQR and z-score | No distributional tails to contain outliers |

## Data quality findings

**Non-genre categories — 219 books (22%)**

| Category | Books | Problem |
|---|---|---|
| `Default` | 152 | Placeholder for unclassified books |
| `Add a comment` | 67 | UI element captured as a breadcrumb |

Notably invisible to standard quality checks: `category` had 50 unique values and zero missing.
The values are present, just meaningless. Only frequency ranking exposed it.

**Long-tailed category distribution** — 25 of 50 categories hold under 10 books. Per-category
statistics on those are noise.

**Stock is multimodal** — clusters at 3 copies and 14–16, sparse band at 9–13. The only numeric
variable with real structure, likely assigned from discrete pools rather than a continuous range.

## The permutation test

Category mean prices ranged from £39.79 (Travel) to £31.41 (Food and Drink) — an £8.38 spread
that reads as a finding once sorted.

Shuffling category labels 2000 times and recomputing the spread produced a mean of £13.27 under
pure chance, with 97.7% of shuffles exceeding the observed value. The observed spread sits in
the **left** tail — category means are more tightly clustered than random assignment produces.

**Conclusion**: no evidence of genre-driven pricing. Had genres carried real pricing structure,
the spread would have landed in the right tail.

**Caveat**: the left-tail position is reported but not fully explained. The range statistic is
dominated by the smallest categories, where random draws swing widest; a more careful null model
would account for that interaction.

## Methodological lessons

1. **Summary statistics are not a substitute for plots.** Stock's skew (+0.212) reads as "mildly
   right-skewed" and misses its multimodality entirely.
2. **A ranked table of group means always looks like a finding.** Sorting guarantees an apparent
   ordering; only a null model distinguishes signal from noise.
3. **Outlier detection encodes distributional assumptions.** The IQR fences for price
   (−£15.92 → £85.48) fell entirely outside the data range (£10–£59.99). Zero outliers meant the
   method didn't fit the data, not that the data was clean.
4. **Missing-value checks don't catch meaningless values.** The `Add a comment` category was
   fully populated and completely useless.

## What this dataset cannot support

- Any claim about real book-market pricing, ratings, or demand.
- Genre-level conclusions, given 22% unusable category labels.
- Predictive modelling — with all correlations near zero, there is nothing to predict from.

## Natural next steps

- **Text analysis of descriptions** — the one field with genuine human-written content. Length
  distribution, keyword extraction, sentiment by genre. Would require handling the on-page text
  duplication first.
- **Enrichment via an external API** (Open Library, Google Books) to attach real publication years
  and page counts, giving genuine variables to correlate against.