"""Render resume.html to the downloadable PDF with Playwright (print styles, A4).
Run locally: .venv-capture/bin/python scripts/build_resume_pdf.py"""
import yaml, re, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---", (ROOT / "content/resume.md").read_text(), re.S).group(1))
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/resume.html"); pg.wait_for_timeout(1500)
    pg.emulate_media(media="print")
    pg.pdf(path=str(ROOT / fm["pdf"]), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
srv.shutdown()
print("wrote", fm["pdf"])
