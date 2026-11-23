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
---

A conversational AI agent over social/content analytics data, expanded from my TikTok Analytics Dashboard into a case-study prototype for a marketing analytics interview. Ask questions in plain English and get guardrailed SQL, results, and an auto-generated chart back — follow-ups carry context like a real chat. A companion account-health mode reads the underlying stats and returns a plain-language read plus content suggestions.
