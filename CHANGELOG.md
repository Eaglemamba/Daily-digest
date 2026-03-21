# Changelog — Daily Digest Skill

All notable changes to this skill are documented here.

---

## [v6.1.5] — 2026-01-19

### Added
- **New source**: Ali Abdaal (`ali@aliabdaal.com`)
  - Productivity tips, personal development, creator economy insights
  - Routes to `hbr-review` agent
- **New category**: `Productivity` with amber badge color (`bg-amber-50 text-amber-700`)
- **Updated Agent Routing Map**: Added `productivity` to hbr-review tags

### Changed
- Source count: 9 → 10 confirmed sources

---

## [v6.1.4] — 2026-01-17

### Added
- **Design Preferences section**: Explicit rules for white/light background theme
- Light theme color guidelines for article cards, action bar, and export modal

### Changed
- HTML template examples updated from dark theme classes to light theme classes
- Default background enforced as `bg-white` / `bg-gray-50`

---

## [v6.1.3] — 2026-01-17

### Fixed
- **PDA sender address**: `parenteral@pda.org` → `newsupdate@pda.org`

---

## [v6.1.2] — 2026-01-10

### Added
- **New source**: Department of Product (`departmentofproduct@substack.com`)
  - Product management insights, strategy, roadmaps
  - Routes to `hbr-review` agent
- **New category**: `Product` with violet badge color (`bg-violet-50 text-violet-700`)
- Search pattern documentation: explicit rules for Substack vs dedicated domain patterns

### Changed
- Source count: 8 → 9 confirmed sources

---

## [v6.1.1] — 2026-01-10

### Fixed
- Gmail search patterns for reliable source matching:
  - Substack sources: use full email address (e.g. `from:aimaker@substack.com`)
  - Dedicated domains: use full domain (e.g. `from:endpointsnews.com`)
  - Subdomains: use full subdomain (e.g. `from:emails.hbr.org`)
- Partial domain matching failed for Substack sources because all Substack emails share `@substack.com`

---

## [v6.1.0] — 2026-01-10

### Added
- **Source Status sanity check**: ✔ / ⚠ / ✗ indicator per source after filtering
  - ✔ = found within 24hr window
  - ⚠ = found but outside 24hr (verify manually)
  - ✗ = no emails found
- **Screenshot fallback**: documented process for manual verification via Gmail app screenshot
- Code-side 24hr filtering using email Date header (precise timestamp comparison)

### Changed
- Gmail search window: `newer_than:1d` → `newer_than:2d`
- Rationale: `newer_than:1d` is approximate and misses boundary emails due to timezone/indexing delays

---

## [v6.0.0] — 2026-01-06

### Changed (Major)
- **Architecture overhaul**: Gmail Newsletter integration replaces web fetch entirely
- Removed web fetch fallback — newsletters are the single source of truth
- Export format redesigned for mobile copy/paste

### Added
- 8 confirmed newsletter sources at launch:
  1. Endpoints News (`*@endpointsnews.com`)
  2. BioPharma Dive (`newsletter@divenewsletter.com`)
  3. HBR (`emailteam@emails.hbr.org`)
  4. Leadership in Change (`leadershipinchange10@substack.com`)
  5. AI Maker (`aimaker@substack.com`)
  6. Import AI (`importai@substack.com`)
  7. The Batch / DeepLearning.AI (`thebatch@deeplearning.ai`)
  8. PDA (`newsupdate@pda.org`)
- TST timezone — all times converted and displayed in Taiwan Standard Time (UTC+8)
- Reliable timestamps from email headers
- "Read →" button on each article card

---

## [v5.x] — Prior to 2026-01-06

Web fetch based implementation. Deprecated due to CDN caching causing 4–6 day stale content.
Key learning: newsletter emails are more reliable than web scraping for real-time content.
