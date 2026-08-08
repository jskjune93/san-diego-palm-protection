#!/usr/bin/env python3
"""Stable semantic guard for SDPP's public portfolio-stewardship position."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
POSITIONING = ROOT / "site-config" / "positioning.json"

CRITICAL = {
    "index.html": (
        "owner-led stewardship for valuable palm portfolios",
        "SDPP preserves valuable palm and landscape assets so they can continue contributing to the appearance, identity, use, and long-term value of the property.",
        "Stewardship &amp; Palm Health",
        "Documentation &amp; Portfolio Management",
        "Response, Removal &amp; Renewal",
        "request a property walkthrough",
    ),
    "managed-property-palm-services.html": (
        "palm portfolio stewardship for managed properties",
        "what sdpp takes responsibility for",
        "palm asset register",
        "baseline condition record",
        "recurring stewardship plan",
        "dated visit and treatment records",
        "material-change alerts",
        "periodic portfolio summary",
        "licensed treatment",
        "Treatment is one tool. Stewardship is the ongoing model.",
        "does not need to replace the landscape team",
    ),
    "palm-records-monitoring-verification.html": (
        "palm assessment, monitoring, and management services",
        "request a property walkthrough",
        "treatment",
    ),
}

FORBIDDEN = (
    r"aguilar plant care",
    r"\b(?:industry-leading|tree doctor|complete tree care|all plant health|sapw-free|eradication)\b",
    r"\bSDPP (?:is|employs) (?:an? )?(?:ISA )?(?:certified )?arborist\b",
    r"\bSDPP (?:is|employs) (?:an? )?(?:licensed )?PCA\b",
    r"\b(?:SDPP|we|our treatment|this treatment) guarantees? (?:prevention|protection|survival|recovery|results?|outcomes?)\b",
)


def main() -> int:
    errors: list[str] = []
    config = json.loads(POSITIONING.read_text(encoding="utf-8"))
    for key in ("primary_market", "secondary_market", "core_product", "canonical_position", "in_house_capability", "differentiators", "service_pillars", "prohibited_drift"):
        if not config.get(key):
            errors.append(f"canonical positioning source missing {key}")
    if config.get("engagement_paths") != ["Palm Portfolio Baseline", "Annual Palm Stewardship Program"]:
        errors.append("commercial offer must contain exactly the two approved engagement paths")
    expected_pillars = ["Stewardship & Palm Health", "Protection & Treatment", "Documentation & Portfolio Management", "Response, Removal & Renewal"]
    if config.get("service_pillars") != expected_pillars:
        errors.append("canonical configuration must contain the four approved capability pillars in order")
    if config.get("canonical_position") != "SDPP preserves valuable palm and landscape assets so they can continue contributing to the appearance, identity, use, and long-term value of the property.":
        errors.append("canonical positioning statement has drifted")

    if not DIST.exists():
        errors.append("dist is missing; run the production build first")
    else:
        public = sorted(DIST.rglob("*.html"))
        corpus = "\n".join(path.read_text(encoding="utf-8-sig") for path in public)
        for pattern in FORBIDDEN:
            if re.search(pattern, corpus, re.I):
                errors.append(f"public positioning violates {pattern}")
        for relative, concepts in CRITICAL.items():
            path = DIST / relative
            if not path.exists():
                errors.append(f"critical positioning page missing: {relative}")
                continue
            text = path.read_text(encoding="utf-8-sig").lower()
            for concept in concepts:
                if concept.lower() not in text:
                    errors.append(f"{relative}: missing positioning concept {concept}")
            for credential in ("175295", "Category B — Landscape Maintenance", "Insured"):
                if credential.lower() not in text:
                    errors.append(f"{relative}: missing credential {credential}")

    print("POSITIONING_VALIDATION_OK" if not errors else "POSITIONING_VALIDATION_FAILED")
    print(f"critical_pages_checked={len(CRITICAL)}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
