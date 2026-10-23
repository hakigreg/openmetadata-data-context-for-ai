from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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

    def test_no_jwt_is_committed_to_ingestion_configs(self) -> None:
        for config in (ROOT / "openmetadata" / "ingestion").glob("*.yaml"):
            text = config.read_text()
            self.assertIn("${OPENMETADATA_JWT_TOKEN}", text)
            self.assertNotIn("eyJhbGciOi", text)

    def test_demo_reindexes_tables_before_dbt_ingestion(self) -> None:
        makefile = (ROOT / "Makefile").read_text()
        self.assertIn(
            "ingest-metadata reindex-search governance-bootstrap ingest-dbt",
            makefile,
        )


if __name__ == "__main__":
    unittest.main()
