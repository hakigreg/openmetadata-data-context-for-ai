#!/usr/bin/env python3
"""Export governed OpenMetadata table context without requiring an LLM provider."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from client import OpenMetadataClient


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "governance" / "catalog.json"
OUTPUT_DIR = ROOT / "artifacts" / "ai-context"
FIELDS = "owners,tags,columns,domains,dataProducts"


def compact_table(table: dict[str, Any]) -> dict[str, Any]:
    return {
        "fullyQualifiedName": table.get("fullyQualifiedName"),
        "displayName": table.get("displayName") or table.get("name"),
        "description": table.get("description"),
        "tableType": table.get("tableType"),
        "owners": [owner.get("fullyQualifiedName") for owner in table.get("owners", [])],
        "domains": [
            domain.get("fullyQualifiedName") for domain in table.get("domains", [])
        ],
        "dataProducts": [
            product.get("fullyQualifiedName") for product in table.get("dataProducts", [])
        ],
        "tags": [tag.get("tagFQN") for tag in table.get("tags", [])],
        "columns": [
            {
                "name": column.get("name"),
                "dataType": column.get("dataTypeDisplay") or column.get("dataType"),
                "description": column.get("description"),
                "tags": [tag.get("tagFQN") for tag in column.get("tags", [])],
            }
            for column in table.get("columns", [])
        ],
    }


def render_markdown(context: dict[str, Any]) -> str:
    lines = [
        "# AI Context Pack: Commerce Insights",
        "",
        f"Generated from OpenMetadata at `{context['generatedAt']}`.",
        "",
        "This artifact is grounded in governed metadata. It contains no source rows or customer values.",
        "",
    ]
    for table in context["tables"]:
        lines.extend(
            [
                f"## {table['displayName']}",
                "",
                table.get("description") or "No description available.",
                "",
                f"- FQN: `{table['fullyQualifiedName']}`",
                f"- Domains: {', '.join(table.get('domains', [])) or 'Unassigned'}",
                f"- Owners: {', '.join(table.get('owners', [])) or 'Unassigned'}",
                f"- Tags: {', '.join(filter(None, table.get('tags', []))) or 'None'}",
                "",
                "| Column | Type | Description |",
                "| --- | --- | --- |",
            ]
        )
        for column in table["columns"]:
            description = (column.get("description") or "").replace("|", "\\|")
            lines.append(f"| `{column['name']}` | `{column['dataType']}` | {description} |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text())
    product_name = spec["dataProducts"][0]["name"]
    table_fqns = spec["dataProductAssets"][product_name]
    client = OpenMetadataClient()
    tables = [compact_table(client.get_by_name("tables", fqn, FIELDS)) for fqn in table_fqns]
    context = {
        "schemaVersion": "1.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "source": "OpenMetadata",
        "purpose": "Governed semantic context for analytics assistants and AI agents",
        "constraints": [
            "Use metric definitions and column descriptions as authoritative context.",
            "Do not infer regulatory status from sensitivity tags.",
            "Do not expose customer-level values; this package contains metadata only.",
        ],
        "tables": tables,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "context.json").write_text(json.dumps(context, indent=2) + "\n")
    (OUTPUT_DIR / "context.md").write_text(render_markdown(context) + "\n")
    print(f"exported {len(tables)} governed assets to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
