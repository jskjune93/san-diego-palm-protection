from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from business_credentials import public_credentials

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.sandiegopalmprotection.com"
MANIFEST = ROOT / "journal-data" / "journal_entries.json"
INDEX = ROOT / "palm-journal-new.html"
SITEMAP = ROOT / "sitemap.xml"
ROBOTS = ROOT / "robots.txt"
RECORDS_PAGE = ROOT / "palm-records-monitoring-verification.html"
REPORT_PAGE = ROOT / "report-a-palm.html"
TREATMENT_PAGE = ROOT / "palm-stewardship-plans.html"
TREATMENT_ROUTE = "./palm-stewardship-plans.html"

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "sms:", "data:")
ENCODING_ARTIFACTS = ["â€", "â€™", "â€œ", "â€�", "Â", "�"]
WINDOWS_PATH_RE = re.compile(r"\b[A-Za-z]:\\\\")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.images: list[str] = []
        self.h1_count = 0
        self.h2_count = 0
        self.title = ""
        self.in_title = False
        self.meta_descriptions: list[str] = []
        self.canonicals: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.in_json_ld = False
        self.current_json_ld: list[str] = []
        self.section_starts = 0
        self.section_ends = 0
        self.div_starts = 0
        self.div_ends = 0
    def handle_starttag(self, tag: str, attrs_list):
        attrs = dict(attrs_list)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "h2":
            self.h2_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name", "").lower() == "description" and attrs.get("content"):
            self.meta_descriptions.append(attrs["content"])
        if tag == "link" and attrs.get("rel", "").lower() == "canonical" and attrs.get("href"):
            self.canonicals.append(attrs["href"])
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.current_json_ld = []
        if tag == "section":
            self.section_starts += 1
        if tag == "div":
            self.div_starts += 1
    def handle_endtag(self, tag: str):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_json_ld:
            self.json_ld_blocks.append("".join(self.current_json_ld).strip())
            self.in_json_ld = False
        if tag == "section":
            self.section_ends += 1
        if tag == "div":
            self.div_ends += 1
    def handle_data(self, data: str):
        if self.in_title:
            self.title += data.strip()
        if self.in_json_ld:
            self.current_json_ld.append(data)


def read_html(path: Path) -> tuple[str, PageParser]:
    text = path.read_text(encoding="utf-8-sig")
    parser = PageParser()
    parser.feed(text)
    return text, parser


def resolve_local(base: Path, href: str) -> tuple[Path, str] | None:
    if not href or href.startswith(SKIP_SCHEMES):
        return None
    if href.startswith("#"):
        return base, href[1:]
    path_part, _, anchor = href.partition("#")
    if path_part.startswith("/"):
        path_part = path_part.lstrip("/")
        target = ROOT / path_part
    else:
        target = (base.parent / path_part).resolve()
    return target, anchor


