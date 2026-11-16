CREATE TABLE IF NOT EXISTS TFA_JiraTicketSyncTBL (
    JiraKey TEXT PRIMARY KEY,
    RawJson TEXT NOT NULL,
    JiraUpdatedAt TEXT NOT NULL,
    FetchedAt TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS TFA_SyncConfigurationTBL (
    ConfigKey TEXT PRIMARY KEY,
    ConfigValue TEXT,
    UpdatedAt TEXT NOT NULL
);
