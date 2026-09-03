from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

from business_credentials import (
    footer_line,
    public_credentials,
    render_about_credential_block,
    render_compact_credential_block,
    render_credential_block,
    render_homepage_credential_block,
)

ROOT = Path(__file__).resolve().parents[1]
STYLE_LINK = '<link rel="stylesheet" href="./site-assets/credentials.css">'
BLOCK = render_credential_block()
COMPACT_BLOCK = render_compact_credential_block()
CONTACT_BLOCK = render_compact_credential_block("BUSINESS_CREDENTIALS_CONTACT")
START = "<!-- BUSINESS_CREDENTIALS:START -->"
END = "<!-- BUSINESS_CREDENTIALS:END -->"
CONTACT_START = "<!-- BUSINESS_CREDENTIALS_CONTACT:START -->"
CONTACT_END = "<!-- BUSINESS_CREDENTIALS_CONTACT:END -->"

PRIMARY_PAGES = (
    "about.html",
    "managed-property-palm-services.html",
    "urban-forest-palm-documentation.html",
    "canary-island-date-palm-care-san-diego.html",
    "old-escondido-palm-preservation.html",
    "palm-care-escondido.html",
    "palm-care-poway.html",
    "palm-care-rancho-santa-fe.html",
    "palm-faq-san-diego.html",
    "palm-records-monitoring-verification.html",
    "report-a-palm.html",
    "palm-stewardship-plans.html",
    "quarterly-palm-care-san-diego.html",
    "sapw.html",
    "south-american-palm-weevil-treatment-san-diego.html",
    "palm-removal-coordination.html",
    "palm-sourcing-installation.html",
    "specimen-palms-cycads.html",
    "cidp-risk-checklist.html",
)

OLD_STATUS_PATTERNS = (
    r"California licensed\s*[·Â]+\s*DPR Category B qualified\s*[·Â]+\s*Insured",
    r"Licensed\s*[·Â]+\s*Qualified\s*[·Â]+\s*Insured",
)


def replace_marked_block(text: str, block: str = BLOCK) -> str:
    pattern = re.compile(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        re.DOTALL,
    )
    text = pattern.sub(block, text)
    contact_pattern = re.compile(
        rf"{re.escape(CONTACT_START)}.*?{re.escape(CONTACT_END)}",
        re.DOTALL,
    )
    return contact_pattern.sub(CONTACT_BLOCK, text)


def insert_for_page(path: Path, text: str) -> str:
    if START in text:
        if path.name == "index.html":
            page_block = render_homepage_credential_block()
        elif path.name == "about.html":
            page_block = render_about_credential_block()
        else:
            page_block = COMPACT_BLOCK
        text = replace_marked_block(text, page_block)
        if path.name == "palm-records-monitoring-verification.html" and CONTACT_START not in text:
            text = text.replace('<form class="inquiry-form"', f'{CONTACT_BLOCK}\n<form class="inquiry-form"', 1)
        if path.name == "report-a-palm.html" and CONTACT_START not in text:
            text = text.replace('<form id="observation-form"', f'{CONTACT_BLOCK}\n<form id="observation-form"', 1)
        return text

    if path.name == "index.html":
        target = re.compile(r'<p class="availability-note">.*?</p>', re.DOTALL)
        return target.sub(BLOCK, text, count=1)

    if path.name == "palm-records-monitoring-verification.html":
        target = re.compile(r'<div class="availability">.*?</div>', re.DOTALL)
        text = target.sub(f'<section class="credential-band">\n{BLOCK}\n</section>', text, count=1)
        return text.replace('<form class="inquiry-form"', f'{CONTACT_BLOCK}\n<form class="inquiry-form"', 1)

    if path.name == "report-a-palm.html":
        text = text.replace("<main>", f"<main>\n<section class=\"credential-band\">\n{BLOCK}\n</section>", 1)
        return text.replace('<form id="observation-form"', f'{CONTACT_BLOCK}\n<form id="observation-form"', 1)

    hero_end = re.compile(r'(<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>.*?</section>)', re.DOTALL)
    return hero_end.sub(rf'\1\n<section class="credential-band">\n{COMPACT_BLOCK}\n</section>', text, count=1)


def update_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    if STYLE_LINK not in text:
        text = text.replace("</head>", f"{STYLE_LINK}\n</head>", 1)
    text = insert_for_page(path, text)
    for pattern in OLD_STATUS_PATTERNS:
        text = re.sub(pattern, footer_line(), text, flags=re.IGNORECASE)
    status_label = public_credentials()["status_label"]
    text = re.sub(
        r'(<div class="eyebrow">).*?(</div>)',
        rf"\1{status_label}\2",
        text,
        count=1,
        flags=re.DOTALL,
    )
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize public business credential wording.")
    parser.add_argument("--check", action="store_true", help="Fail if generated credential copy is stale.")
    args = parser.parse_args()

    public_credentials()
    stale: list[str] = []
    for relative in PRIMARY_PAGES:
        path = ROOT / relative
        updated = update_file(path)
        current = path.read_text(encoding="utf-8-sig")
        if updated != current:
            if args.check:
                stale.append(relative)
            else:
                path.write_text(updated, encoding="utf-8")

    if stale:
        print("BUSINESS_CREDENTIALS_STALE")
        for relative in stale:
            print(f" - {relative}")
        return 1
    print("BUSINESS_CREDENTIALS_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
