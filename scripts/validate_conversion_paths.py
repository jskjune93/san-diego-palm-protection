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
        "data-inquiry-fallback",
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
    else:
        if CONFIG.get("endpoint"):
            errors.append("email fallback must not retain an endpoint")
        if CONFIG.get("verified_lead_conversion_enabled"):
            errors.append("verified-lead conversion cannot be enabled for email fallback")
        if CONFIG.get("direct_uploads_enabled"):
            errors.append("direct uploads cannot be enabled for email fallback")

    public_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore")
                            for path in [*ROOT.glob("*.html"), ROOT / "site-assets" / "site.js"])
    if "Nothing has been delivered yet" not in public_text:
        errors.append("email fallback does not state that the inquiry has not been delivered")
    if "verified-lead" in public_text or "lead-submitted" in public_text:
        errors.append("public output contains an unverified submitted-lead conversion")

    if errors:
        print("Conversion path validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Conversion path validation passed: homeowner and organization paths present; email fallback remains explicit and cannot fire a verified-lead event.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
