---
title: AI-Assisted Price Intelligence
section: agents
order: 4
line: Compared ~1,400 tap listings across 3 marketplaces and saved about S$500.
meta: Personal · Case Study
media:
  type: image
  src: media/price-intel.webp
  alt: Delivered-price shortlist and final buying plan, rebuilt from the comparison sheet
  width: 1200
  height: 750
  caption: Delivered-price shortlist and final buying plan, rebuilt from the comparison sheet
highlights:
- Collected full official-store catalogues across 3 marketplaces and 3 currencies
- Seller-level checks found 300+ Amazon items that ship to SG only via third parties
- Same Hansgrohe taps 40–55% cheaper on Amazon.de than Shopee
- Human in the loop for logins; slowed down after a Tmall flag, never bypassed checks
stack:
- Claude
- Browser Agent
- JavaScript Extraction
- Python
- Google Sheets API
---

A Claude browser session I directed as a personal shopper for my HDB renovation, comparing ~1,400 Hansgrohe and Rigel listings across Amazon.de, Shopee and Tmall in delivered SGD. The result was a mixed-brand buying plan of S$1,780, about S$500 less than going all-Hansgrohe.

## Problem

My renovation needed taps and showers, and the same Hansgrohe models are sold on Shopee, Tmall and Amazon.de at very different prices. Comparing them properly means matching exact model numbers across stores, converting currencies, adding shipping and checking who actually ships to Singapore. That is too many listings to do by hand.

## How it works

1. **Collect.** I directed a Claude browser session to go through the official-store catalogues on Amazon.de, Shopee and Tmall, about 1,400 Hansgrohe and Rigel listings in 3 currencies, extracting them with JavaScript on each page.
2. **Check sellers.** For Amazon, it checked who sells and ships each item. More than 300 items only reach Singapore through third-party sellers, so they were treated differently.
3. **Compare.** Listings were matched by model and converted to delivered prices in SGD, then written to a Google Sheet.
4. **Decide.** The result was a shortlist and a mixed-brand buying plan.

## Key decisions

- **Compare delivered SGD, not sticker price.** A cheaper listing that adds shipping or only ships through a reseller isn't cheaper.
- **Me in the loop for logins.** I handled every sign-in myself. The agent never got credentials.
- **Respect the sites.** When Tmall flagged the session, I slowed down rather than trying to get around the check.
- **Mixed brands.** Picking the best delivered price per item across Hansgrohe and Rigel beat committing to one brand.

## Result

The same Hansgrohe taps were 40 to 55% cheaper on Amazon.de than on Shopee. The final plan cost S$1,780, about S$500 less than buying all Hansgrohe.

## Limits

Prices move, so this is a snapshot from the time of the comparison, not a live tracker.
