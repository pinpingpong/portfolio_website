---
title: Analyst Agent
section: agents
order: 1
line: 'A VS Code agent: question in, Snowflake queries, notebook and slide deck out.'
meta: Local · Enterprise
highlights:
- Reads dbt repo for full table context and team documentation
- Queries Snowflake directly via `.env` credentials — no manual SQL
- Outputs a ready-to-share `.ipynb` notebook and slide deck per analysis
- Teammates install in one bash script — pull repo, run, done
stack:
- VS Code Agent
- GitHub Copilot
- Snowflake
- dbt
- Python
- Jupyter Notebooks
- Bash
---

A VS Code Copilot agent that turns natural language questions into full analyses — querying Snowflake directly, generating Jupyter notebooks as output, and producing presentation slides on demand. Designed for a data team environment: point it at your dbt repo and it understands every available table and its documentation.
