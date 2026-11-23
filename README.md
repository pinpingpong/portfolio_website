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
| `content/projects/*.md` | One file per project: the single source for its homepage entry, its `/projects/<slug>` page and its AI twin chunks |
| `content/about.md` | About, experience, education and skills text the AI twin indexes |
| `content/resume.md` | Public resume (LinkedIn only, no phone or email) for `/resume` and the PDF |
| `scripts/home_template.html` | Homepage design: hero, outcome numbers, the two scroll stories, showcases, All work, digest strip |
| `scripts/build_home.py` | Plain-English lines, badges, skill filters and order for the homepage (`COPY`, `SKILLS`, `INDEX_ORDER`) |
| `scripts/build_site.py` | Builds `index.html`, `resume.html`, `projects/*.html` and `sitemap.xml`; `--check` is used in CI |
| `scripts/build_resume_pdf.py` | Renders `resume.html` to `Lim_Pin_Xiu_Resume.pdf` (Playwright, run locally) |
| `scripts/partials/chat.html`, `chat.css` | AI twin chat widget, included on every generated page |
| `api/chat.js` | AI twin endpoint: request limits, retrieval, Gemini streaming |
| `scripts/build_public_index.py` | Rebuilds the AI twin's Pinecone index from `content/` |
| `styles.css`, `revamp.css` | Styles for the project pages |
| `digest/` | Weekly AI digest issues, archive page and `manifest.json` (written by the digest agent; the homepage reads the manifest live) |
| `.github/workflows/site.yml` | CI: checks generated files are in sync, then rebuilds the AI twin index on push to `main` |

## Add or edit a project

1. Edit or add `content/projects/<slug>.md` (front matter for title, section, media, stack, links;
   text before the first `## ` is the summary; `## ` sections become the write-up).
2. For a new project, add its plain-English line and badge to `COPY` and its slug to `INDEX_ORDER`
   (and optionally `SKILLS`) in `scripts/build_home.py`. The build stops if you forget.
3. `python3 scripts/build_site.py` (needs `pip install markdown pyyaml`), commit, push.
   CI fails if step 3 was skipped, and rebuilds the AI twin index when it passes.

Resume changes: edit `content/resume.md`, run `build_site.py`, then
`.venv-capture/bin/python scripts/build_resume_pdf.py` for the PDF.

## AI twin

1. The browser posts the conversation to `/api/chat`.
2. The function checks the request: same origin, at most 11 turns, 800 characters per message,
   and a per-IP limit of 8 requests a minute and 40 an hour (best effort, per edge instance).
3. It embeds the latest question with `gemini-embedding-001` and queries two Pinecone namespaces:
   - `website`: one chunk per project overview and per write-up section (`content/projects/`),
     plus about and experience (`content/about.md`).
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
