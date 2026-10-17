# D007 — Validate Before Declaring Success

## Status

Accepted

## Decision

Run deterministic validation on the generated Markdown. A failed validation must be visible and must not be converted into a successful-looking output.

## Context

A fluent model response can still omit citations, use rejected evidence, repeat an injection, or violate the one-page structure.

## Alternatives considered

- Human inspection only: not reproducible.
- Trust the model's self-check: same failure source as generation.
- Silently patch the output: violates the requirement to report manual editing honestly.

## Consequences

The verifier must define section, citation, source-leakage, language, freshness, and length checks.

## Validation

Deliberately invalid fixtures should fail the verifier. The final run must pass all acceptance checks.
