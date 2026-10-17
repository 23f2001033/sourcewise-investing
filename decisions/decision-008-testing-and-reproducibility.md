# D008 — Iterative, Honest, Reproducible Testing

## Status

Accepted

## Decision

Run at least three real iterations and record the actual observed weakness, root cause, change, and result. Keep the input pack, as-of date, command, and model configuration explicit.

## Context

The assignment specifically asks what went wrong across runs. A fabricated test history would undermine the submission.

## Alternatives considered

- One final run: does not demonstrate iteration.
- Invent a typical failure progression: dishonest and unverifiable.
- Record every debugging detail: too noisy; retain only material behavior changes.

## Consequences

The implementation should make each run easy to repeat and should update `TEST_LOG.md` only after execution.

## Validation

`TEST_LOG.md` must contain at least three completed entries tied to real commands and output behavior.
