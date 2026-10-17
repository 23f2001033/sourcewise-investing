# SRVCABLE Evidence-Grounded Research Agent

This project implements the Super Investing AI Innovator Part B assignment for the fictional company Sarvottam Cables Ltd (`SRVCABLE`).

The agent does not search the web. It reads the supplied Markdown research pack, triages sources, rejects the wrong entity, detects suspicious document instructions, performs deterministic arithmetic checks, builds an accepted-claim ledger, and writes a one-page Markdown brief.

## Run

Requires Python 3.10 or newer. The reproducible path uses only the standard library.

```powershell
python agent.py --ticker SRVCABLE --docs research_pack --as-of 2026-09-23
```

The command writes:

- `output/SRVCABLE_brief.md`
- `output/run_audit.json`

## Optional model

By default the agent uses a deterministic grounded renderer, so it can run without an API key. To use an OpenAI-compatible Chat Completions endpoint for prose generation, set:

```powershell
$env:LLM_BASE_URL = "https://your-provider.example/v1"
$env:LLM_API_KEY = "replace-locally"
$env:LLM_MODEL = "your-model"
python agent.py --ticker SRVCABLE --docs research_pack --as-of 2026-09-23
```

The model is deliberately bounded: it receives only the accepted claim ledger, conflict evidence, numeric findings, and source metadata. It never receives instructions from a document as instructions. The deterministic path remains the fallback and the validation layer always runs.

## Why this design

The assignment says source judgment matters more than UI. The pipeline therefore separates:

1. deterministic ingestion and metadata parsing;
2. source triage and entity matching;
3. claim classification;
4. Python numeric verification;
5. grounded brief generation; and
6. output validation.

The official press release wins the ₹1,428 crore versus ₹1,248 crore conflict because it is a higher-tier source and its figures recompute consistently. The lower-tier figure is still disclosed as a conflict.

## Important safeguards

- Document content is treated as untrusted data.
- The hidden MultibaggerAlerts HTML instruction is detected but never followed.
- The Nagpur Cable Network article is rejected as the wrong entity.
- The current 4.1% pledge figure supersedes stale historical pledge reporting.
- The GST “no material impact” language is attributed to the company.
- Missing valuation, cash flow, peer comparison, and current price data are reported as open questions.

See [TRAPS.md](TRAPS.md), [TEST_PLAN.md](TEST_PLAN.md), [DECISIONS.md](DECISIONS.md), and [EXECUTION_PLAN.md](EXECUTION_PLAN.md) for the reasoning and acceptance criteria.

## Submission notes

The final generated brief is in `output/SRVCABLE_brief.md`. `TEST_LOG.md` must be updated only with actual runs. The recording should show the CLI execution, one source/numeric decision, and one limitation.
