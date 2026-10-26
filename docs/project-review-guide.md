# Project review guide

The project can be evaluated through a repository-only review or an optional
live validation of the running platform.

## Repository-only review

This path does not require the local stack.

1. Start with the [architecture and metadata provenance](../README.md#architecture)
   to understand the separation between the source warehouse, dbt lifecycle,
   OpenMetadata, and the AI Context Pack.
2. Review the [platform scope decision](adr/0001-platform-scope.md) for the
   intended boundaries and tradeoffs.
3. Inspect the declarative [governance catalog](../governance/catalog.json).
   It defines the `Digital Commerce` domain, `Commerce Analytics` owner,
   glossary, sensitivity classification, `Commerce Insights` Data Product, and
   curated asset membership.
4. Inspect [marts.yml](../dbt/models/marts/marts.yml) and the SQL models under
   [`dbt/models`](../dbt/models/). Their descriptions, tests, tags, and
   `source()`/`ref()` dependencies provide the dbt-authored metadata imported
   into OpenMetadata.
5. Review the versioned [AI Context Pack](../examples/ai-context/context.md).
   It demonstrates that governed metadata can be exported for AI consumers
   without including source rows or customer values.
6. Use the [implementation evidence](../README.md#implementation-evidence) to
   compare the declared configuration with the resulting OpenMetadata views.

## Evidence map

| Capability | Repository evidence | Expected result |
| --- | --- | --- |
| Domain and ownership | [`governance/catalog.json`](../governance/catalog.json) | `Commerce Insights` belongs to `Digital Commerce` and is owned by `Commerce Analytics`. |
| Data Product curation | [`dataProductAssets`](../governance/catalog.json) | Seven governed marts are curated as product assets. |
| Business semantics | [Glossary definitions](../governance/catalog.json) and [dbt metadata](../dbt/models/marts/marts.yml) | Business terms are attached to relevant analytical assets and columns. |
| Sensitivity handling | [`sensitivityAssignments`](../governance/catalog.json) | Customer identifiers and direct identifiers are classified across the data lifecycle. |
| Lineage | dbt [`source()` and `ref()` dependencies](../dbt/models) | Lineage connects source tables, staging, intermediate models, and governed marts. |
| Quality and profiling | [dbt tests](../dbt/models) and [profiler workflow](../openmetadata/ingestion/profiler.yaml) | Test results and aggregate column profiles appear beside governed assets. |
| AI-ready context | [Exporter](../scripts/openmetadata/export_ai_context.py) and [versioned example](../examples/ai-context/context.md) | The output contains definitions, ownership, domains, tags, and classifications, but no warehouse records. |

## Optional live validation

Follow the [prerequisites and quick start](../README.md#prerequisites), then run:

```bash
cp .env.example .env
make demo
```

Open OpenMetadata at <http://localhost:8585> and sign in with the local demo
credentials documented in the README. The following checks exercise the main
claims of the implementation:

1. Find the `Digital Commerce` domain and the `Commerce Insights` Data Product.
   Confirm its domain, owner, description, and seven curated assets, then
   inspect the tier assignments on the curated marts.
2. Open `dim_customers`. Confirm its descriptions, glossary associations,
   `DataSensitivity.Confidential` classifications, dbt tags, and ownership.
3. Follow lineage from `mart_customer_360` or `mart_executive_kpis` through the
   fact, intermediate, staging, and source layers.
4. Inspect imported dbt test results and the latest column profiles for a
   governed mart.
5. Regenerate the context package with `make context-export`, then inspect
   `artifacts/ai-context/context.md` and `context.json`.

## Scope of the review

This is a reproducible local implementation, not a production deployment or a
regulatory compliance claim. Privacy is represented through metadata,
classification, and usage boundaries. Production hardening considerations are
documented in the [Scope and security](../README.md#scope-and-security) section.

