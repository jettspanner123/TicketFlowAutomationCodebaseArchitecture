from __future__ import annotations

from typing import ClassVar


class DatabaseCON:
    DATABASE_FILE_NAME: ClassVar[str] = "JiraTicketDatabase.db"
    SCHEMA_FILE_NAME: ClassVar[str] = "JiraTicketDatabase.sql"
    JIRA_TICKET_SYNC_TABLE: ClassVar[str] = "TFA_JiraTicketSyncTBL"
    SYNC_CONFIGURATION_TABLE: ClassVar[str] = "TFA_SyncConfigurationTBL"
    LAST_SYNCED_AT_CONFIG_KEY: ClassVar[str] = "LastSyncedAt"