def normalize_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    html_files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "palm-journal").glob("**/*.html"))
    pages: dict[Path, tuple[str, PageParser]] = {}
    ids_by_page: dict[Path, set[str]] = {}

    for path in html_files:
        text, parser = read_html(path)
        pages[path.resolve()] = (text, parser)
        ids_by_page[path.resolve()] = set(parser.ids)
        rel = normalize_rel(path)
        if parser.h1_count != 1:
            errors.append(f"{rel}: expected exactly one H1, found {parser.h1_count}")
        if len(parser.ids) != len(set(parser.ids)):
            dupes = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
            errors.append(f"{rel}: duplicate IDs {dupes}")
        if parser.section_starts != parser.section_ends:
            errors.append(f"{rel}: section balance {parser.section_starts}/{parser.section_ends}")
        if parser.div_starts != parser.div_ends:
            errors.append(f"{rel}: div balance {parser.div_starts}/{parser.div_ends}")
        if not parser.title:
            errors.append(f"{rel}: missing title")
        if not parser.meta_descriptions:
            errors.append(f"{rel}: missing meta description")
        if not parser.canonicals:
            errors.append(f"{rel}: missing canonical URL")
        for canonical in parser.canonicals:
            if not canonical.startswith(BASE_URL):
                errors.append(f"{rel}: canonical is not site URL: {canonical}")
        for block in parser.json_ld_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD: {exc}")
        if WINDOWS_PATH_RE.search(text):
            errors.append(f"{rel}: public file contains a local Windows path")
        for artifact in ENCODING_ARTIFACTS:
            if artifact in text:
                errors.append(f"{rel}: encoding artifact found: {artifact}")
        for src in parser.images:
            if src.startswith(SKIP_SCHEMES):
                continue
            image_path = (path.parent / src.split("#", 1)[0].split("?", 1)[0]).resolve()
            if not image_path.exists():
                errors.append(f"{rel}: missing image {src}")
        for href in parser.links:
            resolved = resolve_local(path.resolve(), href)
            if not resolved:
                continue
            target, anchor = resolved
            if not target.exists():
                errors.append(f"{rel}: missing internal link target {href}")
                continue
            if anchor and target.suffix.lower() == ".html":
                target_resolved = target.resolve()
                if target_resolved not in pages:
                    _, target_parser = read_html(target_resolved)
                    ids_by_page[target_resolved] = set(target_parser.ids)
                if anchor not in ids_by_page.get(target_resolved, set()):
                    errors.append(f"{rel}: missing anchor target {href}")

    titles = {}
    descriptions = {}
    for path, (_, parser) in pages.items():
        rel = normalize_rel(path)
        if parser.title in titles:
            warnings.append(f"duplicate title: {parser.title} ({titles[parser.title]}, {rel})")
        else:
            titles[parser.title] = rel
        for description in parser.meta_descriptions[:1]:
            if description in descriptions:
                warnings.append(f"duplicate meta description: {description} ({descriptions[description]}, {rel})")
            else:
                descriptions[description] = rel

    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    slugs = [entry["slug"] for entry in entries]
    if len(slugs) != len(set(slugs)):
        errors.append("journal manifest has duplicate slugs")
    anchors = [entry["legacy_anchor"] for entry in entries]
    if len(anchors) != len(set(anchors)):
        errors.append("journal manifest has duplicate legacy anchors")
    index_text, index_parser = pages[INDEX.resolve()]
    if "status\": \"draft" in index_text.lower():
        errors.append("draft status text appears in journal index")
    for entry in entries:
        slug = entry["slug"]
        if entry.get("status") == "draft" or entry.get("public", True) is False:
            if slug in index_text or entry.get("legacy_anchor", "") in ids_by_page[INDEX.resolve()]:
                errors.append(f"held or draft article exposed in index: {slug}")
            continue
        if entry["legacy_anchor"] not in ids_by_page[INDEX.resolve()]:
            errors.append(f"legacy anchor not preserved on index: {entry['legacy_anchor']}")
        if entry.get("page"):
            article = ROOT / "palm-journal" / f"{slug}.html"
            if not article.exists():
                errors.append(f"missing article page for {slug}")
            if f"palm-journal/{slug}.html" not in index_text:
                errors.append(f"journal card does not point to article page: {slug}")
            article_text = article.read_text(encoding="utf-8-sig") if article.exists() else ""
            if entry["legacy_anchor"] not in article_text:
                errors.append(f"article page does not preserve legacy anchor: {slug}")
        else:
            if f"palm-journal/{slug}.html" in index_text:
                errors.append(f"non-page legacy item links to article page: {slug}")

    try:
        tree = ET.parse(SITEMAP)
        sitemap_root = tree.getroot()
        locs = [node.text or "" for node in sitemap_root.iter() if node.tag.endswith("loc")]
        if f"{BASE_URL}/palm-journal-new.html" not in locs:
            errors.append("sitemap missing Palm Journal index")
        if f"{BASE_URL}/palm-journal/documented-loss/" not in locs:
            errors.append("sitemap missing Documented Loss page")
        if f"{BASE_URL}/palm-records-monitoring-verification.html" not in locs:
            errors.append("sitemap missing Records & Monitoring page")
        if f"{BASE_URL}/report-a-palm.html" not in locs:
            errors.append("sitemap missing Report a Palm page")
        if f"{BASE_URL}/urban-forest-palm-documentation.html" not in locs:
            errors.append("sitemap missing Urban Forest Palm Documentation page")
        for entry in entries:
            if entry.get("status") == "published" and entry.get("page"):
                if entry["canonical_url"] not in locs:
                    errors.append(f"sitemap missing article URL: {entry['slug']}")
    except ET.ParseError as exc:
        errors.append(f"invalid sitemap XML: {exc}")

    if not ROBOTS.exists():
        errors.append("robots.txt missing")
    else:
        robots = ROBOTS.read_text(encoding="utf-8-sig")
        if "Sitemap:" not in robots:
            errors.append("robots.txt missing Sitemap directive")

    homepage_text, homepage_parser = pages[(ROOT / "index.html").resolve()]
    for required_pillar in (
        "Stewardship &amp; Palm Health",
        "Protection &amp; Treatment",
        "Documentation &amp; Portfolio Management",
        "Response, Removal &amp; Renewal",
    ):
        if required_pillar not in homepage_text:
            errors.append(f"homepage missing stewardship-function positioning: {required_pillar}")
    treatment_card = re.search(
        r'<article class="pillar">(?:(?!</article>).)*Protection &amp; Treatment'
        r'(?:(?!</article>).)*href="([^"]+)"(?:(?!</article>).)*</article>',
        homepage_text,
        re.DOTALL,
    )
    if not treatment_card:
        errors.append("homepage Protection & Treatment service card is missing or has no destination")
    elif treatment_card.group(1) != TREATMENT_ROUTE:
        errors.append(
            "homepage Protection & Treatment service card must resolve to "
            f"{TREATMENT_ROUTE}, found {treatment_card.group(1)}"
        )
    if not RECORDS_PAGE.exists():
        errors.append("Records & Monitoring service page is missing")
    elif "./palm-records-monitoring-verification.html" not in homepage_text:
        errors.append("homepage does not link to Records & Monitoring service page")
    business_status = json.loads((ROOT / "site-config" / "business_status.json").read_text(encoding="utf-8"))
    if business_status.get("mode") != "commercial":
        errors.append("production business status must be commercial")
    credentials = public_credentials()
    required_current_scope = credentials["licensing_statement"]
    required_qualified_insured_scope = credentials.get("service_summary", "")
    records_text = RECORDS_PAGE.read_text(encoding="utf-8-sig") if RECORDS_PAGE.exists() else ""
    report_text = REPORT_PAGE.read_text(encoding="utf-8-sig") if REPORT_PAGE.exists() else ""
    treatment_text = TREATMENT_PAGE.read_text(encoding="utf-8-sig") if TREATMENT_PAGE.exists() else ""
    treatment_lower = treatment_text.lower()
    if not TREATMENT_PAGE.exists():
        errors.append("canonical Palm Protection & Treatment page is missing")
    else:
        treatment_parser = read_html(TREATMENT_PAGE)[1]
        if treatment_parser.canonicals != [f"{BASE_URL}/palm-stewardship-plans.html"]:
            errors.append("Palm Protection & Treatment page canonical is incorrect")
        treatment_requirements = {
            "current availability": (("protection", "treatment services"),),
            "assessment-first scope": (("review", "palm", "site"),),
            "monitoring": (("monitor",),),
            "owner voice": (("i ",),),
        }
        for label, alternatives in treatment_requirements.items():
            if not any(all(fragment in treatment_lower for fragment in group) for group in alternatives):
                errors.append(f"Palm Protection & Treatment page missing semantic requirement: {label}")
    public_treatment_unavailable = (
        "pesticide application is not currently offered",
        "treatment is not currently offered",
        "treatment services unavailable",
        "no treatment services",
        "treatment unavailable",
        "limited service scope",
        "documentation-only",
        "treatment coming soon",
        "not yet licensed",
    )
    for path, (page_text, _) in pages.items():
        lowered = page_text.lower()
        for phrase in public_treatment_unavailable:
            if phrase in lowered:
                errors.append(
                    f"{normalize_rel(path)}: public treatment-unavailable contradiction remains: {phrase}"
                )
    if not REPORT_PAGE.exists():
        errors.append("Report a Palm page is missing")
    else:
        for required_fragment in (
            'id="observation-form"',
            'name="contact_permission" required',
            'name="private_retention_permission" required',
            'name="public_use_permission"',
            "Nothing is published automatically",
            "The report is not delivered until you send it",
            "does not upload or store photographs",
            "configured email application",
            "Observation and chronology:",
            "identifiable private-property details remain private",
            "Review status: needs_review",
        ):
            if required_fragment not in report_text:
                errors.append(f"Report a Palm page missing safeguard or field: {required_fragment}")
        if 'type="file"' in report_text:
            errors.append("Report a Palm implies direct upload without a supported backend")
        if "public_use_permission') ? 'yes' : 'no'" not in report_text:
            errors.append("optional public-use permission is not kept separate")
        if "Not provided" in report_text:
            errors.append("Report a Palm handoff should omit empty optional fields")
    if "./report-a-palm.html" not in homepage_text:
        errors.append("homepage does not link to Report a Palm")
    if "./urban-forest-palm-documentation.html" not in homepage_text:
        errors.append("homepage does not link to Urban Forest Palm Documentation")
    old_escondido_text = (ROOT / "old-escondido-palm-preservation.html").read_text(encoding="utf-8-sig")
    if "./report-a-palm.html" not in old_escondido_text:
        errors.append("Old Escondido initiative does not link to Report a Palm")
    if "Share a palm observation or dated photograph." not in index_text:
        errors.append("Palm Journal is missing contribution language")
    article_pages = sorted((ROOT / "palm-journal").glob("*.html"))
    for article in article_pages:
        if "Share a palm observation or dated photograph." not in article.read_text(encoding="utf-8-sig"):
            errors.append(f"journal article missing standardized contribution footer: {article.name}")
    if required_current_scope not in homepage_text or required_qualified_insured_scope not in records_text:
        errors.append("current stewardship offer and credential summary are not consistently identified")
    for path in (
            ROOT / "index.html",
            RECORDS_PAGE,
            REPORT_PAGE,
            ROOT / "palm-stewardship-plans.html",
            ROOT / "quarterly-palm-care-san-diego.html",
            ROOT / "sapw.html",
            ROOT / "south-american-palm-weevil-treatment-san-diego.html",
            ROOT / "palm-removal-coordination.html",
            ROOT / "urban-forest-palm-documentation.html",
    ):
        page_text = path.read_text(encoding="utf-8-sig")
        if required_qualified_insured_scope not in page_text:
            errors.append(f"{normalize_rel(path)}: missing centralized qualified/insured status")
        if "BUSINESS_CREDENTIALS:START" not in page_text:
            errors.append(f"{normalize_rel(path)}: missing reusable business credential block")
    for path in (ROOT / "index.html", RECORDS_PAGE):
        page_text = path.read_text(encoding="utf-8-sig")
        if f'<meta name="business-status" content="{credentials["status_label"]}">' not in page_text:
            errors.append(f"{normalize_rel(path)}: metadata missing qualified/insured service status")
    if "Residential Palm Assessment" not in homepage_text or 'href="./palm-records-monitoring-verification.html#homeowner-inquiry"' not in homepage_text or "Request a Palm Assessment" not in records_text:
        errors.append("commercial-first homepage and service page must preserve the secondary residential assessment path")
    for required_path in (
        "palm-removal-coordination.html",
        "specimen-palms-cycads.html",
        "palm-sourcing-installation.html",
        "palm-journal-new.html",
        "palm-journal/documented-loss/",
        "urban-forest-palm-documentation.html",
    ):
        if required_path not in homepage_text + records_text:
            errors.append(f"preserved service or editorial destination is not reachable from updated pages: {required_path}")
    homepage_canonicals = homepage_parser.canonicals
    if homepage_canonicals != [f"{BASE_URL}/"]:
        errors.append(f"homepage canonical must normalize / and /index.html to {BASE_URL}/")
    unsupported_claims = (
        "SDPP is an ISA Certified Arborist",
        "SDPP is a licensed pest-control business",
        "SDPP certifies contractor performance",
        "official urban forest management plan partner",
    )
    for claim in unsupported_claims:
        if claim.lower() in (homepage_text + records_text).lower():
            errors.append(f"unsupported qualification claim found: {claim}")

    credential_sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_business_credentials.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if credential_sync.stdout.strip():
        print(credential_sync.stdout.strip())
    if credential_sync.stderr.strip():
        print(credential_sync.stderr.strip())
    if credential_sync.returncode != 0:
        errors.append("business credential synchronization check failed")

    credential_validation = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_business_credentials.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if credential_validation.stdout.strip():
        print(credential_validation.stdout.strip())
    if credential_validation.stderr.strip():
        print(credential_validation.stderr.strip())
    if credential_validation.returncode != 0:
        errors.append("business credential validation failed")

    operational_status = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_operational_status.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if operational_status.stdout.strip():
        print(operational_status.stdout.strip())
    if operational_status.stderr.strip():
        print(operational_status.stderr.strip())
    if operational_status.returncode != 0:
        errors.append("operational status regression validator failed")

    active_service = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_active_service_state.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if active_service.stdout.strip():
        print(active_service.stdout.strip())
    if active_service.stderr.strip():
        print(active_service.stderr.strip())
    if active_service.returncode != 0:
        errors.append("active-service-state validator failed")

    positioning = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_positioning.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if positioning.stdout.strip():
        print(positioning.stdout.strip())
    if positioning.stderr.strip():
        print(positioning.stderr.strip())
    if positioning.returncode != 0:
        errors.append("positioning regression validator failed")

    print("VALIDATION_OK" if not errors else "VALIDATION_FAILED")
    print(f"html_files_checked={len(html_files)}")
    print(f"journal_manifest_entries={len(entries)}")
    print(f"journal_article_pages={len(list((ROOT / 'palm-journal').glob('*.html')))}")
    print(f"legacy_anchors_checked={len(anchors)}")
    print(f"sitemap_present={SITEMAP.exists()}")
    print(f"robots_present={ROBOTS.exists()}")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f" - {warning}")
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f" - {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
