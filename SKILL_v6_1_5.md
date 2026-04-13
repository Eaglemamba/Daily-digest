## name: daily-news-digest

description: Fetches the latest biopharma, AI, and leadership news from Gmail newsletters. Outputs an interactive Tailwind CSS artifact with checkbox selection and export functionality for downstream agent routing.
version: 6.1.5
last_updated: 2026-01-19

# Daily News Digest Skill

**Version:** 6.1.5

## Overview

Daily multi-domain news digest using **Gmail Newsletter search** as primary source:

- **Gmail newsletters**: Reliable timestamps, complete content, no paywall issues
- **Timezone**: All times displayed in **TST (Taiwan Standard Time, UTC+8)**

**Coverage Areas:**

- Biopharma (FDA, deals, clinical trials) — via Endpoints News, BioPharma Dive
- Leadership & Strategy — via HBR, Leadership in Change
- Product Management — via Department of Product
- AI & Technology — via AI Maker, Import AI, The Batch
- Productivity & Personal Development — via Ali Abdaal
- Quality & Compliance — via PDA

**Key Features:**

- **Gmail Newsletter integration** — replaces web fetch entirely
- **Wider search + strict filter** — search `newer_than:2d`, filter by exact 24hr in code
- **Source Status sanity check** — flags sources with no results for manual verification
- **Reliable timestamps** — email received date = publish date (converted to TST)
- **Complete content** — newsletters include full summaries, no paywall guessing
- **Interactive selection** — checkbox per article, export for downstream agents

## Trigger Phrases

Standard triggers (system auto-detects current date):

- "跑 pharma digest"
- "daily digest for MM/DD/YY"
- "pharma news digest"
- "今天的生醫新聞"
- "morning briefing"

No date input required — system uses current date automatically.

-----

## CRITICAL: 24-Hour Rule (NO EXCEPTIONS)

<critical_rule>
**Claude MUST NOT expand the 24-hour window under ANY circumstance, including:**

- Holidays (New Year, Christmas, Thanksgiving, etc.)
- Weekends (Saturday, Sunday)
- Slow news days
- "Not enough articles found"
- User appears to want more content

**Time Calculation:**

- Use **TST (Taiwan Standard Time, UTC+8)** for all time displays
- 24-hour window = current TST time minus 24 hours
- Convert all email timestamps from UTC to TST before comparison

**If fewer than 5 articles are found within 24 hours:**

1. Report ONLY those articles that qualify
1. Add a note in header: "Light news day — X articles within 24hr window"
1. DO NOT add older articles to "fill out" the digest

**The user tracks news DAILY. Seeing old articles defeats the purpose.**
</critical_rule>

-----

## Source Architecture

### Gmail Newsletter Sources (10 confirmed)

|Source                   |Gmail Search Query                                    |Sender Address                     |Content Type                       |Agent Route    |
|-------------------------|------------------------------------------------------|-----------------------------------|-----------------------------------|---------------|
|**Endpoints News**       |`from:endpointsnews.com newer_than:2d`                |`*@endpointsnews.com`              |Biopharma, FDA, deals, clinical    |pharma-decipher|
|**BioPharma Dive**       |`from:divenewsletter.com newer_than:2d`               |`newsletter@divenewsletter.com`    |Business analysis, market news     |pharma-decipher|
|**HBR**                  |`from:emails.hbr.org newer_than:2d`                   |`emailteam@emails.hbr.org`         |Strategy, leadership, management   |hbr-review     |
|**Leadership in Change** |`from:leadershipinchange10@substack.com newer_than:2d`|`leadershipinchange10@substack.com`|AI leadership, change management   |hbr-review     |
|**Department of Product**|`from:departmentofproduct@substack.com newer_than:2d` |`departmentofproduct@substack.com` |Product management, strategy       |hbr-review     |
|**Ali Abdaal**           |`from:ali@aliabdaal.com newer_than:2d`                |`ali@aliabdaal.com`                |Productivity, personal development |hbr-review     |
|**AI Maker**             |`from:aimaker@substack.com newer_than:2d`             |`aimaker@substack.com`             |AI implementation, workflows       |ai-articles    |
|**Import AI**            |`from:importai@substack.com newer_than:2d`            |`importai@substack.com`            |AI research, frontier models       |ai-articles    |
|**The Batch**            |`from:deeplearning.ai newer_than:2d`                  |`thebatch@deeplearning.ai`         |AI news, Andrew Ng insights        |ai-articles    |
|**PDA**                  |`from:pda.org newer_than:2d`                          |`newsupdate@pda.org`               |Quality, compliance, training      |pharma-decipher|

