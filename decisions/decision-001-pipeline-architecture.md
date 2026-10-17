# D001 — Deterministic Python Pipeline with Bounded LLM Steps

## Status

Accepted

## Decision

Use a plain Python command-line pipeline. Use the LLM for document triage, claim extraction support, and final prose generation. Keep ingestion, source ranking, arithmetic, claim gating, and output validation deterministic.

## Context

The assignment permits an agent framework, but the evaluation emphasizes how the agent thinks. A visible pipeline makes source judgment and verification easier to inspect and explain than a broad autonomous loop.

## Alternatives considered

- LangGraph or another agent framework: more orchestration overhead than this task needs.
- One large summarization prompt: likely to repeat traps and makes validation difficult.
- Fully deterministic template: safer but less flexible and less representative of an AI research agent.

## Consequences

Positive:

- Reproducible control flow.
- Clear audit points.
- Easier targeted tests.
- Small dependency surface.

Negative:

- More explicit glue code.
- The model does not autonomously discover new tools or sources.

## Validation

The final CLI must execute the complete flow and expose failures rather than silently falling back.
