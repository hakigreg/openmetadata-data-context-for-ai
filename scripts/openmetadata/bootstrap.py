#!/usr/bin/env python3
"""Idempotently create the governance foundation and curate the data product."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote

from client import OpenMetadataClient


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "governance" / "catalog.json"

COLLECTIONS = (
    ("domains", "domains"),
    ("teams", "teams"),
    ("classifications", "classifications"),
    ("tags", "tags"),
    ("glossaries", "glossaries"),
    ("glossaryTerms", "glossaryTerms"),
    ("dataProducts", "dataProducts"),
)


def upsert_foundation(client: OpenMetadataClient, spec: dict) -> None:
    for spec_key, endpoint in COLLECTIONS:
        for entity in spec.get(spec_key, []):
            payload = dict(entity)
            owner_fqns = payload.pop("ownerFqns", [])
            if endpoint == "dataProducts" and owner_fqns:
                payload["owners"] = [
                    {
                        "id": client.get_by_name("teams", owner_fqn)["id"],
                        "type": "team",
                    }
                    for owner_fqn in owner_fqns
                ]
            result = client.request("PUT", f"/v1/{endpoint}", payload)
            print(f"upserted {endpoint}: {result.get('fullyQualifiedName', result.get('name'))}")


def curate_data_product(client: OpenMetadataClient, spec: dict) -> None:
    for product_fqn, table_fqns in spec.get("dataProductAssets", {}).items():
        try:
            product = client.get_by_name("dataProducts", product_fqn)
        except RuntimeError as exc:
            print(f"skipping assets for {product_fqn}: {exc}", file=sys.stderr)
            continue
        assets = []
        missing = []
        for table_fqn in table_fqns:
            try:
                table = client.get_by_name("tables", table_fqn)
                assets.append({"id": table["id"], "type": "table"})
            except RuntimeError:
                missing.append(table_fqn)
        if assets:
            client.request(
                "PUT",
                f"/v1/dataProducts/{quote(product['fullyQualifiedName'], safe='')}/assets/add",
                {"assets": assets},
            )
            print(f"curated {product_fqn}: {len(assets)} assets")
        if missing:
            print(
                f"assets not available yet for {product_fqn}: {', '.join(missing)}",
                file=sys.stderr,
            )


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text())
    client = OpenMetadataClient()
    upsert_foundation(client, spec)
    curate_data_product(client, spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
