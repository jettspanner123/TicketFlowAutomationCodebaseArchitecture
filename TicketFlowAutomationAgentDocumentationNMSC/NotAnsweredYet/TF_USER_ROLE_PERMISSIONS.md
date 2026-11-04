# Open Question: TF_USER Role Permissions

**Status**: Open

## Question

What exactly can `TF_USER` view on the dashboard — all tickets or a subset, which fields, any actions at all beyond viewing?

## Context

Confirmed: `TF_ADMIN` can change ticket status, `TF_DEVELOPER` has full access. `TF_USER` is view-only, but the app owner described the exact scope as "certain stuff (not decided yet)."

## Blocks

- RBAC policy definitions in the backend (which endpoints/fields `TF_USER` can reach).
- Which dashboard routes/components are visible to a `TF_USER`-only session.
