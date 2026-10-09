from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "site-config" / "image_provenance.json"
MEDIA_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".svg", ".mp4"}
DENIED = {"background.jpg"}


class MediaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: set[str] = set()
        self.visible_references: list[str] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = dict(attrs_list)
        if tag in {"img", "video", "source"}:
            for name in ("src", "poster"):
                if attrs.get(name):
                    self.references.add(attrs[name])
                    self.visible_references.append(attrs[name])
            if attrs.get("srcset"):
                for candidate in attrs["srcset"].split(","):
                    value = candidate.strip().split()[0]
                    self.references.add(value)
                    self.visible_references.append(value)
        if tag == "meta" and attrs.get("property") in {"og:image", "twitter:image"}:
            if attrs.get("content"):
                self.references.add(attrs["content"])
        if attrs.get("style"):
            values = re.findall(r"url\(['\"]?([^'\")]+)", attrs["style"])
            self.references.update(values)
            self.visible_references.extend(values)


def normalize(base: Path, value: str) -> str | None:
    value = re.sub(r"^https://www\.sandiegopalmprotection\.com/", "/", value)
    if value.startswith(("http://", "https://", "data:")):
        return None
    clean = value.split("?", 1)[0].split("#", 1)[0]
    target = ROOT / clean.lstrip("/") if clean.startswith("/") else base / clean
    try:
        relative = target.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None
    return relative if Path(relative).suffix.lower() in MEDIA_SUFFIXES else None


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    approved = {
        **manifest.get("approved_assets", {}),
        **manifest.get("approved_derivative_sources", {}),
    }
    referenced: set[str] = set()
    visible_usage: dict[str, list[str]] = {}
    html_files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html"))
    for html in html_files:
        parser = MediaParser()
        parser.feed(html.read_text(encoding="utf-8-sig"))
        for value in parser.references:
            relative = normalize(html.parent, value)
            if relative:
                referenced.add(relative)
        for value in parser.visible_references:
            relative = normalize(html.parent, value)
            if relative:
                visible_usage.setdefault(relative, []).append(html.relative_to(ROOT).as_posix())

    errors: list[str] = []
    for relative in sorted(referenced):
        if relative in DENIED:
            errors.append(f"denied third-party asset is referenced: {relative}")
            continue
        record = approved.get(relative)
        if not record:
            errors.append(f"visible media lacks provenance approval: {relative}")
            continue
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"approved media is missing: {relative}")
            continue
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != record["sha256"]:
            errors.append(f"approved media fingerprint changed: {relative}")
        classification = record.get("classification")
        decision = record.get("publication_decision")
        if classification not in manifest["classification_definitions"]:
            errors.append(f"invalid provenance classification: {relative}")
        if classification in {"third_party_copied_or_externally_sourced", "ai_generated_or_possibly_ai_generated"}:
            errors.append(f"disallowed media classification is visible: {relative} ({classification})")
        if classification == "unverified_or_uncertain" and decision != "approved_context_only":
            errors.append(f"uncertain media lacks context-only decision: {relative}")

    # An SDPP photograph belongs to one visible placement. Licensed reference
    # imagery may be reused, but owner photography must not become wallpaper.
    duplicate_exceptions = {
        "logo.png",
        "images/palm-journal/where-we-care-for-palms-october-2026/sdpp-customer-map-2026-10-03.webp",
    }
    for relative, pages in sorted(visible_usage.items()):
        record = approved.get(relative, {})
        if relative in duplicate_exceptions or record.get("classification") != "confirmed_original_sdpp":
            continue
        if len(pages) > 1:
            locations = ", ".join(pages)
            errors.append(f"SDPP-owned photograph is reused in visible placements: {relative} ({locations})")

    # Different derivatives or filenames can still contain the same original
    # photograph. Keep those known source-equivalent groups to one public use.
    for group in manifest.get("same_source_photo_groups", []):
        used = [(relative, visible_usage[relative]) for relative in group if relative in visible_usage]
        placements = sum(len(pages) for _, pages in used)
        if placements > 1:
            detail = "; ".join(f"{relative} ({', '.join(pages)})" for relative, pages in used)
            errors.append(f"same SDPP source photograph is reused through multiple assets: {detail}")

    print("IMAGE_PROVENANCE_OK" if not errors else "IMAGE_PROVENANCE_FAILED")
    print(f"visible_media_assets_checked={len(referenced)}")
    print(f"approved_media_assets={len(approved)}")
    counts = Counter(record.get("classification", "missing") for record in approved.values())
    for classification, count in sorted(counts.items()):
        print(f"classification_{classification}={count}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
