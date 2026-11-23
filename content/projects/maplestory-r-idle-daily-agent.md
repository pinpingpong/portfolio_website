---
title: MapleStory R Idle Daily Agent
section: agents
order: 2
line: Plays my daily game routine hands-free through computer use, on a schedule.
meta: Personal
highlights:
- 'Covers ~15 daily tasks: rewards, missions, dungeons, arena, summons, and more'
- Custom `SKILL.md` SOP encodes coordinate maps, execution order, and edge case handling
- Token-saving rules built into the SOP — batches clicks, minimises screenshots, uses long waits
- Scheduled to trigger daily — zero manual intervention, audit-friendly report output
stack:
- Claude Cowork
- Computer Use
- BlueStacks
- Claude Routines
- Prompt Engineering
---

A fully hands-free AI agent that plays my MapleStory R Idle daily routine on BlueStacks — because life's too short for repetitive tapping. Claude takes control of the screen each day and works through ~15 tasks autonomously, guided by a custom SOP that encodes all game knowledge, UI quirks, and hard guardrails like zero gem spending.

## Problem

Honestly: I was lazy and kept forgetting to log in for my dailies. MapleStory R Idle has about 15 daily tasks (rewards, missions, dungeons, arena, summons and more), and missing a day means losing those rewards. None of the tasks need thought, so instead of relying on memory, I handed them to an agent on a schedule. It also turned out to be a good low-stakes test of how reliable computer use is on a real, messy interface.

## How it works

1. **Schedule.** A Claude routine starts the run every day.
2. **Control.** Claude takes over the screen through computer use and works in the game running on BlueStacks.
3. **Follow the SOP.** A custom `SKILL.md` tells it what to do: where each button is, the order of tasks, and how to handle pop-ups, loading delays and other edge cases.
4. **Report.** It ends with a report of what was done and anything it skipped, so I can check a run without watching it.

## Key decisions

- **Game knowledge lives in the SOP, not the model.** Coordinate maps, task order and UI quirks are written down once. The model follows instructions instead of rediscovering the game every day.
- **Hard guardrails.** The SOP forbids spending premium currency (gems) under any circumstance. An agent with control of the screen should not be able to make purchases.
- **Token-saving rules.** Screenshots are the expensive part of computer use. The SOP batches clicks, takes as few screenshots as possible, and uses longer waits rather than checking the screen repeatedly.
- **A report every time.** A run that says what it did can be trusted without being watched.

## Limits

It is a personal project with no public code.
