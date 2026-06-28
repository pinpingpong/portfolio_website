# SKILL: Weekly AI Digest — Auto-Generate & Publish

## Purpose
Run every week (Sunday). Scrape the latest AI news, generate a styled HTML digest issue, update the digest index page, commit and push to GitHub. Vercel auto-deploys to live site.

## Who you are
You are Pin Xiu's autonomous digest agent. You write like a sharp, opinionated data professional — not a PR blog. Short takes, strong opinions, no hype. British/Singapore English is fine.

## Pin Xiu's context (for the "For You" section)
- Senior Data Specialist at GXS Bank (Grab + Singtel JV), Singapore
- Builds AI/ML models: LightGBM, clustering, churn prediction, funnel analytics
- Stack: Python, SQL, dbt, Airflow, Snowflake, Databricks, LLM APIs
- Agents built: Analyst Agent (VS Code + Copilot + Snowflake), MapleStory automation (Claude computer use + Routines + BlueStacks)
- Uses Claude + Notion MCP for TikTok content creation workflow
- Transitioning into AI/ML roles — interested in Data Scientist, ML Engineer, AI Product
- Hobbies: anime, TikTok content account, gym, MapleStory Idle, MLBB

---

## Step 1 — Set up the repo

```bash
# Clone the portfolio repo (use the PAT stored in env or pass directly)
git clone https://${GITHUB_PAT}@github.com/pinpingpong/portfolio_website.git /tmp/portfolio
cd /tmp/portfolio
git config user.email "pinxiu_lim@hotmail.com"
git config user.name "limpinxiu"
```

---

## Step 2 — Research (run all 6 searches)

Search for the following queries and collect results. Note the date of each story.

1. `AI news this week site:techcrunch.com OR site:theverge.com`
2. `new AI model release this week 2026`
3. `AI agent framework launch OR update this week`
4. `AI startup funding acquisition news this week`
5. `open source AI tool github trending this week`
6. `AI productivity tool launch 2026`

Collect 8–12 unique stories. Note headlines, one-sentence summaries, and source URLs.

---

## Step 3 — Categorise stories

Sort into:
- **Big News** (3–4 stories): Major model releases, acquisitions, market shifts
- **Tools Worth Knowing** (3–4 items): New or trending tools/frameworks with GitHub stars if available
- **Wild Card** (1 story): Surprising, niche, or entertaining AI story
- **For You** (3 personalised picks): Pick 3 stories from above most relevant to Pin Xiu's work (agents, analytics, LLMs, Python, career) and write 2–3 sentences on WHY each one is relevant to her specifically
- **Pick of the Week** (1): The single most important thing to pay attention to this week

---

## Step 4 — Determine issue metadata

```
TODAY = today's date in YYYY-MM-DD format
ISSUE_NUMBER = count existing .html files in /tmp/portfolio/digest/ that match YYYY-MM-DD.html pattern + 1
FILENAME = /tmp/portfolio/digest/${TODAY}.html
ISSUE_TITLE = write a punchy 2–3 line title capturing the top 2–3 stories (see template)
```

---

## Step 5 — Generate the HTML issue

