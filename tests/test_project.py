from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "openmetadata"))

from bootstrap import build_sensitivity_patch


class ProjectContractTest(unittest.TestCase):
    def test_chinook_fixture_is_pinned(self) -> None:
        fixture = ROOT / "data" / "chinook" / "Chinook_PostgreSql.sql"
        digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            "e3fde5c1a5b51a2a91429a702c9ca6e69ba56e6c7f5e112724d70c3d03db695e",
        )

    def test_governance_spec_has_ai_context_assets(self) -> None:
        spec = json.loads((ROOT / "governance" / "catalog.json").read_text())
        assets = spec["dataProductAssets"]["CommerceInsights"]
        self.assertGreaterEqual(len(assets), 5)
        self.assertTrue(all(".marts." in asset for asset in assets))
        product = next(
            item for item in spec["dataProducts"] if item["name"] == "CommerceInsights"
        )
        self.assertEqual(product["ownerFqns"], ["CommerceAnalytics"])

    def test_confidential_data_is_classified_across_the_dbt_lifecycle(self) -> None:
        spec = json.loads((ROOT / "governance" / "catalog.json").read_text())
        assignments = {
            item["table"]: item["columns"]
            for item in spec["sensitivityAssignments"]
        }
        for schema, table, columns in (
            ("public", "customer", {"customer_id", "first_name", "last_name", "email"}),
            ("staging", "stg_customers", {"customer_id", "first_name", "last_name", "email"}),
            ("marts", "dim_customers", {"customer_id", "customer_name", "email"}),
            ("marts", "mart_customer_360", {"customer_id", "customer_name"}),
        ):
            fqn = f"digital_commerce_postgres.chinook.{schema}.{table}"
            self.assertEqual(set(assignments[fqn]), columns)
            self.assertEqual(
                set(assignments[fqn].values()),
                {"DataSensitivity.Confidential"},
            )

    def test_sensitivity_patch_replaces_conflicts_and_preserves_dbt_tags(self) -> None:
        table = {
            "fullyQualifiedName": "service.database.schema.customers",
            "columns": [
                {
                    "name": "email",
                    "tags": [
                        {"tagFQN": "DbtTags.personal_data"},
                        {"tagFQN": "DataSensitivity.Internal"},
                    ],
                }
            ],
        }
        patch = build_sensitivity_patch(
            table, {"email": "DataSensitivity.Confidential"}
        )
        self.assertEqual(patch[0], {"op": "remove", "path": "/columns/0/tags/1"})
        self.assertEqual(patch[1]["op"], "add")
        self.assertEqual(patch[1]["value"]["tagFQN"], "DataSensitivity.Confidential")

    def test_sensitivity_patch_is_idempotent(self) -> None:
        table = {
            "fullyQualifiedName": "service.database.schema.customers",
            "columns": [
                {
                    "name": "email",
                    "tags": [{"tagFQN": "DataSensitivity.Confidential"}],
                }
            ],
        }
        self.assertEqual(
            build_sensitivity_patch(
                table, {"email": "DataSensitivity.Confidential"}
            ),
            [],
        )

    def test_no_jwt_is_committed_to_ingestion_configs(self) -> None:
        for config in (ROOT / "openmetadata" / "ingestion").glob("*.yaml"):
            text = config.read_text()
            self.assertIn("${OPENMETADATA_JWT_TOKEN}", text)
            self.assertNotIn("eyJhbGciOi", text)

    def test_demo_reindexes_tables_before_dbt_ingestion(self) -> None:
        makefile = (ROOT / "Makefile").read_text()
        self.assertIn(
            "ingest-metadata reindex-search governance-bootstrap "
            "reindex-governance ingest-dbt",
            makefile,
        )

    def test_demo_reindexes_governance_for_marketplace(self) -> None:
        makefile = (ROOT / "Makefile").read_text()
        self.assertIn(
            "governance-bootstrap reindex-governance ingest-dbt",
            makefile,
        )
        reindex_script = (
            ROOT / "scripts" / "openmetadata" / "reindex_governance.py"
        ).read_text()
        self.assertIn("domain_search_index", reindex_script)
        self.assertIn("data_product_search_index", reindex_script)
        self.assertIn('"type": entity_type', reindex_script)

    def test_demo_preserves_and_indexes_executed_dbt_test_results(self) -> None:
        makefile = (ROOT / "Makefile").read_text()
        self.assertIn("dbt-build dbt-docs dbt-test ingest-metadata", makefile)
        self.assertIn("ingest-dbt reindex-tests profile", makefile)
        reindex_script = (
            ROOT / "scripts" / "openmetadata" / "reindex_test_cases.py"
        ).read_text()
        self.assertIn("test_case_search_index", reindex_script)
        self.assertIn('"type": "testCase"', reindex_script)

    def test_compose_overrides_restrict_host_access(self) -> None:
        compose = (ROOT / "compose.yaml").read_text()
        self.assertIn('127.0.0.1:${COMMERCE_DB_HOST_PORT:-55432}:5432', compose)
        self.assertIn('127.0.0.1:8080:8080', compose)
        self.assertIn('127.0.0.1:8585:8585', compose)
        self.assertIn("mysql:\n    ports: !override []", compose)
        self.assertIn("elasticsearch:\n    ports: !override []", compose)

    def test_readiness_check_uses_the_public_api_port(self) -> None:
        wait_script = (ROOT / "scripts" / "wait-for-openmetadata.sh").read_text()
        self.assertIn("localhost:8585/api/v1/system/version", wait_script)
        self.assertNotIn("localhost:8586", wait_script)

    def test_versioned_context_example_matches_governed_assets(self) -> None:
        spec = json.loads((ROOT / "governance" / "catalog.json").read_text())
        example = json.loads(
            (ROOT / "examples" / "ai-context" / "context.json").read_text()
        )
        expected = set(spec["dataProductAssets"]["CommerceInsights"])
        actual = {table["fullyQualifiedName"] for table in example["tables"]}
        self.assertEqual(actual, expected)
        self.assertEqual(example["source"], "OpenMetadata")

    def test_readme_documents_metadata_provenance(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn("## Metadata provenance", readme)
        for source in (
            "openmetadata/ingestion/postgres.yaml",
            "openmetadata/ingestion/dbt.yaml",
            "openmetadata/ingestion/profiler.yaml",
            "governance/catalog.json",
            "scripts/openmetadata/bootstrap.py",
            "scripts/openmetadata/export_ai_context.py",
        ):
            self.assertIn(source, readme)

    def test_implementation_screenshots_are_real_jpeg_files(self) -> None:
        image_dir = ROOT / "docs" / "images"
        for name in (
            "data-product-overview.jpg",
            "data-product-assets.jpg",
            "lineage-dim-customers.jpg",
            "column-profiling.jpg",
            "column-governance.jpg",
            "data-quality-tests.jpg",
        ):
            data = (image_dir / name).read_bytes()
            self.assertTrue(data.startswith(b"\xff\xd8\xff"), name)
            self.assertGreater(len(data), 20_000, name)


if __name__ == "__main__":
    unittest.main()
