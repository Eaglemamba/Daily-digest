## name: nightly-publisher

description: Nightly pipeline agent — processes queue files to generate bilingual educational HTMLs for each selected article, then rebuilds indexes across all content repos.
version: 1.0.0
last_updated: 2026-04-13

# Nightly Publisher & Maintenance Skill

**Version:** 1.0.0

## Overview

Runs at 01:00 TST every night. Two phases:

1. **Publisher** — reads `queue/YYYY-MM-DD.json` (dropped by user after Daily Digest review), generates bilingual educational HTMLs, routes to correct repos
2. **Maintenance** — rebuilds indexes across all content repos, commits and pushes

## Trigger Schedule

- **Cron**: `0 1 * * *` (01:00 TST daily)
- **Repos**: Daily-digest, Pharma-news-decipher, Harvard-Business-Review, david-ai-learning

---

## Queue File Format

User drops `YYYY-MM-DD.json` into `Daily-digest/queue/` after reviewing the daily digest.

```json
{
  "date": "2026-04-13",
  "exported_at": "2026-04-13T23:15:00+08:00",
  "articles": [
    {
      "id": "unique-string-id",
      "route": "pharma-decipher",
      "category": "FDA+",
      "title": "FDA Approves New ALK Inhibitor",
      "source": "Endpoints News",
      "url": "https://endpointsnews.com/...",
      "date": "2026-04-13",
      "time_tst": "14:30",
      "summary": "FDA accelerated approval for 4th gen ALK inhibitor",
      "full_content": "Full article text extracted from newsletter email body..."
    }
  ]
}
```

### Route → Repo Mapping

| Route | Target Repo | Index Script |
|-------|-------------|--------------|
| `pharma-decipher` | `Pharma-news-decipher/docs/` | `python3 build_index.py` |
| `hbr-review` | `Harvard-Business-Review/docs/` | `python3 build_index.py` |
| `ai-articles` | `david-ai-learning/docs/` | `node auto-classify.js` |

---

## Execution Workflow

### Step 0: Discover repo directories

```bash
ls -la
```

---

### PHASE 1: Publisher

#### 1.1 Check queue

```bash
ls Daily-digest/queue/*.json 2>/dev/null
```

If no `.json` files found (only .gitkeep): output `[Publisher] No queue files. Skipping.` and jump to PHASE 2.

#### 1.2 Process each queue file

For each `Daily-digest/queue/YYYY-MM-DD.json`:

1. Read and parse the `articles` array
2. Group articles by `route`
3. Generate bilingual HTML for each article (see §1.3)
4. Move queue file to processed:
   ```bash
   mv Daily-digest/queue/YYYY-MM-DD.json Daily-digest/queue/processed/
   ```
5. Commit Daily-digest:
   ```bash
   cd Daily-digest
   git add queue/
   git commit -m "Auto: processed queue YYYY-MM-DD"
   git push origin main
   cd ..
   ```

#### 1.3 Generating Bilingual HTML Per Article

**File naming:** `YYYY-MM-DD_short-title.html`
- `YYYY-MM-DD` = article's `date` field
- `short-title` = 3–5 words from title, lowercase, hyphens only (e.g. `fda-approves-alk-inhibitor`)

**Steps for each article:**

1. Read the target repo's `CLAUDE.md` for HTML format instructions (meta tags, template, box types, available tags)
2. Generate a complete bilingual Traditional Chinese / English educational HTML using the article's `title`, `source`, `date`, `url`, `summary`, `full_content`, and `category`
3. Required `<meta>` tags:
   - `doc-date` — article `date`
   - `doc-title` — Chinese title (translate/adapt the English title)
   - `doc-source` — article `source`
   - `doc-tags` — comma-separated tags appropriate for the repo (see target CLAUDE.md Available Tags)
   - `doc-rating` — assign 3.5–4.8 based on article significance
   - `doc-summary` — ≤30 chars Traditional Chinese one-liner
   - `doc-file` — the filename (`YYYY-MM-DD_short-title.html`)
4. Write the HTML file to the target repo's `docs/` folder
5. Report: `[route] Generated: FILENAME`

**Content quality guidelines:**

- `full_content` is the raw newsletter text — use it as source material for analysis
- Structure the HTML as a bilingual educational document (not just a translation)
- Use `.bilingual-block` with `.zh-text` / `.en-text` for all major sections
- Required sections: Executive Summary, Key Concepts, Analysis/Implications, Practical Takeaway
- Use appropriate box types per the CLAUDE.md (`box-concept`, `box-key`, `box-practical`, `box-warning`, `box-compare`, `box-cost`)
- Rating bars: assess each dimension individually (Clinical/Technical/Business significance)
- Link `<link rel="stylesheet" href="styles.css">` — do NOT use inline CSS

---

### PHASE 2: Maintenance

Rebuild indexes for all content repos.

#### Repo 1: david-ai-learning

```bash
cd david-ai-learning
node auto-classify.js --dry-run
# If 0 new files → skip
# If new files:
node auto-classify.js
git add docs/processed/ dashboard-data.js search-index.js curriculum-data.js
git commit -m "Auto: classify N new doc(s) (YYYY-MM-DD)"
git push origin main
cd ..
```

#### Repo 2: Pharma-news-decipher

```bash
cd Pharma-news-decipher
python3 build_index.py
git diff --quiet docs/index.html
# Exit 0 → no change, skip
# Exit 1 → changed:
git add docs/
git commit -m "Auto: rebuild index (YYYY-MM-DD)"
git push origin main
cd ..
```

#### Repo 3: Harvard-Business-Review

```bash
cd Harvard-Business-Review
python3 build_index.py
git diff --quiet docs/index.html
# Exit 0 → no change, skip
# Exit 1 → changed:
git add docs/
git commit -m "Auto: rebuild index (YYYY-MM-DD)"
git push origin main
cd ..
```

---

### Final Summary Output

```
=== Nightly Pipeline Summary (YYYY-MM-DD) ===
[Publisher]
  Queue files processed: N
  Articles generated: N (pharma: X, hbr: Y, ai: Z)

[Maintenance]
  david-ai-learning:       [Classified N | No change]
  Pharma-news-decipher:    [Updated N articles | No change]
  Harvard-Business-Review: [Updated N articles | No change]
```

---

## Notes

- If `git push` fails: `git pull --rebase origin main` then retry
- If a repo directory is not found: skip and note `[REPO] Directory not found — skipping.`
- Use today's actual date (TST) in all commit messages
- Do NOT manually edit any `index.html` article arrays — always use the scripts

---

## Changelog

### v1.0.0 (2026-04-13)
- Initial release
- Two-phase pipeline: Publisher + Maintenance
- Supports pharma-decipher, hbr-review, ai-articles routes
- Queue-based JSON file trigger
