#!/usr/bin/env python3
"""Focused homepage deduplication and About-page safeguards."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from business_credentials import load_business_status, public_credentials


ROOT = Path(__file__).resolve().parents[1]


def visible_text(html: str) -> str:
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.I | re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def main() -> int:
    status = load_business_status()
    public = public_credentials()
    homepage_html = (ROOT / "index.html").read_text(encoding="utf-8")
    about_html = (ROOT / "about.html").read_text(encoding="utf-8")
    home = visible_text(homepage_html)
    about = visible_text(about_html)
    errors: list[str] = []

    limits = {
        public["individual_license"]: 2,
        public["category"]: 2,
        "Insured": 3,
        public["exact_status"]: 1,
    }
    for phrase, maximum in limits.items():
        count = home.lower().count(phrase.lower())
        if count > maximum:
            errors.append(f"homepage repeats {phrase!r} {count} times; maximum is {maximum}")
    descriptive_qualified = len(re.findall(r"\bQualified\b(?!\s+Applicator\s+License)", home))
    if descriptive_qualified > 1:
        errors.append(f"homepage repeats descriptive 'Qualified' {descriptive_qualified} times; maximum is 1")
    if home.count(public["exact_status"]) != 1:
        errors.append("homepage must contain exactly one authoritative service statement")
    if "Available now:" not in home:
        errors.append("homepage lacks the plain-language service availability label")
    for scoped_fragment in (
        "I assess the concern, explain the options",
        "The work is shaped by the palms, the property, and the decisions",
        "John Krause personally assesses and photographs mature palms from Old Escondido.",
    ):
        if scoped_fragment not in home:
            errors.append(f"homepage expected positive replacement is missing: {scoped_fragment}")
    if 'href="./about.html"' not in homepage_html or "About John and SDPP" not in home:
        errors.append("homepage owner section does not link to About")
    if homepage_html.lower().count("<h1") != 1:
        errors.append("homepage must contain exactly one H1")
    if "<title>Mature Palm Protection in North County San Diego | SDPP</title>" not in homepage_html:
        errors.append("homepage title changed unexpectedly")

    for phrase in (
        "John Krause",
        public["individual_license"],
        public["category"],
        public["insurance"],
        public["exact_status"],
        "based in Old Escondido",
        "I have my B.S. from the University of Minnesota in environmental science and am also a Navy veteran.",
        "South American palm weevil activity and palm loss on my own Old Escondido property",
    ):
        if phrase.lower() not in about.lower():
            errors.append(f"About page lacks approved fact or boundary: {phrase}")
    if about_html.lower().count("<h1") != 1:
        errors.append("About page must contain exactly one H1")
    for anchor in ("#homeowner-inquiry", "#organization-inquiry"):
        if anchor not in about_html:
            errors.append(f"About page lacks inquiry link: {anchor}")
    for photo_asset in (
        "john-krause-palm-640.webp",
        "john-krause-palm-960.webp",
        "john-krause-palm-1280.webp",
        "john-krause-palm-960.jpg",
    ):
        if photo_asset not in about_html:
            errors.append(f"About page lacks responsive John photo asset: {photo_asset}")
    if "about-john-profile" not in about_html:
        errors.append("About page lacks the dedicated John profile layout")
    for unsupported in (
        "ISA Certified Arborist",
        "TRAQ",
        "veteran-owned certified",
        "municipal appointment",
        "I guarantee outcomes",
        "Pest Control Business License No. 175295",
    ):
        if unsupported.lower() in about.lower():
            errors.append(f"About page contains unsupported claim: {unsupported}")
    if status["pesticide_services_enabled"] is not True or status["owner_activation_approved"] is not True:
        errors.append("authoritative treatment status changed unexpectedly")

    if errors:
        print("HOMEPAGE_ABOUT_VALIDATION_FAILED")
        for error in errors:
            print(f" - {error}")
        return 1
    print("HOMEPAGE_ABOUT_VALIDATION_OK")
    print("homepage_full_qal<=2 homepage_full_category<=2 homepage_insured<=3 homepage_service_statement=1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
