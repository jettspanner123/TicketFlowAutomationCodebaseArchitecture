# Open Question: Kafka Managed Provider Choice

**Status**: Open

## Question

Which managed Kafka service will host the cluster — Confluent Cloud, Azure Event Hubs (Kafka-compatible endpoint), AWS MSK Serverless, or another provider?

## Context

Confirmed: the Kafka cluster is built from scratch (no existing cluster to reuse) and will be a managed cloud service, not self-hosted. The chosen plan caps the account at 5 topics total — a constraint already factored into the topic design (see `ARCHITECTURE.md` → Kafka topic design), but the specific provider is still to be told by the app owner.

## Blocks

- Auth mechanism (SASL/mTLS/etc.) used by both the Orchestrator and the VM-side receiver.
- Connection string / client configuration.
- Which .NET Kafka client library to use (e.g. Confluent's `confluent-kafka-dotnet` vs. a provider-specific SDK).
