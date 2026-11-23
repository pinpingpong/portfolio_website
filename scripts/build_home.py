"""Render the homepage (index.html) from scripts/home_template.html + content/projects.

Called by scripts/build_site.py; not run on its own. Page order: hero, outcome numbers,
two scroll stories (hand-written in the template), two showcases, then "All work" with every
project once (grid or list, filterable). Plain-English lines, badges and skill filters for
each project live in COPY and SKILLS below; a new project must be added to COPY and
INDEX_ORDER (the build stops with an error otherwise).
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import load_projects, ROOT

COPY = {
    "ai-twin-recruiter-chatbot": ("Ask a chatbot version of me anything about my work. It only answers from what's published on this site.", "Try it live"),
    "ai-assisted-price-intelligence": ("Found the same designer taps 40 to 55% cheaper overseas by comparing ~1,400 listings across Singapore, China and Germany.", "S$500 saved"),
    "content-analytics-agent": ("Ask questions about social media data in plain English and get answers, tables and charts back.", "Live app"),
    "weekly-ai-digest-agent": ("An agent that reads the week's AI news, keeps what matters and publishes a newsletter here by itself.", "Published weekly"),
    "aws-ai-certification-tutor": ("Unlimited practice questions for a brand-new AWS exam, with an explanation for every answer.", "Live app"),
    "claude-usage-menu-bar": ("A tiny Mac widget that shows my AI usage limits at a glance.", "Open source"),
    "analyst-agent": ("Turns a business question into data queries, a notebook and slides.", "Used at work"),
    "maplestory-r-idle-daily-agent": ("Plays my daily game chores for me so I never miss the rewards.", "Runs daily"),
    "career-interview-intelligence": ("Interview prep grounded in my real track record, with nothing made up.", "Landed the role"),
    "weekly-youtube-upload-tracker": ("Checks my favourite channels and emails me what's new.", "Every Saturday"),
    "ai-bazi-reader": ("Calculates a Chinese astrology chart exactly, then AI explains what it means.", "Live app"),
    "tiktok-content-workflow": ("Plans and drafts my TikTok content in my own voice.", "Content workflow"),
    "tiktok-analytics-dashboard": ("My first AI app: charts my TikTok posting and suggests what to post next.", "Live app"),
}
COPY.update({
    "renovation-ai-agent": ("Turns supplier catalogue links and a design brief into whole-room material schemes, rendered onto a real room.", "Live app"),
    "personal-finance-pipeline": ("Turns 80 bank statements from 5 banks into one dashboard that tracks big life goals.", "Personal system"),
    "inbox-cleanup-with-claude": ("A Claude skill I call when my inbox gets noisy: it finds promo senders in Gmail and Exchange and unsubscribes the ones I approve.", "100 lists cleared"),
})
# Skill filters on the project index (draft mapping for review)
SKILLS = {
    "RAG & LLM apps": ["ai-twin-recruiter-chatbot", "aws-ai-certification-tutor", "ai-bazi-reader", "content-analytics-agent",
                       "tiktok-analytics-dashboard"],
    "SQL & analytics": ["content-analytics-agent", "analyst-agent", "personal-finance-pipeline", "tiktok-analytics-dashboard"],
    "Automation": ["weekly-ai-digest-agent", "weekly-youtube-upload-tracker", "maplestory-r-idle-daily-agent",
                   "tiktok-content-workflow", "personal-finance-pipeline", "ai-assisted-price-intelligence",
                   "content-analytics-agent", "inbox-cleanup-with-claude"],
    "Prompt & workflow design": ["career-interview-intelligence", "tiktok-content-workflow", "inbox-cleanup-with-claude"],
}
TYPE = {"projects": "App", "agents": "Agent", "tools": "Tool", "workflow": "Workflow"}
INDEX_ORDER = ["renovation-ai-agent", "ai-twin-recruiter-chatbot", "personal-finance-pipeline", "ai-assisted-price-intelligence",
               "content-analytics-agent", "weekly-ai-digest-agent", "aws-ai-certification-tutor", "analyst-agent",
               "claude-usage-menu-bar", "maplestory-r-idle-daily-agent", "career-interview-intelligence",
               "weekly-youtube-upload-tracker", "inbox-cleanup-with-claude", "ai-bazi-reader", "tiktok-content-workflow", "tiktok-analytics-dashboard"]

SHOWCASE = ["ai-twin-recruiter-chatbot", "ai-assisted-price-intelligence"]

esc = html.escape
P = {p["slug"]: p for p in load_projects()}


def visual(p, autoplay=False):
    m = p.get("media") or {}
    if m.get("type") == "video" and autoplay:
        return f'<video src="/{m["src"]}" poster="/{m["poster"]}" muted loop playsinline preload="none" data-auto aria-label="{esc(m["alt"])}"></video>'
    src = m.get("poster") or m.get("src")
    return f'<img src="/{src}" alt="{esc(m.get("alt", ""))}" loading="lazy" decoding="async">' if src else ""


def showcase(slug, i):
    p = P[slug]; line, badge = COPY[slug]
    flip = " flip" if i % 2 else ""
    return f'''  <section class="show{flip}">
    <div class="wrap show-grid">
      <a class="show-visual reveal" href="/projects/{slug}">{visual(p, autoplay=True)}</a>
      <div class="show-text reveal">
        <span class="badge">{esc(badge)}</span>
        <h3>{esc(p["title"])}</h3>
        <p>{esc(line)}</p>
        <a class="story-link" href="/projects/{slug}">See how it works <span>→</span></a>
      </div>
    </div>
  </section>'''





def index_row(slug):
    p = P[slug]; line, badge = COPY[slug]
    skills = [s.lower().replace(" & ", "-").replace(" ", "-") for s, v in SKILLS.items() if slug in v]
    tags = "".join(f"<span>{esc(s)}</span>" for s in p.get("stack", [])[:3])
    links = p.get("links") or {}
    btn = []
    if links.get("live"):
        btn.append(f'<a href="{esc(links["live"])}" target="_blank" rel="noopener">Live ↗</a>')
    if links.get("github"):
        btn.append(f'<a href="{esc(links["github"])}" target="_blank" rel="noopener">Code ↗</a>')
    btn.append(f'<a class="primary" href="/projects/{slug}">Write-up →</a>')
    return f'''        <div class="irow" data-type="{TYPE[p["section"]].lower()}" data-skills="{" ".join(skills)}">
          <div><div class="iname">{esc(p["title"])}</div><div class="iline">{esc(line)}</div></div>
          <div class="itype mono">{TYPE[p["section"]]}</div>
          <div class="itags">{tags}</div>
          <div class="istatus"{' data-digest-badge' if slug == "weekly-ai-digest-agent" else ''}>{esc(badge)}</div>
          <div class="ilinks">{"".join(btn)}</div>
        </div>'''


THUMB = {  # grid thumbnails where the row media is a diagram or missing
    "renovation-ai-agent": "media/reno-after.webp",
    "personal-finance-pipeline": "media/finance-dashboard-charts.webp",
}


def grid_card(slug):
    p = P[slug]; line, badge = COPY[slug]
    skills = [s.lower().replace(" & ", "-").replace(" ", "-") for s, v in SKILLS.items() if slug in v]
    m = p.get("media") or {}
    img = THUMB.get(slug) or (m.get("poster") or m.get("src") if m.get("type") in ("image", "video") else None)
    pic = (f'<div class="pic"><img src="/{img}" alt="" loading="lazy" decoding="async"></div>' if img
           else f'<div class="pic noimg"><span>{TYPE[p["section"]]}</span></div>')
    return f'''          <a class="wcard reveal" href="/projects/{slug}" data-type="{TYPE[p["section"]].lower()}" data-skills="{" ".join(skills)}">
            {pic}
            <div class="body"><div class="meta"><span class="itype mono">{TYPE[p["section"]]}</span><span class="istatus"{' data-digest-badge' if slug == "weekly-ai-digest-agent" else ''}>{esc(badge)}</span></div>
              <h3>{esc(p["title"])}</h3><p>{esc(line)}</p></div>
          </a>'''


def chips():
    c = ['<button class="chip" data-f="all" aria-pressed="true">All</button>']
    c += [f'<button class="chip" data-f="{t.lower()}" aria-pressed="false">{t}s</button>' for t in TYPE.values()]
    c.append('<span class="chip-sep" aria-hidden="true"></span>')
    c += [f'<button class="chip" data-f="{s.lower().replace(" & ", "-").replace(" ", "-")}" aria-pressed="false">{esc(s)}</button>' for s in SKILLS]
    return "\n".join("        " + x for x in c)


assert sorted(INDEX_ORDER) == sorted(P), "INDEX_ORDER must list every project"
def render(chat_html=""):
    missing = set(P) - set(INDEX_ORDER)
    if missing:
        sys.exit(f"Add these projects to COPY and INDEX_ORDER in scripts/build_home.py: {sorted(missing)}")
    tpl = (ROOT / "scripts" / "home_template.html").read_text()
    return (tpl.replace("{{SHOWCASES}}", "\n".join(showcase(s, i) for i, s in enumerate(SHOWCASE)))
               .replace("{{CHIPS}}", chips())
               .replace("{{GRID}}", "\n".join(grid_card(s) for s in INDEX_ORDER))
               .replace("{{INDEX_ROWS}}", "\n".join(index_row(s) for s in INDEX_ORDER))
               .replace("{{N_PROJECTS}}", str(len(P)))
               .replace("{{CHAT}}", chat_html))
