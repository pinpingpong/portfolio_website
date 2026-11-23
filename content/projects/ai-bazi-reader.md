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

The other reason is personal. I enjoy reading how a chart is interpreted, and when life feels heavy, a thoughtful reading is a small motivation boost. Building my own meant I could ask follow-up questions whenever I needed one.

## How it works

1. **Calculate (pure Python, `bazi.py`).** Year, month, day and hour pillars, with month boundaries from exact solar term times, plus hidden stems, element balance, five special stars and eight ten-year luck pillars (Da Yun) with their direction and start ages.
2. **Show.** Colour-coded pillar cards, element balance and luck pillars, with the current one highlighted. Birth details are encoded in the URL so a chart can be shared.
3. **Interpret (Gemini).** Four separate prompts cover the natal reading, an annual and month-by-month forecast, two-person compatibility, and a chat. Each prompt gets the full calculated chart.
4. **Export.** The full reading can be saved as an HTML file.

## Key decisions

- **Calculation in code, interpretation by the model.** The chart is deterministic and must be exactly right, so the model never computes it. It only explains a chart the code already produced. This also makes readings consistent between runs.
- **Exact solar term boundaries.** The month pillar changes at solar terms, not calendar months. The code uses century-specific constants for the 20th and 21st centuries, so births near a boundary get the right pillar.
- **Separate prompts per task.** One giant prompt gave shallow answers. Splitting natal, forecast, compatibility and chat lets each prompt ask for a specific structure.
- **The chat knows everything already generated.** Its context is the full chart plus any natal reading, forecast or compatibility reading produced so far, so it can build on them instead of starting from zero.

## What broke and how I fixed it

- **The chat didn't remember what I'd entered or read.** The first version gave the chat only the raw chart, so it couldn't refer to the readings I had just generated. I rebuilt the chat context to include the chart and every reading generated so far, rebuilt it whenever a new reading arrives, and cleared the conversation when the birth details change so an old chart never leaks into a new one. The HTML export now includes the chat too.

## Limits and next steps

- All times are read as UTC+8 (Singapore, Malaysia, Hong Kong, China), with no longitude correction. Births elsewhere need converting first.
- For entertainment and cultural reference only.
- Next: time zone and longitude correction, and saving charts between visits.
