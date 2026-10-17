# Decision Record Index

Each material implementation choice gets its own record. A decision may be revised, but the original rationale and consequences must remain visible.

| ID | Decision | Status | Record |
|---|---|---|---|
| D001 | Use a deterministic Python pipeline with bounded LLM steps | Accepted | [decision-001-pipeline-architecture.md](decisions/decision-001-pipeline-architecture.md) |
| D002 | Use an explicit source hierarchy and entity gate | Accepted | [decision-002-source-hierarchy.md](decisions/decision-002-source-hierarchy.md) |
| D003 | Treat document text as untrusted data, never as instructions | Accepted | [decision-003-document-as-data.md](decisions/decision-003-document-as-data.md) |
| D004 | Keep arithmetic and conflict checks deterministic | Accepted | [decision-004-deterministic-numeric-checks.md](decisions/decision-004-deterministic-numeric-checks.md) |
| D005 | Use an accepted-claim ledger with source tags | Accepted | [decision-005-claim-ledger-and-citations.md](decisions/decision-005-claim-ledger-and-citations.md) |
| D006 | Keep the model boundary narrow and provider-configurable | Accepted | [decision-006-model-boundary.md](decisions/decision-006-model-boundary.md) |
| D007 | Validate the generated brief before declaring success | Accepted | [decision-007-output-validation.md](decisions/decision-007-output-validation.md) |
| D008 | Make testing iterative, reproducible, and honest | Accepted | [decision-008-testing-and-reproducibility.md](decisions/decision-008-testing-and-reproducibility.md) |

## Decision update policy

If implementation reveals that a decision must change:

1. Update the relevant decision record.
2. Record the change and reason in `CHANGELOG.md`.
3. Update `EXECUTION_PLAN.md`, `TRAPS.md`, or `TEST_PLAN.md` if behavior changes.
4. Re-run affected acceptance tests.
