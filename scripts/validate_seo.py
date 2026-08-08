#!/usr/bin/env python3
"""Durable, local SEO checks for generated production output."""

from __future__ import annotations

import json
import html
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
    "about.html",
    "residential-palm-assessment.html",
    "managed-property-palm-services.html",
    "south-american-palm-weevil-treatment-san-diego.html",
    "sapw.html",
    "urban-forest-palm-documentation.html",
    "palm-proof-examples.html",
    "palm-records-monitoring-verification.html",
}

INTENT_REQUIREMENTS = {
    "index.html": ("palm portfolio stewardship", "treatment", "san diego"),
    "sapw.html": ("south american palm weevil", "san diego", "signs", "prevention"),
    "south-american-palm-weevil-treatment-san-diego.html": ("south american palm weevil", "treatment", "san diego"),
    "palm-stewardship-plans.html": ("palm", "treatment", "preventive protection", "san diego"),
    "quarterly-palm-care-san-diego.html": ("palm stewardship", "preservation", "san diego"),
    "managed-property-palm-services.html": ("palm portfolio stewardship", "managed properties", "san diego"),
    "palm-records-monitoring-verification.html": ("palm assessment", "monitoring", "management"),
    "residential-palm-assessment.html": ("palm health assessment", "san diego"),
    "canary-island-date-palm-care-san-diego.html": ("canary island date palm", "care", "treatment", "san diego"),
    "palm-care-escondido.html": ("palm care", "treatment", "escondido"),
    "palm-care-rancho-santa-fe.html": ("palm care", "treatment", "rancho santa fe"),
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
    descriptions: dict[str, str] = {}
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
        og_title = one(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', text, "Open Graph title", path)
        og_description = one(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', text, "Open Graph description", path)
        if og_title != title or og_description != description:
            raise AssertionError(f"{rel}: Open Graph metadata does not match canonical title and description")
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

        for image_tag in re.findall(r"<img\b[^>]*>", text, flags=re.I | re.S):
            alt_match = re.search(r'\balt=["\'](.*?)["\']', image_tag, flags=re.I | re.S)
            if alt_match is None:
                raise AssertionError(f"{rel}: image is missing an alt attribute")
            src_match = re.search(r'\bsrc=["\'](.*?)["\']', image_tag, flags=re.I | re.S)
            src = src_match.group(1) if src_match else "unknown image"
            if not html.unescape(alt_match.group(1)).strip() and "logo" not in src.lower():
                raise AssertionError(f"{rel}: content image has empty alt text: {src}")

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
        descriptions[rel] = description
        canonicals[rel] = canonical

    duplicates = {t: rs for t in set(titles.values()) if len(rs := [r for r, v in titles.items() if v == t]) > 1}
    if duplicates:
        raise AssertionError(f"duplicate page titles: {duplicates}")
    duplicate_descriptions = {d: rs for d in set(descriptions.values()) if len(rs := [r for r, v in descriptions.items() if v == d]) > 1}
    if duplicate_descriptions:
        raise AssertionError(f"duplicate meta descriptions: {duplicate_descriptions}")

    for rel, tokens in INTENT_REQUIREMENTS.items():
        title_description = html.unescape(f"{titles[rel]} {descriptions[rel]}").lower()
        missing = [token for token in tokens if token not in title_description]
        if missing:
            raise AssertionError(f"{rel}: assigned search intent is missing {missing}")
        title_length = len(html.unescape(titles[rel]))
        description_length = len(html.unescape(descriptions[rel]))
        if not 30 <= title_length <= 70:
            raise AssertionError(f"{rel}: primary title length is {title_length}, expected 30-70")
        if not 90 <= description_length <= 170:
            raise AssertionError(f"{rel}: primary description length is {description_length}, expected 90-170")

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

    logo_size = (DIST / "logo.png").stat().st_size
    if logo_size > 100_000:
        raise AssertionError(f"logo.png is oversized at {logo_size} bytes")

    print(f"SEO_VALIDATION_OK pages={len(pages)} sitemap_urls={len(urls)} primary_pages={len(PRIMARY)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"SEO_VALIDATION_FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
