# Open Question: Target VM Identities

**Status**: Open

## Question

How many VMs will run acceptance scripts, and what are their hostnames/IPs/identifiers?

## Context

The app owner doesn't know yet — similar to the Jira project/board scope, this may end up configurable rather than fixed.

## Blocks

- Seed data for the category→script/VM mapping table.
- The `targetVm`-style field value each VM-side receiver filters the `ticket-accepted` topic by.
