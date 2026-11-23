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

## Problem

I follow a handful of YouTube channels and was checking each one by hand every week. Some channels also post far more than I want to see.

## How it works

1. **Schedule.** A Claude Code cloud routine runs every Saturday morning.
2. **Fetch.** It reads each channel's free YouTube RSS feed. RSS only lists the latest 15 items, so for busy channels it falls back to the channel page.
3. **Filter.** Each source has its own rules: one drops podcasts and livestreams, another keeps a single show from a high-volume network channel.
4. **Deliver.** It sends an email digest through the Gmail MCP connector plus a phone notification, even when there's nothing new.

## Key decisions

- **RSS instead of the YouTube API.** No API key, no quota, no setup, and enough for this job.
- **Per-source filters.** One global filter doesn't work when channels post very different things.
- **Always send, always say what failed.** A failed fetch is reported for that source instead of showing a misleading "0 new". If the digest stops arriving, I know something is broken.
- **No custom agent.** A routine with a clear prompt spec is enough. The work is in the spec, the source handling and the failure cases.

## What broke and how I fixed it

- **403 on the first run.** The cloud sandbox's network proxy blocked YouTube. The failure alerts still arrived, which proved the delivery path worked. Adding youtube.com to the allowlist fixed it.

## Limits

Personal routine, no public code. If a channel's page layout changes, the fallback needs updating.
