# D005 — Accepted Claim Ledger and Source Tags

## Status

Accepted

## Decision

Build a structured accepted-claim ledger and make it the only evidence context available to the final writer. Use stable source tags in the brief.

## Context

The required output says every claim must trace back to a source. Directly giving all documents to the writer would allow rejected material to leak into the result.

## Alternatives considered

- Cite documents only in a bibliography: weak claim-to-source traceability.
- Let the model cite from memory: unreliable.
- Put all documents in the final prompt: makes source exclusion difficult.

## Consequences

The pipeline needs claim IDs, source IDs, claim types, acceptance status, and conflict relationships.

## Validation

Every material generated claim must have a known source tag. Rejected sources may be listed as excluded evidence only when clearly labelled.
