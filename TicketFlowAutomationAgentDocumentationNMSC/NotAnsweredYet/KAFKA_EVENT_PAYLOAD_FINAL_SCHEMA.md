# Open Question: Kafka Event Payload — Final Schema

**Status**: Open (partially agreed)

## Question

Finalize the complete field list for both Kafka event payloads.

## Context

**`ticket-accepted` topic** — starting fields agreed so far: ticket id (ours), Jira issue key, category, script/VM identifier, accepted-by user, timestamp, correlation id. The app owner confirmed this as a starting point but wants to revisit before it's final, once more is known about what the VM-side script actually needs.

**`script-result` topic** — not yet discussed at all. Likely needs at minimum: correlation id (to match back to the originating `ticket-accepted` event), outcome (`Succeeded`/`Failed`), a reference to script output/logs, timestamp, and the VM identifier — but this is a guess, not a decision.

## Blocks

- The Orchestrator's Kafka producer/consumer DTOs.
- The contract the app owner's independently-built VM-side receiver needs to implement against.
