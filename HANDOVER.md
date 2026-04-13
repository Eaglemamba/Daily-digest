# Handover: Three-Column Digest Redesign

## Branch
`claude/redesign-three-column-layout-dEZDe` — pushed to origin

## Goal
Redesign the **daily digest HTML pages** (not index.html) into a three-column layout:

| Left | Center | Right |
|------|--------|-------|
| **Pharma News** | **AI Articles** | **Strategy & Leadership** |
| `data-agent="pharma-decipher"` | `data-agent="ai-articles"` | `data-agent="hbr-review"` |
| Endpoints News, BioPharma Dive, PDA | AI Maker, Import AI, The Batch | HBR, Leadership in Change, Dept of Product |
| Red accent | Cyan accent | Indigo accent |

## What Was Done

### Committed (2 commits on branch, pushed)
1. **3d47905** — Redesigned `index.html` to three-column layout
2. **47bf6f9** — Renamed "Harvard Business Review" column to "Strategy & Leadership"

### Reverted (unstaged)
- `index.html` has been restored to its original state (from commit `2d10819`) but **not yet committed**. The user clarified that the redesign should apply to the **daily digest files**, not the dashboard index.

## What Remains

### 1. Commit the index.html revert
```bash
git add index.html
git commit -m "Revert index.html to original dashboard layout"
```

### 2. Redesign the daily digest HTML files
These files need the three-column treatment:
- `digests/2026-04/digest-2026-04-12.html` (14 articles: 13 pharma, 0 AI, 1 leadership)
- `digests/2026-04/digest-2026-04-13.html` (4 articles: 0 pharma, 1 AI, 3 leadership)
- `digest-sample.html` (template in repo root — should match the new format)

#### Key changes needed per digest file:
- Widen container from `max-w-lg` to `max-w-7xl`
- Replace single-column article list with `grid grid-cols-1 lg:grid-cols-3 gap-6`
- Each column gets a sticky header with color-coded dot, title, source names, article count
- Articles routed to columns by their `data-agent` attribute
- Empty columns show a "No articles today" placeholder
- Floating action bar and export modal: widen `max-w-lg` to `max-w-7xl`
- Source Status section moves below the three columns (full width)

#### Article routing (existing `data-agent` values):
- `data-agent="pharma-decipher"` → Left column
- `data-agent="ai-articles"` → Center column
- `data-agent="hbr-review"` → Right column

### 3. Push and (optionally) create PR

## File Reference

| File | Purpose | Status |
|------|---------|--------|
| `index.html` | Dashboard archive page | Restored to original, uncommitted |
| `dashboard-data.js` | Dashboard data | Unchanged |
| `digests/2026-04/digest-2026-04-12.html` | Sat Apr 12 digest | **Needs redesign** |
| `digests/2026-04/digest-2026-04-13.html` | Sun Apr 13 digest | **Needs redesign** |
| `digest-sample.html` | Template sample | **Needs redesign** |
| `SKILL_v6_1_5.md` | Workflow spec | May need updated HTML template section |

## Design Notes
- Column headers use sticky positioning (`position: sticky; top: 0`) with backdrop blur
- Accent colors: red-500 (pharma), cyan-500 (AI), indigo-500 (leadership)
- Progress bars show relative article count per column
- Responsive: stacks to single column on mobile (`grid-cols-1`), three columns on `lg:`
- All existing functionality preserved: checkboxes, export modal, copy to clipboard
