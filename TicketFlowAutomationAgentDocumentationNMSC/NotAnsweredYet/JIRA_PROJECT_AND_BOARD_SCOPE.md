# Open Question: Jira Project & Board Scope

**Status**: Open

## Question

Which Jira project(s) and board(s) should TiketaFlow pull tickets from? Should any issue types be excluded (e.g. only `Task`/`Bug`, not `Epic`/`Sub-task`)?

## Context

Confirmed: tickets can come from any project/board — the exact scope is to be configured later, not fixed in code. This will live in PostgreSQL and be editable via the same admin settings screen as the categorization rules and category→script mappings.

## Blocks

- The Jira Sync job's initial query filter.
- Default/seed values for the admin settings screen.
