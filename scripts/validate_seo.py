#!/usr/bin/env python3
"""Durable, local SEO checks for generated production output."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BASE = "https://www.sandiegopalmprotection.com"
PRIMARY = {
    "index.html",
    "residential-palm-assessment.html",
    "managed-property-palm-services.html",
    "south-american-palm-weevil-treatment-san-diego.html",
    "sapw.html",
    "urban-forest-palm-documentation.html",
    "palm-proof-examples.html",
    "palm-records-monitoring-verification.html",
}


def one(pattern: str, text: str, label: str, path: Path) -> str:
    values = re.findall(pattern, text, flags=re.I | re.S)
    if len(values) != 1:
        raise AssertionError(f"{path.name}: expected one {label}, found {len(values)}")
    return re.sub(r"\s+", " ", values[0]).strip()


def main() -> int:
    if not DIST.exists():
        raise AssertionError("dist is missing; run the production build first")

    pages = sorted(DIST.rglob("*.html"))
    titles: dict[str, str] = {}
    canonicals: dict[str, str] = {}
    linked_paths: Counter[str] = Counter()

    for path in pages:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(DIST).as_posix()
        title = one(r"<title>(.*?)</title>", text, "title", path)
        description = one(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            text,
            "meta description",
            path,
        )
        canonical = one(
            r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
            text,
            "canonical",
            path,
        )
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", text, flags=re.I | re.S)
        if len(h1s) != 1:
            raise AssertionError(f"{rel}: expected one H1, found {len(h1s)}")
        if not description:
            raise AssertionError(f"{rel}: empty meta description")
        if rel == "index.html":
            expected_canonical = BASE + "/"
        elif rel.endswith("/index.html"):
            expected_canonical = BASE + "/" + rel.removesuffix("index.html")
        else:
            expected_canonical = BASE + f"/{rel}"
        if canonical != expected_canonical:
            raise AssertionError(f"{rel}: inconsistent canonical {canonical}")
        if "noindex" in text.lower() and rel in PRIMARY:
            raise AssertionError(f"{rel}: primary page contains noindex")
        if "Quarterly Palm Care Plans" in title:
            raise AssertionError(f"{rel}: stale homepage title language")
        if "Pest Control Business License No. 175295" in text:
            raise AssertionError(f"{rel}: QAL/business-license confusion")

        for block in re.findall(
            r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text,
            flags=re.I | re.S,
        ):
            json.loads(block)

        for href in re.findall(r'href=["\']([^"\']+)["\']', text, flags=re.I):
            if href.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue
            parsed = urlparse(href)
            if parsed.scheme in {"http", "https"}:
                if parsed.netloc == "www.sandiegopalmprotection.com":
                    linked_paths[parsed.path.lstrip("/") or "index.html"] += 1
                continue
            target = (path.parent / parsed.path).resolve()
            try:
                linked_paths[target.relative_to(DIST.resolve()).as_posix()] += 1
            except ValueError:
                raise AssertionError(f"{rel}: link escapes production output: {href}")

        titles[rel] = title
        canonicals[rel] = canonical

    duplicates = {t: rs for t in set(titles.values()) if len(rs := [r for r, v in titles.items() if v == t]) > 1}
    if duplicates:
        raise AssertionError(f"duplicate page titles: {duplicates}")

    sitemap = ET.parse(DIST / "sitemap.xml")
    urls = [node.text or "" for node in sitemap.findall(".//{*}loc")]
    if len(urls) != len(set(urls)):
        raise AssertionError("sitemap contains duplicate URLs")
    if any(not url.startswith(BASE + "/") for url in urls):
        raise AssertionError("sitemap contains a noncanonical host")
    if set(urls) != set(canonicals.values()):
        raise AssertionError("sitemap and HTML canonicals differ")
    if any(token in (DIST / "sitemap.xml").read_text(encoding="utf-8") for token in ("localhost", "vercel.app", "C:\\Users")):
        raise AssertionError("sitemap contains a private or nonproduction URL")

    for rel in PRIMARY - {"index.html"}:
        if linked_paths[rel] == 0:
            raise AssertionError(f"orphaned primary page: {rel}")

    print(f"SEO_VALIDATION_OK pages={len(pages)} sitemap_urls={len(urls)} primary_pages={len(PRIMARY)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"SEO_VALIDATION_FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
