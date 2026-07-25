from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
UFMP = "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process."
PRIVATE_TERMS = ("karrie", "gate code", "private-client@", "confidential avenue", "source_report_path")
ENDORSEMENT = ("city endorsed", "city partner", "official ufmp partner", "approved by the city")
NAV_LABELS = ("Services", "Residential", "Managed Properties", "Palm Decline", "Palm Journal", "Field Work", "Call or Text", "Request Assessment")


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden += 1
    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden:
            self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def main() -> int:
    errors = []
    html = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html"))
    for path in html:
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8-sig")
        parser = VisibleText(); parser.feed(raw)
        visible = " ".join(parser.parts)
        lower = raw.lower()
        for label in NAV_LABELS:
            if label not in visible:
                errors.append(f"{rel}: canonical navigation missing {label}")
        if "site-assets/site.css" not in raw or "site-assets/site.js" not in raw:
            errors.append(f"{rel}: global design/navigation assets missing")
        if len(re.findall(r'<nav[^>]+aria-label="Primary navigation"', raw)) != 1:
            errors.append(f"{rel}: expected one primary navigation")
        for term in PRIVATE_TERMS:
            if term in lower and rel != "palm-proof-examples.html":
                errors.append(f"{rel}: private-proof token found: {term}")
        for phrase in ENDORSEMENT:
            if phrase in lower:
                errors.append(f"{rel}: municipal endorsement implication: {phrase}")
    managed = (ROOT / "managed-property-palm-services.html").read_text(encoding="utf-8")
    if UFMP not in managed:
        errors.append("managed-property route: exact UFMP wording missing")
    proof = (ROOT / "palm-proof-examples.html").read_text(encoding="utf-8")
    for phrase in ("separately approved", "sanitized", "Private client reports", "No unapproved proof bundle can render publicly"):
        if phrase not in proof:
            errors.append(f"proof route: missing boundary phrase {phrase}")
    route_doc = (ROOT / "docs" / "route-inventory.md").read_text(encoding="utf-8")
    if route_doc.count("| `/") != len(html):
        errors.append(f"route inventory count {route_doc.count('| `/')} does not match {len(html)} HTML routes")
    screenshot_count = len(list((ROOT / "docs" / "audit-screenshots").glob("*.png")))
    if screenshot_count != len(html) * 5:
        errors.append(f"expected {len(html) * 5} screenshots, found {screenshot_count}")
    print("ADVERSARIAL_AUDIT_OK" if not errors else "ADVERSARIAL_AUDIT_FAILED")
    print(json.dumps({"html_routes": len(html), "screenshots": screenshot_count, "viewports": 5, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
