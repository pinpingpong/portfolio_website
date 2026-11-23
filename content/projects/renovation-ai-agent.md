---
title: Renovation AI Agent
section: projects
order: 5
line: Supplier links and design rules in, whole-room schemes rendered onto your room photo.
meta: Multimodal · Gemini
media:
  type: image
  src: media/reno-agent.webp
  alt: 'Step-by-step flow: room photo, supplier catalogues, curation, render'
  width: 1200
  height: 750
  caption: 'Step-by-step flow: room photo, supplier catalogues, curation, render'
stack:
- Gemini API
- Search Grounding
- Multimodal Inpainting
- Streamlit
- Python
- Structured Outputs
- Prompt Engineering
links:
  live: https://px-renovation-ai-agent.streamlit.app/
  github: https://github.com/pinpingpong/renovation-ai-agent
streamlit_note: true
dates: Oct 2026 to now
featured: 1
---

An interior design copilot born from renovating my own 5-room BTO in a zero-wood Desert Modernism style. Paste real supplier catalogue links (laminates, paint, countertops) and describe your design rules in plain English. The agent resolves official product codes with Gemini Search grounding, filters them against your brief with a deterministic validator, composes whole-room schemes, then renders the chosen scheme onto your own room photo while preserving its geometry and lighting.

## Problem

I was choosing materials for my own 5-room BTO, with a Desert Modernism brief: plaster, limestone, travertine and earth tones, and zero wood, including printed woodgrain. Two steps were slow.

- **Curation.** Each supplier publishes hundreds of laminate codes. Checking every one against a brief that is partly negative ("no wood of any kind") by hand is tedious and easy to get wrong.
- **Visualisation.** General AI image tools reimagine the room. Doors move, perspective shifts, and the preview no longer matches the real space, so it can't support a decision.

## How it works

1. **Resolve.** Paste supplier catalogue links. Gemini reads each page with URL Context and fills gaps with Google Search grounding, returning only real, published product codes with colour, finish and category. Grounding citations are shown so every code can be checked.
2. **Curate.** All materials go to Gemini with the brief in plain English. It returns typed JSON: excluded categories, must-haves, and a score and reason per item. A deterministic validator then enforces the hard rules in code.
3. **Pair.** Approved materials are grouped into base, feature and accent combinations for named surfaces (for example lower and upper cabinets). A rule-based fallback pairs calm with expressive materials if the model returns nothing usable.
4. **Render.** One multimodal request sends the room photo plus one swatch per surface. The prompt fixes camera, perspective, cabinet layout and lighting, and only changes surface materials.

Three modules: `app.py` (Streamlit UI and state), `agent_logic.py` (grounding, evaluation, validator, pairing), `renderer.py` (swatches and inpainting).

## Key decisions

- **Gemini grounding instead of a scraper.** Supplier sites are JavaScript-rendered, paginated or bot-protected, so a hand-written scraper would break per site. Grounding reads any page, at the cost of having to verify output, which is why citations are surfaced.
- **The model never gets the final say on hard rules.** "Zero wood" is enforced by a validator in code. If the model approves a wood item, the validator rejects it and labels the reason "Validator override". LLM judgement is used for taste and scoring, code for constraints.
- **The brief is input, not code.** Nothing about Desert Modernism is hard-coded, so a Japandi brief that requires light oak and fluting works with the same app.
- **Pair before render.** Image calls are the expensive step, so combinations are checked and filtered first (unknown ids, duplicates, base equal to feature) and only a chosen one is rendered.
- **A public demo that can't cost me money.** Visitors without a key use a free-tier demo key from a separate Google project with no billing, capped at 3 runs per session. Rendering needs a paid image model, so the code refuses to send image requests with the demo key, not just the UI.
- **Newest stable model by default.** The app lists the models a key can call and picks the highest stable flash-lite and flash-image version, skipping preview and dated variants, so it doesn't need an update for each Gemini release.

## What broke and how I fixed it

- **Demo stopped working for visitors (Nov 2026).** Fetch & Curate failed with a 429. The free demo key had used up its Google Search grounding quota, while plain calls and URL Context calls still worked. The fix: on a 429, retry the catalogue fetch with URL Context only, and skip the Search-only retry because it would hit the same quota. The existing fallback for 400 errors (URL Context unsupported, retry with Search only) stays as it was.
- **Grounded calls can't return JSON-schema output.** Search grounding and structured output can't be combined in one call, so the resolve step asks for a fenced JSON block and validates it with Pydantic. Every later step uses full structured output.
- **Unsafe swatch downloads.** The app fetches swatch images from URLs the model returns, which is a server-side request forgery risk. The fetcher re-checks every redirect against private, loopback and link-local addresses, and limits content type and size.

## Limits and next steps

- Product codes are resolved by AI from public pages. Check them with the supplier before ordering.
- When no official swatch image is available, the render uses a synthesised swatch from the material's colour profile, so texture is approximate.
- Next: a mask-painting canvas for pixel-exact surface selection, batch rendering of all combinations, and a PDF mood board export with codes and renders.

