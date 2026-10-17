# Changelog

This log records repository changes and the reason for each change. It must be updated after every coherent implementation phase.

## 2026-10-17 — Planning baseline

### Added

- `EXECUTION_PLAN.md`: complete implementation sequence, acceptance criteria, and stop conditions.
- `FILE_MANIFEST.md`: planned repository layout and file responsibilities.
- `CHANGELOG.md`: change-and-reason tracking.
- `DECISIONS.md`: decision-record index.
- `TRAPS.md`: known assignment traps and safeguards.
- `TEST_PLAN.md`: pre-coding verification plan.
- `decisions/`: decision records for the core architecture.

### Reason

The assignment evaluates reasoning quality and reproducibility. These files make the evidence policy, design choices, and validation expectations explicit before implementation begins.

### Not changed

- No Python implementation was written.
- No supplied research document was modified.
- No generated brief was claimed as final.

## 2026-10-17 — Core implementation

### Added

- `agent.py`: standard-library CLI pipeline for ingestion, triage, claims, numeric checks, generation, and validation.
- `system_prompt.md`: explicit grounding and prompt-injection policy.
- `requirements.txt`: documents the zero-third-party-dependency runtime.
- `research_pack/`: exact copy of the eight evidence documents.
- `output/SRVCABLE_brief.md`: generated final brief.
- `output/run_audit.json`: machine-readable audit of sources, claims, checks, and validation.
- Root `README.md`: setup and design explanation.

### Changed

- Completed `TEST_LOG.md` with three real implementation iterations and final verification.
- Marked runtime files complete in `FILE_MANIFEST.md`.

### Reason

The implementation makes the source-judgment workflow visible and reproducible while keeping arithmetic and output constraints deterministic.

### Validation

- Python compilation passed.
- Final CLI run passed.
- Final acceptance assertions passed.