### Sender Email Reference

```
Endpoints News:
  - alerts@endpointsnews.com (Breaking alerts)
  - news@endpointsnews.com (Main Edition)
  - early@endpointsnews.com (Early Edition)
  - studio@endpointsnews.com (Webinars)
  - drew@endpointsnews.com (Editor)

BioPharma Dive:
  - newsletter@divenewsletter.com

HBR:
  - emailteam@emails.hbr.org

Leadership in Change (Joel):
  - leadershipinchange10@substack.com

Department of Product:
  - departmentofproduct@substack.com

Ali Abdaal:
  - ali@aliabdaal.com

AI Maker:
  - aimaker@substack.com

Import AI (Jack Clark):
  - importai@substack.com

The Batch (DeepLearning.AI):
  - thebatch@deeplearning.ai

PDA:
  - newsupdate@pda.org
```

-----

## Execution Workflow

### Step 1: Get Current Time

Call `user_time_v0` to get current TST time. Calculate:

- **Current time**: e.g., Jan 10, 2026 08:30 TST
- **24hr cutoff**: e.g., Jan 9, 2026 08:30 TST

### Step 2: Search Gmail (Wider Window)

Execute Gmail searches with **`newer_than:2d`** to compensate for Gmail API timing inconsistencies:

```
search_gmail_messages: from:endpointsnews.com newer_than:2d
search_gmail_messages: from:divenewsletter.com newer_than:2d
search_gmail_messages: from:emails.hbr.org newer_than:2d
search_gmail_messages: from:leadershipinchange10@substack.com newer_than:2d
search_gmail_messages: from:departmentofproduct@substack.com newer_than:2d
search_gmail_messages: from:ali@aliabdaal.com newer_than:2d
search_gmail_messages: from:aimaker@substack.com newer_than:2d
search_gmail_messages: from:importai@substack.com newer_than:2d
search_gmail_messages: from:deeplearning.ai newer_than:2d
search_gmail_messages: from:pda.org newer_than:2d
```

**Why `newer_than:2d`?** Gmail's `newer_than:1d` is approximate and can miss emails near the boundary due to timezone/indexing delays. Searching 2 days ensures we capture all candidates, then filter precisely in Step 3.

**Search Pattern Rules:**

- **Substack sources** → Use full email address (e.g., `from:aimaker@substack.com`)
- **Dedicated domains** → Use full domain (e.g., `from:endpointsnews.com`)
- **Subdomains** → Use full subdomain (e.g., `from:emails.hbr.org`)
- **Personal domains** → Use full email address (e.g., `from:ali@aliabdaal.com`)

### Step 3: Strict 24-Hour Filter (Code-Side)

For each email returned:

1. **Extract email Date header** — this is the authoritative timestamp
1. **Parse and convert to TST (UTC+8)**
1. **Compare against exact 24hr cutoff from Step 1**
1. **INCLUDE only if email_time >= cutoff_time**

```
Example:
Current: Jan 10, 08:30 TST
Cutoff:  Jan 9, 08:30 TST

Email 1: Jan 9, 18:30 TST  → INCLUDE (after cutoff)
Email 2: Jan 9, 06:00 TST  → EXCLUDE (before cutoff)
Email 3: Jan 8, 22:00 TST  → EXCLUDE (before cutoff)
```

### Step 4: Source Status Sanity Check

After filtering, generate a **Source Status** report:

|Status|Meaning                                                           |
|------|------------------------------------------------------------------|
|✔     |Found emails within 24hr window                                   |
|⚠     |Search returned emails, but ALL were outside 24hr (potential miss)|
|✗     |Search returned zero emails (no newsletter sent)                  |

**⚠ Warning status** indicates the source sent newsletters recently but none qualified. User should manually verify if this seems wrong (e.g., via Gmail app screenshot).

```
Source Status:
✔ Endpoints News (4 emails)
✔ BioPharma Dive (1 email)
⚠ Leadership in Change — 1 found, 0 within 24hr (last: Jan 8, 18:01 TST)
✗ Department of Product — no newsletter
✗ Ali Abdaal — no newsletter
✗ HBR — no newsletter
✗ AI Maker — no newsletter
✔ Import AI (1 email)
✔ The Batch (1 email)
✗ PDA — no newsletter
```

