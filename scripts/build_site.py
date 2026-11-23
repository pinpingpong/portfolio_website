"""
Build the work rows in index.html and one detail page per project from content/projects/*.md.

Each Markdown file is the single source for a project:
  - front matter (YAML): title, section, order, line, meta, media, highlights, stack, links
  - text before the first "## " heading: the summary shown in the homepage row
  - "## " sections (Problem, How it works, Key decisions, ...): the detail page only.
    A project gets a page at /projects/<slug> (and a "Read the write-up" link on its row)
    only when its file has at least one "## " section.

The same files feed the AI Twin index (scripts/build_public_index.py).

Usage:
  python3 scripts/build_site.py           # write index.html, projects/*.html, sitemap.xml
  python3 scripts/build_site.py --check   # exit 1 if any output is out of date (used in CI)

Requires: pip install markdown pyyaml
"""

import html
import re
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "projects"
INDEX = ROOT / "index.html"
PAGES = ROOT / "projects"
SITEMAP = ROOT / "sitemap.xml"
SITE = "https://limpinxiu-portfolio-website.vercel.app"
SECTIONS = ["projects", "agents", "tools", "workflow"]
SECTION_LABEL = {"projects": "Live App", "agents": "AI Agent", "tools": "Tool built with AI", "workflow": "AI Workflow"}

ICON_LAUNCH = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
ICON_GITHUB = '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>'
ICON_CHAT = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
STREAMLIT_NOTE = "Hosted on Streamlit's free tier. If it's asleep, click \"Yes, get this app back up\" and give it about 30 seconds."

esc = html.escape


# ── Loading ──────────────────────────────────────────────────────────────────

def load_projects():
    projects = []
    for path in sorted(CONTENT.glob("*.md")):
        raw = path.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            sys.exit(f"{path}: missing front matter")
        fm = yaml.safe_load(m.group(1))
        body = m.group(2)
        parts = re.split(r"^## ", body, flags=re.M)
        fm["slug"] = path.stem
        fm["summary"] = parts[0].strip()
        fm["sections"] = []
        for part in parts[1:]:
            heading, _, text = part.partition("\n")
            fm["sections"].append((heading.strip(), text.strip()))
        fm["has_page"] = bool(fm["sections"])
        if fm.get("section") not in SECTIONS:
            sys.exit(f"{path}: section must be one of {SECTIONS}")
        projects.append(fm)
    return projects


