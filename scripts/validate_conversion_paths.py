from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site-config" / "inquiry.json").read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    pages = {
        "home": (ROOT / "index.html").read_text(encoding="utf-8"),
        "services": (ROOT / "palm-records-monitoring-verification.html").read_text(encoding="utf-8"),
    }
    required_home = (
        "Single palms and small groups welcome",
        "homeowner-inquiry-initiation",
        "organization-inquiry-initiation",
        "Scope and pricing",
    )
    required_services = (
        'id="homeowner-inquiry"',
        'id="organization-inquiry"',
        "data-inquiry-direct",
    )
    for phrase in required_home:
        if phrase not in pages["home"]:
            errors.append(f"homepage missing conversion requirement: {phrase}")
    for phrase in required_services:
        if phrase not in pages["services"]:
            errors.append(f"services page missing inquiry requirement: {phrase}")

    if CONFIG["submitted_form_enabled"]:
        if not CONFIG.get("endpoint"):
            errors.append("submitted form enabled without endpoint")
        if CONFIG["submission_mode"] != "first_party":
            errors.append("submitted form enabled outside first_party mode")
        if not CONFIG.get("verified_lead_conversion_enabled"):
            errors.append("first-party delivery must enable only the server-confirmed verified-lead boundary")
        if CONFIG.get("direct_uploads_enabled"):
            errors.append("direct uploads must remain disabled")
    else:
        if CONFIG.get("endpoint"):
            errors.append("email fallback must not retain an endpoint")
        if CONFIG.get("verified_lead_conversion_enabled"):
            errors.append("verified-lead conversion cannot be enabled for email fallback")
        if CONFIG.get("direct_uploads_enabled"):
            errors.append("direct uploads cannot be enabled for email fallback")

    public_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore")
                            for path in [*ROOT.glob("*.html"), ROOT / "site-assets" / "site.js"])
    required_direct = (
        "/api/inquiry",
        "homeowner-inquiry-delivered",
        "organization-inquiry-delivered",
        "Delivery could not be confirmed",
    )
    for phrase in required_direct:
        if phrase not in public_text and phrase not in (ROOT / "api" / "inquiry.mjs").read_text(encoding="utf-8"):
            errors.append(f"direct inquiry implementation missing: {phrase}")

    if errors:
        print("Conversion path validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Conversion path validation passed: direct homeowner and organization delivery is first-party; email fallback remains available; verified-lead events require confirmed provider delivery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
