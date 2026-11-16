from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SyncedTicket:
    JiraKey: str
    RawJson: str
    JiraUpdatedAt: str
    FetchedAt: str
