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
---

A scheduled agent that autonomously scrapes AI news each week, generates a styled HTML newsletter, and publishes it directly to this website — no manual steps. Built around a `SKILL.md` SOP that defines research queries, output format, a personalised "For You" section, and the full git push pipeline to auto-deploy via Vercel.
