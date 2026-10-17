# File Manifest

This file describes the intended repository contents. It is updated as implementation progresses.

| Path | Type | Responsibility | Status |
|---|---|---|---|
| `README.md` | Documentation | Setup, command, model choice, architecture, limitations, submission notes | Complete |
| `EXECUTION_PLAN.md` | Planning | Ordered execution phases and acceptance criteria | Complete |
| `FILE_MANIFEST.md` | Planning | File responsibility and status index | Complete |
| `CHANGELOG.md` | Tracking | What changed and why | Complete |
| `DECISIONS.md` | Tracking | Index of material design decisions | Complete |
| `TRAPS.md` | Testing/design | Assignment traps and mitigations | Complete |
| `TEST_PLAN.md` | Testing | Predefined verification and acceptance tests | Complete |
| `TEST_LOG.md` | Testing | Actual run-by-run failures and fixes | Complete |
| `system_prompt.md` | Prompt | Separate system prompt used by the model | Complete |
| `agent.py` | Source | CLI orchestration and deterministic checks | Complete |
| `requirements.txt` | Configuration | Minimal Python dependencies | Complete |
| `research_pack/` | Input data | Copy of the eight supplied documents | Complete |
| `output/SRVCABLE_brief.md` | Generated artifact | Final brief from the final run | Complete |
| `output/run_audit.json` | Generated audit | Source triage, claims, arithmetic, and validation evidence | Complete |
| `decisions/` | Records | One Markdown record per material design decision | Complete |

## Planning-only files versus runtime files

Planning and audit files are not runtime inputs:

- `EXECUTION_PLAN.md`
- `FILE_MANIFEST.md`
- `CHANGELOG.md`
- `DECISIONS.md`
- `TRAPS.md`
- `TEST_PLAN.md`
- `TEST_LOG.md`

The runtime reads only the selected document folder, `system_prompt.md`, and configuration supplied through the CLI/environment. `research_pack/` contains exactly the eight evidence documents.
