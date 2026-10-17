# D006 — Narrow, Provider-Configurable Model Boundary

## Status

Accepted

## Decision

Keep the LLM provider and model configurable through environment variables or a small configuration section. Do not hard-code credentials or make the core pipeline depend on one vendor-specific framework.

## Context

The assignment allows free-tier models and asks for an explanation of model choice. The core quality should come from the evidence workflow, not an opaque vendor lock-in.

## Alternatives considered

- Hard-code one provider: difficult for reviewers to reproduce.
- Add multiple providers immediately: unnecessary complexity before the core works.
- Use no model: does not demonstrate the requested AI agent behavior.

## Consequences

The implementation must define a clear provider interface and explicit errors for missing credentials or malformed model responses.

## Validation

README documentation must state the selected model, why it was selected, and what configuration is required.
