# ADR: Ticket Categorization Execution Model

**Status**: Proposed — pending input from the app owner

## Context

Once a ticket is ingested from Jira, the rule-based categorization logic has to execute somewhere. A default was discussed during scoping — running it inline and synchronously, as one step in the Jira Sync ingestion pipeline, on the reasoning that evaluating simple rules over a handful of fields is cheap and a separate async step would add a moving part (its own trigger, its own failure mode) without real benefit at this app's scale (~15-20 tickets/day).

The app owner has indicated they already have a specific system design in mind for this and will provide it later, rather than confirming the inline/synchronous default.

## Decision

**Deferred.** The inline/synchronous description that appears elsewhere in these docs (`ARCHITECTURE.md`) is a placeholder only, carried over from the scoping discussion — it is explicitly **not** a confirmed decision. Do not implement against it until this ADR is updated with the app owner's actual design.

## Consequences

Implementation of the categorization execution step is blocked on this ADR being updated. Everything downstream of categorization (status transitions, dashboard display, category→script mapping lookup) is written to depend only on "a ticket ends up with a category," not on how/when that assignment happens — so this deferral shouldn't block other work in parallel.
