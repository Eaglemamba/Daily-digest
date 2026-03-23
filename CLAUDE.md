# Daily Digest — Claude Code Instructions

## What This Repo Is

Daily multi-domain news digest. Pulls from 10 Gmail newsletter sources, applies strict 24hr TST filter, outputs interactive HTML digest, and archives it into this repo.

## Trigger

When the user says **"daily digest for MM/DD/YY"** or **"跑 digest MM/DD/YY"**:

1. Read `SKILL_v6_1_5.md` in this repo root — that is the authoritative workflow spec
2. Execute the full workflow as defined in the SKILL file
3. Save the output HTML to the correct archive path (see below)
4. Git commit and push

## Output Path Convention

```
digests/YYYY-MM/digest-YYYY-MM-DD.html
```

Examples:
- `digests/2026-03/digest-2026-03-24.html`
- `digests/2026-04/digest-2026-04-01.html`

If the month folder doesn't exist yet, create it.

## Git Workflow (after generating the digest)

```bash
git add digests/YYYY-MM/digest-YYYY-MM-DD.html
git commit -m "Add digest YYYY-MM-DD"
git push origin main
```

Run these commands automatically after saving the file — no need to ask the user.

## MCP Tools Required

- **Gmail**: `gmail_search_messages` + `gmail_read_thread` — for fetching newsletters
- Gmail MCP is configured in `.claude/settings.json`

## Timezone

All timestamps in **TST (UTC+8)**. The 24hr cutoff is calculated from current TST time.

## Critical Rules (from SKILL file)

- **Never expand the 24hr window** — not for weekends, holidays, or light news days
- **Two-stage Gmail filter**: search `newer_than:2d`, then filter precisely in code by exact TST timestamp
- **Exclude** `studio@endpointsnews.com` (webinar promos) from article extraction
- If < 5 articles found, note "Light news day" in the digest header — do not backfill

## Repo Structure

```
Daily-digest/
├── CLAUDE.md                     ← You are here
├── README.md
├── SKILL_v6_1_5.md               ← Full workflow spec — read this first
├── CHANGELOG.md
├── sample/
│   └── digest-sample.html
└── digests/
    ├── 2026-03/
    │   └── digest-2026-03-24.html
    └── ...
```

## Updating the SKILL File

When a new SKILL version is released (e.g. v6.2.0), replace `SKILL_v6_1_5.md` with the new file and update references in this `CLAUDE.md` accordingly.
