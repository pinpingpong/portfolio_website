---
title: Inbox Cleanup with Claude
section: workflow
order: 5
line: A Claude Code skill that finds promo senders across Gmail and Exchange and unsubscribes the ones I approve.
meta: Automation
highlights:
- 100 mailing lists unsubscribed across two inboxes in the first session
- Scans both inboxes in about a second by reading Apple Mail's local index, not the mail servers
- Remembers what I kept and cut, so each run only asks about new senders
stack:
- Claude Code
- Python
- SQLite
- Apple Mail
- Claude in Chrome
- Gmail MCP
dates: Nov 2026
---

My inboxes were flooded with promo emails, and I was too lazy to open each one and hunt for the unsubscribe link. So I had Claude do it. It's a Claude Code skill (`/inbox-cleanup`) that scans my Gmail and Exchange inboxes, lists the senders I haven't decided on yet, and unsubscribes from the ones I tick. I call it whenever my inbox feels noisy, and it can also be paired with a local scheduler for a regular run.

## Problem

My Gmail Promotions tab alone had about 708 emails in 60 days, and my Exchange inbox had over 1,200 messages in the same period. Unsubscribing means opening each sender, scrolling to the tiny link and confirming, dozens of times, for two accounts. I never got round to it, so the pile kept growing.

## How it works

1. **Scan.** A Python script reads Apple Mail's local index (a SQLite database) to group the last month of mail by sender, across every account in Mail. For each sender it reads one message's headers and keeps only real mailing lists, the ones with a `List-Unsubscribe` header. Personal mail and receipts without that header never show up.
2. **Sort.** Each sender is checked against two lists: `keep` (airline miles, bills, bank alerts, recruiters) and `cut` (already unsubscribed). Only senders on neither list count as new.
3. **Approve.** Claude groups the new senders (shopping, food, events, finance) and suggests cut or keep. It flags trade-offs, like card promos that sometimes carry good sign-up offers, or account emails I'd miss. I reply with edits, and nothing happens until I do.
4. **Unsubscribe.** For each approved sender, the script sends the standard one-click unsubscribe request (RFC 8058), the same one Gmail's Unsubscribe button sends. Senders that only offer email or website unsubscribes go on a short to-do list for me.
5. **Remember.** Decisions are saved to the keep and cut lists, so the next run only shows new senders. If a cut sender keeps mailing after a few days' grace, it gets unsubscribed again without asking.

## How it evolved

- **Version 1: Gmail in the browser.** Claude read Gmail through the Gmail connector, recommended what to cut, then drove Chrome through Gmail's Manage subscriptions page with a small in-page script: 61 lists in one session. It worked, but only for Gmail, and it depended on Gmail's page layout.
- **Version 2: Apple Mail's local store.** Both accounts already sync into Apple Mail on my Mac, so the script reads Mail's local files instead. One scan covers Gmail and Exchange, needs no browser, and the first Exchange run cut 39 more lists.

## Key decisions

- **Read the index, don't drive the app.** Asking Mail.app for messages through AppleScript timed out after 2 minutes. Reading its SQLite index directly, read-only, takes about a second.
- **Unsubscribe headers only.** The script never clicks links inside email bodies. It only uses the unsubscribe address the sender publishes in the email headers.
- **Approval stays manual.** Grouping, recommending and unsubscribing are automatic. Deciding what goes isn't, because some "promo" senders also send things I need, like bills or recruiter messages.
- **A skill, run locally.** The mail data stays on my Mac, so this is a skill I call on demand rather than a cloud job. For a regular run it can be paired with a local scheduler (for example macOS launchd running the read-only scan and sending a notification when new senders turn up). The unsubscribe step still waits for my approval.

## What broke and how I fixed it

- **Gmail's layout changed mid-run (v1).** When the browser window got narrower, Gmail swapped the text buttons for icons and the script stopped finding them. The fix was to also match the button's accessibility label.
- **Wrong confirm dialog (v1).** Gmail left an old, hidden dialog on the page. The script now picks the last visible one.
- **Script time limit (v1).** A run of 22 senders hit the browser tool's 45-second limit, so the script runs in batches of 10.
- **Exchange mail wasn't flagged (v2).** Apple Mail's index marks Gmail newsletters but not Exchange ones. The script reads the unsubscribe header from each message file instead of trusting the index flag.

## Results and limits

- 100 lists unsubscribed in the first session: 61 on Gmail and 39 on Exchange. 3 senders still need doing by hand (one refused the request, two only offer email or website unsubscribes).
- Senders can take a few days to stop. Spam that ignores unsubscribes should go to junk instead.
- It only covers accounts set up in Apple Mail, on my Mac.
