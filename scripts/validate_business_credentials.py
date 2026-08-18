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
    r"\btreatment services (?:remain )?unavailable",
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
    credentials = public_credentials()
    exact = credentials["exact_status"]
    summary = credentials["service_summary"]
    label = credentials["status_label"]
    individual_license = credentials["individual_license"]
    business_license = credentials["business_license"]
    category = credentials["category"]
    insurance = credentials["insurance"]
    licensing_statement = credentials["licensing_statement"]
    errors: list[str] = []

    for path in PUBLIC_HTML:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(ROOT).as_posix()
        lowered = text.lower()
        for pattern in OBSOLETE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{rel}: obsolete qualification/licensing language matches {pattern}")
        for phrase in DRIFTED_STATUS:
            if phrase.lower() in lowered:
                errors.append(f"{rel}: drifted credential description remains: {phrase}")
        for phrase in UNSUPPORTED_CLAIMS:
            if phrase.lower() in lowered:
                errors.append(f"{rel}: unsupported credential or insurance claim: {phrase}")
        for match in re.finditer(r"(?:QAL|Qualified Applicator License)(?:\s+No\.|\s*#)?\s*175295", text, re.I):
            nearby = text[max(0, match.start() - 300):match.end() + 300]
            if not re.search(r"Pest Control Business License(?:\s+No\.|\s*#)?\s*47756", nearby, re.I):
                errors.append(f"{rel}: QAL listing is not paired with Pest Control Business License No. 47756")

    for relative in PRIMARY_PAGES:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8-sig")
        if START not in text or STYLE_LINK not in text:
            errors.append(f"{relative}: centralized credential component is missing")
        if relative == "index.html":
            required_values = (summary, business_license, individual_license, category, insurance, "John Krause, Owner", label)
        elif relative == "about.html":
            required_values = (business_license, individual_license, category, insurance, "John Krause", summary)
        else:
            required_values = (summary, label, business_license, individual_license, category, insurance)
        if any(value not in text for value in required_values):
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

    all_public = "\n".join(path.read_text(encoding="utf-8-sig") for path in PUBLIC_HTML)
    qal_numbers = re.findall(r"(?:QAL|Qualified Applicator License)(?:\s+No\.|\s*#)?\s*(\d{4,})", all_public, re.I)
    if not qal_numbers or set(qal_numbers) != {"175295"}:
        errors.append(f"public QAL number set must be exactly 175295; found {sorted(set(qal_numbers))}")
    business_license_numbers = re.findall(r"Pest Control Business License(?:\s+No\.|\s*#)?\s*(\d{4,})", all_public, re.I)
    if not business_license_numbers or set(business_license_numbers) != {"47756"}:
        errors.append(f"public Pest Control Business License number set must be exactly 47756; found {sorted(set(business_license_numbers))}")
    if "Category B — Landscape Maintenance" not in all_public:
        errors.append("public Category B wording is not Landscape Maintenance")
    if licensing_statement not in all_public:
        errors.append("authoritative sitewide licensing statement is missing from public HTML")
    if insurance in all_public and status.get("insurance", {}).get("insured") is not True:
        errors.append("insured wording appears without authoritative insurance support")

    if status.get("pest_control_business_license_issued_and_active") is not True:
        errors.append("Pest Control Business License must remain active")
    if status.get("qal_issued_and_active") is not True:
        errors.append("DPR QAL Category B must remain active")
    if status.get("financial_responsibility_active") is not True:
        errors.append("Financial responsibility must remain active")

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
