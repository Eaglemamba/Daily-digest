# Daily Digest — Claude Code Instructions

## What This Repo Is

Daily multi-domain news digest. Pulls from 10 Gmail newsletter sources, applies strict 24hr TST filter, outputs interactive HTML digest via template system, and archives it into this repo.

## Trigger

When the user says **"daily digest for MM/DD/YY"** or **"跑 digest MM/DD/YY"**:

1. Get current TST time, calculate 24hr cutoff
2. Search all 10 Gmail sources in parallel with `newer_than:2d`
3. Apply strict 24hr TST filter on returned emails
4. Read qualifying threads in parallel to extract articles
5. Deduplicate articles across overlapping newsletters
6. Write JSON data file to `data/YYYY-MM-DD.json` (see `data/` for schema examples)
7. Build the digest HTML:
   ```bash
   bash scripts/build-digest.sh data/YYYY-MM-DD.json digests/YYYY-MM/digest-YYYY-MM-DD.html
   ```
8. Git add, commit, and push

## Template System

- **Template**: `templates/digest-template.html` — all Tailwind CSS, JS rendering, export logic
- **Build script**: `scripts/build-digest.sh` — injects JSON data into template
- **Data files**: `data/YYYY-MM-DD.json` — article data per digest run

To change layout, badge colors, export format, or column structure, edit the template.
Each digest run only produces a JSON file (~150 lines) instead of full HTML (~400 lines).

## Output Path Convention

```
digests/YYYY-MM/digest-YYYY-MM-DD.html
```

If the month folder doesn't exist yet, the build script creates it.

## Git Workflow (after generating the digest)

```bash
git add data/YYYY-MM-DD.json digests/YYYY-MM/digest-YYYY-MM-DD.html
git commit -m "Add digest YYYY-MM-DD"
git push origin main
```

Run these commands automatically after saving the file — no need to ask the user.

## MCP Tools Required

- **Gmail**: `gmail_search_messages` + `gmail_read_thread` — for fetching newsletters
- Gmail MCP is configured in `.claude/settings.json`

## Timezone

All timestamps in **TST (UTC+8)**. The 24hr cutoff is calculated from current TST time.

## Critical Rules

- **Never expand the 24hr window** — not for weekends, holidays, or light news days
- **Two-stage Gmail filter**: search `newer_than:2d`, then filter precisely in code by exact TST timestamp
- **Exclude** `studio@endpointsnews.com` and `events@endpointsnews.com` (webinar/event promos)
- If < 5 articles, set `"lightNewsDay": true` in JSON — do not backfill

## Gmail Sources (10)

| Source | Gmail Search Query | Sender Addresses | Agent Route |
|--------|-------------------|-----------------|-------------|
| **Endpoints News** | `from:endpointsnews.com newer_than:2d` | `alerts@`, `news@`, `early@`, `fdaplus@`, `pharma@`, `healthtech@` (exclude `studio@`, `events@`) | pharma-decipher |
| **BioPharma Dive** | `from:divenewsletter.com newer_than:2d` | `newsletter@divenewsletter.com` | pharma-decipher |
| **HBR** | `from:emails.hbr.org newer_than:2d` | `emailteam@emails.hbr.org` | hbr-review |
| **Leadership in Change** | `from:leadershipinchange10@substack.com newer_than:2d` | `leadershipinchange10@substack.com` | hbr-review |
| **Dept of Product** | `from:departmentofproduct@substack.com newer_than:2d` | `departmentofproduct@substack.com` | hbr-review |
| **Ali Abdaal** | `from:ali@aliabdaal.com newer_than:2d` | `ali@aliabdaal.com` | hbr-review |
| **AI Maker** | `from:aimaker@substack.com newer_than:2d` | `aimaker@substack.com` | ai-articles |
| **Import AI** | `from:importai@substack.com newer_than:2d` | `importai@substack.com` | ai-articles |
| **The Batch** | `from:deeplearning.ai newer_than:2d` | `thebatch@deeplearning.ai`, `hello@deeplearning.ai` | ai-articles |
| **PDA** | `from:pda.org newer_than:2d` | `newsupdate@pda.org`, `parenteral@pda.org`, `asia-pacific@pda.org` | pharma-decipher |

## Categories & Columns

| Category | Badge Color | Column | Agent Route |
|----------|------------|--------|-------------|
| FDA+ | red | pharma | pharma-decipher |
| Quality/Compliance | rose | pharma | pharma-decipher |
| Deals | green | pharma | pharma-decipher |
| Clinical | blue | pharma | pharma-decipher |
| Financing | purple | pharma | pharma-decipher |
| Pipeline | teal | pharma | pharma-decipher |
| Policy | orange | pharma | pharma-decipher |
| Strategy | indigo | strategy | hbr-review |
| Leadership | pink | strategy | hbr-review |
| Product | violet | strategy | hbr-review |
| Productivity | amber | strategy | hbr-review |
| AI | cyan | ai | ai-articles |

## JSON Data Schema

```json
{
  "date": "YYYY-MM-DD",
  "displayDate": "Day, Month DD, YYYY",
  "shortDate": "Mon DD, YYYY",
  "cutoffTime": "Mon DD, HH:MM TST",
  "articleCount": 0,
  "sourceCount": 0,
  "domainCount": 3,
  "lightNewsDay": false,
  "sourceStatus": [
    {"name": "Source Name", "status": "ok|warn|none", "count": 0, "detail": "..."}
  ],
  "articles": [
    {
      "column": "pharma|ai|strategy",
      "category": "FDA+|Deals|Clinical|...",
      "agent": "pharma-decipher|hbr-review|ai-articles",
      "source": "Endpoints News|HBR|...",
      "title": "...",
      "summary": "...",
      "url": "...",
      "time": "Mon DD, HH:MM TST"
    }
  ]
}
```

## Queue-Based Publisher Pipeline

Full spec: see `PUBLISHER_v1.0.md` in this repo.

After reviewing the daily digest, export selected articles as a JSON file and drop it into `queue/`:

```
1. Daily Digest artifact → select articles → click "Export" → download YYYY-MM-DD.json
2. Move file to: Daily-digest/queue/YYYY-MM-DD.json
3. Nightly trigger at 01:00 TST automatically:
   - Reads queue file
   - Generates bilingual HTML for each article in the correct repo
   - Moves queue file to queue/processed/
   - Rebuilds indexes + pushes all repos
```

**Queue file format:** JSON with `date`, `exported_at`, and `articles` array.
Each article includes: `route`, `category`, `title`, `source`, `url`, `date`, `time_tst`, `summary`, `full_content`.

Route → Repo mapping:
- `pharma-decipher` → `Pharma-news-decipher/docs/`
- `hbr-review` → `Harvard-Business-Review/docs/`
- `ai-articles` → `david-ai-learning/docs/`

## Repo Structure

```
Daily-digest/
├── CLAUDE.md                     ← You are here
├── README.md
├── SKILL_v6_1_5.md               ← Legacy spec (archival reference)
├── PUBLISHER_v1.0.md             ← Nightly publisher pipeline spec
├── CHANGELOG.md
├── templates/
│   └── digest-template.html      ← Reusable HTML template
├── scripts/
│   └── build-digest.sh           ← Template → HTML builder
├── data/
│   └── YYYY-MM-DD.json           ← Article data per digest
├── queue/
│   ├── .gitkeep
│   └── processed/
│       └── .gitkeep
└── digests/
    └── YYYY-MM/
        └── digest-YYYY-MM-DD.html
```
