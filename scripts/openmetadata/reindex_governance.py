#!/usr/bin/env python3
"""Ensure project domains and data products are searchable in the UI."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from client import OpenMetadataClient


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "governance" / "catalog.json"
ENTITY_CONFIG = (
    ("domains", "domain", "domain_search_index"),
    ("dataProducts", "dataProduct", "data_product_search_index"),
)


def indexed_fqns(client: OpenMetadataClient, index: str) -> set[str]:
    response = client.request(
        "GET", f"/v1/search/query?q=*&index={index}&from=0&size=100"
    )
    if not isinstance(response, dict):
        raise RuntimeError(f"Unexpected search response for {index}")
    return {
        hit.get("_source", {}).get("fullyQualifiedName")
        for hit in response.get("hits", {}).get("hits", [])
        if hit.get("_source", {}).get("fullyQualifiedName")
    }


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text())
    client = OpenMetadataClient()
    entities: list[dict[str, Any]] = []
    expected_by_index: dict[str, set[str]] = {}

    for collection, entity_type, index in ENTITY_CONFIG:
        expected_by_index[index] = set()
        for declared in spec.get(collection, []):
            entity = client.get_by_name(collection, declared["name"])
            entities.append({"id": entity["id"], "type": entity_type})
            expected_by_index[index].add(entity["fullyQualifiedName"])

    if not entities:
        raise RuntimeError("No project governance entities are available to reindex")

    client.request(
        "POST",
        "/v1/search/reindexEntities?timeoutMinutes=5",
        entities,
    )

    missing_by_index = expected_by_index
    for _ in range(30):
        missing_by_index = {
            index: expected - indexed_fqns(client, index)
            for index, expected in expected_by_index.items()
        }
        if not any(missing_by_index.values()):
            print(f"reindexed {len(entities)} governance entities")
            return 0
        time.sleep(1)

    missing = sorted(
        fqn for index_missing in missing_by_index.values() for fqn in index_missing
    )
    raise RuntimeError(
        "Governance entities missing from search index after reindex: "
        + ", ".join(missing)
    )


if __name__ == "__main__":
    raise SystemExit(main())
