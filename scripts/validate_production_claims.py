from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STATUS = ROOT / "site-config" / "business_status.json"
REQUIRED_SERVICE = "protection and treatment services"

ACTIVE_CREDENTIAL = re.compile(
    r"\b(?:california\s+licensed|qualified\s+and\s+insured|licensed,\s*qualified|"
    r"pest control business license(?:\s+no\.?|\s*#)?\s*175295|"
    r"qal(?:\s+no\.?|\s*#)?\s*(?!175295\b)\d+|financial responsibility.{0,20}active)\b",
    re.I,
)
COMMERCIAL_TREATMENT = re.compile(
    r"\b(?:request|book|schedule|quote|deposit|reserve|sign up for).{0,80}"
    r"\b(?:pesticide|treatment|application)\b|"
    r"\b(?:we|sdpp|san diego palm protection)\b.{0,80}"
    r"\b(?:apply|perform|provide|offer).{0,30}\b(?:pesticide|regulated treatment|treatment)\b",
    re.I,
)
PRIVATE_TOKENS = re.compile(r"\b(?:Karen\s+Oberlander|art_13328317f6d64b86912b19f2b39143eb)\b", re.I)


def main() -> int:
    errors: list[str] = []
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    scope_note = status.get("public_credentials", {}).get("scope_note", "")
    if status.get("mode") != "commercial":
        errors.append("authoritative status is not commercial")
    if status.get("pesticide_services_enabled") is not True:
        errors.append("protection and treatment services must be enabled")
    if status.get("qal_issued_and_active") is not True:
        errors.append("verified individual QAL must be active")
    if status.get("individual_qualification", {}).get("license_number") != "175295":
        errors.append("verified individual QAL number must be 175295")
    if status.get("insurance", {}).get("insured") is not True:
        errors.append("verified insured status must be active")

    manifest_path = DIST / "production-manifest.json"
    if not manifest_path.is_file():
        errors.append("production manifest is missing")
        html_paths: list[Path] = []
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        html_paths = sorted(DIST / item for item in manifest.get("files", []) if item.endswith(".html"))
        hashes = manifest.get("sha256_by_file", {})
        for relative in manifest.get("files", []):
            path = DIST / relative
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            if hashes.get(relative) != actual:
                errors.append(f"{relative}: production manifest hash mismatch")
        approved = manifest.get("approved_release_items", {}).get("palm-journal/when-sapw-became-local.html", {})
        if approved.get("approval_fingerprint") != "2204939026f694390763cebe4c2250c9964bd92f6597296fef66b874074fcbba":
            errors.append("SAPW article approval fingerprint is missing or stale")
        if approved.get("observation_dates") != ["2026-06-15", "2026-06-16", "2026-06-26"]:
            errors.append("SAPW observation dates changed")
        expected_publication_date = os.environ.get("SDPP_EXPECTED_PUBLICATION_DATE")
        if expected_publication_date and approved.get("publication_date") != expected_publication_date:
            errors.append(
                f"SAPW publication date {approved.get('publication_date')} does not match deployment date "
                f"{expected_publication_date}"
            )

    for path in html_paths:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(DIST).as_posix()
        if REQUIRED_SERVICE not in text.lower() and "BUSINESS_CREDENTIALS:START" in text:
            errors.append(f"{rel}: current service statement is missing")
        if PRIVATE_TOKENS.search(text):
            errors.append(f"{rel}: private Karen material in production output")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S | re.I):
            lowered = block.lower()

    print("PRODUCTION_CLAIMS_OK" if not errors else "PRODUCTION_CLAIMS_FAILED")
    print(f"production_html_checked={len(html_paths)}")
    print("mode=commercial")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
