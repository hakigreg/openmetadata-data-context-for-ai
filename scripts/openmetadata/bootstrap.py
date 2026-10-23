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

TAG_LABEL = {
    "source": "Classification",
    "labelType": "Manual",
    "state": "Confirmed",
}


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


def build_sensitivity_patch(
    table: dict, column_assignments: dict[str, str]
) -> list[dict]:
    """Build an idempotent JSON Patch for mutually exclusive sensitivity tags."""
    columns = table.get("columns", [])
    indexes = {column["name"]: index for index, column in enumerate(columns)}
    missing = sorted(set(column_assignments) - set(indexes))
    if missing:
        raise RuntimeError(
            f"columns not found on {table.get('fullyQualifiedName')}: {', '.join(missing)}"
        )

    patch = []
    for column_name, tag_fqn in column_assignments.items():
        column_index = indexes[column_name]
        column = columns[column_index]
        classification = tag_fqn.split(".", 1)[0]
        tags = column.get("tags", [])
        sensitivity_indexes = [
            index
            for index, tag in enumerate(tags)
            if tag.get("tagFQN", "").split(".", 1)[0] == classification
        ]
        has_target = any(tag.get("tagFQN") == tag_fqn for tag in tags)

        for tag_index in reversed(sensitivity_indexes):
            if tags[tag_index].get("tagFQN") != tag_fqn:
                patch.append(
                    {
                        "op": "remove",
                        "path": f"/columns/{column_index}/tags/{tag_index}",
                    }
                )

        if not has_target:
            label = {"tagFQN": tag_fqn, **TAG_LABEL}
            if "tags" in column:
                patch.append(
                    {
                        "op": "add",
                        "path": f"/columns/{column_index}/tags/-",
                        "value": label,
                    }
                )
            else:
                patch.append(
                    {
                        "op": "add",
                        "path": f"/columns/{column_index}/tags",
                        "value": [label],
                    }
                )
    return patch


def apply_sensitivity_assignments(client: OpenMetadataClient, spec: dict) -> None:
    for assignment in spec.get("sensitivityAssignments", []):
        table_fqn = assignment["table"]
        table = client.get_by_name("tables", table_fqn, "columns,tags")
        patch = build_sensitivity_patch(table, assignment["columns"])
        if patch:
            client.request(
                "PATCH",
                f"/v1/tables/{table['id']}",
                patch,
                content_type="application/json-patch+json",
            )
        print(
            f"ensured classification for {table_fqn}: "
            f"{len(assignment['columns'])} sensitive columns"
        )


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text())
    client = OpenMetadataClient()
    upsert_foundation(client, spec)
    curate_data_product(client, spec)
    apply_sensitivity_assignments(client, spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
