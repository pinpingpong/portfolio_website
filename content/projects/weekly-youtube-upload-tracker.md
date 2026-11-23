---
title: Weekly YouTube Upload Tracker
section: workflow
order: 4
line: A Saturday routine that checks 4 channels and emails me what's new.
meta: Scheduled Automation
media:
  type: flow
  label: How the YouTube tracker works
  steps:
  - title: Saturday schedule
    detail: Claude Code cloud routine
    kind: in
  - title: Fetch 4 sources
    detail: YouTube RSS, channel page fallback past 15 items. A failed fetch is reported per source
  - title: Filter per source
    detail: Drop podcasts and livestreams, keep one show
  - title: Deliver
    detail: Email digest via Gmail MCP plus a phone notification, sent even with zero new videos
    kind: out
  caption: 'How it works. No screenshot: the digest goes to my inbox.'
highlights:
- Free YouTube RSS feeds, no API key or quota. Falls back to parsing the channel page where RSS only covers
  15 items
- 'Per-source filters: drops podcasts and livestreams on one channel, keeps a single show from a high-volume
  network channel'
- Reports a failed fetch per source instead of a false "0 new", and always sends, even with zero results
- First run hit a 403 from the cloud sandbox's network proxy. Failure alerts still arrived, proving delivery
  worked; allowlisting youtube.com fixed it
stack:
- Claude Code Routines
- Gmail MCP
- YouTube RSS
- Python
- Workflow Design
---

I watch a handful of YouTube channels and was checking each one by hand every week for new videos. Now a Claude Code cloud routine does it every Saturday morning: it checks all four sources for the past week's uploads, applies per-source filters, and sends me an email digest plus a phone notification. No custom agent. The work is in the prompt spec, source handling, filtering logic and failure handling, tested end to end.
