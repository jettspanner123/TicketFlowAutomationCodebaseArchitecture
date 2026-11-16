from __future__ import annotations

from datetime import datetime

from JiraTicketExtraction.Models.SyncedTicket import SyncedTicket
from JiraTicketExtraction.Services.JiraExtractionService import JiraExtractionService
from JiraTicketExtraction.Utilities.ConsoleTableUtility import ConsoleTableUtility
from JiraTicketExtraction.Utilities.DatabaseUtility import DatabaseUtility
from JiraTicketExtraction.Utilities.EnvironmentUtility import EnvironmentUtility


class SyncOrchestrationService:
    def __init__(self) -> None:
        self._JiraExtractionService: JiraExtractionService = JiraExtractionService()

    def RunSync(self) -> int:
        lastSyncedAt: str | None = DatabaseUtility.Current.GetLastSyncedAt()
        configuredJql: str = EnvironmentUtility.Current.GetJiraJql()
        jql: str = self._BuildJql(configuredJql, lastSyncedAt)

        fetchedTickets: list[SyncedTicket] = self._JiraExtractionService.FetchIssuesMatching(jql)
        ConsoleTableUtility.Current.PrintTickets(fetchedTickets)

        latestUpdatedAt: str | None = lastSyncedAt
        for ticket in fetchedTickets:
            DatabaseUtility.Current.UpsertTicket(ticket)
            if latestUpdatedAt is None or ticket.JiraUpdatedAt > latestUpdatedAt:
                latestUpdatedAt = ticket.JiraUpdatedAt

        if latestUpdatedAt is not None:
            DatabaseUtility.Current.SetLastSyncedAt(latestUpdatedAt)

        return len(fetchedTickets)

    @staticmethod
    def _BuildJql(configuredJql: str, lastSyncedAt: str | None) -> str:
        if lastSyncedAt is None:
            return configuredJql
        jqlDateTime: str = SyncOrchestrationService._ToJqlDateTime(lastSyncedAt)
        return f'({configuredJql}) AND updated >= "{jqlDateTime}"'

    @staticmethod
    def _ToJqlDateTime(jiraIsoTimestamp: str) -> str:
        parsedDateTime: datetime = datetime.strptime(jiraIsoTimestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        return parsedDateTime.strftime("%Y-%m-%d %H:%M")
