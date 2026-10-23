#!/usr/bin/env python3
"""Ensure dbt test cases are searchable after OpenMetadata ingestion."""

from __future__ import annotations

import time
from typing import Any

from client import OpenMetadataClient


SERVICE_PREFIX = "digital_commerce_postgres."
SEARCH_PATH = "/v1/search/query?q=*&index=test_case_search_index&from=0&size=100"


def project_test_cases(client: OpenMetadataClient) -> list[dict[str, Any]]:
    response = client.request("GET", "/v1/dataQuality/testCases?limit=100")
    if not isinstance(response, dict):
        raise RuntimeError("Unexpected test case list response")
    return [
        test_case
        for test_case in response.get("data", [])
        if SERVICE_PREFIX in test_case.get("entityLink", "")
    ]


def indexed_fqns(client: OpenMetadataClient) -> set[str]:
    response = client.request("GET", SEARCH_PATH)
    if not isinstance(response, dict):
        raise RuntimeError("Unexpected test case search response")
    return {
        hit.get("_source", {}).get("fullyQualifiedName")
        for hit in response.get("hits", {}).get("hits", [])
        if hit.get("_source", {}).get("fullyQualifiedName", "").startswith(
            SERVICE_PREFIX
        )
    }


def main() -> int:
    client = OpenMetadataClient()
    test_cases = project_test_cases(client)
    if not test_cases:
        raise RuntimeError("No project dbt test cases are available to reindex")

    client.request(
        "POST",
        "/v1/search/reindexEntities?timeoutMinutes=5",
        [{"id": test_case["id"], "type": "testCase"} for test_case in test_cases],
    )

    expected = {test_case["fullyQualifiedName"] for test_case in test_cases}
    missing = expected
    for _ in range(30):
        missing = expected - indexed_fqns(client)
        if not missing:
            print(f"reindexed {len(expected)} dbt test cases")
            return 0
        time.sleep(1)

    raise RuntimeError(
        "Test cases missing from search index after reindex: "
        + ", ".join(sorted(missing))
    )


if __name__ == "__main__":
    raise SystemExit(main())
