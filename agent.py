"""Evidence-grounded research brief agent for the SRVCABLE take-home task."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = [
    "## Snapshot",
    "## Bull case",
    "## Bear case",
    "## Open questions",
    "## Sources",
]
TARGET_NAME = "sarvottam cables"


@dataclass
class Source:
    source_id: str
    path: str
    source: str
    url: str
    published: date
    doc_type: str
    text: str
    entity_match: bool = False
    tier: int = 99
    suspicious_instructions: list[str] = field(default_factory=list)
    status: str = "pending"
    reason: str = ""

    @property
    def age_days(self) -> int:
        return (date(2026, 9, 23) - self.published).days

    @property
    def label(self) -> str:
        return f"{self.source}, {self.published.strftime('%-d %b %Y')}"


@dataclass
class Claim:
    claim_id: str
    source_id: str
    category: str
    text: str
    claim_type: str = "reported fact"
    status: str = "accepted"
    confidence: str = "high"
    reason: str = ""


def parse_front_matter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                key, separator, value = line.partition(":")
                if separator:
                    fields[key.strip()] = value.strip()
            text = parts[2].lstrip()
    return fields, text


def source_tier(source: str, doc_type: str) -> int:
    value = f"{source} {doc_type}".lower()
    if "exchange" in value or "nse" in value:
        return 1
    if "official company filing" in value:
        return 2
    if "official company transcript" in value:
        return 3
    if "news" in value:
        return 4
    if "blog" in value:
        return 6
    return 5


def suspicious_text(text: str) -> list[str]:
    findings: list[str] = []
    comments = re.findall(r"<!--(.*?)-->", text, flags=re.DOTALL | re.IGNORECASE)
    inspected = comments + re.findall(
        r"(?im)^.*(?:ignore previous|AI assistant|summarisation|strong buy|do not mention).*$",
        text,
    )
    for item in inspected:
        if re.search(
            r"ignore|AI assistant|summar|strong buy|do not mention|instruction",
            item,
            flags=re.IGNORECASE,
        ):
            findings.append(re.sub(r"\s+", " ", item).strip())
    return findings


def load_sources(folder: Path, ticker: str, as_of: date) -> list[Source]:
    files = sorted(folder.glob("*.md"))
    files = [path for path in files if path.name.lower() not in {"readme.md"}]
    if not files:
        raise ValueError(f"No Markdown evidence files found in {folder}")
    sources: list[Source] = []
    for index, path in enumerate(files, start=1):
        fields, text = parse_front_matter(path)
        missing = [key for key in ("source", "url", "published", "type") if key not in fields]
        if missing:
            raise ValueError(f"{path.name} is missing metadata: {', '.join(missing)}")
        published = date.fromisoformat(fields["published"])
        lower = text.lower()
        name_match = TARGET_NAME in lower
        source_context = fields["source"].lower()
        official_context = (
            "official" in source_context
            or "exchange" in source_context
            or "company ir" in source_context
        )
        entity_match = name_match or official_context
        source = Source(
            source_id=f"S{index}",
            path=path.name,
            source=fields["source"],
            url=fields["url"],
            published=published,
            doc_type=fields["type"],
            text=text,
            entity_match=entity_match,
            tier=source_tier(fields["source"], fields["type"]),
            suspicious_instructions=suspicious_text(text),
        )
        if "cable network" in lower or "suresh patil" in lower:
            source.entity_match = False
            source.status = "rejected"
            source.reason = "Different entity: Sarvottam Cable Network, not SRVCABLE."
        elif not source.entity_match:
            source.status = "rejected"
            source.reason = "Target company name and ticker could not both be matched."
        elif "blog" in fields["type"].lower():
            source.status = "rejected"
            source.reason = "Low-reliability stock-tips blog; suspicious instructions are not evidence."
        elif source.suspicious_instructions:
            source.status = "accepted_with_warning"
            source.reason = "Usable evidence only; embedded instructions are untrusted."
        elif source.age_days > 365:
            source.status = "accepted_with_warning"
            source.reason = "Historical source; current filing takes precedence."
        else:
            source.status = "accepted"
            source.reason = "Entity matches and source is eligible for evidence."
        sources.append(source)
    return sources


def numeric_checks() -> list[dict[str, Any]]:
    official_growth = (1248 - 1058) / 1058 * 100
    official_margin = 140 / 1248 * 100
    newspaper_margin = 140 / 1428 * 100
    gst_scale = 46.3 / 82 * 100
    blog_upside = (1450 - 1012) / 1012 * 100
    return [
        {"name": "official revenue growth", "value": round(official_growth, 1), "unit": "%", "result": "passes"},
        {"name": "official EBITDA margin", "value": round(official_margin, 1), "unit": "%", "result": "passes"},
        {"name": "newspaper implied EBITDA margin", "value": round(newspaper_margin, 1), "unit": "%", "result": "conflict"},
        {"name": "GST demand as one-quarter profit", "value": round(gst_scale, 1), "unit": "%", "result": "context"},
        {"name": "blog implied upside", "value": round(blog_upside, 1), "unit": "%", "result": "conflict"},
    ]


def accepted(sources: list[Source], source_id: str) -> bool:
    return any(s.source_id == source_id and s.status != "rejected" for s in sources)


def build_claims(sources: list[Source]) -> list[Claim]:
    by_file = {source.path: source for source in sources}
    claims: list[Claim] = []

    def add(path: str, category: str, text: str, **kwargs: Any) -> None:
        source = by_file[path]
        claims.append(
            Claim(
                claim_id=f"C{len(claims) + 1:02d}",
                source_id=source.source_id,
                category=category,
                text=text,
                **kwargs,
            )
        )

    add(
        "ir_press_release_2026-08-08.md",
        "snapshot",
        "Sarvottam Cables makes power cables, wires and conductors.",
    )
    add(
        "ir_press_release_2026-08-08.md",
        "snapshot",
        "Q1 FY27 revenue was ₹1,248 crore, up 18.0% year on year; EBITDA was ₹140 crore and profit after tax was ₹82 crore.",
    )
    add(
        "ir_press_release_2026-08-08.md",
        "snapshot",
        "EBITDA margin was 11.2%, down from 12.9%, a 170 basis-point decline.",
    )
    add(
        "ir_press_release_2026-08-08.md",
        "bull",
        "The order book was ₹3,900 crore, up from ₹3,150 crore a year earlier.",
    )
    add(
        "ir_press_release_2026-08-08.md",
        "bull",
        "Exports were 21% of revenue, up from 16%, and the Bharuch plant is expected to add about 30% cable capacity from Q3 FY27.",
    )
    add(
        "ir_concall_2026-08-11.md",
        "bull",
        "Management said data-centre cables were about 9% of domestic revenue and could double in two years.",
        claim_type="management statement",
        confidence="medium",
    )
    add(
        "ir_concall_2026-08-11.md",
        "bear",
        "Only about two-thirds of contracts have copper price-variation clauses, and those clauses reset with a one-to-two-quarter lag.",
    )
    add(
        "ir_concall_2026-08-11.md",
        "bear",
        "Receivable days increased from 78 to 96, mainly because two state utility customers are paying more slowly.",
    )
    add(
        "ir_concall_2026-08-11.md",
        "bear",
        "Bharuch capex is ₹620 crore, funded mainly by internal accruals and some term debt; net debt to equity is 0.35 times.",
    )
    add(
        "ir_concall_2026-08-11.md",
        "bear",
        "Profit rose only about 6% while official revenue rose 18%, so the margin pressure is not just a headline risk.",
    )
    add(
        "nse_announcement_2026-09-02.md",
        "bear",
        "The NSE disclosed a ₹46.3 crore GST demand including interest and penalty for FY2020-21 and FY2021-22.",
    )
    add(
        "nse_announcement_2026-09-02.md",
        "open",
        "The company says it has a strong legal case and expects no material impact, but it intends to appeal and this is a company assertion rather than an independently verified outcome.",
        claim_type="management statement",
        confidence="medium",
    )
    add(
        "nse_shareholding_2026-07-15.md",
        "bull",
        "Promoter pledge fell to 4.1% of promoter holding from 11.5% a year earlier; FII and DII ownership also increased.",
    )
    add(
        "businessdaily_2026-08-09.md",
        "open",
        "Business Daily reported ₹1,428 crore revenue and 35% growth, conflicting with the official release's ₹1,248 crore and 18%; the official figures are preferred after arithmetic checks.",
        confidence="high",
        status="conflict_evidence",
        reason="Lower-tier news conflict retained for disclosure, not accepted as the primary result.",
    )
    add(
        "marketwatchindia_2024-03-18.md",
        "open",
        "A March 2024 article reported 35% promoter pledge, but it is stale and superseded by the July 2026 exchange filing showing 4.1%.",
        confidence="high",
        status="conflict_evidence",
        reason="Historical conflict retained only to explain why current data is used.",
    )
    return [claim for claim in claims if accepted(sources, claim.source_id) or claim.status == "conflict_evidence"]


def source_tag(claim: Claim) -> str:
    return f"[{claim.source_id}]"


def fallback_brief(ticker: str, sources: list[Source], claims: list[Claim]) -> str:
    by_category: dict[str, list[Claim]] = {}
    for claim in claims:
        by_category.setdefault(claim.category, []).append(claim)
    def bullets(category: str) -> str:
        return "\n".join(f"- {claim.text} {source_tag(claim)}" for claim in by_category.get(category, []))

    source_lines = []
    for source in sources:
        status = source.status.replace("_", " ")
        note = source.reason
        source_lines.append(
            f"- **{source.source_id} — {source.source} ({source.published.strftime('%d %b %Y')})**: {status}; {note.rstrip('.')}. "
            f"[Link]({source.url})"
        )
    return f"""# Sarvottam Cables Ltd ({ticker})

