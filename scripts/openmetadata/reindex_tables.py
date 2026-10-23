#!/usr/bin/env python3
"""Ensure project tables are searchable before dbt metadata enrichment."""

from __future__ import annotations

import time
from typing import Any

from client import OpenMetadataClient


SERVICE_PREFIX = "digital_commerce_postgres."
SEARCH_PATH = "/v1/search/query?q=*&index=table_search_index&from=0&size=100"


def project_tables(client: OpenMetadataClient) -> list[dict[str, Any]]:
    response = client.request("GET", "/v1/tables?limit=100")
    if not isinstance(response, dict):
        raise RuntimeError("Unexpected table list response")
    return [
        table
        for table in response.get("data", [])
        if table.get("fullyQualifiedName", "").startswith(SERVICE_PREFIX)
    ]


def indexed_fqns(client: OpenMetadataClient) -> set[str]:
    response = client.request("GET", SEARCH_PATH)
    if not isinstance(response, dict):
        raise RuntimeError("Unexpected search response")
    return {
        hit.get("_source", {}).get("fullyQualifiedName")
        for hit in response.get("hits", {}).get("hits", [])
        if hit.get("_source", {}).get("fullyQualifiedName", "").startswith(
            SERVICE_PREFIX
        )
    }


def main() -> int:
    client = OpenMetadataClient()
    tables = project_tables(client)
    if not tables:
        raise RuntimeError("No project tables are available to reindex")

    client.request(
        "POST",
        "/v1/search/reindexEntities?timeoutMinutes=5",
        [{"id": table["id"], "type": "table"} for table in tables],
    )

    expected = {table["fullyQualifiedName"] for table in tables}
    missing = expected
    for _ in range(30):
        missing = expected - indexed_fqns(client)
        if not missing:
            print(f"reindexed {len(expected)} project tables")
            return 0
        time.sleep(1)

    raise RuntimeError(
        "Tables missing from search index after reindex: " + ", ".join(sorted(missing))
    )


if __name__ == "__main__":
    raise SystemExit(main())
