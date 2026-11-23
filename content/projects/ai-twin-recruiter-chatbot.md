---
title: AI Twin Recruiter Chatbot
section: projects
order: 2
line: Ask "me" about my work. RAG over this site, running in the corner of this site.
meta: RAG · Pinecone
media:
  type: video
  src: media/ai-twin.mp4
  poster: media/ai-twin.webp
  alt: Asking the AI twin a question on this site
  caption: Asking the AI twin a question on this site
stack:
- Gemini API
- RAG
- Pinecone
- Vector Embeddings
- Streaming
- Vanilla JS
- Prompt Engineering
links:
  try_twin: true
  github: https://github.com/pinpingpong/portfolio_website
dates: May 2026 to now
featured: 2
---

A digital twin that lets visitors ask "me" about my work directly on this site. Built with RAG: the published content of this site (project write-ups, workflows, experience) is chunked, embedded and stored in Pinecone. Each question retrieves the most relevant chunks before answering, so replies stay grounded in what's public here. The API caps message size, history length and request rate to keep the free tier healthy.

## Problem

Recruiters skim a portfolio for a minute and leave with questions a static page can't answer: "has she used RAG in production?", "what does she do when a model fails?". I wanted visitors to be able to ask, and get answers grounded only in what I've published.

## How it works

1. **Index.** Each project, its detail page sections, and my experience become chunks. They are embedded with `gemini-embedding-001` and stored in a Pinecone "website" namespace. A second namespace holds short, anonymous colleague feedback that I curated and approved.
2. **Ask.** The browser sends the conversation to a Vercel serverless function.
3. **Check.** The function enforces same-origin requests, caps message length and history, and rate limits per IP. A Vercel Firewall rule adds a hard limit in front of it.
4. **Retrieve.** It embeds the question, queries both namespaces in parallel, and keeps the best 5 matches.
5. **Answer.** The matches go into the system prompt, and Gemini streams the reply back, which the page renders as formatted text.

Since Nov 2026 every project on this site comes from one Markdown file, and a GitHub Action rebuilds the index on each push, so the twin knows about new work as soon as it's published.

## Key decisions

- **Only public content in the index.** The chatbot can quote anything it retrieves, so the index is built only from what is on this site plus feedback I approved for publishing.
- **A serverless proxy, not keys in the browser.** The Gemini and Pinecone keys never reach the client, and the proxy is where limits and checks live.
- **Answers stay within a time budget.** Vercel cuts a function off at 25 seconds before the first byte. Retrieval gets 3 seconds, the main model 10, and the fallback 7, so the worst case still answers in time.
- **Fail open on retrieval.** If Pinecone is slow or down, the twin answers from its base prompt instead of failing.
- **Free tier by design.** Gemini free tier, Pinecone free tier and Vercel hobby, with the limits above protecting the quota.

## What broke and how I fixed it

- **Gemini overload stalled replies (Nov 2026).** `gemini-flash-latest` returned 503s and hung past Vercel's limit, so visitors saw nothing. Each model now has its own timeout, and the function falls back to Flash-Lite.
- **Long replies cut off mid-sentence.** The timeout was also aborting the stream once the answer had started. It now only covers the wait for the first response, not the stream itself.
- **Raw markdown in replies.** Gemini answers with `**bold**` and bullet lists, which showed as raw symbols. Replies are now rendered as formatted text, with HTML escaped first so a reply can never inject markup.
- **A stale index.** The index used to be rebuilt by hand, so new projects were invisible to the twin until I remembered. It now rebuilds in CI on every content change.

## Limits and next steps

- The per-IP limiter lives in memory per edge instance, so it is best effort. The firewall rule is the real cap.
- With the Gemini free tier, replies can take around 15 seconds when the main model is overloaded.
- Next: link to the relevant project page in each answer, and log anonymous question topics to see what visitors actually ask.
