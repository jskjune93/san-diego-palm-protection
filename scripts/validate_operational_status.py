from __future__ import annotations

from pathlib import Path
import json
import re
import sys

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STATUS = ROOT / "site-config" / "business_status.json"

FORBIDDEN = (
    r"not currently offering pesticide",
    r"pesticide applications? (?:are|is) not currently",
    r"pesticide applications? (?:are|is) not offered",
    r"appropriately licensed treatment provider",
    r"appropriately licensed-provider referral",
    r"regulated work must be discussed with",
    r"referral[- ]only treatment",
    r"production prelicense status",
    r"(?:sdpp|san diego palm protection) (?:cannot|can not|does not|doesn't) (?:provide )?(?:pesticide )?treat(?:ment)?",
    r"treatment must be (?:provided|performed) by (?:a )?third[- ]party",
    r"licensed applicator referral",
    r"awaiting (?:its |our )?(?:license|licence|insurance)",
    r"does not establish business[- ]level pesticide authorization",
    r"current service scope.{0,100}(?:exclude|without|does not include|unavailable).{0,40}treatment",
    r"(?:only|solely) (?:provides?|offers?) (?:documentation|monitoring|reporting|sourcing|coordination)",
)

CRITICAL_PAGES = (
    "index.html",
    "managed-property-palm-services.html",
    "palm-records-monitoring-verification.html",
    "palm-stewardship-plans.html",
    "south-american-palm-weevil-treatment-san-diego.html",
)

AUTHORITATIVE_LICENSE_STATEMENT = (
    "San Diego Palm Protection — California Pest Control Business License active. "
    "John Krause, California Qualified Applicator License No. 175295, "
    "Category B — Landscape Maintenance. Insured."
)

SOURCE_FILES = (
    ROOT / "scripts" / "build_core_pages.py",
    ROOT / "scripts" / "build_journal.py",
    ROOT / "scripts" / "business_credentials.py",
    ROOT / "scripts" / "site_components.py",
    ROOT / "site-config" / "business_status.json",
    ROOT / "journal-data" / "journal_entries.json",
)


def main() -> int:
    errors: list[str] = []
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    if status.get("mode") != "commercial" or status.get("pesticide_services_enabled") is not True:
        errors.append("authoritative business status is not operational commercial mode")
    scope = status.get("operating_scope") or {}
    for key in ("primary_growth_path", "residential_path", "regulated_work_boundary", "excluded_direct_work", "outcome_boundary"):
        if not scope.get(key):
            errors.append(f"authoritative operating scope missing {key}")

    source_paths = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html")) + list(SOURCE_FILES)
    for path in source_paths:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(ROOT).as_posix()
        for pattern in FORBIDDEN:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{rel}: obsolete service-status source language matched {pattern}")

    if not DIST.exists():
        errors.append("dist is missing; run the production build first")
    else:
        html_paths = sorted(DIST.rglob("*.html"))
        for path in html_paths:
            text = path.read_text(encoding="utf-8-sig")
            rel = path.relative_to(DIST).as_posix()
            for pattern in FORBIDDEN:
                if re.search(pattern, text, re.IGNORECASE):
                    errors.append(f"{rel}: obsolete service-status language matched {pattern}")
        required_shared = (
            "California Pest Control Business License active",
            "California Qualified Applicator License No. 175295",
            "Category B — Landscape Maintenance",
            "Insured",
        )
        for path in html_paths:
            text = path.read_text(encoding="utf-8-sig")
            rel = path.relative_to(DIST).as_posix()
            if AUTHORITATIVE_LICENSE_STATEMENT not in text:
                errors.append(f"{rel}: authoritative sitewide licensing statement is missing")
            head = text.split("</head>", 1)[0]
            if 'name="business-credentials"' not in head or "California Pest Control Business License active" not in head:
                errors.append(f"{rel}: licensing metadata is missing or stale")
            if 'type="application/ld+json"' not in head or "California Pest Control Business License active" not in head:
                errors.append(f"{rel}: licensing structured data is missing or stale")
        for relative in CRITICAL_PAGES:
            path = DIST / relative
            if not path.exists():
                errors.append(f"missing critical production page: {relative}")
                continue
            text = path.read_text(encoding="utf-8-sig")
            for phrase in required_shared:
                if phrase not in text:
                    errors.append(f"{relative}: missing {phrase}")
            for concept in ("Assessment", "Monitoring", "Treatment"):
                if concept.lower() not in text.lower():
                    errors.append(f"{relative}: missing operational concept {concept}")

        homepage = (DIST / "index.html").read_text(encoding="utf-8-sig") if (DIST / "index.html").exists() else ""
        managed = (DIST / "managed-property-palm-services.html").read_text(encoding="utf-8-sig") if (DIST / "managed-property-palm-services.html").exists() else ""
        records = (DIST / "palm-records-monitoring-verification.html").read_text(encoding="utf-8-sig") if (DIST / "palm-records-monitoring-verification.html").exists() else ""
        for phrase in ("Owner-Led Palm Stewardship", "Palm stewardship, treatment, and preservation for valuable properties.", "Mature palm care", "Stewardship &amp; Palm Health", "Documentation &amp; Portfolio Management", "Response, Removal &amp; Renewal", "Request a Property Walkthrough", "Residential &amp; Estate Properties", "treatment and work history", "budgeting support"):
            if phrase not in homepage:
                errors.append(f"homepage missing commercial/residential pathway: {phrase}")
        treatment_page = (DIST / "south-american-palm-weevil-treatment-san-diego.html").read_text(encoding="utf-8-sig") if (DIST / "south-american-palm-weevil-treatment-san-diego.html").exists() else ""
        for phrase in ("South American Palm Weevil Treatment in San Diego", "Preventive treatment is available when appropriate", "California Pest Control Business License active"):
            if phrase not in treatment_page:
                errors.append(f"SAPW treatment page missing active service language: {phrase}")
        recurring = (DIST / "quarterly-palm-care-san-diego.html").read_text(encoding="utf-8-sig") if (DIST / "quarterly-palm-care-san-diego.html").exists() else ""
        for phrase in ("Palm stewardship and preservation, visit after visit.", "fertilization", "preventive protection", "treatment", "Managed-property stewardship"):
            if phrase not in recurring:
                errors.append(f"recurring-stewardship page missing current service language: {phrase}")
        for phrase in ("Commercial palm care and management for valuable properties.", "Palm Portfolio Baseline", "Protection and Monitoring", "Palm Stewardship", "fertilization", "irrigation guidance", "existing landscapers", "certificate of insurance", "W-9"):
            if phrase not in managed:
                errors.append(f"managed-property page missing service pathway: {phrase}")
        for field in ("known_palm_species", "existing_contractor", "desired_service", "preferred_contact"):
            if f'name="{field}"' not in records:
                errors.append(f"managed-property inquiry missing field: {field}")

    for path in sorted(ROOT.glob("*.pdf")):
        try:
            text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        except Exception as exc:
            errors.append(f"{path.name}: PDF text audit failed: {exc}")
            continue
        for pattern in FORBIDDEN:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{path.name}: obsolete service-status language matched {pattern}")

    print("OPERATIONAL_STATUS_OK" if not errors else "OPERATIONAL_STATUS_FAILED")
    print(f"critical_pages_checked={len(CRITICAL_PAGES)}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
