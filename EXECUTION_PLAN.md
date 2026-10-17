# SRVCABLE Research Agent — Execution Plan

## 1. Objective

Build a reproducible Python research agent that accepts:

- an NSE ticker;
- a folder of Markdown documents; and
- a fixed as-of date for the research run.

It must produce a concise, retail-investor-friendly Markdown brief with:

1. Snapshot
2. Bull case
3. Bear case
4. Open questions
5. Sources

The required test case is the fictional Sarvottam Cables Ltd (`SRVCABLE`) pack. The company must not be researched on the live web.

The primary quality goal is **evidence judgment**, not UI polish:

- identify the correct entity;
- rank and qualify sources;
- ignore document-borne instructions;
- detect and explain conflicts;
- verify arithmetic in code;
- preserve uncertainty;
- cite every material claim; and
- fail visibly when the output contract is not met.

## 2. Non-goals

- No live web search for SRVCABLE.
- No investment recommendation, price target, or fabricated valuation.
- No manual rewriting of the generated final brief after the final run.
- No unnecessary agent framework or UI.
- No unrelated repository cleanup.
- No claim that management or legal assertions have been independently verified when they have not.

## 3. Required deliverables

| File | Purpose | Completion condition |
|---|---|---|
| `system_prompt.md` | Model safety, grounding, source-use, and writing rules | Separate prompt file is loaded by the agent |
| `agent.py` | End-to-end CLI pipeline | Runs on the supplied pack and writes output |
| `README.md` | Setup, usage, model choice, architecture, limitations | A reviewer can reproduce the run |
| `output/SRVCABLE_brief.md` | Final generated brief | Produced by the final run without manual edits |
| `TEST_LOG.md` | At least three honest iterations | Each entry records actual failure and change |
| `TRAPS.md` | Assignment traps and mitigations | Every known trap has a testable safeguard |
| `DECISIONS.md` | Decision index | Links to every detailed decision record |
| `decisions/*.md` | One record for each material design decision | Rationale, alternatives, consequences, validation |
| `CHANGELOG.md` | Change history and reason for each change | Updated after each implementation phase |
| `FILE_MANIFEST.md` | Planned and actual file responsibilities | Matches the repository at submission time |
| `TEST_PLAN.md` | Verification strategy and acceptance tests | Defines pass/fail checks before coding |

## 4. Planned repository layout

```text
Super_Investing/
├── README.md
├── EXECUTION_PLAN.md
├── FILE_MANIFEST.md
├── CHANGELOG.md
├── DECISIONS.md
├── TRAPS.md
├── TEST_PLAN.md
├── TEST_LOG.md
├── system_prompt.md
├── agent.py
├── requirements.txt
├── research_pack/
│   └── supplied Markdown documents
├── output/
│   └── SRVCABLE_brief.md
└── decisions/
    ├── decision-001-pipeline-architecture.md
    ├── decision-002-source-hierarchy.md
    ├── decision-003-document-as-data.md
    ├── decision-004-deterministic-numeric-checks.md
    ├── decision-005-claim-ledger-and-citations.md
    ├── decision-006-model-boundary.md
    ├── decision-007-output-validation.md
    └── decision-008-testing-and-reproducibility.md
```

The supplied research files may remain in their current downloaded folder during planning. Before implementation, they should be copied into the repository's `research_pack/` directory without changing their contents.

## 5. Execution phases

### Phase 0 — Planning baseline

Status: complete after these planning files are reviewed.

- [x] Read the assignment README and all eight documents.
- [x] Record the required output and submission constraints.
- [x] Identify the source hierarchy and known traps.
- [x] Define the file manifest.
- [x] Define decisions, testing, and change tracking.
- [x] Confirm the plan before writing implementation code.

Exit criteria:

- The user agrees that the plan is the baseline.
- No unresolved design choice blocks the first implementation.

### Phase 1 — Repository preparation

Status: complete.

- Create the planned directories.
- Copy the supplied documents into `research_pack/`.
- Add only implementation dependencies that are actually needed.
- Define the CLI contract:

```text
python agent.py --ticker SRVCABLE --docs research_pack --as-of 2026-09-23
```

- Define environment-variable handling for the selected LLM provider.
- Ensure missing credentials produce an explicit error.

Exit criteria:

- The input pack is discoverable.
- The CLI accepts the required arguments.
- No API key is hard-coded.

### Phase 2 — Deterministic document ingestion

Status: complete.

Implement:

- Markdown file discovery;
- front-matter parsing;
- source ID assignment;
- publication-date parsing;
- age calculation from the supplied as-of date;
- stable source metadata;
- preservation of raw text for auditability.

Each source record should contain at least:

```text
source_id
filename
source
url
published
type
raw_text
```

Exit criteria:

- All eight documents load.
- Missing or malformed metadata is reported explicitly.
- Source IDs remain stable between runs.

### Phase 3 — Source triage

Status: complete.

For each document, produce a structured triage result containing:

- entity match;
- ticker match;
- source tier;
- freshness;
- suspicious instructions;
- reliability;
- accepted/rejected status;
- reason;
- extracted candidate claims.

