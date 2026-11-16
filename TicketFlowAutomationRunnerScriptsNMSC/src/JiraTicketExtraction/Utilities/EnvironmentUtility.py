from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv

from JiraTicketExtraction.Constants.EnvironmentCON import EnvironmentCON


class EnvironmentUtility:
    Current: ClassVar[EnvironmentUtility]

    def __init__(self) -> None:
        projectRootPath: Path = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(dotenv_path=projectRootPath / ".env")

    def _GetRequired(self, variableName: str) -> str:
        value: str | None = os.environ.get(variableName)
        if not value:
            raise RuntimeError(
                f"Missing required environment variable: {variableName}. "
                f"Copy .env.example to .env and fill it in."
            )
        return value

    def GetJiraBaseUrl(self) -> str:
        return self._GetRequired(EnvironmentCON.JIRA_BASE_URL).rstrip("/")

    def GetJiraEmail(self) -> str:
        return self._GetRequired(EnvironmentCON.JIRA_EMAIL)

    def GetJiraApiToken(self) -> str:
        return self._GetRequired(EnvironmentCON.JIRA_API_TOKEN)

    def GetJiraJql(self) -> str:
        return self._GetRequired(EnvironmentCON.JIRA_JQL)


EnvironmentUtility.Current = EnvironmentUtility()