### Step 5: Extract Articles from Newsletters

**Endpoints News format:**

- Main Edition: Numbered list of top stories with summaries
- Early Edition: Breaking news summaries
- Alert: Single breaking story with full summary

**BioPharma Dive format:**

- Daily Dive: Multiple headlines with brief descriptions
- Links to full articles on biopharmadive.com

**HBR format:**

- Article titles with brief descriptions
- Links to full articles on hbr.org

**Leadership in Change (Joel) format:**

- Substack format with main article content
- Usually single long-form article per email
- Full article content available in email body

**Department of Product format:**

- Substack format with product management insights
- Usually single long-form article per email
- Focus on product strategy, roadmaps, execution

**Ali Abdaal format:**

- Newsletter format with productivity tips and insights
- Usually single main topic per email
- Focus on productivity, personal development, creator economy

**AI Maker format:**

- Substack format with main article
- AI tools and implementation guides

**PDA format:**

- Event announcements and training updates
- Technical report releases

**Import AI (Jack Clark) format:**

- Substack format with multiple AI research stories
- Deep technical analysis of frontier AI
- Usually 3-5 stories per newsletter

**The Batch (DeepLearning.AI) format:**

- Weekly AI news digest from Andrew Ng
- Multiple sections: news, research, business
- Links to full articles on deeplearning.ai

### Step 6: Categorize

|Category              |Badge Color|Content                               |Priority|Agent Route    |
|----------------------|-----------|--------------------------------------|--------|---------------|
|**FDA+**              |`red`      |Approvals, CRLs, 483s, Warning Letters|**HIGH**|pharma-decipher|
|**Quality/Compliance**|`rose`     |PDA letters, GMP, audit findings      |**HIGH**|pharma-decipher|
|Deals                 |`green`    |M&A, licensing, partnerships          |Standard|pharma-decipher|
|Clinical              |`blue`     |Trial results, data readouts          |Standard|pharma-decipher|
|Financing             |`purple`   |IPOs, funding rounds                  |Standard|pharma-decipher|
|Pipeline              |`teal`     |Drug development updates              |Standard|pharma-decipher|
|Policy                |`orange`   |Regulations, pricing                  |Standard|pharma-decipher|
|Strategy              |`indigo`   |Business analysis (HBR)               |Standard|hbr-review     |
|Product               |`violet`   |Product management, roadmaps          |Standard|hbr-review     |
|Productivity          |`amber`    |Productivity, personal development    |Standard|hbr-review     |
|AI                    |`cyan`     |AI/ML implementation                  |Standard|ai-articles    |
|Leadership            |`pink`     |Change management, AI leadership      |Standard|hbr-review     |

### Step 7: Generate HTML Artifact

Output as **interactive HTML artifact** with:

- Checkbox selection per article
- **"Read →" button** on each article for direct navigation
- Floating action bar showing selection count
- Export button generating **downloadable JSON file** (`YYYY-MM-DD.json`) with full article content
- Articles grouped by source
- All timestamps displayed in TST
- **Source Status section** at bottom showing ✔/⚠/✗ for each source

-----

## Export Format — JSON Download

When user clicks "Export Selected", the artifact must trigger a **browser JSON file download** (not clipboard text).

### Article Data Object

Each article in the HTML artifact JavaScript must store a complete object:

```javascript
{
  id: "unique-string-id",
  route: "pharma-decipher",    // "pharma-decipher" | "hbr-review" | "ai-articles"
  category: "FDA+",
  title: "Full article title",
  source: "Endpoints News",
  url: "https://...",
  date: "2026-04-13",
  time_tst: "14:30",
  summary: "One-line summary from newsletter",
  full_content: "Complete article text extracted from newsletter email body — include all paragraphs, bullet points, and key details from the email"
}
```

### Export Button JavaScript

