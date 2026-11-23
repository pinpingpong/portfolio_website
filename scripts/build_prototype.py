"""Build prototype.html (revamp preview) from scripts/prototype_template.html + content/projects."""
import html, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import load_projects, md_inline, SECTION_LABEL, ROOT

SKIP = {"renovation-ai-agent", "personal-finance-pipeline"}          # told as stories
ORDER = ["ai-twin-recruiter-chatbot", "content-analytics-agent", "weekly-ai-digest-agent", "ai-assisted-price-intelligence",
         "aws-ai-certification-tutor", "claude-usage-menu-bar", "maplestory-r-idle-daily-agent", "career-interview-intelligence",
         "weekly-youtube-upload-tracker", "analyst-agent", "ai-bazi-reader", "tiktok-content-workflow", "tiktok-analytics-dashboard"]
BIG = {"ai-twin-recruiter-chatbot", "ai-assisted-price-intelligence"}

projects = {p["slug"]: p for p in load_projects()}
cards = []
for slug in ORDER + sorted(set(projects) - set(ORDER) - SKIP):
    p = projects[slug]
    m = p.get("media") or {}
    img = m.get("poster") or m.get("src") if m.get("type") in ("image", "video") else None
    cls = "card reveal" + (" big" if slug in BIG else "") + ("" if img else " noimg")
    pic = f'<img src="/{img}" alt="" loading="lazy" decoding="async">' if img else ""
    cards.append(f'''        <a class="{cls}" href="/projects/{slug}">{pic}
          <div class="card-body"><div class="card-kind mono">{html.escape(SECTION_LABEL[p["section"]])}</div>
            <h3>{html.escape(p["title"])}</h3><p>{md_inline(p["line"])}</p></div>
        </a>''')
tpl = (ROOT / "scripts" / "prototype_template.html").read_text()
(ROOT / "prototype.html").write_text(tpl.replace("{{WALL}}", "\n".join(cards)))
print(f"prototype.html: {len(cards)} wall cards")
