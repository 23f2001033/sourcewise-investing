# D002 — Explicit Source Hierarchy and Entity Gate

## Status

Accepted

## Decision

Rank sources explicitly and reject wrong-entity documents before their claims can be accepted.

Default order:

1. NSE/exchange filing
2. Official company filing or IR material
3. Official company transcript
4. Established financial news
5. Attributed analyst opinion
6. Stock-tip blog

Wrong entity is a hard exclusion.

## Context

The pack intentionally includes a conflict, stale evidence, a stock-tips blog, and an article about a different company.

## Alternatives considered

- Treat every source equally: fails the assignment's central test.
- Let the model choose without a declared hierarchy: difficult to audit and prone to recency bias.
- Exclude every non-official source: loses useful conflict evidence.

## Consequences

Lower-tier sources can help identify conflicts, but they cannot override stronger evidence without an explicit review.

## Validation

The Nagpur article must be rejected. Business Daily must remain visible as conflicting evidence but not override the official release.
