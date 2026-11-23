---
title: Content Analytics Agent
section: projects
order: 1
line: Plain-English questions in, guardrailed SQL, results and a chart out.
meta: NL-to-SQL · DuckDB
media:
  type: video
  src: media/content-agent.mp4
  poster: media/content-agent.webp
  alt: Plain-English question in, SQL result and chart out
  caption: Plain-English question in, SQL result and chart out
stack:
- Gemini API
- Streamlit
- DuckDB
- Python
- Plotly
- NL-to-SQL
- Prompt Engineering
links:
  live: https://px-content-analytics-agent.streamlit.app/
  github: https://github.com/pinpingpong/content-analytics-agent
streamlit_note: true
dates: Jul 2026
---

A conversational AI agent over social/content analytics data, expanded from my TikTok Analytics Dashboard into a case-study prototype for a marketing analytics interview. Ask questions in plain English and get guardrailed SQL, results, and an auto-generated chart back — follow-ups carry context like a real chat. A companion account-health mode reads the underlying stats and returns a plain-language read plus content suggestions.

## Problem

This started as a take-home case study for a marketing analytics interview: map where AI could help a marketing team, then build one opportunity for real. I picked ad hoc analysis. Analysts spend a lot of time on small one-off questions ("what were our top posts last month?") that a well-guarded agent could answer directly.

## How it works

1. **Load.** My own TikTok data export stands in for a marketing warehouse. It is flattened into four DuckDB tables: posts, followers, hashtags and profile.
2. **Chat with your data.** A question in plain English goes to Gemini with the schema and a few example question and SQL pairs. Gemini writes SQL, the app checks it, DuckDB runs it, and you get a narrated answer, the SQL, a results table and one chart. Follow-ups like "now just the top 1" use the last few turns as context.
3. **Account health.** One click sends stats computed in code (top posts, hashtags, follower growth) to Gemini, which returns a plain-language read and about three content suggestions.

## Key decisions

- **Guardrails in code, not in the prompt.** Generated SQL must start with `SELECT`, a blocklist rejects anything that writes or changes schema (even nested), and every query is capped at 100 rows. The model is never trusted to behave.
- **Numbers computed in code, words from the model.** The health summary reads statistics the app calculated itself, so the model narrates numbers rather than inventing them.
- **An honest proxy metric.** A personal export has no view counts, so true engagement rate is impossible. I used likes divided by follower count, named it as a proxy, and documented why.
- **Privacy by construction.** The full export contains DMs, login IPs and location history. The app never reads it. It reads a sanitised extract with only post metadata, followers, hashtags and public profile stats, and only that extract is in the repo.
- **Pinned to Flash-Lite.** On a free key, `gemini-2.0-flash` had zero quota, and `gemini-2.5-flash` and the `-latest` alias returned occasional 503s under light load. `gemini-2.5-flash-lite` held up, so I pinned it rather than use `-latest`.

## What broke and how I fixed it

- **Free-tier errors during demos.** Gemini returned 503 (overloaded) and 429 (rate limited) errors. Calls are now retried, using the server's own `retryDelay` hint on 429s and a fixed backoff otherwise, before any error reaches the user.
- **Missing keys or malformed replies crashed the app.** Every model call is wrapped so a bad response shows a clear message in the UI instead of a stack trace.

## Limits and next steps

- The two modes don't share context. Chat only sees the schema and history, and the health summary only sees the stats.
- Next: merge them into one agent that has the schema, history and stats together, calls SQL as a tool when it needs data, and flags patterns without being asked.
- In production the schema and examples would live in a shared context layer (for example an MCP server) that grows with vetted SQL and metric definitions, instead of being hard-coded in the prompt.
