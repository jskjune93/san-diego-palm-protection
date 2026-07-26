from __future__ import annotations

from pathlib import Path
import json
import re
import sys

from business_credentials import load_business_status, public_credentials
from sync_business_credentials import CONTACT_START, PRIMARY_PAGES, START, STYLE_LINK

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_HTML = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html"))

OBSOLETE_PATTERNS = (
    r"\bpending licen[cs]",
    r"\bawaiting licen[cs]",
    r"\bawaiting qualification",
    r"\bstill awaiting qualification",
    r"\btreatment services are not currently offered",
    r"\bpassed (?:the )?(?:qualification )?(?:exam|examination)\b",
    r"\bprequalification\b",
)
DRIFTED_STATUS = (
    "California licensed · DPR Category B qualified · Insured",
    "Licensed · Qualified · Insured",
)
UNSUPPORTED_CLAIMS = (
    "SDPP is an ISA Certified Arborist",
    "SDPP is a licensed tree contractor",
    "SDPP certifies contractor performance",
    "insurance guarantees",
    "guaranteed protection",
)


def main() -> int:
    status = load_business_status()
    prelicense = status["mode"] == "prelicense"
    credentials = public_credentials()
    exact = credentials["exact_status"]
    summary = credentials["service_summary"]
    label = credentials["status_label"]
    errors: list[str] = []

    for path in PUBLIC_HTML:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(ROOT).as_posix()
        lowered = text.lower()
        for pattern in OBSOLETE_PATTERNS:
            if not prelicense and re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{rel}: obsolete qualification/licensing language matches {pattern}")
        for phrase in DRIFTED_STATUS:
            if phrase.lower() in lowered:
                errors.append(f"{rel}: drifted credential description remains: {phrase}")
        for phrase in UNSUPPORTED_CLAIMS:
            if phrase.lower() in lowered:
                errors.append(f"{rel}: unsupported credential or insurance claim: {phrase}")

    for relative in PRIMARY_PAGES:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8-sig")
        if START not in text or STYLE_LINK not in text:
            errors.append(f"{relative}: centralized credential component is missing")
        if summary not in text or exact not in text or label not in text:
            errors.append(f"{relative}: qualified and insured wording is incomplete")

    for relative in ("index.html", "palm-records-monitoring-verification.html", "report-a-palm.html"):
        text = (ROOT / relative).read_text(encoding="utf-8-sig")
        head = text.split("</head>", 1)[0]
        if label.lower() not in head.lower():
            errors.append(f"{relative}: metadata/structured data lacks qualified and insured status")

    for relative in ("palm-records-monitoring-verification.html", "report-a-palm.html"):
        text = (ROOT / relative).read_text(encoding="utf-8-sig")
        if CONTACT_START not in text or text.index(CONTACT_START) > text.index("<form"):
            errors.append(f"{relative}: inquiry area lacks a credential block before the form")

    journal_pages = sorted((ROOT / "palm-journal").glob("**/*.html"))
    for path in journal_pages:
        if exact not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"{path.relative_to(ROOT).as_posix()}: generated page footer lacks exact credential status")

    if prelicense:
        prohibited = re.compile(
            r"\b(?:california\s+licensed|licensed,\s*qualified|qualified\s+and\s+insured|"
            r"qal\s*#?\d+|qualified applicator license.{0,30}active|financial responsibility.{0,20}active)\b",
            re.I,
        )
        for path in PUBLIC_HTML:
            text = path.read_text(encoding="utf-8-sig")
            if prohibited.search(text):
                errors.append(f"{path.relative_to(ROOT).as_posix()}: active credential language appears in prelicense mode")
        if status.get("pest_control_business_license_issued_and_active") is not False:
            errors.append("Prelicense premise requires inactive Pest Control Business License")
        if status.get("pesticide_services_enabled") is not False:
            errors.append("Prelicense premise requires pesticide services disabled")
    else:
        if status.get("pest_control_business_license_issued_and_active") is not True:
            errors.append("Pest Control Business License is not active; licensed public wording must be removed")
        if status.get("qal_issued_and_active") is not True:
            errors.append("DPR QAL Category B is not active; qualified public wording must be removed")
        if status.get("financial_responsibility_active") is not True:
            errors.append("Financial responsibility is not active; insured public wording must be removed")

    print("BUSINESS_CREDENTIAL_VALIDATION_OK" if not errors else "BUSINESS_CREDENTIAL_VALIDATION_FAILED")
    print(f"public_html_checked={len(PUBLIC_HTML)}")
    print(f"primary_pages_checked={len(PRIMARY_PAGES)}")
    print(f"generated_pages_checked={len(journal_pages)}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
