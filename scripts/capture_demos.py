"""Capture demo screenshots and short recordings for the portfolio work rows.

Drives each public demo with Playwright (headless Chromium), waits for a real result,
then saves a PNG (and, for some, a WebM recording) to RAW_DIR. `--publish` converts
the raw files into compressed media in ../media/ (WebP stills, MP4 loops).

Setup (once):
  python3.11 -m venv .venv-capture
  .venv-capture/bin/pip install playwright pillow
  .venv-capture/bin/python -m playwright install chromium

Usage:
  .venv-capture/bin/python scripts/capture_demos.py [name ...] [--raw DIR]
  .venv-capture/bin/python scripts/capture_demos.py --publish [--raw DIR]

Notes:
- Streamlit apps may be asleep; the script clicks the wake button and waits.
- Each run uses real API calls on the apps' demo keys (one run per app).
- The TikTok demos use tiktok_sample_data.json from the public content-analytics-agent repo.
"""
import argparse
import asyncio
import os
import shutil
import subprocess
import time
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media"
SAMPLE_TIKTOK = Path.home() / "Document" / "nlp_sql" / "tiktok_sample_data.json"
VIEW = {"width": 1440, "height": 900}
SITE = "https://limpinxiu-portfolio-website.vercel.app/"

# name -> (url, record_video)
TARGETS = {
    "aws-tutor": ("https://px-aws-tutor.streamlit.app/", True),
    "tiktok-analytics": ("https://px-tiktok-strategist.streamlit.app/", False),
    "bazi-reader": ("https://px-bazireader.streamlit.app/", False),
    "content-agent": ("https://px-content-analytics-agent.streamlit.app/", True),
    "reno-agent": ("https://px-renovation-ai-agent.streamlit.app/", False),
    "ai-twin": (SITE, True),
    "ai-digest": (SITE, False),
}


# Streamlit apps without a fixed theme follow the browser; capture these in dark mode to match the site
DARK = {"content-agent"}

START = {}  # page -> monotonic time when the demo interaction starts (video trim point)


def mark(page):
    START[id(page)] = time.monotonic()


async def streamlit_frame(page, url):
    """Open a Streamlit Cloud app, wake it if asleep, return the app iframe."""
    await page.goto(url, wait_until="domcontentloaded", timeout=90000)
    await page.wait_for_timeout(5000)
    wake = page.get_by_role("button", name="Yes, get this app back up!")
    if await wake.count():
        print(f"  waking {url}")
        await wake.click()
    for _ in range(60):
        frame = next((f for f in page.frames if "/~/+/" in f.url), None)
        if frame and await frame.locator('[data-testid="stApp"]').count():
            await frame.locator('[data-testid="stApp"]').wait_for(timeout=120000)
            await page.wait_for_timeout(4000)
            return frame
        await page.wait_for_timeout(3000)
    raise RuntimeError(f"Streamlit app never loaded: {url}")


