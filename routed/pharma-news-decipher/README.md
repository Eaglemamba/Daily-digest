# Pharma News Decipher

Bilingual Pharma & Drug Industry Analysis Dashboard. Powered by Claude AI.

Curated analysis of pharma newsletters (Endpoints News, BioPharma Dive, PDA) with bilingual Traditional Chinese/English educational summaries.

## Structure

```
pharma-news-decipher/
├── README.md
├── CLAUDE.md
├── build_index.py
├── .gitignore
└── docs/
    ├── index.html          ← Dashboard with search/filter
    ├── styles.css           ← Shared stylesheet
    └── YYYY-MM-DD_short-title.html  ← Individual article analyses
```

## Usage

1. Add a new article HTML file to `docs/` following the naming pattern `YYYY-MM-DD_short-title.html`
2. Include required meta tags in the HTML head (doc-date, doc-title, doc-source, doc-tags, doc-rating, doc-summary, doc-file)
3. Run `python build_index.py` to regenerate the dashboard index
4. Commit and push

## Tags

FDA | Clinical | Deals | Pipeline | Financing | Policy | Biotech | ADC | Oncology | Regulatory
