---
title: AWS AI Certification Tutor
section: projects
order: 3
line: Practice questions and explanations that adapt to your weak areas.
meta: Gemini · Streamlit
media:
  type: video
  src: media/aws-tutor.mp4
  poster: media/aws-tutor.webp
  alt: Generating a scenario question, answering it, and getting AI feedback
  caption: Generating a scenario question, answering it, and getting AI feedback
stack:
- Gemini API
- Streamlit
- Python
- Jina AI
- Prompt Engineering
links:
  live: https://px-aws-tutor.streamlit.app/
  github: https://github.com/pinpingpong/aws_ai_tutor
streamlit_note: true
dates: May 2026
---

An exam tutor for the AWS Certified Generative AI Developer Professional (AIP-C01). It generates scenario-based practice questions per exam domain, explains every answer, and tracks accuracy against an 85% readiness target. Optional web research pulls recent candidate experiences from forums and blogs so questions reflect what people actually saw in the exam.

## Problem

I was preparing for AIP-C01, a new professional-level exam with few good practice banks. Question dumps go stale fast, and the exam is known for scenario questions with two or three plausible answers, where cost, latency and security constraints decide which one is right. I wanted unlimited practice at that level, grounded in what recent candidates reported.

## How it works

1. **Pick a domain.** Each of the exam domains carries a dense list of the services and concepts it covers (for example CountTokens, prompt caching, provisioned throughput, circuit breakers). That list goes into the prompt, so questions stay on syllabus.
2. **Optional research.** A search through Jina AI pulls recent Reddit threads, forum posts and blogs about the exam. Gemini summarises them into insights, which are added to the question prompt.
3. **Generate.** Gemini returns one question as JSON: scenario, four options, the answer and an explanation.
4. **Answer and review.** You get instant feedback on why your choice was right or wrong, plus a running score, streak, history and readiness bar.

## Key decisions

- **Domain context in the prompt, not left to the model.** A plain "write an AIP-C01 question" prompt drifts to generic AWS trivia. Spelling out each domain's services keeps questions on what the exam tests.
- **Research is cached, not fetched per question.** Searching and summarising takes several API calls. The result is saved to `research_cache.json` and reused for dozens of questions, with a 60 second cooldown on refreshes.
- **Gemini instead of Claude.** The first version used the Anthropic API. I switched to Gemini on day one so the public demo could run on a free tier.
- **The app works without research.** If the search key is missing or search fails, questions fall back to the model's own knowledge instead of failing.

## What broke and how I fixed it

- **Slow or overloaded Gemini (Nov 2026).** Question generation sometimes hung. The app now gives the main model 30 seconds, then falls back to Flash-Lite, and stays on the fallback for the rest of the session so you only wait once.
- **Research overflowing the prompt.** Scraped pages could be very long. Research text is now capped at 30,000 characters before summarising, and the search timeout was raised from 18 to 60 seconds because the search API is slow but reliable.
- **Noisy logs on every rerun.** Streamlit reruns the script on each click, so debug logging flooded the output. Logging now captures errors only and silences chatty libraries.

## Limits and next steps

- Questions are generated, not official. Treat explanations as study aids and check them against AWS documentation.
- Accuracy is tracked overall, not per domain, so it can't yet point you to your weakest domain.
- The app still uses the older `google-generativeai` SDK. Moving to `google-genai` is the next maintenance step.
- Next: per-domain stats, and steering new questions toward domains you get wrong.