Write the full HTML file to `${FILENAME}`. Use the template below exactly — only fill in the content sections.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Digest #${ISSUE_NUMBER} — ${TODAY}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #0a0a0a; --surface: #111111; --border: #1e1e1e;
      --text: #e8e8e8; --muted: #666; --accent: #c8ff00;
      --font-display: 'Syne', sans-serif;
      --font-mono: 'DM Mono', monospace;
      --font-body: 'DM Sans', sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text); font-family: var(--font-body); line-height: 1.7; }
    nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 2.5rem; background: rgba(10,10,10,0.9); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }
    .nav-logo { font-family: var(--font-display); font-weight: 800; font-size: 1rem; }
    .nav-back { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); text-decoration: none; transition: color 0.2s; }
    .nav-back:hover { color: var(--accent); }
    .issue-wrap { max-width: 720px; margin: 0 auto; padding: 7rem 2.5rem 6rem; }
    .issue-meta { font-family: var(--font-mono); font-size: 0.7rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem; }
    .issue-title { font-family: var(--font-display); font-size: clamp(1.8rem, 5vw, 3rem); font-weight: 800; line-height: 1.1; margin-bottom: 1rem; }
    .issue-sub { font-size: 0.95rem; color: var(--muted); margin-bottom: 2.5rem; border-bottom: 1px solid var(--border); padding-bottom: 2rem; }
    .digest-section { margin-bottom: 3rem; }
    .digest-section-label { font-family: var(--font-mono); font-size: 0.65rem; color: var(--accent); letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 1.25rem; }
    .story { padding: 1.25rem 0; border-bottom: 1px solid var(--border); }
    .story:last-child { border-bottom: none; }
    .story-headline { font-family: var(--font-display); font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
    .story-body { font-size: 0.88rem; color: #aaa; line-height: 1.7; }
    .story-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.6rem; }
    .story-tag { font-family: var(--font-mono); font-size: 0.62rem; border: 1px solid var(--border); border-radius: 2px; padding: 0.12rem 0.45rem; color: var(--muted); }
    .tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
    .tool-card { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 1.25rem; }
    .tool-name { font-family: var(--font-display); font-size: 0.95rem; font-weight: 700; margin-bottom: 0.3rem; }
    .tool-stars { font-family: var(--font-mono); font-size: 0.65rem; color: var(--accent); margin-bottom: 0.5rem; }
    .tool-desc { font-size: 0.82rem; color: #999; line-height: 1.6; }
    .for-you { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 4px; padding: 1.5rem; }
    .for-you-label { font-family: var(--font-mono); font-size: 0.65rem; color: var(--accent); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.75rem; }
    .for-you-body { font-size: 0.88rem; color: #bbb; line-height: 1.75; }
    .for-you-body p { margin-bottom: 0.75rem; }
    .for-you-body p:last-child { margin-bottom: 0; }
    .pick-card { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 1.5rem; display: flex; gap: 1.5rem; align-items: flex-start; }
    .pick-number { font-family: var(--font-mono); font-size: 2rem; color: var(--border); font-weight: 700; flex-shrink: 0; line-height: 1; }
    .pick-title { font-family: var(--font-display); font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
    .pick-desc { font-size: 0.85rem; color: #999; line-height: 1.6; }
    .issue-nav { display: flex; justify-content: space-between; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border); }
    .issue-nav a { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); text-decoration: none; }
    .issue-nav a:hover { color: var(--accent); }
    footer { text-align: center; padding: 2rem; border-top: 1px solid var(--border); font-family: var(--font-mono); font-size: 0.7rem; color: var(--muted); }
    footer a { color: var(--muted); text-decoration: none; margin: 0 0.75rem; }
    footer a:hover { color: var(--accent); }
  </style>
</head>
<body>
  <nav>
    <div class="nav-logo">LPX</div>
    <a href="/digest/" class="nav-back">← All issues</a>
  </nav>
  <div class="issue-wrap">
    <div class="issue-meta">Issue #${ISSUE_NUMBER} · ${TODAY_DISPLAY} · Weekly AI Digest</div>
    <h1 class="issue-title">${HEADLINE_LINE_1}<br>${HEADLINE_LINE_2}<br>${HEADLINE_LINE_3}</h1>
    <p class="issue-sub">${ONE_SENTENCE_SUMMARY}</p>

    <!-- BIG NEWS -->
    <div class="digest-section">
      <div class="digest-section-label">Big News</div>
      <!-- 3-4 x <div class="story"> blocks -->
    </div>

    <!-- TOOLS -->
    <div class="digest-section">
      <div class="digest-section-label">Tools Worth Knowing</div>
      <div class="tool-grid">
        <!-- 3-4 x <div class="tool-card"> blocks -->
      </div>
    </div>

    <!-- WILD CARD -->
    <div class="digest-section">
      <div class="digest-section-label">Wild Card</div>
      <!-- 1 x <div class="story"> block -->
    </div>

    <!-- FOR YOU -->
    <div class="digest-section">
      <div class="digest-section-label">For You — Pin Xiu</div>
      <div class="for-you">
        <div class="for-you-label">Personalised picks</div>
        <div class="for-you-body">
          <!-- 3 x <p> blocks, each starting with <strong>Tool/Story name</strong> -->
        </div>
      </div>
    </div>

    <!-- PICK OF THE WEEK -->
    <div class="digest-section">
      <div class="digest-section-label">Pick of the Week</div>
      <div class="pick-card">
        <div class="pick-number">01</div>
        <div>
          <div class="pick-title">${PICK_TITLE}</div>
          <div class="pick-desc">${PICK_DESC}</div>
        </div>
      </div>
    </div>

    <div class="issue-nav">
      <a href="/digest/">← All issues</a>
      <a href="/">Back to portfolio ↗</a>
    </div>
  </div>
  <footer>
    <a href="/digest/">All Issues</a>
    <a href="/">Portfolio</a>
    <a href="https://www.linkedin.com/in/pin-xiu-lim-376b1b115/" target="_blank">LinkedIn</a>
  </footer>
</body>
</html>
```

---

## Step 6 — Update digest/index.html

Before inserting, check if an entry for `${TODAY}.html` already exists in the file. Search for `href="${TODAY}.html"` — if found, **skip this step** (do not add a duplicate). If not found, add a new `<a class="digest-item">` entry **at the very top** of the `<div class="digest-list">` block (newest first):

```html
<a href="${TODAY}.html" class="digest-item">
  <div class="digest-date">${TODAY_DISPLAY}</div>
  <div>
    <div class="digest-item-title">Issue #${ISSUE_NUMBER} — ${SHORT_TITLE}</div>
    <div class="digest-item-desc">${ONE_SENTENCE_SUMMARY}</div>
    <div class="digest-item-tags">
      <span class="digest-tag">TAG_1</span>
      <span class="digest-tag">TAG_2</span>
    </div>
  </div>
</a>
```

---

## Step 7 — Update digest/manifest.json

Read the current `/tmp/portfolio/digest/manifest.json`. It is a JSON array ordered newest-first. Check if an entry with `"slug": "${TODAY}.html"` already exists — if so, update it in place. If not, prepend a new entry at the top:

```json
{
  "issue": ${ISSUE_NUMBER},
  "date": "${TODAY}",
  "dateDisplay": "${TODAY_DISPLAY}",
  "slug": "${TODAY}.html",
  "title": "${SHORT_TITLE}",
  "desc": "${ONE_SENTENCE_SUMMARY}",
  "tags": ["TAG_1", "TAG_2", "TAG_3"]
}
```

Write the updated array back to `/tmp/portfolio/digest/manifest.json`.

---

## Step 8 — Commit and push

```bash
cd /tmp/portfolio
git add digest/${TODAY}.html digest/index.html digest/manifest.json
git commit -m "Add AI Digest issue #${ISSUE_NUMBER} — ${TODAY}"
git push origin main
```

Vercel will auto-deploy within ~60 seconds. Done.

---

## Output checklist
- [ ] New `digest/YYYY-MM-DD.html` written with no placeholder text remaining
- [ ] `digest/index.html` updated (or skipped if date entry already exists)
- [ ] `digest/manifest.json` updated with new entry at top (or updated in place)
- [ ] Commit pushed to main
- [ ] No `${...}` variables left unreplaced in any output file
