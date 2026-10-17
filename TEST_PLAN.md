# Test Plan

This plan is written before implementation. It defines what must be verified rather than what we hope the agent will do.

## 1. Static and input tests

| Test | Expected result |
|---|---|
| Discover the supplied research pack | Exactly eight Markdown source files are found |
| Parse all front matter | Source, URL, date, and type are available for each file |
| Calculate age as of `2026-09-23` | Ages are deterministic and non-negative |
| Stable source ordering | Same folder produces same source IDs |
| Missing metadata fixture | Agent reports the problem explicitly |
| Missing folder | Agent exits non-zero with a useful error |

## 2. Triage tests

| Test | Expected result |
|---|---|
| Official press release | Entity match, high tier, accepted |
| NSE announcement | Entity match, highest tier, accepted |
| Shareholding filing | Entity match, highest tier, accepted |
| Earnings call | Entity match, official transcript, accepted with management statements labelled |
| Business Daily | Entity match, lower tier, conflict evidence |
| MultibaggerAlerts | Low tier, suspicious instructions flagged |
| Nagpur City Times | Entity mismatch, rejected |
| Market Watch India | Stale, superseded by current filing |

## 3. Numeric tests

| Check | Expected result |
|---|---|
| Official revenue growth | Approximately 18.0% |
| Official EBITDA margin | Approximately 11.2% |
| Margin decline | 170 basis points |
| Profit growth | Approximately 5.9% |
| Business Daily implied margin | Approximately 9.8% |
| GST demand/profit | Approximately 56.5% |
| Blog price upside | Approximately 43.3%, not 60% |
| Pledge trend | 11.5% to 4.1%, declining |

## 4. Generation tests

The final brief must:

- contain Snapshot, Bull case, Bear case, Open questions, and Sources;
- use plain-language explanations;
- cite every material claim;
- select official revenue of ₹1,248 crore;
- mention the conflicting ₹1,428 crore report under Open questions;
- include order book, exports, data-centre opportunity, Bharuch capacity, and pledge decline where space permits;
- include margin pressure, pass-through lag, receivables, GST demand, and Bharuch leverage;
- distinguish company statements from independently established facts;
- state that valuation, cash flow, peers, and a current price are missing;
- omit the wrong-company fine;
- omit unsupported buy/sell language and target price.

## 5. Output validation tests

The verifier must reject:

- missing required sections;
- unknown source tags;
- uncited material bullets;
- rejected source used as evidence;
- current-price wording attached to the stale ₹1,012 value;
- “STRONG BUY”, “60% upside”, or equivalent unsupported recommendation;
- GST written as a settled liability with no uncertainty;
- output exceeding the configured one-page threshold.

## 6. Iteration tests

At least three actual runs are required:

1. Baseline behavior.
2. Triage-improved behavior.
3. Numeric-verification and output-validation behavior.

The observed behavior, not an invented narrative, goes into `TEST_LOG.md`.
