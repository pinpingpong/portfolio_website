---
title: Personal Finance Pipeline
section: workflow
order: 2
line: 80 bank statement PDFs turned into a clean, redacted, interactive dashboard.
meta: Data Engineering
media:
  type: flow
  label: How the finance pipeline works
  steps:
  - title: 80 statement PDFs
    detail: 5 Singapore banks
    kind: in
  - title: Extract
    detail: Text layer, or Tesseract OCR for scanned HSBC pages
  - title: Clean
    detail: Fix signs, re-tag transactions, split bonus months, drop reimbursed travel
  - title: Redact PII
    detail: Several rounds, each re-checked for leaks
  - title: Dashboard
    detail: KPIs, spend trends, categories, editable goals and runway
    kind: out
  caption: 'How it works. No screenshot: the real data is private.'
highlights:
- OCR'd scanned HSBC statements with Tesseract — no text layer, no problem
- 'Multi-round PII redaction: found and fixed real leaks (two names, 52 name fragments, CPF over-redaction)'
- Fixed sign conventions, separated bonus months, excluded $25K group travel fronted and reimbursed
- 'Interactive HTML dashboard: KPIs, spend trends, category breakdown, editable goals & runway'
stack:
- Python
- Tesseract OCR
- Pandas
- Claude
- Data Cleaning
- HTML Dashboard
---

Turned 80 PDF bank statements across 5 Singapore banks into a clean, structured financial picture — with Claude handling the messy parts: OCR on scanned HSBC images, iterative PII redaction (caught real leaks along the way), and correcting mis-tagged transactions. Delivered a self-contained interactive dashboard with live goal-tracking for reno, travel, and wedding.
