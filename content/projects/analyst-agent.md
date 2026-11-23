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

## Problem

On a data team, many requests are small analyses: pull some numbers from the warehouse, chart them, write it up for a stakeholder. Each one means finding the right tables, writing SQL, building a notebook and then a deck. Most of that is routine, and the hard part is knowing which tables to trust.

## How it works

1. **Context from dbt.** The agent reads the team's dbt repo, so it knows every model, its columns and its documentation before writing any SQL.
2. **Query.** It turns the question into SQL and runs it against Snowflake directly, using credentials from a local `.env` file.
3. **Output.** Each analysis is saved as a Jupyter notebook, with the queries and results in order, and a slide deck when a summary is needed.
4. **Install.** Teammates set it up with one bash script: pull the repo and run it.

## Key decisions

- **dbt docs as the agent's map.** Pointing the agent at the dbt repo gives it the same table documentation the team already maintains, instead of a separate context file that goes stale.
- **A notebook as the deliverable.** A notebook shows every query and result, so a colleague can check and rerun the analysis, rather than trusting a chat answer.
- **Runs locally in VS Code.** It works inside the editor the team already uses, and credentials stay on each person's machine.
- **One-script install.** Teammates can start using it without a setup guide.

## Limits

This was built for a day job, so it is shared as a case study only: no code, data or company details. Results still need an analyst's review, because a correct-looking query can still use the wrong table or definition.