```javascript
function exportSelected() {
  const selected = allArticles.filter(a => selectedIds.has(a.id));
  const payload = {
    date: digestDate,              // "YYYY-MM-DD"
    exported_at: new Date().toISOString(),
    articles: selected
  };
  const json = JSON.stringify(payload, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = digestDate + '.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

The downloaded file is named `YYYY-MM-DD.json` (e.g., `2026-04-13.json`).

**User next step**: Move the downloaded file into `Daily-digest/queue/` — the 01:00 nightly trigger picks it up automatically and generates all bilingual HTMLs.

-----

## Agent Routing Map

|Category Tags                                                           |Agent Route      |Project Purpose                 |
|------------------------------------------------------------------------|-----------------|--------------------------------|
|`fda`, `quality`, `deals`, `clinical`, `financing`, `pipeline`, `policy`|`pharma-decipher`|Pharma news deep dive & analysis|
|`strategy`, `leadership`, `product`, `productivity`                     |`hbr-review`     |Leadership & strategy insights  |
|`ai`                                                                    |`ai-articles`    |AI implementation guides        |

-----

## HTML Template Key Elements

### Header with TST timezone indicator

```html
<p class="text-purple-600 text-xs mt-2">
    ✔ 24hr filter active | Emails received since [CUTOFF_TIME] TST
</p>
```

### Article card with Read button

```html
<div class="flex items-center justify-between mt-2">
    <p class="text-xs text-gray-500">[DATE], [TIME] TST</p>
    <a href="[URL]" target="_blank" 
       class="text-xs bg-amaran-purple text-white px-3 py-1 rounded hover:bg-amaran-purple-light">
        Read →
    </a>
</div>
```

### Source Status Section

```html
<div class="bg-gray-100 rounded-lg p-3 mb-4">
    <h3 class="text-sm font-medium text-gray-700 mb-2">Source Status</h3>
    <div class="text-xs space-y-1">
        <p><span class="text-green-600">✔</span> Endpoints News (4)</p>
        <p><span class="text-green-600">✔</span> BioPharma Dive (1)</p>
        <p><span class="text-yellow-600">⚠</span> Leadership in Change — 1 found, 0 in 24hr (last: Jan 8)</p>
        <p><span class="text-gray-400">✗</span> Department of Product — no newsletter</p>
        <p><span class="text-gray-400">✗</span> Ali Abdaal — no newsletter</p>
        <p><span class="text-gray-400">✗</span> HBR — no newsletter</p>
    </div>
</div>
```

-----

## Category Badge Colors

|Category          |Tailwind Color Classes                          |Priority|
|------------------|------------------------------------------------|--------|
|FDA+              |`bg-red-50 text-red-700 border-red-200`         |**HIGH**|
|Quality/Compliance|`bg-rose-100 text-rose-800 border-rose-300`     |**HIGH**|
|Deals             |`bg-green-50 text-green-700 border-green-200`   |Standard|
|Clinical          |`bg-blue-50 text-blue-700 border-blue-200`      |Standard|
|Financing         |`bg-purple-50 text-purple-700 border-purple-200`|Standard|
|Strategy          |`bg-indigo-50 text-indigo-700 border-indigo-200`|Standard|
|Product           |`bg-violet-50 text-violet-700 border-violet-200`|Standard|
|Productivity      |`bg-amber-50 text-amber-700 border-amber-200`   |Standard|
|AI                |`bg-cyan-50 text-cyan-700 border-cyan-200`      |Standard|
|Leadership        |`bg-pink-50 text-pink-700 border-pink-200`      |Standard|
|Policy            |`bg-orange-50 text-orange-700 border-orange-200`|Standard|
|Pipeline          |`bg-teal-50 text-teal-700 border-teal-200`      |Standard|

-----

## Amaran Brand Colors

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'amaran': {
                    'purple': '#482A77',
                    'purple-light': '#6B4A9E',
                    'purple-dark': '#351F59'
                }
            }
        }
    }
}
```

-----

## Design Preferences

<design_rules>
**Background and Theme:**
- **USE WHITE BACKGROUND** as the default — `bg-white` or `bg-gray-50` for the page body
- Article cards use light gray backgrounds: `bg-gray-50` or `bg-gray-100`
- Source status section: `bg-gray-100`
- Floating action bar: `bg-white` with `shadow-lg` and `border border-gray-200`
- Export modal: `bg-white` with dark overlay backdrop

**Text Colors (for light background):**
- Primary text: `text-gray-900` or `text-gray-800`
- Secondary text: `text-gray-600`
- Muted text: `text-gray-500`
- Timestamps: `text-gray-500`

**Header:**
- Keep the gradient header with Amaran purple: `bg-gradient-to-r from-amaran-purple to-amaran-purple-light`
- Header text remains white for contrast

