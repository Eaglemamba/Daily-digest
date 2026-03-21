# Daily Digest — Claude Skill

A daily multi-domain news digest powered by **Claude + Gmail integration**. Fetches newsletters from 10 curated sources, applies a strict 24-hour filter, and outputs an interactive HTML digest with one-click routing to downstream Claude Projects.

---

## How It Works

```
Gmail (10 sources)
      │
      ▼
Claude reads newsletters via Gmail MCP
      │
      ▼
Strict 24hr TST filter applied in code
      │
      ▼
Interactive HTML digest generated
      │
      ▼
Export → route to downstream Claude Projects
   ├── pharma-decipher
   ├── hbr-review
   └── ai-articles
```

You trigger it with a simple message to Claude:

```
daily digest for 03/21/26
```

Claude reads the SKILL file, searches Gmail, filters to the last 24 hours, and outputs a fully interactive digest — no configuration needed per run.

---

## Sources

| Source | Domain | Routes To |
|---|---|---|
| Endpoints News | `*@endpointsnews.com` | pharma-decipher |
| BioPharma Dive | `newsletter@divenewsletter.com` | pharma-decipher |
| HBR | `emailteam@emails.hbr.org` | hbr-review |
| Leadership in Change | `leadershipinchange10@substack.com` | hbr-review |
| Department of Product | `departmentofproduct@substack.com` | hbr-review |
| Ali Abdaal | `ali@aliabdaal.com` | hbr-review |
| AI Maker | `aimaker@substack.com` | ai-articles |
| Import AI | `importai@substack.com` | ai-articles |
| The Batch (DeepLearning.AI) | `thebatch@deeplearning.ai` | ai-articles |
| PDA | `newsupdate@pda.org` | pharma-decipher |

---

## Requirements

- **Claude.ai** (Pro or Team) with a Project configured
- **Gmail MCP connector** enabled in Claude
- The `SKILL_v6_1_5.md` file uploaded to your Claude Project

---

## Setup

1. Create a Claude Project (e.g. `daily-digest`)
2. Upload `SKILL_v6_1_5.md` to the Project's files
3. Add the trigger instruction to your Project's system prompt:

```
When the user says "Daily digest for MM/DD/YY", read SKILL_v6_1_5.md and execute the workflow.
```

4. Connect Gmail via Claude's MCP connector settings
5. Run: `daily digest for MM/DD/26`

---

## Output

Claude generates an **interactive HTML file** (`daily-digest-YYYY-MM-DD.html`) with:

- Checkbox selection per article
- Category badges (FDA+, Deals, Clinical, AI, Strategy, etc.)
- "Read →" button linking to the original article
- Floating action bar showing selected count
- Export modal grouping articles by downstream project

See [`sample/digest-sample.html`](sample/digest-sample.html) for a live example.

---

## Downstream Projects

The export modal formats selected articles for pasting directly into:

| Project | Purpose |
|---|---|
| `pharma-decipher` | Deep-dive pharma/biotech/FDA analysis |
| `hbr-review` | Leadership, strategy, productivity insights |
| `ai-articles` | AI implementation and research summaries |

---

## Design

- **Brand**: Amaran purple (`#482A77`)
- **Theme**: White/light background, Tailwind CSS via CDN
- **Timezone**: All timestamps in TST (UTC+8)

---

## File Structure

```
Daily-digest/
├── README.md
├── SKILL_v6_1_5.md               ← Active skill file (upload to Claude Project)
├── CHANGELOG.md                  ← Full version history
├── sample/
│   └── digest-sample.html        ← Example output
└── digests/
    ├── 2026-03/
    │   ├── digest-2026-03-21.html
    │   └── digest-2026-03-22.html
    ├── 2026-02/
    │   └── digest-2026-02-15.html
    └── ...
```

### Adding a new digest

Each day, upload the generated HTML into `digests/YYYY-MM/`:

1. Go to the repo → `digests/` → your month folder
2. Click `Add file` → `Upload files`
3. Drop in `digest-YYYY-MM-DD.html`
4. Commit message: `Add digest YYYY-MM-DD`

---

## Key Design Decisions

**Why Gmail newsletters instead of web scraping?**
Early versions used web fetch, but CDN caching caused 4–6 day stale content. Gmail newsletters have reliable timestamps and no paywall issues.

**Why `newer_than:2d` with a code-side 24hr filter?**
Gmail's `newer_than:1d` is approximate near timezone boundaries. Casting a 2-day net and filtering precisely in code ensures nothing is missed or incorrectly included.

**Why strict 24-hour rule with no exceptions?**
This digest runs daily. Including older articles would create duplicates across days and defeat the purpose of daily tracking.

---

## Version

Current: **v6.1.5** (2026-01-19) — 10 sources, white theme, Ali Abdaal added

See [CHANGELOG.md](CHANGELOG.md) for full history.
