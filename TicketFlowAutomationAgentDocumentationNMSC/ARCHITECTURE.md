# Architecture

See `CONTEXT.md` for vision, domain language, and roles. This document covers stack, data flow, and conventions.

## Stack

| Layer | Choice |
|---|---|
| Backend | ASP.NET Core Web API (.NET), EF Core, PostgreSQL |
| Auth | JWT Bearer + RBAC (`TF_ADMIN`, `TF_DEVELOPER`, `TF_USER`) |
| Real-time | SignalR |
| Frontend | React 19 + TypeScript + Vite + bun |
| Frontend libs | TanStack Query, TanStack Router, Zustand, Tailwind, Zod, Sonner, Framer Motion, lucide-react |
| Messaging | Kafka, managed cloud service (provider TBD — see `NotAnsweredYet/KAFKA_MANAGED_PROVIDER_CHOICE.md`) |
| Jira integration | Jira Cloud REST API, polled every 5 minutes, auth via the app owner's existing Jira account |

Hosting for the POC phase: Vercel (frontend) and Render (backend), or localhost for local development. Single environment for now.

## High-level data flow

```
Jira Cloud
   │  poll every 5 min (one-way: Jira → us)
   ▼
Orchestrator: Jira Sync job
   │  ingest ticket, run categorization rules inline, persist (PostgreSQL)
   ▼
Orchestrator: SignalR push ──────────► Dashboard (React): new/updated ticket card
                                              │
                                              │ TF_ADMIN / TF_DEVELOPER: accept / reject / requeue
                                              │ (optional reason captured either way)
                                              ▼
                                       Orchestrator: write Status + audit log entry
                                              │
                                              │ on Accept
                                              ▼
                                   Kafka topic: ticket-accepted
                                   (payload: ticket id, Jira key, category,
                                    script/VM id, accepted-by, timestamp,
                                    correlation id — see
                                    NotAnsweredYet/KAFKA_EVENT_PAYLOAD_FINAL_SCHEMA.md)
                                              │
                                              ▼
                              VM-side Receiver (built independently,
                              outside this repo) runs the mapped script
                                              │
                                              ▼
                                   Kafka topic: script-result
                                              │
                                              ▼
                        Orchestrator consumer: update Status to
                        Succeeded/Failed, write audit log entry
                                              │
                                              ▼
                                   SignalR push ──► Dashboard reflects final status
```

Status lifecycle: `Pending` → `Accepted`/`Rejected` (admin action) → `Running` (set optimistically on Kafka publish) → `Succeeded`/`Failed` (from the script-result event) → `Requeued` (manual admin action only — no auto-retry).

## Kafka topic design

Capped at 5 topics total on the chosen managed plan, so topics are deliberately consolidated rather than split per category/VM:

- `ticket-accepted` — one shared topic for every accept action; consumers (VM receivers) filter by the `category`/`targetVm` field in the payload.
- `script-result` — one shared topic for every script outcome; the Orchestrator's consumer matches results back to tickets via `correlation id`.

This leaves headroom under the 5-topic cap for future needs.

## Categorization

Rule-based (not ML/LLM). Rules and category→script/VM mappings are stored in PostgreSQL and editable via an admin-only screen — never hardcoded, never requiring a redeploy to change. Evaluated inline, synchronously, as part of the Jira Sync ingestion step.

**Execution model is a placeholder pending the app owner's own design** — see `ArchitecturalDecisionRecords/TICKET_CATEGORIZATION_EXECUTION_MODEL.md`. Do not build against the "inline/synchronous" description above as final until that ADR is updated.

Admins (`TF_ADMIN`, `TF_DEVELOPER`) can manually override a ticket's assigned category from the dashboard.

## Jira integration

- Jira Cloud, polled every 5 minutes.
- Auth: API token under the app owner's own/shared existing Jira account (no dedicated service account, for now).
- Scope (which project(s)/board(s)/issue types to pull): DB-configurable via the same admin settings screen as categorization rules — not hardcoded. Actual scope values: `NotAnsweredYet/JIRA_PROJECT_AND_BOARD_SCOPE.md`.
- One-way sync only: we never write ticket status or comments back to Jira.

## Dashboard

- Cards show: Jira key, title/summary, category, current status, requester/reporter, created date, plus accept/reject controls and a status dropdown.
- Live updates via SignalR — no manual refresh needed.
- Accept/reject reason is optional on both actions, captured in the audit log when provided.

## Data & audit

- PostgreSQL via EF Core.
- Full audit log: every status change and admin action is recorded with who/what/when, independent of whether a reason was given.

## Conventions

- New markdown files created under `TicketFlowAutomationAgentDocumentationNMSC/` (NotAnsweredYet entries, ADRs) use `SCREAMING_SNAKE_CASE.md` naming. `CONTEXT.md`/`ARCHITECTURE.md` keep their established names.
- Role names are prefixed `TF_` (`TF_ADMIN`, `TF_DEVELOPER`, `TF_USER`).
- Coding-standard details (once code exists) belong in a `CODING-RULES.md` at this same level, per the account's usual convention — not yet created.

## Open items

Anything referenced above as "TBD" or "NotAnsweredYet" is tracked individually in `NotAnsweredYet/`, one file per open question. Architectural decisions — including ones still pending a design from the app owner — are tracked in `ArchitecturalDecisionRecords/`.
