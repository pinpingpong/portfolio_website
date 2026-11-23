---
title: AI BaZi Reader
section: projects
order: 6
line: A Four Pillars chart from your birth details, then a personalised reading you can chat with.
meta: Gemini · Chat
media:
  type: image
  src: media/bazi-reader.webp
  alt: Four Pillars chart calculated from birth details
  width: 1200
  height: 750
  caption: Four Pillars chart calculated from birth details
stack:
- Gemini API
- Streamlit
- Python
- Prompt Engineering
- Chinese Metaphysics
links:
  live: https://px-bazireader.streamlit.app/
  github: https://github.com/pinpingpong/bazi_reader/tree/main
streamlit_note: true
dates: May 2026
---

An AI-powered Chinese astrology app that generates a full BaZi (Four Pillars of Destiny) chart from a user's birth date and time, then delivers a personalised reading across luck, career, wealth, and relationships — with an interactive chat for follow-up questions.

## Problem

BaZi (Four Pillars of Destiny) is a traditional Chinese system that reads a person's chart from their birth date and time. Most online calculators either get the hard parts wrong (solar term boundaries, hidden stems, luck pillars) or hand everything to a chatbot that guesses the chart itself. I wanted exact calculation with an AI layer only for interpretation.

## How it works

1. **Calculate (pure Python, `bazi.py`).** Year, month, day and hour pillars, with month boundaries from exact solar term times, plus hidden stems, element balance, five special stars and eight ten-year luck pillars (Da Yun) with their direction and start ages.
2. **Show.** Colour-coded pillar cards, element balance and luck pillars, with the current one highlighted. Birth details are encoded in the URL so a chart can be shared.
3. **Interpret (Gemini).** Four separate prompts cover the natal reading, an annual and month-by-month forecast, two-person compatibility, and a chat. Each prompt gets the full calculated chart.
4. **Export.** The full reading can be saved as an HTML file.

## Key decisions

- **Calculation in code, interpretation by the model.** The chart is deterministic and must be exactly right, so the model never computes it. It only explains a chart the code already produced. This also makes readings consistent between runs.
- **Exact solar term boundaries.** The month pillar changes at solar terms, not calendar months. The code uses century-specific constants for the 20th and 21st centuries, so births near a boundary get the right pillar.
- **Separate prompts per task.** One giant prompt gave shallow answers. Splitting natal, forecast, compatibility and chat lets each prompt ask for a specific structure.
- **Chat with memory.** The chat keeps the whole conversation in the session, so follow-ups like "what about next year?" work.

## What broke and how I fixed it

- **Streamlit Cloud kept serving an old build.** After adding hidden stems and special stars, the deployed app didn't pick up the change. Adding an explicit version tag forced a redeploy.
- **Chat forgot earlier turns.** Streamlit reruns the script on each message, which reset the chat. History now lives in session state, so the conversation survives reruns.

## Limits and next steps

- All times are read as UTC+8 (Singapore, Malaysia, Hong Kong, China), with no longitude correction. Births elsewhere need converting first.
- For entertainment and cultural reference only.
- Next: time zone and longitude correction, and saving charts between visits.