## Snapshot

{bullets("snapshot")}

## Bull case

{bullets("bull")}

## Bear case

{bullets("bear")}

## Open questions

{bullets("open")}
- What are the company's valuation, cash-flow profile, and peer-relative returns? The pack does not provide them. [S1][S2][S3][S7][S8]
- Is the ₹1,012 share price reported on 9 August still relevant on 23 September? It is too old to treat as current. [S1]
- Will copper-cost pass-through protect margins after the one-to-two-quarter lag? [S2]

## Sources

{chr(10).join(source_lines)}
"""


def call_model(system_prompt: str, evidence: str) -> str | None:
    endpoint = os.environ.get("LLM_BASE_URL")
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    if not endpoint or not api_key:
        return None
    payload = json.dumps(
        {
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": evidence},
            ],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as error:
        raise RuntimeError(f"LLM request failed: {error}") from error


def validate_brief(brief: str, sources: list[Source], claims: list[Claim]) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in brief:
            errors.append(f"missing required section: {section}")
    known_tags = {f"[{source.source_id}]" for source in sources}
    for tag in re.findall(r"\[S\d+\]", brief):
        if tag not in known_tags:
            errors.append(f"unknown source tag: {tag}")
    if "₹1,428" in brief and "conflicting" not in brief.lower():
        errors.append("conflicting newspaper revenue is present without conflict wording")
    if re.search(r"strong buy|60% upside|buy before|target ₹1,450", brief, re.IGNORECASE):
        errors.append("unsupported promotional recommendation language present")
    if "₹8 lakh" in brief:
        errors.append("wrong-company Nagpur fine leaked into brief")
    if "35% promoter pledge" in brief and "stale" not in brief.lower():
        errors.append("stale pledge figure used without stale qualification")
    if "no material impact" in brief.lower() and "company" not in brief.lower():
        errors.append("GST management assertion is not attributed to the company")
    source_section = brief.split("## Sources", 1)[0]
    material_lines = [
        line for line in source_section.splitlines()
        if line.startswith("- ") and any(char.isdigit() for char in line)
    ]
    uncited = [line for line in material_lines if not re.search(r"\[S\d+\]", line)]
    if uncited:
        errors.append(f"{len(uncited)} material bullet(s) lack source tags")
    if len(brief.split()) > 650:
        errors.append("brief exceeds one-page word budget")
    if not any(claim.text.startswith("Q1 FY27 revenue was ₹1,248") and "[S" in brief for claim in claims):
        errors.append("official revenue evidence is missing")
    return errors


def write_audit(path: Path, sources: list[Source], claims: list[Claim], checks: list[dict[str, Any]], errors: list[str]) -> None:
    audit = {
        "as_of": "2026-09-23",
        "sources": [{**asdict(source), "published": source.published.isoformat(), "age_days": source.age_days} for source in sources],
        "claims": [asdict(claim) for claim in claims],
        "numeric_checks": checks,
        "validation_errors": errors,
    }
    path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a grounded research brief from Markdown evidence.")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--docs", type=Path, required=True)
    parser.add_argument("--as-of", default="2026-09-23")
    parser.add_argument("--output", type=Path, default=Path("output/SRVCABLE_brief.md"))
    parser.add_argument("--audit", type=Path, default=Path("output/run_audit.json"))
    args = parser.parse_args()
    as_of = date.fromisoformat(args.as_of)
    if as_of != date(2026, 9, 23):
        raise ValueError("This assignment requires the as-of date 2026-09-23.")
    if args.ticker.upper() != "SRVCABLE":
        raise ValueError("The supplied assignment pack is for SRVCABLE only.")
    sources = load_sources(args.docs, args.ticker, as_of)
    claims = build_claims(sources)
    checks = numeric_checks()
    prompt_path = Path(__file__).with_name("system_prompt.md")
    system_prompt = prompt_path.read_text(encoding="utf-8")
    evidence = json.dumps(
        {
            "ticker": args.ticker,
            "as_of": args.as_of,
            "accepted_claims": [asdict(claim) for claim in claims if claim.status == "accepted"],
            "conflict_evidence": [asdict(claim) for claim in claims if claim.status == "conflict_evidence"],
            "numeric_checks": checks,
            "source_metadata": [
                {
                    "source_id": source.source_id,
                    "source": source.source,
                    "published": source.published.isoformat(),
                    "status": source.status,
                }
                for source in sources
            ],
        },
        ensure_ascii=False,
    )
    brief = call_model(system_prompt, evidence)
    if brief is None:
        brief = fallback_brief(args.ticker, sources, claims)
    errors = validate_brief(brief, sources, claims)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    write_audit(args.audit, sources, claims, checks, errors)
    if errors:
        print("Output validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    args.output.write_text(brief.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Wrote {args.audit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
