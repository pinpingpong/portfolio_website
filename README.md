# Lim Pin Xiu: Portfolio

Live: https://limpinxiu-portfolio-website.vercel.app

A static site showcasing my data science, analytics and AI work: live GenAI apps, agents,
tools built with AI, the AI workflows I use daily, and a weekly AI digest written by a
scheduled Claude agent. It also hosts an AI twin chatbot that visitors can question about my work.

## Stack

- Plain HTML, CSS and vanilla JS. No framework, no build step.
- Vercel for hosting and one Edge Function (`api/chat.js`).
- AI twin: Gemini (`gemini-flash-latest`, falling back to `gemini-flash-lite-latest`) with RAG over Pinecone.
- Google Fonts (Syne, DM Sans, DM Mono). Vercel Web Analytics and Speed Insights.

## Layout

| Path | What it is |
|---|---|
| `content/projects/*.md` | One file per project: the single source for its homepage row, detail page and AI twin chunks |
| `index.html` | The homepage. Project rows sit between `BUILD:rows` markers and are generated; edit everything else by hand |
| `projects/*.html` | Generated detail pages, served at `/projects/<slug>` |
| `scripts/build_site.py` | Builds the rows, detail pages and `sitemap.xml` from `content/projects/` |
| `styles.css` | All styles, including the mobile layout |
| `api/chat.js` | AI twin endpoint: request limits, retrieval, Gemini streaming |
| `scripts/build_public_index.py` | Rebuilds the AI twin's Pinecone index from the site content |
| `digest/` | Weekly AI digest issues, archive page and `manifest.json` (written by the digest agent) |
| `og-image.png`, `favicon.svg`, `robots.txt`, `sitemap.xml` | Link previews, icon and crawler files |
| `.github/workflows/site.yml` | CI: checks generated files are in sync, then rebuilds the AI twin index on push to `main` |
| `.vercelignore` | Keeps the README, scripts, content sources and the digest agent's skill file off the live site |

## Add or edit a project

1. Edit or add `content/projects/<slug>.md`. Front matter holds the row fields (title, section,
   order, line, meta, media, highlights, stack, links). Text before the first `## ` heading is the
   row summary. Any `## ` sections (Problem, How it works, Key decisions, What broke and how I
   fixed it, Limits and next steps) become a detail page at `/projects/<slug>` and add a
   "Read the write-up" link to the row.
2. `python3 scripts/build_site.py` (needs `pip install markdown pyyaml`).
3. Commit the Markdown and the generated files, then push. CI fails if you skipped step 2, and
   rebuilds the AI twin index when it passes.

## AI twin

1. The browser posts the conversation to `/api/chat`.
2. The function checks the request: same origin, at most 11 turns, 800 characters per message,
   and a per-IP limit of 8 requests a minute and 40 an hour (best effort, per edge instance).
3. It embeds the latest question with `gemini-embedding-001` and queries two Pinecone namespaces:
   - `website`: one chunk per project overview and per detail-page section (from `content/projects/`),
     plus the hero and experience entries from `index.html`.
   - `working-style`: curated, anonymous colleague feedback, built from a file kept outside this repo.
4. The best 5 matches are added to the system prompt and Gemini streams the answer back.

Each Gemini model gets its own timeout so the function always responds within Vercel's 25 second limit.
Only public, approved content goes into Pinecone, because the chatbot can quote anything it retrieves.

### Rebuild the index by hand

CI does this on every push to `main` that touches site content (repo secrets `PINECONE_API_KEY`
and `GEMINI_API_KEY`). To run it locally:

```bash
pip install pinecone google-genai
PINECONE_API_KEY=... GEMINI_API_KEY=... python scripts/build_public_index.py           # rebuild
python scripts/build_public_index.py --dry-run                                          # preview chunks only
```

The `working-style` namespace is rebuilt only when its source file exists locally
(default `~/Document/resume/how_i_work.md`, override with `HOW_I_WORK_PATH`); otherwise it is left as is.

## Run locally

```bash
npm install
cp .env.example .env      # add GEMINI_API_KEY, PINECONE_API_KEY, PINECONE_HOST
npm start                 # vercel dev on http://localhost:3000, includes /api/chat
npm run dev               # static preview only, no chatbot
```

## Deploy

Pushing to `main` deploys to production through Vercel's GitHub integration.
Set `GEMINI_API_KEY`, `PINECONE_API_KEY` and `PINECONE_HOST` in the Vercel project settings.
