---
title: TikTok Content Workflow
section: workflow
order: 1
line: An agentic content workflow. Every week Claude proposes posts from my calendar and life, I tick what to make, and it builds them, carousel images included.
meta: Content Creation
highlights:
- 'Weekly run on my Mac proposes posts as a checklist in Notion; nothing is built until I tick it'
- 'Builds approved posts end to end: copy, 5 discovery hashtags, photos from my library, rendered carousel slides'
- '11 finished carousels in the first two days, at zero API cost'
- 'Faceless by design: photos with a detected face are filtered out before I see them'
stack:
- Claude Code
- Notion MCP
- Python
- Playwright
- SQLite
- launchd
---

My TikTok content runs as a two-step agentic workflow. Every week, Claude reads my Notion content calendar and my private planning notes, then proposes what to post as a checklist. I tick what I want, and a second step builds those posts: captions and hashtags in my voice and, for carousels, the finished slide images made from my own photos.

## Problem

Running a TikTok account alongside a full-time job means captions, hashtags and slides every week, and generic AI output sounds like everyone else. Carousels were the slowest part: copying text into a design app slide by slide, then hunting for the right trip photo among thousands. And planning kept slipping: posts went overdue, and things I was actually doing never made it onto the calendar.

## How it works

1. **Suggest (scheduled).** A scheduled job on my Mac runs every Sunday, or at the next login if the laptop was off, so a missed week still runs. Claude Code reads the Notion calendar and my private notes (upcoming trips, events, milestones), finds open slots, overdue posts and posts that still need slides, and writes a "Weekly plan" checklist page in Notion. It changes nothing else.
2. **Approve.** I tick the items I want built, moved or added as ideas. Unticked items are ignored.
3. **Build (on demand).** One command builds only the ticked items:
   - **Carousels:** slide copy, caption, 5 hashtags, photos and rendered PNG slides, plus a paste-ready block in Notion.
   - **Videos:** a title, caption and 5 hashtags, ready to paste over my own edit.
4. **Pick photos.** For travel posts, a script reads a copy of my photo library's metadata, finds the trip by date and GPS (even which hotel, by where the phone spent the night), shortlists the best-rated shots and drops any photo with a detected face. I check a contact sheet before anything is used.
5. **Render.** Each carousel is a small JSON file. An HTML/CSS template turns it into 1080x1350 slides with a headless browser, in one of three colour themes (travel, lifestyle, review).

## Key decisions

- **Suggest and build are separate steps.** The weekly run can only propose. Nothing gets written, moved or rendered until I approve it, which keeps the agent useful without letting it run my account.
- **Rules, not vibes.** A written rulebook sets my voice and hard rules: no em dashes, exactly 5 hashtags chosen for discovery, a verdict on every review, and posting days by theme. Specific rules are easy to check and fix most of what makes AI captions sound generic.
- **Private notes stay private.** The scheduled job can read my planning notes but only writes public topics and loose timing to Notion. It never writes dates, names, amounts or anything about work, and access to raw files is blocked.
- **Render locally instead of using an image-generation API.** Templates keep every post on brand, cost nothing, and use real photos instead of generated ones.
- **Faceless by design.** Faces are filtered out automatically, and serial numbers and licence plates are blurred. Reviews use only official artwork, credited on the slide.

## Limits and next steps

- Face detection misses some photos, so I still check each contact sheet.
- It runs only when my Mac is on, because the photos and notes are local.
- Posting is still manual. Next: video rough cuts from raw footage (local transcription plus automated trims).
