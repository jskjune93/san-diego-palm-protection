from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
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

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = dict(attrs_list)
        if tag in {"img", "video", "source"}:
            for name in ("src", "poster"):
                if attrs.get(name):
                    self.references.add(attrs[name])
            if attrs.get("srcset"):
                for candidate in attrs["srcset"].split(","):
                    self.references.add(candidate.strip().split()[0])
        if tag == "meta" and attrs.get("property") in {"og:image", "twitter:image"}:
            if attrs.get("content"):
                self.references.add(attrs["content"])
        if attrs.get("style"):
            self.references.update(re.findall(r"url\(['\"]?([^'\")]+)", attrs["style"]))


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
    approved = manifest["approved_assets"]
    referenced: set[str] = set()
    html_files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html"))
    for html in html_files:
        parser = MediaParser()
        parser.feed(html.read_text(encoding="utf-8-sig"))
        for value in parser.references:
            relative = normalize(html.parent, value)
            if relative:
                referenced.add(relative)

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

    stale = sorted(set(approved) - referenced)
    if stale:
        errors.append("provenance manifest contains unreferenced assets: " + ", ".join(stale))

    print("IMAGE_PROVENANCE_OK" if not errors else "IMAGE_PROVENANCE_FAILED")
    print(f"visible_media_assets_checked={len(referenced)}")
    print(f"approved_media_assets={len(approved)}")
    if errors:
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
