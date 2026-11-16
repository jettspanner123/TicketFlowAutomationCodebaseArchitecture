from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import requests

from JiraTicketExtraction.Constants.JiraCON import JiraCON
from JiraTicketExtraction.Models.SyncedTicket import SyncedTicket
from JiraTicketExtraction.Utilities.EnvironmentUtility import EnvironmentUtility


class JiraExtractionService:
    def __init__(self) -> None:
        self._BaseUrl: str = EnvironmentUtility.Current.GetJiraBaseUrl()
        self._Email: str = EnvironmentUtility.Current.GetJiraEmail()
        self._ApiToken: str = EnvironmentUtility.Current.GetJiraApiToken()

    def FetchIssuesMatching(self, jql: str) -> list[SyncedTicket]:
        fetchedTickets: list[SyncedTicket] = []
        nextPageToken: str | None = None
        fetchedAt: str = datetime.now(timezone.utc).isoformat()

        while True:
            responseBody: dict[str, Any] = self._FetchPage(jql, nextPageToken)

            for issue in responseBody.get("issues", []):
                fetchedTickets.append(self._ToSyncedTicket(issue, fetchedAt))

            nextPageToken = responseBody.get("nextPageToken")
            if nextPageToken is None:
                break

        return fetchedTickets

    def _FetchPage(self, jql: str, nextPageToken: str | None) -> dict[str, Any]:
        requestBody: dict[str, Any] = {
            "jql": jql,
            "maxResults": JiraCON.DEFAULT_MAX_RESULTS,
            "fields": [JiraCON.ALL_FIELDS_WILDCARD],
        }
        if nextPageToken is not None:
            requestBody["nextPageToken"] = nextPageToken

        response: requests.Response = requests.post(
            f"{self._BaseUrl}{JiraCON.SEARCH_ENDPOINT_PATH}",
            auth=(self._Email, self._ApiToken),
            headers={"Content-Type": "application/json"},
            data=json.dumps(requestBody),
            timeout=JiraCON.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        responseBody: dict[str, Any] = response.json()
        return responseBody

    @staticmethod
    def _ToSyncedTicket(issue: dict[str, Any], fetchedAt: str) -> SyncedTicket:
        jiraKey: str = issue["key"]
        jiraUpdatedAt: str = issue["fields"]["updated"]
        return SyncedTicket(
            JiraKey=jiraKey,
            RawJson=json.dumps(issue),
            JiraUpdatedAt=jiraUpdatedAt,
            FetchedAt=fetchedAt,
        )
