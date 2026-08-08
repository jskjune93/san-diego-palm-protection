#!/usr/bin/env python3
"""Validate the two-path offering, QAL-only public credentials, and outreach PDF."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
POSITIONING = ROOT / "site-config" / "positioning.json"
PDF = ROOT / "SDPP-Commercial-Palm-Stewardship.pdf"

QAL = "California Qualified Applicator License No. 175295"
CATEGORY = "Category B — Landscape Maintenance"
PUBLIC_BUSINESS_LICENSE = re.compile(r"Pest Control Business License|\bPCBL?\b", re.I)
PRELICENSE = (
    r"not currently offering pesticide",
    r"cannot treat",
    r"treatment (?:is|remains) unavailable",
    r"pesticide applications? (?:are|is) not offered",
    r"discuss treatment with another licensed provider",
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
    if config.get("public_credentials") != f"{QAL} · {CATEGORY} · Insured":
        errors.append("canonical public credential line is not QAL-only")
    if "business licens" not in config.get("private_operational_credentials", "").lower():
        errors.append("private operational business-license state is not preserved")

    if not DIST.exists():
        errors.append("dist is missing")
        public_html: list[Path] = []
    else:
        public_html = sorted(DIST.rglob("*.html"))
    for path in public_html:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(DIST).as_posix()
        if PUBLIC_BUSINESS_LICENSE.search(text):
            errors.append(f"{rel}: public business-license credential remains")
        for pattern in PRELICENSE:
            if re.search(pattern, text, re.I):
                errors.append(f"{rel}: pre-license language matched {pattern}")
        if QAL not in text or CATEGORY not in text or "Insured" not in text:
            errors.append(f"{rel}: QAL-only public credentials are incomplete")
        if re.search(r"QAL.{0,30}(?:authorizes?|licenses?) (?:SDPP|the business)", text, re.I):
            errors.append(f"{rel}: QAL is represented as business authorization")

    managed = (DIST / "managed-property-palm-services.html").read_text(encoding="utf-8-sig") if (DIST / "managed-property-palm-services.html").exists() else ""
    paths = re.findall(r'data-engagement-path="([^"]+)"', managed)
    if paths != ["palm-portfolio-baseline", "annual-palm-stewardship-program"]:
        errors.append(f"managed page must expose exactly two ordered engagement paths; found {paths}")
    for phrase in ("Standardize the stewardship system; customize the property scope.", "Stewardship &amp; Palm Health", "Protection &amp; Treatment", "Documentation &amp; Portfolio Management", "Response, Removal &amp; Renewal"):
        if phrase not in managed:
            errors.append(f"managed page missing commercial hierarchy concept: {phrase}")
    if re.search(r"(?:bronze|silver|gold) (?:package|plan|tier)", managed, re.I):
        errors.append("managed page contains an artificial package tier")

    if not PDF.exists():
        errors.append("canonical commercial outreach PDF is missing")
    else:
        text = compact(pdf_text(PDF))
        for phrase in ("Palm Portfolio Baseline", "Annual Palm Stewardship Program", "Licensed preventive protection and treatment within scope", "Our goal is to preserve the value of your mature landscape assets.", "Request a Property Walkthrough", "175295", "Category B - Landscape Maintenance", "Insured"):
            if phrase.lower() not in text.lower():
                errors.append(f"commercial PDF missing {phrase}")
        if PUBLIC_BUSINESS_LICENSE.search(text):
            errors.append("commercial PDF displays the business license")
        for pattern in PRELICENSE:
            if re.search(pattern, text, re.I):
                errors.append(f"commercial PDF contains pre-license language: {pattern}")

    for path in sorted(ROOT.glob("*.pdf")):
        text = compact(pdf_text(path))
        if PUBLIC_BUSINESS_LICENSE.search(text):
            errors.append(f"{path.name}: public PDF displays the business license")
        for pattern in PRELICENSE:
            if re.search(pattern, text, re.I):
                errors.append(f"{path.name}: public PDF contains pre-license language: {pattern}")

    print("COMMERCIAL_OFFERING_VALIDATION_OK" if not errors else "COMMERCIAL_OFFERING_VALIDATION_FAILED")
    print(f"public_html_checked={len(public_html)} public_pdfs_checked={len(list(ROOT.glob('*.pdf')))}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
