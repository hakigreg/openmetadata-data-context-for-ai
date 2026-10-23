SHELL := /bin/sh

-include .env
export

OPENMETADATA_VERSION ?= 2.0.2
OPENMETADATA_COMPOSE := .generated/openmetadata/docker-compose.yml
COMPOSE := docker compose --project-directory . -f $(OPENMETADATA_COMPOSE) -f compose.yaml

.PHONY: help setup compose-config up wait down reset dbt-build dbt-docs ingest-metadata reindex-search ingest-dbt profile governance-bootstrap context-export token validate demo

help:
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Prepare local configuration and fetch the pinned official OpenMetadata Compose file
	@test -f .env || cp .env.example .env
	@test -f $(OPENMETADATA_COMPOSE) || ./scripts/fetch-openmetadata-compose.sh $(OPENMETADATA_VERSION) $(OPENMETADATA_COMPOSE)

compose-config: setup ## Render and validate the merged Docker Compose configuration
	@$(COMPOSE) config --quiet
	@$(COMPOSE) config --format json | python3 scripts/validate_compose_network.py

up: setup ## Start OpenMetadata and the digital commerce PostgreSQL warehouse
	@$(COMPOSE) up --detach

wait: ## Wait until the OpenMetadata API reports healthy
	@./scripts/wait-for-openmetadata.sh

down: setup ## Stop the local stack without deleting data
	@$(COMPOSE) down

reset: setup ## Delete local containers and volumes; all demo state will be lost
	@$(COMPOSE) down --volumes --remove-orphans

dbt-build: setup ## Build and test every dbt model
	@$(COMPOSE) --profile tools run --rm dbt build

dbt-docs: setup ## Generate dbt manifest and catalog artifacts
	@$(COMPOSE) --profile tools run --rm dbt docs generate

token: ## Print a temporary local OpenMetadata access token
	@python3 scripts/openmetadata/token.py

ingest-metadata: setup ## Ingest PostgreSQL schemas, tables, and views into OpenMetadata
	@token="$$(python3 scripts/openmetadata/token.py)"; \
	$(COMPOSE) exec -T \
	  -e OPENMETADATA_JWT_TOKEN="$$token" \
	  -e COMMERCE_DB_USER="$${COMMERCE_DB_USER}" \
	  -e COMMERCE_DB_PASSWORD="$${COMMERCE_DB_PASSWORD}" \
	  ingestion metadata ingest -c /workspace/openmetadata/ingestion/postgres.yaml

reindex-search: ## Ensure ingested tables are searchable before dbt enrichment
	@python3 scripts/openmetadata/reindex_tables.py

ingest-dbt: setup ## Ingest dbt descriptions, tests, tags, owners, and lineage
	@token="$$(python3 scripts/openmetadata/token.py)"; \
	$(COMPOSE) exec -T -e OPENMETADATA_JWT_TOKEN="$$token" \
	  ingestion metadata ingest -c /workspace/openmetadata/ingestion/dbt.yaml

profile: setup ## Profile governed marts and publish metrics to OpenMetadata
	@token="$$(python3 scripts/openmetadata/token.py)"; \
	$(COMPOSE) exec -T \
	  -e OPENMETADATA_JWT_TOKEN="$$token" \
	  -e COMMERCE_DB_USER="$${COMMERCE_DB_USER}" \
	  -e COMMERCE_DB_PASSWORD="$${COMMERCE_DB_PASSWORD}" \
	  ingestion metadata profile -c /workspace/openmetadata/ingestion/profiler.yaml

governance-bootstrap: ## Idempotently create governance entities and curate the Data Product
	@python3 scripts/openmetadata/bootstrap.py

context-export: ## Export an AI-ready context package from governed OpenMetadata assets
	@python3 scripts/openmetadata/export_ai_context.py

validate: compose-config ## Run fast, non-destructive project validation
	@python3 -m unittest discover -s tests -v

demo: up wait dbt-build dbt-docs ingest-metadata reindex-search governance-bootstrap ingest-dbt profile context-export ## Build the end-to-end governed metadata demo
	@printf 'Base demo ready. Open http://localhost:8585\n'
