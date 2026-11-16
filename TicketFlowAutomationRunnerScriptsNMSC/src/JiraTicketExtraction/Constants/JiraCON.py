from __future__ import annotations

from typing import ClassVar


class JiraCON:
    SEARCH_ENDPOINT_PATH: ClassVar[str] = "/rest/api/3/search/jql"
    ALL_FIELDS_WILDCARD: ClassVar[str] = "*all"
    DEFAULT_MAX_RESULTS: ClassVar[int] = 100
    REQUEST_TIMEOUT_SECONDS: ClassVar[int] = 30
