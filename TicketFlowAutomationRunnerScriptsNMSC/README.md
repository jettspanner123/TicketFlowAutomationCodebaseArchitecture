# Jira Ticket Extraction

Standalone script — not wired into the TiketaFlow backend. Pulls every field of every ticket matching a JQL query from Jira Cloud into a local SQLite database, incrementally (only tickets updated since the last run).

## Setup

```
uv sync
cp .env.example .env   # then fill in JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_JQL
```

## Run

```
uv run python Main.py
```

Manual invocation only, by design — no scheduler.

## Where things live

- `src/JiraTicketExtraction/Database/JiraTicketDatabase.sql` — schema. `JiraTicketDatabase.db` (the actual SQLite file) is created here on first run and is gitignored.
- `src/JiraTicketExtraction/Constants/` — `*CON.py` classes, accessed as `SomethingCON.SOMETHING`.
- `src/JiraTicketExtraction/Utilities/` — `*Utility.py` singletons, accessed as `SomethingUtility.Current.DoSomething()`.
- `src/JiraTicketExtraction/Models/` — data classes.
- `src/JiraTicketExtraction/Services/` — the actual Jira-calling and sync-orchestration logic.
