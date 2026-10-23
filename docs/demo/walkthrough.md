# Ten-minute portfolio walkthrough

## 1. Frame the problem — 1 minute

Analytics and AI consumers need more than table names. They need definitions,
ownership, quality signals, lineage, and clear usage boundaries. Explain that
OpenMetadata is the context control plane for this demo.

## 2. Show the architecture — 1 minute

Use the README diagram to explain the separation between the operational
Chinook fixture, the dbt analytical lifecycle, and OpenMetadata.

## 3. Explore the domain and Data Product — 2 minutes

Open `Digital Commerce` and `Commerce Insights`. Highlight the owner, curated
assets, descriptions, and tiering.

## 4. Follow lineage — 2 minutes

Start at `mart_customer_360` or `mart_executive_kpis` and trace lineage back
through the fact, intermediate model, staging models, and source tables.

## 5. Inspect trust signals — 2 minutes

Show dbt tests, profiler results, column descriptions, glossary associations,
and sensitivity metadata on customer attributes.

## 6. Export context for AI — 2 minutes

Run `make context-export` and inspect `context.md` and `context.json`. Emphasize
that AI context is derived from governed metadata and excludes customer rows.

Close with the production-hardening items listed in the README to demonstrate
architectural judgment without pretending the local quickstart is production.
