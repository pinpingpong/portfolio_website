---
title: Weekly AI Digest Agent
section: agents
order: 3
line: Researches AI news every week and publishes the issue to this site by itself.
meta: Personal
media:
  type: image
  src: media/ai-digest.webp
  alt: Digest issues published to this site by the scheduled agent
  width: 1200
  height: 750
  caption: Digest issues published to this site by the scheduled agent
highlights:
- Runs 6 targeted search queries to sweep models, tools, research, and industry news
- Generates a dark-themed HTML issue with Big News, Tool Cards, Wild Card, and Pick of the Week
- '"For You" section personalised to my stack, projects, and career direction each week'
- Auto-commits new issue + updates archive index — Vercel deploys within 60s
stack:
- Claude Code Routines
- SKILL.md
- Web Search
- GitHub API
- Vercel
featured: 4
---

A scheduled agent that autonomously scrapes AI news each week, generates a styled HTML newsletter, and publishes it directly to this website — no manual steps. Built around a `SKILL.md` SOP that defines research queries, output format, a personalised "For You" section, and the full git push pipeline to auto-deploy via Vercel.

## Problem

There is far too much AI news, and most of it isn't relevant to me. I wanted a filter: once a week, only the stories that are interesting or related to my work, without reading ten sites. I also wanted the result published somewhere useful, not lost in an inbox. The [digest archive](/digest/) on this site is the output.

## How it works

1. **Schedule.** A Claude Code routine runs once a week.
2. **Research.** It runs 6 searches covering news sites, model releases, agent frameworks, funding, trending open-source tools and productivity tools, then picks 8 to 12 unique stories.
3. **Write.** It sorts the stories into sections (Big News, Tool Cards, Wild Card, Pick of the Week) and writes a "For You" section based on my stack, projects and direction.
4. **Publish.** It generates the issue as HTML, adds it to the archive page and `manifest.json`, then commits and pushes to GitHub. Vercel deploys it within about a minute, and the homepage preview updates from the manifest.

## Key decisions

- **The SOP is the product.** The whole agent is one `SKILL.md` file: searches, format, HTML template and the git steps. Changing the digest means editing a document, not code.
- **Fixed searches for coverage.** Six set queries cover different parts of the field every week, so the issue doesn't depend on what happens to trend that day.
- **Publish through git.** Pushing to the site repo reuses the existing deploy, with no separate hosting or CMS.
- **A manifest for the homepage.** The homepage reads `manifest.json` to show the latest issues, so the agent never has to edit the homepage itself.

## What broke and how I fixed it

- **Duplicate issues.** A rerun on the same day added a second archive entry. The SOP now checks whether the day's issue already exists, updates it in place if so, and skips adding another link.
- **Personal details in a public file.** The SOP lives in a public repo, so its commit identity now uses GitHub's no-reply email.

## Limits

Story selection depends on what web search returns that week, so coverage of niche releases is uneven.
