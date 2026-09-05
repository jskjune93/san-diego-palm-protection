#!/usr/bin/env python3
"""Validate the two-path offering, public credentials, and outreach PDF."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
POSITIONING = ROOT / "site-config" / "positioning.json"
PDF = ROOT / "SDPP-Commercial-Palm-Stewardship.pdf"
PDF_SHA256 = "013e0600c1859b4cdf196e59a1c6c7b56c388feaf447af92b1670ebd0f526885"

QAL = "California Qualified Applicator License No. 175295"
BUSINESS_LICENSE = "California Pest Control Business License No. 47756"
CATEGORY = "Category B — Landscape Maintenance"
OBSOLETE_SERVICE_STATUS = (
    r"not currently offering pesticide",
    r"cannot treat",
    r"treatment (?:is|remains) unavailable",
    r"pesticide applications? (?:are|is) not offered",
    r"discuss treatment with another licensed provider",
    r"regulated work must be discussed with an appropriately licensed provider",
    r"documentation, monitoring, reporting, sourcing, and coordination are available now",
    r"pre[- ]license",
)


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    errors: list[str] = []
    config = json.loads(POSITIONING.read_text(encoding="utf-8"))
    if config.get("engagement_paths") != ["Palm Portfolio Baseline", "Annual Palm Stewardship Program"]:
        errors.append("canonical configuration must contain exactly the two approved engagement paths")
    expected_pillars = ["Stewardship & Palm Health", "Protection & Treatment", "Documentation & Portfolio Management", "Response, Removal & Renewal"]
    if config.get("service_pillars") != expected_pillars:
        errors.append("canonical configuration must retain the four approved capability pillars in order")
    if config.get("public_credentials") != f"{BUSINESS_LICENSE} · {QAL} · {CATEGORY} · Insured":
        errors.append("canonical public credential line is incomplete")

    if not DIST.exists():
        errors.append("dist is missing")
        public_html: list[Path] = []
    else:
        public_html = sorted(DIST.rglob("*.html"))
    for path in public_html:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(DIST).as_posix()
        for pattern in OBSOLETE_SERVICE_STATUS:
            if re.search(pattern, text, re.I):
                errors.append(f"{rel}: obsolete service-status language matched {pattern}")
        if BUSINESS_LICENSE not in text or QAL not in text or CATEGORY not in text or "Insured" not in text:
            errors.append(f"{rel}: public credentials are incomplete")
        if re.search(r"QAL.{0,30}(?:authorizes?|licenses?) (?:SDPP|the business)", text, re.I):
            errors.append(f"{rel}: QAL is represented as business authorization")

    services = (DIST / "palm-records-monitoring-verification.html").read_text(encoding="utf-8-sig") if (DIST / "palm-records-monitoring-verification.html").exists() else ""
    paths = re.findall(r'data-engagement-path="([^"]+)"', services)
    if paths != ["palm-portfolio-baseline", "annual-palm-stewardship-program"]:
        errors.append(f"consolidated services page must expose exactly two ordered engagement paths; found {paths}")
    for phrase in ("Protect valuable palms from SAPW", "Treatment is what SDPP does", "Preventive SAPW treatment", "Coordinating removals", "Coordinating replacements", "Palm Portfolio Baseline", "Annual Palm Stewardship Program", "View Commercial Overview", "Download Commercial Overview"):
        if phrase not in services:
            errors.append(f"consolidated services page missing commercial hierarchy concept: {phrase}")
    if re.search(r"(?:bronze|silver|gold) (?:package|plan|tier)", services, re.I):
        errors.append("consolidated services page contains an artificial package tier")

    if not PDF.exists():
        errors.append("canonical commercial outreach PDF is missing")
    else:
        if hashlib.sha256(PDF.read_bytes()).hexdigest() != PDF_SHA256:
            errors.append("canonical commercial outreach PDF hash has changed")
        text = compact(pdf_text(PDF))
        for phrase in ("Palm Portfolio Baseline", "Annual Palm Stewardship Program", "Licensed preventive protection and treatment within scope", "Our goal is to preserve the value of your mature landscape assets.", "Request a Property Walkthrough", "47756", "175295", "Category B", "Insured"):
            if phrase.lower() not in text.lower():
                errors.append(f"commercial PDF missing {phrase}")
        for pattern in OBSOLETE_SERVICE_STATUS:
            if re.search(pattern, text, re.I):
                errors.append(f"commercial PDF contains obsolete service-status language: {pattern}")

    for path in sorted(ROOT.glob("*.pdf")):
        text = compact(pdf_text(path))
        for pattern in OBSOLETE_SERVICE_STATUS:
            if re.search(pattern, text, re.I):
                errors.append(f"{path.name}: public PDF contains obsolete service-status language: {pattern}")

    print("COMMERCIAL_OFFERING_VALIDATION_OK" if not errors else "COMMERCIAL_OFFERING_VALIDATION_FAILED")
    print(f"public_html_checked={len(public_html)} public_pdfs_checked={len(list(ROOT.glob('*.pdf')))}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
