# Open Question: Ticket Categorization Rules

**Status**: Open

## Question

What are the actual rule-based categorization rules — i.e., the condition(s) over ticket fields that assign each ticket to a category?

## Context

Confirmed: categorization is rule-based (not ML/LLM-based), evaluated inline during Jira ingestion, and stored in PostgreSQL as admin-editable data rather than hardcoded logic. The app owner will specify the actual rules later.

Depends on `TICKET_CATEGORY_TAXONOMY.md` (the categories these rules assign into) being defined, or can be defined alongside it.

## Blocks

- The rule-engine's data schema (what a "rule" record actually contains).
- Implementation of the categorization step itself.
