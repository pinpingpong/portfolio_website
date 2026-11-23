---
title: Claude Usage Menu Bar
section: tools
order: 1
line: A macOS menu bar widget showing my Claude plan usage and reset times.
meta: Python · SwiftBar
media:
  type: image
  src: media/menubar.webp
  alt: 'SwiftBar dropdown: session and weekly limits, reset times, and share of usage by surface'
  width: 1200
  height: 750
  caption: 'SwiftBar dropdown: session and weekly limits, reset times, and share of usage by surface'
stack:
- Python
- SwiftBar
- macOS Keychain
- Built with Claude Code
links:
  github: https://github.com/pinpingpong/claude-usage-menubar
dates: Nov 2026
---

A macOS menu bar widget that shows my Claude plan usage (5-hour session and weekly) with reset times, so I can pace heavy Claude Code sessions without checking settings. Reuses the existing Claude Code login from Keychain, so there's no extra setup or API key.

## Problem

I run long Claude Code sessions and kept hitting plan limits mid-task. Checking meant typing `/usage` or opening the settings page, so I only checked after it was too late. I wanted the number visible all the time.

## How it works

1. **SwiftBar** runs a single Python script every 5 minutes and shows its output in the macOS menu bar.
2. The script reads the login that Claude Code already stores in the macOS Keychain.
3. It requests the same usage data Claude Code shows for `/usage`, then prints session (5-hour) and weekly percentages in the bar.
4. The dropdown shows reset times in local time, model-specific weekly limits when the plan has them, and how the week splits across Claude Code, chat and Cowork. The icon turns orange at 70% and red at 90%.

## Key decisions

- **Reuse the existing login.** No API key, no extra sign-in. The token stays on the machine and is only sent to Anthropic.
- **Standard library only.** One Python file with no dependencies, so installing it is a single download.
- **SwiftBar instead of a native app.** A menu bar app in Swift would be heavier to build and maintain. SwiftBar turns any script's printed output into a menu bar item.
- **Refresh rate in the filename.** SwiftBar reads the interval from the filename (`claude-usage.5m.py`), so changing it is a rename.

## What broke and how I fixed it

- **Expired logins.** When the stored token expires, the plugin shows "Login expired" rather than an error. Opening Claude Code once refreshes it.
- **First run asks for Keychain access.** macOS asks whether SwiftBar can read the credentials item. The README tells users to choose Always Allow so it only asks once.

## Limits and next steps

- It relies on an undocumented endpoint, the one Claude Code itself appears to use, so it can break without notice. The README says so up front.
- macOS only.
