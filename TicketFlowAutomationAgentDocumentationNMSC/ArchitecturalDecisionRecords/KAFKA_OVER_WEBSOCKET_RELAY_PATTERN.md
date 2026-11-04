# ADR: Kafka Over the Account's Established WebSocket-Relay Pattern

**Status**: Accepted

## Context

This account's other apps already solve backend↔remote-VM communication: `MonitoringDashboardClientMachineRelayWorkerMSC` is a .NET Windows Service running on each target VM that opens an outbound WebSocket to the backend (shared-secret auth, auto-reconnect), receives JSON commands, executes them, and streams JSON responses back. No message broker is involved.

That same codebase documents an explicit ADR (`DATABASE_OVER_EVENT_BUS_FOR_SMOKE_TEST_RESULTS.md`) rejecting an event bus for a comparably low-frequency, single-consumer case — reasoning that a broker's operational overhead (running and maintaining it, plus a consumer) is only worth it when there's real-time push to **multiple independent consumers**.

TiketaFlow's expected volume (~15-20 tickets/day) sits in a similar low range, and — at least initially — each category maps to a known, small set of VM receivers, not an open-ended set of independent consumers.

## Decision

TiketaFlow uses Kafka — a managed cloud service, built from scratch — for both the `ticket-accepted` and `script-result` events, rather than following the account's relay pattern.

**Rationale given**: explicit preference of the app owner. No additional justification (e.g. a specific need for replay, durability, or multiple independent consumers) was stated beyond that preference at the time this decision was made.

## Consequences

- Adds a managed Kafka dependency and its operational surface, including a 5-topic cap on the chosen plan — addressed by consolidating to 2 shared topics (see `ARCHITECTURE.md`).
- Gains over the relay pattern: a durable, replayable event log of every accept action and script result (useful given the full-audit-trail requirement), and a VM-side receiver that's decoupled from needing an always-open connection to the backend — it can consume whenever it comes online.
- This is a deliberate divergence from the account's own documented precedent for a similar low-volume, single-consumer case. If actual usage stays at this volume with effectively one consumer per event type, revisit whether Kafka's operational cost is still justified, or whether the relay pattern would have served just as well.
