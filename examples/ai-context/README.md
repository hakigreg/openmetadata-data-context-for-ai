# AI Context Pack example

This directory contains a static snapshot produced by `make context-export`
after a validated end-to-end local run.

The example contains governed metadata only: asset identifiers, descriptions,
ownership, domains, Data Product membership, tags, and column definitions. It
does not contain source rows, customer values, credentials, or access tokens.

- [`context.md`](context.md) is optimized for human review and prompt inspection.
- [`context.json`](context.json) is the machine-readable representation.

To regenerate the runtime artifacts, run `make context-export`. Generated
outputs are written to `artifacts/ai-context/` and remain ignored by Git.
