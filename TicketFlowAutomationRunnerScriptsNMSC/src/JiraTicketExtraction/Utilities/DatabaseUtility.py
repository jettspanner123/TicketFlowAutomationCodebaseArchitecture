from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar

from JiraTicketExtraction.Constants.DatabaseCON import DatabaseCON
from JiraTicketExtraction.Models.SyncedTicket import SyncedTicket


class DatabaseUtility:
    Current: ClassVar[DatabaseUtility]

    def __init__(self) -> None:
        databaseFolderPath: Path = Path(__file__).resolve().parent.parent / "Database"
        self._DatabaseFilePath: Path = databaseFolderPath / DatabaseCON.DATABASE_FILE_NAME
        self._SchemaFilePath: Path = databaseFolderPath / DatabaseCON.SCHEMA_FILE_NAME
        self.EnsureSchema()

    def _OpenConnection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._DatabaseFilePath)

    def EnsureSchema(self) -> None:
        schemaSql: str = self._SchemaFilePath.read_text(encoding="utf-8")
        connection: sqlite3.Connection = self._OpenConnection()
        try:
            connection.executescript(schemaSql)
            connection.commit()
        finally:
            connection.close()

    def GetLastSyncedAt(self) -> str | None:
        connection: sqlite3.Connection = self._OpenConnection()
        try:
            cursor: sqlite3.Cursor = connection.execute(
                f"SELECT ConfigValue FROM {DatabaseCON.SYNC_CONFIGURATION_TABLE} WHERE ConfigKey = ?",
                (DatabaseCON.LAST_SYNCED_AT_CONFIG_KEY,),
            )
            row: tuple[str] | None = cursor.fetchone()
            return row[0] if row is not None else None
        finally:
            connection.close()

    def SetLastSyncedAt(self, lastSyncedAt: str) -> None:
        nowIsoTimestamp: str = datetime.now(timezone.utc).isoformat()
        connection: sqlite3.Connection = self._OpenConnection()
        try:
            connection.execute(
                f"""
                INSERT INTO {DatabaseCON.SYNC_CONFIGURATION_TABLE} (ConfigKey, ConfigValue, UpdatedAt)
                VALUES (?, ?, ?)
                ON CONFLICT(ConfigKey) DO UPDATE SET
                    ConfigValue = excluded.ConfigValue,
                    UpdatedAt = excluded.UpdatedAt
                """,
                (DatabaseCON.LAST_SYNCED_AT_CONFIG_KEY, lastSyncedAt, nowIsoTimestamp),
            )
            connection.commit()
        finally:
            connection.close()

    def UpsertTicket(self, ticket: SyncedTicket) -> None:
        connection: sqlite3.Connection = self._OpenConnection()
        try:
            connection.execute(
                f"""
                INSERT INTO {DatabaseCON.JIRA_TICKET_SYNC_TABLE} (JiraKey, RawJson, JiraUpdatedAt, FetchedAt)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(JiraKey) DO UPDATE SET
                    RawJson = excluded.RawJson,
                    JiraUpdatedAt = excluded.JiraUpdatedAt,
                    FetchedAt = excluded.FetchedAt
                """,
                (ticket.JiraKey, ticket.RawJson, ticket.JiraUpdatedAt, ticket.FetchedAt),
            )
            connection.commit()
        finally:
            connection.close()


DatabaseUtility.Current = DatabaseUtility()
