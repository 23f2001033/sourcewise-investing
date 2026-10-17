# Test Log

This file contains observations from actual executions. The first three entries reflect the implementation iterations that occurred while building the pipeline.

## Required entry format

### Run N — YYYY-MM-DD HH:MM IST

- **Command/configuration:**
- **Design version:**
- **Observed output:**
- **What failed or was weak:**
- **Root cause:**
- **Change made:**
- **Regression checks:**
- **Result:**

## Planned minimum runs

### Run 1 — 2026-10-17 02:17 IST

- **Command/configuration:** `python agent.py --ticker SRVCABLE --docs research_pack --as-of 2026-09-23`
- **Design version:** Initial deterministic pipeline.
- **Observed output:** The command completed, but the earnings-call source (`S2`) was marked rejected because its body did not repeat the ticker/company name.
- **What failed or was weak:** Copper pass-through, receivables, and Bharuch leverage evidence were absent from the generated brief.
- **Root cause:** Entity matching required a company-name/ticker match and did not recognize official company IR context in the source metadata.
- **Change made:** Entity matching now accepts explicit company IR context while retaining hard rejection for the Cable Network entity.
- **Regression checks:** Re-ran the same command and confirmed `S2` is accepted and its claims appear.
- **Result:** Fixed.

### Run 2 — 2026-10-17 02:18 IST

- **Command/configuration:** Same command after the entity-triage fix.
- **Design version:** Source triage with official IR recognition and deterministic numeric checks.
- **Observed output:** The brief included official revenue, source conflict, current pledge, and earnings-call risks. The blog remained listed as “accepted with warning,” and two fallback open-question citations needed tightening.
- **What failed or was weak:** The source list overstated the usability of the stock-tips blog, and the fallback renderer used an incorrect source tag for the copper pass-through question.
- **Root cause:** The source-status policy and fallback citation strings were not fully aligned with the evidence policy.
- **Change made:** Rejected blog evidence explicitly; corrected source tags and cited the missing-data question.
- **Regression checks:** Checked that the blog has no accepted claims and that all material generated bullets have source tags.
- **Result:** Fixed.

### Run 3 — 2026-10-17 02:19 IST

- **Command/configuration:** Same command after source-policy and citation fixes.
- **Design version:** Final offline renderer with triage, numeric verification, claim gating, and output validation.
- **Observed output:** Brief generated successfully with all five sections. It selected ₹1,248 crore, disclosed the ₹1,428 crore conflict, omitted the ₹8 lakh wrong-company fine, ignored the hidden recommendation, and included the current 4.1% pledge.
- **What failed or was weak:** PowerShell's console encoding displayed the rupee symbol incorrectly when printed through a default code page; the file itself was UTF-8.
- **Root cause:** Console output encoding, not the generated file.
- **Change made:** No product change; final verification reads the file as UTF-8 rather than relying on the console renderer.
- **Regression checks:** UTF-8 file read, Python compilation, audit assertions, and output validation all pass.
- **Result:** Passed.

### Final verification

- **Command/configuration:** `python agent.py --ticker SRVCABLE --docs research_pack --as-of 2026-09-23`
- **Result:** Passed; final artifact is `output/SRVCABLE_brief.md` and audit data is `output/run_audit.json`.
