---
title: AI Twin Recruiter Chatbot
section: projects
order: 2
line: Ask "me" about my work. RAG over this site, running in the corner of this page.
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
---

A digital twin that lets visitors ask "me" about my work directly on this site. Built with RAG: the published content of this site (project write-ups, workflows, experience) is chunked, embedded and stored in Pinecone. Each question retrieves the most relevant chunks before answering, so replies stay grounded in what's public here. The API caps message size, history length and request rate to keep the free tier healthy.
