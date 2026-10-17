# D004 — Deterministic Numeric and Conflict Checks

## Status

Accepted

## Decision

Use Python for arithmetic and conflict checks. The model may explain the findings, but it does not own the calculations.

## Context

The pack contains revenue, margin, growth, price, pledge, and GST figures that can be checked mechanically.

## Alternatives considered

- Trust model arithmetic: vulnerable to the deliberate 35% versus 18% conflict.
- Use an external calculator service: unnecessary dependency and weaker reproducibility.
- Manual calculations in the prompt: less auditable.

## Consequences

The numeric checker must normalize units and define rounding tolerances. It also becomes part of the evidence ledger.

## Validation

The checker must report approximately 18.0% official revenue growth, 11.2% official EBITDA margin, 9.8% implied newspaper margin, 56.5% GST-to-profit scale, and 43.3% blog upside.