def md_block(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def md_inline(text):
    out = md_block(text).strip()
    return re.sub(r"^<p>(.*)</p>$", r"\1", out, flags=re.S)


# ── Shared pieces ────────────────────────────────────────────────────────────

def media_html(media, indent="            "):
    if not media:
        return ""
    t = media["type"]
    cap = esc(media["caption"])
    if t == "image":
        inner = (f'<img src="/{media["src"]}" alt="{esc(media["alt"])}" width="{media["width"]}" '
                 f'height="{media["height"]}" loading="lazy" decoding="async">')
        return (f'{indent}<figure class="row-media">\n{indent}  {inner}\n'
                f'{indent}  <figcaption>{cap}</figcaption>\n{indent}</figure>\n')
    if t == "video":
        inner = (f'<video src="/{media["src"]}" poster="/{media["poster"]}" muted loop playsinline '
                 f'preload="none" aria-label="{esc(media["alt"])}"></video>')
        return (f'{indent}<figure class="row-media">\n{indent}  {inner}\n'
                f'{indent}  <figcaption>{cap}</figcaption>\n{indent}</figure>\n')
    if t == "flow":
        items = []
        for i, st in enumerate(media["steps"]):
            if i:
                items.append('<li class="flow-arrow" aria-hidden="true"></li>')
            kind = f' flow-{st["kind"]}' if st.get("kind") else ""
            items.append(f'<li class="flow-step{kind}"><span class="flow-title">{esc(st["title"])}</span>'
                         f'<span class="flow-detail">{esc(st["detail"])}</span></li>')
        lis = "".join(f"\n{indent}    {x}" for x in items)
        return (f'{indent}<figure class="row-media row-flow" aria-label="{esc(media["label"])}">\n'
                f'{indent}  <ol class="flow">{lis}\n{indent}  </ol>\n'
                f'{indent}  <figcaption>{cap}</figcaption>\n{indent}</figure>\n')
    sys.exit(f"unknown media type {t}")


def stack_html(p, cls, indent):
    tags = "".join(f'\n{indent}  <span class="stack-tag">{esc(s)}</span>' for s in p.get("stack", []))
    return f'{indent}<div class="{cls}">{tags}\n{indent}</div>\n'


def buttons_html(p, indent, on_page=False):
    links = p.get("links", {}) or {}
    btns = []
    if links.get("live"):
        btns.append(f'<a href="{esc(links["live"])}" target="_blank" class="btn-launch">{ICON_LAUNCH} Launch Live App</a>')
    if links.get("try_twin"):
        if on_page:
            btns.append(f'<a href="/#projects" class="btn-launch">{ICON_CHAT} Try It on the Homepage</a>')
        else:
            btns.append(f'<button class="btn-launch" onclick="document.getElementById(\'chat-btn\').click(); '
                        f'this.closest(\'section\').scrollIntoView();">{ICON_CHAT} Try It Live ↗</button>')
    if links.get("github"):
        btns.append(f'<a href="{esc(links["github"])}" target="_blank" class="btn-github">{ICON_GITHUB} GitHub</a>')
    if p["has_page"] and not on_page:
        btns.append(f'<a href="/projects/{p["slug"]}" class="btn-github btn-more">Read the write-up →</a>')
    if not btns:
        return ""
    inner = "".join(f"\n{indent}  {b}" for b in btns)
    out = f'{indent}<div class="card-footer">{inner}\n{indent}</div>\n'
    if p.get("streamlit_note"):
        out += f'{indent}<div class="card-note">{esc(STREAMLIT_NOTE)}</div>\n'
    return out


# ── Homepage rows ────────────────────────────────────────────────────────────

def row_html(p):
    i = "            "
    workflow = p["section"] == "workflow"
    desc_cls = "workflow-desc" if workflow else "card-desc"
    hl_cls = "workflow-highlights" if workflow else "agent-highlights"
    stack_cls = "workflow-stack" if workflow else "card-stack"
    out = [f'''        <details class="work-row reveal" data-title="{esc(p["title"])}">
          <summary>
            <span class="row-num">{p["order"]:02d}</span>
            <span class="row-main">
              <span class="row-title">{esc(p["title"])}</span>
              <span class="row-line">{md_inline(p["line"])}</span>
            </span>
            <span class="row-meta">{esc(p["meta"])}</span>
            <span class="row-icon" aria-hidden="true"></span>
          </summary>
          <div class="row-body">
''']
    out.append(media_html(p.get("media"), i))
    out.append(f'{i}<p class="{desc_cls}">{md_inline(p["summary"])}</p>\n')
    if p.get("highlights"):
        items = "".join(f'\n{i}  <div class="highlight-item"><span class="highlight-dot"></span><span>{md_inline(h)}</span></div>'
                        for h in p["highlights"])
        out.append(f'{i}<div class="{hl_cls}">{items}\n{i}</div>\n')
    out.append(stack_html(p, stack_cls, i))
    out.append(buttons_html(p, i))
    out.append("          </div>\n        </details>\n")
    return "".join(out)


def tile_html(p):
    m = p.get("media") or {}
    img = m.get("poster") or m.get("src") if m.get("type") in ("image", "video") else None
    visual = (f'<div class="tile-frame"><span class="tile-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
              f'<img src="/{img}" alt="{esc(m.get("alt", ""))}" loading="lazy" decoding="async"></div>') if img else ""
    href = f"/projects/{p['slug']}" if p["has_page"] else f"#{p['section']}"
    return f'''        <a class="feature-tile reveal" href="{href}">
          {visual}
          <div class="tile-text">
            <span class="tile-kind">{esc(SECTION_LABEL[p["section"]])}</span>
            <span class="tile-title">{esc(p["title"])}</span>
            <span class="tile-line">{md_inline(p["line"])}</span>
            <span class="tile-more">View project <span aria-hidden="true">→</span></span>
          </div>
        </a>
'''


def build_index(projects):
    s = INDEX.read_text()
    if "<!-- BUILD:featured -->" in s:
        feats = sorted((p for p in projects if p.get("featured")), key=lambda p: p["featured"])
        a = s.index("<!-- BUILD:featured -->") + len("<!-- BUILD:featured -->")
        s = s[:a] + "\n" + "".join(tile_html(p) for p in feats) + "        " + s[s.index("<!-- /BUILD:featured -->"):]
    for sec in SECTIONS:
        rows = sorted((p for p in projects if p["section"] == sec), key=lambda p: p["order"])
        block = "\n".join(row_html(p) for p in rows)
        start, end = f"<!-- BUILD:rows:{sec} -->", f"<!-- /BUILD:rows:{sec} -->"
        if start not in s:
            sys.exit(f"index.html: marker {start} missing")
        a = s.index(start) + len(start)
        b = s.index(end)
        s = s[:a] + "\n" + block + "        " + s[b:]
    return s


# ── Detail pages ─────────────────────────────────────────────────────────────

def page_html(p):
    url = f"{SITE}/projects/{p['slug']}"
    desc = re.sub(r"\s+", " ", re.sub(r"[`*_\[\]]", "", p["line"]))
    links = p.get("links", {}) or {}
    status = p.get("status")
    meta_bits = [SECTION_LABEL[p["section"]]] + ([status] if status else []) + ([p["dates"]] if p.get("dates") else [])
    og_img = f'{SITE}/{p["media"]["poster"] if p.get("media", {}).get("type") == "video" else p["media"]["src"]}' \
        if p.get("media") and p["media"]["type"] in ("image", "video") else f"{SITE}/og-image.png"
    sections = "".join(
        f'\n      <div class="proj-section">\n        <h2>{esc(h)}</h2>\n        {md_block(t)}\n      </div>'
        for h, t in p["sections"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Generated by scripts/build_site.py from content/projects/{p["slug"]}.md. Edit the Markdown, not this file. -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(p["title"])} | Lim Pin Xiu</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#09090b" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{esc(p["title"])} | Lim Pin Xiu" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:image" content="{og_img}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/revamp.css">
</head>
<body class="proj-page">
  <nav>
    <a class="nav-logo" href="/">LPX</a>
    <div class="nav-links">
      <a href="/#{p["section"]}">← All work</a>
    </div>
  </nav>

  <main class="proj-inner">
    <header class="proj-header">
      <div class="section-label">{" · ".join(esc(b) for b in meta_bits)}</div>
      <h1 class="proj-title">{esc(p["title"])}</h1>
      <p class="proj-line">{md_inline(p["line"])}</p>
{stack_html(p, "card-stack", "      ")}{buttons_html(p, "      ", on_page=True)}    </header>

{media_html(p.get("media"), "    ")}
    <p class="proj-summary">{md_inline(p["summary"])}</p>
    <article class="proj-body">{sections}
    </article>

    <footer class="proj-footer">
      <a href="/#{p["section"]}">← Back to all work</a>
      <span>Questions? Ask my AI twin on the <a href="/">homepage</a>.</span>
    </footer>
  </main>
</body>
</html>
'''


def build_sitemap(projects):
    urls = [f"{SITE}/", f"{SITE}/digest/"] + [f"{SITE}/projects/{p['slug']}" for p in projects if p["has_page"]]
    locs = "".join(f"\n  <url><loc>{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}\n</urlset>\n'


def main():
    check = "--check" in sys.argv
    projects = load_projects()
    outputs = {INDEX: build_index(projects), SITEMAP: build_sitemap(projects)}
    for p in projects:
        if p["has_page"]:
            outputs[PAGES / f"{p['slug']}.html"] = page_html(p)
    stale_pages = [f for f in PAGES.glob("*.html") if f not in outputs] if PAGES.exists() else []

    changed = [f for f, text in outputs.items() if not f.exists() or f.read_text() != text]
    if check:
        problems = [str(f.relative_to(ROOT)) for f in changed + stale_pages]
        if problems:
            print("Out of date, run: python3 scripts/build_site.py\n  " + "\n  ".join(problems))
            sys.exit(1)
        print("Site is in sync with content/projects.")
        return
    PAGES.mkdir(exist_ok=True)
    for f in changed:
        f.write_text(outputs[f])
    for f in stale_pages:
        f.unlink()
    print(f"{len(projects)} projects, {sum(p['has_page'] for p in projects)} detail pages. "
          f"Updated: {', '.join(str(f.relative_to(ROOT)) for f in changed + stale_pages) or 'nothing'}")


if __name__ == "__main__":
    main()
