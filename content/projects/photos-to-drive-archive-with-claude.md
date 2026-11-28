---
title: Photos to Drive Archive with Claude
section: workflow
order: 6
line: A Claude Code workflow that finds my heaviest iCloud videos, moves them to Google Drive and checks every copy before anything is deleted.
meta: Automation
highlights:
- 173 videos (about 23 GB) moved out of iCloud in one session, every file size checked against the original
- Runs on my Mac's own Photos library and Google Drive folder, with no cloud APIs or upload limits
- Nothing is deleted until the copies are confirmed in Drive, and the delete stays with me
stack:
- Claude Code
- Python
- osxphotos
- Apple Photos
- Google Drive for desktop
- Google Drive MCP
dates: Nov 2026
---

My iCloud storage was nearly full, mostly from videos. I already pay for plenty of Google Drive space, so the fix was obvious: move the heavy, old videos there. Doing it by hand means downloading each video from iCloud, copying it into the right folder, checking it uploaded and then deleting it from Photos, hundreds of times. So I had Claude Code run it with me.

## Problem

I had 1,964 videos taking up 64.5 GB in iCloud, and none of them were stored on my Mac. Concert videos alone were about a third of that. The hard part isn't copying files. It's choosing the right videos, not losing any, and being sure each one really is in Drive before it's gone from iCloud.

## How it works

1. **Size it up.** Claude reads my Photos library with `osxphotos`, a read-only open-source tool, and builds a report of every video by size, year, place and Photos' own scene labels. Labels like Concert, Stage and Audience picked out the concert videos without me tagging anything.
2. **Pick a batch.** Claude suggests batches with the space each one frees (concert days, videos over 50 MB, everything before a given year). I choose. The first batch was 86 concert videos (21.1 GB) and the second was 87 videos from 2016 to 2018.
3. **Export.** `osxphotos` downloads each original from iCloud and saves it into the Google Drive folder on my Mac, sorted into date folders. The Drive app uploads them in the background. Every exported video is also added to a "Moved to Drive" album in Photos.
4. **Check.** Claude compares every file's size with the original in Photos, then checks the copies in Google Drive itself through the Drive connector, not just the folder on my Mac.
5. **Delete, by me.** Only after the check do I delete the album's videos in Photos. Claude then confirms they all landed in Recently Deleted.

## Key decisions

- **Use the local Drive folder, not the Drive API.** Google Drive for desktop already syncs a folder on my Mac. Saving into it uploads the file with no API setup, no size limits and no token handling. Stream mode means Drive clears its local copy by itself once uploaded.
- **Read the library, don't touch it.** `osxphotos` reads Photos' database read-only for the report. The only change it makes in Photos is the "Moved to Drive" album.
- **Check in two places.** A file sitting in the Drive folder isn't proof it uploaded. The check also looks at the copy in Google Drive.
- **Deleting stays manual.** Deleting from Photos removes a video from iCloud and every Apple device, so I do that step myself.

## What broke and how I fixed it

- **No permission popup.** macOS asks before a script can control Photos, but it doesn't show that popup for commands Claude runs in the background. The request timed out (`User cancelled. (-128)`). The fix was to run the export command in my own Terminal window, where the popup could reach me, while Claude watched progress and did the checks.
- **A leftover file blocked the rerun.** The failed first run left a tracking file in the folder, so the next run stopped to ask a yes/no question. Adding `--update` fixed it, and it also made stopping and resuming safe: a rerun skips files already done.
- **One video missed the album.** One of the 86 didn't get added to "Moved to Drive", probably because of the early permission hiccup. Claude found it, confirmed its Drive copy matched to the byte, and I deleted it by hand.
- **Deleting the album didn't delete the videos.** In Photos, deleting an album only removes the album. Claude caught this by checking Recently Deleted and gave me the command to rebuild the album, then I deleted the videos themselves.

## Results and limits

- 173 videos, about 23 GB, now in Drive in date folders. All 173 file sizes match the originals, and the first batch was also confirmed in Google Drive itself before deletion.
- The space only frees up once Recently Deleted is emptied, or after Photos clears it in 30 days.
- It's a workflow I run with Claude when storage gets full, not a scheduled job. It needs my Mac, my Photos library and my clicks on the permission popups.
