# Open Question: Category → Script Execution Mode

**Status**: Open

## Question

A category can map to multiple scripts/VMs (one-to-many, confirmed). When an admin accepts a ticket in such a category, should **all** mapped scripts fire automatically, or should the admin pick which of the mapped scripts/VMs to trigger at accept-time?

## Context

The app owner doesn't have an answer yet. This directly shapes:

- The dashboard's accept-action UI: a plain "Accept" button (all-mapped-scripts mode) vs. an "Accept" flow that opens a script/VM picker.
- The Orchestrator's Kafka producer logic: publish one `ticket-accepted` event per accept action, or one per selected script/VM.

## Blocks

- Dashboard accept-action UI design.
- Kafka producer logic for the `ticket-accepted` topic.
