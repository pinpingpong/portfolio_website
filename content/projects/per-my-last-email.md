---
title: 'Per My Last Email (v1)'
section: tools
order: 2
line: A satirical office survival game. Survive 12 weeks under a workplace bully, keep receipts, and decide whether to speak up.
meta: Game · JavaScript
media:
  type: image
  src: media/office-satire.webp
  alt: 'A story card where Veronica runs onboarding, next to the Escape to Nebula stealth minigame'
  width: 1200
  height: 750
  caption: 'Left: a story card with choices. Right: the Escape to Nebula stealth minigame.'
highlights:
- 49 story events across 4 acts, with 8 different endings
- Hand-drawn SVG art and a stealth minigame, all in one offline HTML file
- Balanced with a simulator that plays thousands of runs per playstyle
stack:
- JavaScript
- HTML Canvas
- SVG
- Python
- Built with Claude Code
links:
  live: https://per-my-last-email-sigma.vercel.app
  github: https://github.com/pinpingpong/per-my-last-email
dates: Nov 2026
---

A satirical office survival game set at Celestial Pte Ltd ("reaching for the stars, one escalation at a time"). You're a junior analyst whose manager, Veronica, is a little too attached to you, and who is quietly going after Marcus, the new lead. Each week brings event cards with choices that move your sanity, performance and reputation. The real question is whether you stay a bystander or become a witness. It's inspired by real office life and fully fictionalised. All characters and companies are made up.

It plays in the browser on desktop or phone, takes about 15 minutes per run, and is built to be replayed for different endings.

## How it plays

1. **Event cards.** Two or three cards a week: after-hours calls, "come, toilet", a 14-metric dashboard for a single counter, ERDs whose lines must never cross. Every choice changes your stats and can add evidence to your log.
2. **A story that builds.** A fixed spine of story beats runs across 4 acts (The Favourite, The Target, The Meeting, The Call). Satire cards fill the weeks in between, so no two runs are the same.
3. **Marcus's strikes.** Marcus has given Veronica ten strikes before he resigns. Helping him buys time. Looking away costs strikes.
4. **The call.** The climax is a phone call with your boss. What you've written down, who will back you, and whether she thinks you're her favourite decide how it ends.
5. **Minigames.** When Veronica comes to collect you for a toilet trip, you can make a run for meeting room Nebula in a top-down stealth game.

## How it's built

- **Content is data.** Every event, ending and character lives in JSON files. The engine is a small JavaScript module with no framework and no dependencies.
- **Art is code.** Portraits and scenes are hand-written SVG, so there's no image API and nothing to pay for.
- **One-file build.** A Python script inlines the engine, data and art into a single HTML file. It runs offline and can be sent as an attachment.
- **Tested by simulation.** A Node script plays thousands of runs with random, "smart" and "self-care" playstyles to check that every ending is reachable and none is too easy.
- **Content checks.** A validator runs before every build and catches broken story links, missing art and flags that nothing sets.

## Roadmap

- **v1.1:** a second minigame (escaping the 6pm "team dinner?" at the lift), harder choices where the right answer isn't obvious, sound effects.
- **v1.5:** playable roles. Replay the same 12 weeks as Marcus, the peer, the boss, HR, or a villain run as Veronica.
- **Season 2: After Veronica.** A return-to-office mandate, reorgs and layoffs, and a group chat that outlives the company.

## Changelog

- **v1 (Nov 2026):** first public release. Season 1 with 49 events, 4 acts, 8 endings, an endings gallery, Marcus's strike meter and the first minigame.
