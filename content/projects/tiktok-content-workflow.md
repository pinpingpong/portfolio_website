---
title: TikTok Content Workflow
section: workflow
order: 1
line: A Claude persona plus a Notion calendar run my content planning and scripts.
meta: Content Creation
highlights:
- 'Custom persona enforces voice rules: no em dashes, exactly 5 hashtags, verdict on every review'
- Notion MCP connects Claude directly to my content calendar — plan, draft, slot in one flow
- 'Content mapped around real events: Ipoh trip, concerts, Vancouver-Alaska cruise series'
stack:
- Claude
- Notion MCP
- Prompt Engineering
- Workflow Design
---

My entire TikTok content operation runs through Claude and Notion. I designed a custom content persona (`SKILL.md`) that nails my voice — grounded, casual, no AI buzzwords — and generates scripts, captions, and hashtags on demand. A Notion workspace with linked Content Calendar and Ideas databases keeps everything planned around real life events like trips, concerts, and reviews.

## Problem

Running a TikTok account alongside a full-time job means scripts, captions and hashtags every week, and generic AI output sounds like everyone else. I wanted help with the writing that sounds like me, tied to a calendar planned around my real life.

## How it works

1. **Persona.** A custom `SKILL.md` describes my voice (grounded, casual, no AI buzzwords) and hard rules: no em dashes, exactly 5 hashtags, and a clear verdict on every review.
2. **Plan.** A Notion workspace holds linked Content Calendar and Ideas databases. Content is planned around real events, like an Ipoh trip, concerts and a Vancouver to Alaska cruise series.
3. **Draft.** Through the Notion MCP connection, Claude reads the calendar, drafts the script and caption, and slots it into the right date in one conversation.

## Key decisions

- **Rules, not vibes.** "Sound casual" is vague. Specific rules (no em dashes, 5 hashtags, always a verdict) are easy to check and fix most of what makes AI captions sound generic.
- **Notion as the single source.** Claude works directly in the calendar, so there's no copying between a chat and a planning tool.
- **This is a workflow, not an agent.** It's prompt and workflow design: I drive each step and Claude does the drafting.

## Limits and next steps

- The Notion connection is sometimes unavailable, so the persona also produces paste-ready output.
- Next: automating carousel posts (ideas, generated images, text overlays). Explored but not built.