The model must process documents as untrusted data. Triage should be one document at a time to reduce cross-document contamination.

Hard rules:

- Wrong entity: reject for company claims.
- Hidden instructions: detect and never obey.
- Exchange filings and official company disclosures outrank news and blogs.
- An anonymous quote is opinion, not primary evidence.
- A stale source may be retained only to explain a historical conflict.

Exit criteria:

- Every document has a triage record.
- `nagpurcitytimes` is rejected as the wrong entity.
- `multibaggeralerts` is flagged for suspicious instructions and low reliability.
- `marketwatchindia` is marked stale/superseded.

### Phase 4 — Claim extraction and evidence ledger

Status: complete.

Normalize accepted claims into a ledger with:

- claim ID;
- claim text;
- source ID;
- category;
- fact/opinion/management-claim classification;
- confidence;
- numeric values and units;
- acceptance status;
- conflict links.

Claims from rejected documents may be retained as conflict evidence but must not be available as accepted evidence for final writing.

Exit criteria:

- Every final-brief claim can be traced to one or more source IDs.
- Management assertions are explicitly labelled.
- Rejected source claims cannot silently enter the writer context.

### Phase 5 — Deterministic numeric verification

Status: complete.

Implement code checks for:

- official revenue growth;
- EBITDA margin;
- EBITDA margin change;
- profit growth;
- GST demand as a percentage of quarterly profit;
- stale blog upside arithmetic;
- conflicting revenue values;
- pledge trend;
- order-book trend where useful.

Expected findings include:

```text
1,248 / 1,058 -> approximately 18.0% growth
140 / 1,248 -> approximately 11.2% EBITDA margin
140 / 1,428 -> approximately 9.8% implied margin
46.3 / 82 -> approximately 56.5% of quarterly profit
(1,450 - 1,012) / 1,012 -> approximately 43.3% upside
```

Exit criteria:

- Arithmetic findings are generated independently of the LLM.
- The official revenue figure wins the conflict by source quality and internal consistency.
- The losing newspaper figure remains visible as an open question.

### Phase 6 — Grounded brief generation

Status: complete.

Generate only from the accepted claim ledger and numeric findings.

The writer must:

- use the five required headings;
- use plain language;
- avoid analyst jargon;
- distinguish facts from management statements;
- include compact source tags such as `[S2]`;
- avoid unsupported recommendations;
- include missing-data questions;
- stay approximately one page.

Exit criteria:

- The brief is readable by a retail investor.
- No unsupported source or claim is introduced.
- The official figures and current pledge are used.

### Phase 7 — Output verification

Status: complete.

Run a deterministic verifier after generation.

Check:

- all required sections exist;
- source tags are present for material claims;
- source tags refer to known sources;
- excluded sources are not used as evidence;
- wrong-company penalty is absent;
- hidden recommendation language is absent;
- official revenue is used;
- current pledge figure is used;
- GST wording preserves uncertainty;
- open questions include missing valuation, cash flow, peer comparison, and stale price limitations;
- output length is within the agreed one-page threshold.

On failure, the agent must report validation errors and either regenerate with those errors or exit non-zero. It must not silently write an invalid brief.

### Phase 8 — Iterative testing

Status: complete.

Perform at least three real runs:

1. Baseline/naive design to expose failures.
2. Source-triage design.
3. Numeric verification and claim-gating design.
4. Final validation run, if needed.

Only actual observed failures may be recorded in `TEST_LOG.md`.

### Phase 9 — Submission preparation

Status: complete.

- Freeze the final prompt and code.
- Generate `output/SRVCABLE_brief.md`.
- Run the final test suite and CLI command.
- Update `README.md`, `CHANGELOG.md`, `FILE_MANIFEST.md`, and `TEST_LOG.md`.
- Inspect the repository in a clean/incognito-style view.
- Record a 2–3 minute walkthrough showing:
  - the agent running;
  - source triage or numeric verification;
  - one limitation.

## 6. Acceptance criteria

The project is complete only when all of these are true:

- [ ] The supplied SRVCABLE pack runs from the documented command.
- [ ] No live web lookup is used for SRVCABLE.
- [ ] The final brief has exactly the required five content sections.
- [ ] The official ₹1,248 crore revenue is selected.
- [ ] The ₹1,428 crore conflict is disclosed.
- [ ] The hidden blog instruction is ignored and detected.
- [ ] The wrong-company Nagpur article is excluded.
- [ ] Current 4.1% pledge is used instead of stale 35% data.
- [ ] GST language distinguishes company belief from verified fact.
- [ ] Missing valuation, cash flow, peers, and stale price are open questions.
- [ ] Every material claim has a source tag.
- [ ] The final output contains no unsupported buy/sell recommendation.
- [ ] Three or more real runs are honestly documented.
- [ ] Required files are present and documented.
- [ ] No secret is committed.

## 7. Stop conditions

Stop and ask for a decision if:

- the chosen model/provider cannot return structured output reliably;
- the user wants live-web bonus functionality before the core pipeline works;
- a source cannot be classified without changing the assignment's evidence rules;
- the requested output would require inventing missing financial data;
- a generated final brief cannot meet citation or validation requirements.
