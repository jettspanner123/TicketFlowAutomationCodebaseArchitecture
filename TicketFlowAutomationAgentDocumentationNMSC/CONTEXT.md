# Ticket Flow Automation

Replaces manual triage of Jira tickets with an automated pipeline: tickets are pulled from Jira, categorized by a rule-based decision model, and surfaced as cards on an admin dashboard. Accepting a card fires a Kafka event that a remote VM-side receiver (built independently, outside this repo) picks up to run the script tied to that ticket's category.

The product is branded **TiketaFlow** in the UI; the repo/folder names keep the formal project name (`TicketFlowAutomation*`) — same split as other apps in this account (e.g. "PLM Infrastructure Register" repo → "InfraGrid" branded UI).

## Language

**Ticket**:
A single item pulled from Jira and tracked in our own database once ingested. Not the Jira issue itself — our copy of it, carrying our own status and category on top of the Jira data.
_Avoid_: Issue, Card (Card is the UI representation of a Ticket, not the Ticket itself)

**Category**:
The bucket a Ticket is sorted into by the rule-based decision model. Drives which script(s)/VM(s) get triggered on acceptance. Can be reassigned manually by `TF_ADMIN`/`TF_DEVELOPER` if the rules misfire.
_Avoid_: Type, Classification

**Status**:
The lifecycle state of a Ticket: `Pending` → `Accepted`/`Rejected` → `Running` → `Succeeded`/`Failed` → `Requeued`. Owned entirely by our system — never written back to Jira.
_Avoid_: State (reserve "state" for describing a VM or script's own condition, not a Ticket's)

**Sync**:
The scheduled job that polls Jira (every 5 minutes) and creates/updates Tickets to match what's in Jira. One-way only — Jira is the source of truth for ticket content; we never push changes back to Jira.
_Avoid_: Fetch, Ingestion, Import

**Rule**:
One piece of the categorization logic: a condition over Ticket fields that assigns a Category. Stored in the database and editable via an admin-only screen — never hardcoded. Actual rules not yet defined; see `NotAnsweredYet/TICKET_CATEGORIZATION_RULES.md`.
_Avoid_: Condition, Filter

**Mapping**:
The DB-backed, admin-editable link from a Category to the script(s)/VM(s) that should run when a Ticket in that category is accepted. One Category can map to multiple scripts/VMs.
_Avoid_: Binding, Route

**Receiver**:
The VM-side component that consumes Kafka ticket-acceptance events and actually runs the script. Built and owned independently by the app owner — **out of scope** for this repo. Our only contract with it is the Kafka event schema.
_Avoid_: Agent, Worker (this repo doesn't implement it, so don't name it like we do)

## Roles

- **`TF_ADMIN`** — can change ticket status (accept/reject/requeue/etc.)
- **`TF_DEVELOPER`** — full access to everything in the app
- **`TF_USER`** — view-only; exact scope not yet decided, see `NotAnsweredYet/TF_USER_ROLE_PERMISSIONS.md`

## Stack

- **Backend**: ASP.NET Core Web API (.NET), EF Core, PostgreSQL, JWT Bearer auth + RBAC, SignalR for live dashboard push — matching the convention used across this account's other apps.
- **Frontend**: React 19 + TypeScript + Vite + bun, TanStack Query + TanStack Router, Zustand, Tailwind, Zod, Sonner, Framer Motion, lucide-react — same convention.
- **Messaging**: Kafka (managed cloud service, provider TBD), built from scratch for this app. See `ArchitecturalDecisionRecords/KAFKA_OVER_WEBSOCKET_RELAY_PATTERN.md` for why this departs from the account's usual VM-communication pattern.

## Structure

Single monorepo (this repo), no separate repos per layer:

```
TicketFlowAutomationCodebaseArchitecture/
├── TicketFlowAutomationClientServiceLayerMSC/        # frontend
├── TicketFlowAutomationOrchestratorServiceLayerMSC/  # backend
└── TicketFlowAutomationAgentDocumentationNMSC/       # this folder
    ├── CONTEXT.md
    ├── ARCHITECTURE.md
    ├── NotAnsweredYet/              # open questions, one file each
    └── ArchitecturalDecisionRecords/ # ADRs
```

No scripts/receiver folder — the VM-side receiver is a separate project owned by the app owner.

## Scope boundaries

- We own: Jira ingestion, categorization, the dashboard, the audit log, and publishing/consuming the two Kafka topics.
- We do **not** own: the VM-side receiver, the actual scripts it runs, or the VMs themselves.
- Jira sync is one-way (Jira → us). We never write ticket status back to Jira.

## Open items & decisions

- Unresolved questions (need the app owner's input before implementation): `NotAnsweredYet/`
- Architectural decisions, including ones still pending a design from the app owner: `ArchitecturalDecisionRecords/`

## Running locally

Not yet applicable — no code exists yet. This section will be filled in once the backend/frontend projects are scaffolded.