async def idle(frame, timeout_s=240):
    """Wait until Streamlit stops running (no spinner / status widget)."""
    await frame.page.wait_for_timeout(2000)
    for _ in range(timeout_s // 2):
        busy = await frame.locator('[data-testid="stSpinner"], [data-testid="stStatusWidget"]').count()
        if not busy:
            await frame.page.wait_for_timeout(2500)
            return
        await frame.page.wait_for_timeout(2000)
    print("  warning: still busy after timeout")


async def scroll_main(frame, y):
    await frame.evaluate(
        "y => { const m = document.querySelector('[data-testid=\"stMain\"]') || document.querySelector('section.main');"
        " if (m) m.scrollTo(0, y); window.scrollTo(0, y); }", y)
    await frame.page.wait_for_timeout(800)


# ── per-target flows ─────────────────────────────────────────────────────────
async def aws_tutor(page, url):
    f = await streamlit_frame(page, url)
    mark(page)
    await f.get_by_role("button", name="Generate Question").click()
    await idle(f)
    await f.locator('[data-testid="stRadio"] label').first.wait_for(timeout=120000)
    await page.wait_for_timeout(1500)
    await page.screenshot(path=str(RAW / "aws-tutor.png"))
    await f.locator('[data-testid="stRadio"] label').nth(1).click()
    await page.wait_for_timeout(800)
    await f.get_by_role("button", name="Submit Answer").click()
    await idle(f)
    await scroll_main(f, 400)
    await page.wait_for_timeout(2500)
    await page.screenshot(path=str(RAW / "aws-tutor-feedback.png"))


async def tiktok_analytics(page, url):
    f = await streamlit_frame(page, url)
    await f.locator('input[type="file"]').set_input_files(str(SAMPLE_TIKTOK))
    await idle(f)
    await page.wait_for_timeout(4000)
    await scroll_main(f, 450)
    await page.screenshot(path=str(RAW / "tiktok-analytics.png"))


async def bazi_reader(page, url):
    f = await streamlit_frame(page, url)
    await f.get_by_role("button", name="Calculate & Analyse").click()
    await idle(f, 300)
    await page.screenshot(path=str(RAW / "bazi-reader.png"))
    await scroll_main(f, 700)
    await page.screenshot(path=str(RAW / "bazi-reader-2.png"))


async def content_agent(page, url):
    f = await streamlit_frame(page, url)
    mark(page)
    box = f.locator('[data-testid="stChatInputTextArea"], textarea').first
    await box.click()
    await box.type("Top 5 posts by likes, as a bar chart", delay=35)
    await box.press("Enter")
    await idle(f)
    await page.wait_for_timeout(3000)
    await scroll_main(f, 420)
    await page.screenshot(path=str(RAW / "content-agent.png"))


async def reno_agent(page, url):
    f = await streamlit_frame(page, url)
    ta = f.get_by_role("textbox", name="One URL per line").first
    await ta.fill("https://www.lamitak.com/collections/solids\nhttps://www.lamitak.com/collections/patterns")
    await f.get_by_text("Fetch & curate").first.click()  # blur so Streamlit registers the text
    btn = f.get_by_role("button", name="Fetch & Curate Catalog")
    await f.wait_for_function("() => [...document.querySelectorAll('button')].some("
                              "b => b.innerText.includes('Fetch & Curate Catalog') && !b.disabled)", timeout=30000)
    await btn.click()
    await idle(f, 300)
    await scroll_main(f, 600)
    await page.screenshot(path=str(RAW / "reno-agent.png"))


async def ai_twin(page, url):
    await page.goto(url, wait_until="networkidle", timeout=90000)
    await page.wait_for_timeout(2000)
    mark(page)
    await page.click("#chat-btn")
    await page.wait_for_timeout(1200)
    await page.fill("#chat-input", "")
    await page.type("#chat-input", "What have you built with AI agents?", delay=35)
    await page.click("#chat-send")
    # wait for the typing indicator to go and a second bot bubble to appear (Gemini can take ~15s)
    await page.wait_for_function(
        "document.querySelectorAll('#chat-messages .msg.bot .msg-bubble').length >= 2 &&"
        " !document.getElementById('typing-indicator')", timeout=90000)
    await page.wait_for_timeout(2000)
    await page.screenshot(path=str(RAW / "ai-twin.png"))


async def ai_digest(page, url):
    await page.goto(url + "#digest", wait_until="networkidle", timeout=90000)
    await page.wait_for_timeout(2500)
    el = page.locator("#digest")
    await el.scroll_into_view_if_needed()
    await page.evaluate("document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible','in','show'))")
    await page.wait_for_timeout(1500)
    await el.screenshot(path=str(RAW / "ai-digest.png"))


FLOWS = {
    "aws-tutor": aws_tutor, "tiktok-analytics": tiktok_analytics, "bazi-reader": bazi_reader,
    "content-agent": content_agent, "reno-agent": reno_agent, "ai-twin": ai_twin, "ai-digest": ai_digest,
}


async def run_one(browser, name):
    url, record = TARGETS[name]
    vid_dir = RAW / f"_video_{name}"
    ctx = await browser.new_context(viewport=VIEW, device_scale_factor=1,
                                    color_scheme="dark" if name in DARK else "light",
                                    record_video_dir=str(vid_dir) if record else None,
                                    record_video_size=VIEW if record else None)
    t0 = time.monotonic()
    page = await ctx.new_page()
    try:
        await FLOWS[name](page, url)
        print(f"ok   {name}")
    except Exception as e:
        print(f"FAIL {name}: {type(e).__name__}: {str(e)[:200]}")
        await page.screenshot(path=str(RAW / f"{name}-FAILED.png"))
    finally:
        await ctx.close()
        if record:
            vids = list(vid_dir.glob("*.webm"))
            if vids:
                shutil.move(str(vids[0]), str(RAW / f"{name}.webm"))
                offset = max(0.0, START.get(id(page), t0) - t0 - 0.5)
                (RAW / f"{name}.start").write_text(f"{offset:.1f}")
            shutil.rmtree(vid_dir, ignore_errors=True)


async def capture(names):
    RAW.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        await asyncio.gather(*(run_one(browser, n) for n in names))
        await browser.close()


# ── publish: compress into media/ ────────────────────────────────────────────
def publish():
    from PIL import Image
    MEDIA.mkdir(exist_ok=True)
    for png in sorted(RAW.glob("*.png")):
        if png.stem.endswith("FAILED"):
            continue
        img = Image.open(png).convert("RGB")
        if img.width > 1200:
            img = img.resize((1200, round(img.height * 1200 / img.width)), Image.LANCZOS)
        # Wider than the 16:10 row frame: pad top/bottom with the page background so
        # object-fit: cover does not crop the sides
        target_h = round(img.width * 10 / 16)
        if img.height < target_h:
            canvas = Image.new("RGB", (img.width, target_h), img.getpixel((2, 2)))
            canvas.paste(img, (0, (target_h - img.height) // 2))
            img = canvas
        out = MEDIA / f"{png.stem}.webp"
        img.save(out, "WEBP", quality=80, method=6)
        print(f"{out.name}: {out.stat().st_size // 1024} KB")
    for webm in sorted(RAW.glob("*.webm")):
        out = MEDIA / f"{webm.stem}.mp4"
        start = (RAW / f"{webm.stem}.start")
        ss = start.read_text().strip() if start.exists() else "0"
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", str(webm)], capture_output=True, text=True).stdout)
        speed = max(1.0, (dur - float(ss)) / 16)  # aim for <=16s of motion
        # skip the app wake-up, speed up only long clips, hold the result 2.5s, 960px wide, no audio
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", ss, "-i", str(webm),
                        "-vf", f"setpts=PTS/{speed:.2f},scale=960:-2,fps=15,tpad=stop_mode=clone:stop_duration=2.5",
                        "-an", "-t", "20",
                        "-c:v", "libx264", "-crf", "30", "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(out)], check=True)
        print(f"{out.name}: {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", help=f"subset of {list(TARGETS)}")
    ap.add_argument("--raw", default=str(ROOT / ".demo_raw"))
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    RAW = Path(a.raw)
    if a.publish:
        publish()
    else:
        asyncio.run(capture(a.names or list(TARGETS)))
