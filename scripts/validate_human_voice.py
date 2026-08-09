from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PRIORITY_PAGES = (
    "index.html",
    "about.html",
    "residential-palm-assessment.html",
    "palm-records-monitoring-verification.html",
    "managed-property-palm-services.html",
    "palm-proof-examples.html",
    "sapw.html",
    "old-escondido-palm-preservation.html",
)
REMOVED_PHRASES = (
    "three pillars support the full palm lifecycle",
    "one record connects each decision",
    "from evidence to outcome",
    "support better palm decisions",
    "a direct route for your kind of property",
    "contractor-work verification records evidence; it does not certify the unknowable",
    "owner-level accountability",
    "one point of contact from walkthrough through follow-up",
    "you work with me from the first call",
    "no sales-to-field handoff",
    "work directly with the owner",
    "i stay with the work",
)


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def visible(path: Path) -> str:
    parser = VisibleText()
    parser.feed(path.read_text(encoding="utf-8"))
    return " ".join(parser.parts)


def main() -> None:
    errors: list[str] = []
    combined = []
    for filename in PRIORITY_PAGES:
        text = visible(ROOT / filename)
        combined.append(text)
        if filename in {
            "index.html",
            "about.html",
            "residential-palm-assessment.html",
            "palm-records-monitoring-verification.html",
            "sapw.html",
        } and len(re.findall(r"\bI\b|\bmy\b|\bme\b", text, re.I)) < 3:
            errors.append(f"{filename}: owner voice is not sustained")
    all_text = " ".join(combined).lower()
    for phrase in REMOVED_PHRASES:
        if phrase in all_text:
            errors.append(f"priority copy retains templated phrase: {phrase}")
    if "south american palm weevil activity on my own" not in all_text:
        errors.append("firsthand SAPW experience is missing from priority copy")
    journal_source = (ROOT / "journal-data" / "articles" / "las-palmas-no-reply-then-the-saws.html").read_text(encoding="utf-8")
    if re.search(r"\bplam\b", journal_source, re.I):
        errors.append("No Reply. Then the Saws. retains the 'plam' typo")
    if errors:
        raise SystemExit("\n".join(errors))
    print("HUMAN_VOICE_VALIDATION_OK")
    print(f"priority_pages_checked={len(PRIORITY_PAGES)}")


if __name__ == "__main__":
    main()
