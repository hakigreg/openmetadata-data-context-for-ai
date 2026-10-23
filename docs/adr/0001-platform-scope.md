# ADR 0001: Platform-led Digital Commerce Analytics scope

- Status: Accepted
- Date: 2026-10-23

## Context

The repository must demonstrate a credible, hands-on OpenMetadata
implementation without combining the portfolio piece with a regulatory control
framework. It should show Data Governance, Data Management, Data Privacy, and AI
Governance capabilities while remaining easy to run and evaluate.

## Decision

Use the Chinook digital media store fixture as an existing representative data
model, load it into PostgreSQL, and transform it with dbt into a small governed
analytical product.

OpenMetadata is the control plane for:

- discovery and technical metadata
- ownership and domain accountability
- glossary and classification semantics
- lineage, quality tests, and profiling
- Data Product curation
- governed metadata exported as context for AI consumers

The AI deliverable is a provider-neutral context package generated from the
OpenMetadata API. A chatbot, vector database, and LLM integration are explicitly
outside the initial scope.

## Consequences

- The demo remains small enough to run locally and explain in ten minutes.
- Existing representative data avoids building a synthetic data generator.
- Privacy is demonstrated semantically, without asserting legal compliance.
- The architecture can later be extended to cloud deployment, policy controls,
  or an AI agent without changing the core metadata model.
