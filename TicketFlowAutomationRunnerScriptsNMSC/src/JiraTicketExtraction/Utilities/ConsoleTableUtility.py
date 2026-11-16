from __future__ import annotations

import json
from datetime import datetime
from typing import Any, ClassVar

from rich.console import Console
from rich.status import Status
from rich.table import Table

from JiraTicketExtraction.Models.SyncedTicket import SyncedTicket


class ConsoleTableUtility:
    Current: ClassVar[ConsoleTableUtility]

    def __init__(self) -> None:
        self._Console: Console = Console()

    def Status(self, message: str) -> Status:
        return self._Console.status(message, spinner="dots")

    def PrintTickets(self, tickets: list[SyncedTicket]) -> None:
        if not tickets:
            self._Console.print("[yellow]No tickets fetched this run.[/yellow]")
            return

        table: Table = Table(
            title=f"Fetched {len(tickets)} Jira Ticket(s)",
            header_style="bold magenta",
            border_style="cyan",
        )
        table.add_column("Jira Key", style="bold cyan", no_wrap=True)
        table.add_column("Issue Type", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Summary", style="white")
        table.add_column("Assignee", style="blue")
        table.add_column("Updated", style="magenta")

        for ticket in tickets:
            table.add_row(*self._ToRow(ticket))

        self._Console.print(table)

    @staticmethod
    def _ToRow(ticket: SyncedTicket) -> tuple[str, str, str, str, str, str]:
        issueFields: dict[str, Any] = json.loads(ticket.RawJson).get("fields", {})
        issueType: str = issueFields.get("issuetype", {}).get("name", "-")
        status: str = issueFields.get("status", {}).get("name", "-")
        summary: str = issueFields.get("summary") or "-"

        assigneeField: dict[str, Any] | None = issueFields.get("assignee")
        assignee: str = assigneeField.get("displayName", "-") if assigneeField else "Unassigned"

        return (ticket.JiraKey, issueType, status, summary, assignee, ConsoleTableUtility._FormatUpdatedAt(ticket.JiraUpdatedAt))

    @staticmethod
    def _FormatUpdatedAt(jiraIsoTimestamp: str) -> str:
        try:
            parsedDateTime: datetime = datetime.strptime(jiraIsoTimestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
            return parsedDateTime.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return jiraIsoTimestamp


ConsoleTableUtility.Current = ConsoleTableUtility()
