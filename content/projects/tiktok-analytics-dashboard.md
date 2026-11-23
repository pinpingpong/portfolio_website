---
title: TikTok Analytics Dashboard
section: projects
order: 4
line: TikTok performance data in, engagement trends and AI-written recommendations out.
meta: Plotly · LLM insights
media:
  type: image
  src: media/tiktok-analytics.webp
  alt: Posting trends charted from a TikTok data export
  width: 1200
  height: 750
  caption: Posting trends charted from a TikTok data export
stack:
- Streamlit
- Python
- Pandas
- Plotly
- LLM Insights
- Gemini API
- Prompt Engineering
links:
  live: https://px-tiktok-strategist.streamlit.app/
  github: https://github.com/pinpingpong/tiktok_analytics
streamlit_note: true
dates: Feb to May 2026
---

My first Streamlit and Gemini app, built to understand my own TikTok account. Upload the JSON from TikTok's "Download your data" export and it charts posting frequency and content library growth, then sends your recent videos to Gemini for a short strategy report: a performance summary, three hook ideas and the best time to post. It later grew into the Content Analytics Agent.

## Problem

TikTok's in-app analytics only cover recent weeks, and the full history sits in a large JSON export that isn't readable as is. I wanted a quick way to see my posting pattern and get a second opinion on what to post next.

## How it works

1. **Upload.** The app reads the video list from the TikTok data export.
2. **Chart.** pandas and Plotly turn it into two charts: videos per day, and cumulative library growth.
3. **Report.** The 15 most recent videos and your niche go to Gemini, which returns a summary, three hook ideas and a suggested posting time.

## Key decisions

- **Streamlit over a CLI.** The first version was a command line report bot. I rebuilt it in Streamlit the same day so anyone could upload a file and see the charts without installing anything.
- **Only recent videos go to the model.** Sending 15 videos keeps the prompt small and the report focused on current performance.
- **Your file stays in your session.** The upload is read in memory and isn't stored.

## What broke and how I fixed it

- **TikTok changed its export format.** The app stopped finding any videos. The video list had moved inside the JSON, so I updated the parser to the new path and added a clear error message for when no videos are found.

## Limits and next steps

- The personal export has no view counts, so the charts show posting activity, not reach.
- The prompt passes raw records to the model, so the report is a starting point rather than analysis.
- These limits are what the [Content Analytics Agent](/projects/content-analytics-agent) addresses: structured tables, guarded SQL, and numbers computed in code before the model sees them.
