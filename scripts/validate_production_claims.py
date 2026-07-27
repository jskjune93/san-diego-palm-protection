from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STATUS = ROOT / "site-config" / "business_status.json"
NOTICE = "SDPP is not currently offering pesticide applications."

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
    if status.get("mode") != "prelicense":
        errors.append("authoritative status is not prelicense")
    if status.get("pest_control_business_license_issued_and_active") is not False:
        errors.append("Pest Control Business License must be inactive")
    if status.get("pesticide_services_enabled") is not False:
        errors.append("pesticide services must be disabled")
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

    for path in html_paths:
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(DIST).as_posix()
        if ACTIVE_CREDENTIAL.search(text):
            errors.append(f"{rel}: active credential claim in production output")
        claim_scan = text.replace(NOTICE, "").replace(scope_note, "")
        if COMMERCIAL_TREATMENT.search(claim_scan):
            errors.append(f"{rel}: current regulated-treatment offer or CTA in production output")
        if PRIVATE_TOKENS.search(text):
            errors.append(f"{rel}: private Karen material in production output")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S | re.I):
            lowered = block.lower()
            if '"@type": "service"' in lowered or '"servicestatus"' in lowered:
                errors.append(f"{rel}: prelicense structured data implies an active service")

    for relative in ("palm-stewardship-plans.html", "south-american-palm-weevil-treatment-san-diego.html"):
        path = DIST / relative
        if not path.is_file() or NOTICE not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"{relative}: required prelicense pesticide notice is missing")

    print("PRODUCTION_CLAIMS_OK" if not errors else "PRODUCTION_CLAIMS_FAILED")
    print(f"production_html_checked={len(html_paths)}")
    print("mode=prelicense")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
