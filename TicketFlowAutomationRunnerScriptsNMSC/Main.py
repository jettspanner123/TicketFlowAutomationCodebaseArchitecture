from __future__ import annotations

from JiraTicketExtraction.Services.SyncOrchestrationService import SyncOrchestrationService


def Main() -> None:
    syncOrchestrationService: SyncOrchestrationService = SyncOrchestrationService()
    syncedCount: int = syncOrchestrationService.RunSync()
    print(f"Synced {syncedCount} ticket(s) from Jira.")


if __name__ == "__main__":
    Main()