**DO NOT use:**
- `bg-gray-900` (dark background)
- `bg-gray-800` (dark cards)
- `text-gray-100` / `text-gray-200` / `text-gray-300` (light text for dark backgrounds)
</design_rules>

-----

## Error Handling

|Scenario                              |Action                                |
|--------------------------------------|--------------------------------------|
|Gmail search returns no results       |Mark source as ✗, note "no newsletter"|
|Gmail returns results but none in 24hr|Mark source as ⚠, show last email date|
|Email parsing fails                   |Skip that email, continue with others |
|< 5 articles within 24hr              |Note "Light news day" in header       |
|Timezone unclear                      |Default to UTC, then convert to TST   |

-----

## Fallback: Screenshot Verification

If user suspects missed newsletters (especially for ⚠ sources):

1. User provides Gmail app screenshot showing recent emails from that source
1. Claude extracts article info from screenshot
1. Claude adds missing articles to digest manually

This serves as human-in-the-loop verification for edge cases.

-----

## Changelog

### v6.1.5 (2026-01-19)

- **New source**: Ali Abdaal (`ali@aliabdaal.com`)
  - Productivity tips, personal development, creator economy insights
  - Routes to `hbr-review` agent
- **New category**: `Productivity` with amber badge color
- **Source count**: 9 → 10 confirmed sources
- **Updated Agent Routing Map**: Added `productivity` to hbr-review tags

### v6.1.4 (2026-01-17)

- **Design preference**: Added explicit rule to use **white background** as default
- **New section**: Added "Design Preferences" section with light theme color guidelines
- **Updated HTML template examples**: Changed from dark theme classes to light theme classes

### v6.1.3 (2026-01-17)

- **Updated PDA sender address**: `parenteral@pda.org` → `newsupdate@pda.org`

### v6.1.2 (2026-01-10)

- **New source**: Department of Product (`departmentofproduct@substack.com`)
  - Product management insights, strategy, roadmaps
  - Routes to `hbr-review` agent
- **New category**: `Product` with violet badge color
- **Source count**: 8 → 9 confirmed sources
- **Search pattern documentation**: Added explicit rules for Substack vs dedicated domain patterns

### v6.1.1 (2026-01-10)

- **Fixed Gmail search patterns** for reliable source matching:
  - Substack sources: Use full email address (e.g., `from:aimaker@substack.com`)
  - Dedicated domains: Use full domain (e.g., `from:endpointsnews.com`)
  - Subdomains: Use full subdomain (e.g., `from:emails.hbr.org`)
- **Why this change**: Partial domain matching (e.g., `from:leadershipinchange`) failed for Substack sources because all Substack emails share `@substack.com` domain

### v6.1.0 (2026-01-10)

- **Wider search + strict filter**: Changed from `newer_than:1d` to `newer_than:2d` in Gmail queries
- **Code-side 24hr filtering**: Precise timestamp comparison using email Date header
- **Source Status sanity check**: New ✔/⚠/✗ status indicator for each source
  - ✔ = found within 24hr
  - ⚠ = found but outside 24hr (potential miss, verify manually)
  - ✗ = no emails found
- **Screenshot fallback**: Documented process for manual verification via Gmail app screenshot
- **Why this change**: Gmail's `newer_than:1d` is approximate and can miss boundary emails due to timezone/indexing inconsistencies

### v6.0.0 (2026-01-06)

- **Major architecture change**: Gmail Newsletter integration replaces web fetch
- **8 confirmed newsletter sources**:
1. Endpoints News (`*@endpointsnews.com`)
1. BioPharma Dive (`newsletter@divenewsletter.com`)
1. HBR (`emailteam@emails.hbr.org`)
1. Leadership in Change / Joel (`leadershipinchange10@substack.com`)
1. AI Maker (`aimaker@substack.com`)
1. Import AI / Jack Clark (`importai@substack.com`)
1. The Batch / DeepLearning.AI (`thebatch@deeplearning.ai`)
1. PDA (`newsupdate@pda.org`)
- **TST timezone** — all times converted and displayed in Taiwan Standard Time (UTC+8)
- **Reliable timestamps** from email headers
- **Complete content** from newsletter bodies (no paywall issues)
- **"Read →" button** on each article for direct navigation
- Export format optimized for mobile copy/paste
- Removed web fetch fallback (newsletters are the single source of truth)

### Previous Versions

See v5.x changelog for web fetch based implementation history.
