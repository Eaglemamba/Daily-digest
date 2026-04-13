# Pharma News Decipher — Claude Code Instructions

## Core System

- All article HTML files live in `docs/` directory
- Naming pattern: `YYYY-MM-DD_short-title.html` (e.g., `2026-04-13_fda-approves-alk-inhibitor.html`)
- Each article uses `<link rel="stylesheet" href="styles.css">` for consistent styling
- Dashboard lives at `docs/index.html`

## Metadata Convention

Every article HTML must include these meta tags in `<head>`:

```html
<meta name="doc-date" content="2026-04-13">
<meta name="doc-title" content="FDA 批准新型 ALK 抑制劑">
<meta name="doc-source" content="Endpoints News">
<meta name="doc-tags" content="FDA,Oncology,Pipeline">
<meta name="doc-rating" content="4.5">
<meta name="doc-summary" content="FDA 加速批准第四代 ALK 抑制劑，為 NSCLC 患者帶來新選擇。">
<meta name="doc-file" content="2026-04-13_fda-approves-alk-inhibitor.html">
```

## Index Generation

- **Do NOT manually edit** the `const articles = [...]` block in `docs/index.html`
- Run `python build_index.py` to regenerate the article list from meta tags
- The script scans all `docs/*.html` files (excluding `index.html`), extracts meta tags, and injects a sorted array between the `AUTO-GENERATED START` and `AUTO-GENERATED END` markers

## Available Tags

Use these standardized tags for pharma articles:

| Tag | Usage |
|-----|-------|
| FDA | FDA decisions, approvals, CRLs, advisory committees |
| Clinical | Clinical trial results, data readouts, phase transitions |
| Deals | M&A, licensing deals, partnerships, collaborations |
| Pipeline | Drug pipeline updates, R&D milestones |
| Financing | IPOs, fundraising, venture rounds |
| Policy | Healthcare policy, pricing, reimbursement |
| Biotech | Biotech company news, platform technology |
| ADC | Antibody-drug conjugates specifically |
| Oncology | Cancer-related therapeutics and research |
| Regulatory | Regulatory filings, submissions, global approvals |

## Article HTML Template

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="doc-date" content="YYYY-MM-DD">
    <meta name="doc-title" content="Title here">
    <meta name="doc-source" content="Source here">
    <meta name="doc-tags" content="Tag1,Tag2">
    <meta name="doc-rating" content="4.0">
    <meta name="doc-summary" content="Summary here">
    <meta name="doc-file" content="YYYY-MM-DD_short-title.html">
    <title>Title here</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Article content using bilingual blocks, info boxes, etc. -->
</body>
</html>
```

## Newsletter Sources

- **Endpoints News** — pharma/biotech industry news
- **BioPharma Dive** — biopharma business and clinical news
- **PDA (Pharma Deal Analyst)** — M&A and deal analysis
- **STAT News** — health and medicine reporting
- **FiercePharma** — pharma industry news

## Bilingual Format

All content should be bilingual Traditional Chinese/English using:
- `.bilingual-block` wrapper
- `.zh-text` for Traditional Chinese
- `.en-text` for English

## Box Types for Analysis

- `.box-concept` — Core concepts and definitions
- `.box-analogy` — Analogies and comparisons
- `.box-key` — Key insights and takeaways
- `.box-practical` — Practical implications
- `.box-warning` — Risks and cautions
- `.box-compare` — Competitive landscape comparisons
- `.box-cost` — Financial and cost analysis
- `.box-code` — Technical/scientific detail

## Workflow

1. Receive pharma newsletter content
2. Create article HTML with proper meta tags and bilingual analysis
3. Save to `docs/YYYY-MM-DD_short-title.html`
4. Run `python build_index.py`
5. Commit and push
