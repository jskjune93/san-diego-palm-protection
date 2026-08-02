from __future__ import annotations

from html import escape
from pathlib import Path
import json

from business_credentials import (
    load_business_status,
    render_about_credential_block,
    render_credential_block,
    render_homepage_credential_block,
    public_credentials,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.sandiegopalmprotection.com"
PHONE = "262-492-3135"
EMAIL = "sandiegopalmprotection@gmail.com"
INQUIRY = json.loads((ROOT / "site-config" / "inquiry.json").read_text(encoding="utf-8"))


def asset_prefix(relative_root: str) -> str:
    return relative_root


def head(title: str, description: str, path: str, image: str = "background.jpg",
         schema_type: str = "WebPage", extra_schema: dict | None = None,
         relative_root: str = "./", publish_extra_schema: bool = False) -> str:
    canonical = BASE_URL + ("/" if path == "index.html" else f"/{path}")
    image_url = image if image.startswith("http") else f"{BASE_URL}/{image}"
    credential = public_credentials()
    schemas = [{
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title.split(" | ")[0],
        "description": description,
        "url": canonical,
        "isPartOf": {"@type": "WebSite", "name": "San Diego Palm Protection", "url": BASE_URL},
    }]
    if extra_schema and (load_business_status()["mode"] == "commercial" or publish_extra_schema):
        schemas.append(extra_schema)
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="business-status" content="{escape(credential["status_label"])}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:type" content="website">
  <link rel="icon" href="{relative_root}logo.png" type="image/png">
  <link rel="stylesheet" href="{relative_root}site-assets/site.css">
  <link rel="stylesheet" href="{relative_root}site-assets/credentials.css">
  <script type="application/ld+json">{json.dumps(schemas, ensure_ascii=False)}</script>
  <!-- SDPP analytics integration point: existing measurement configuration is preserved; no identifier is invented here. -->"""


def header(relative_root: str = "./") -> str:
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="nav-shell">
    <a class="brand" href="{relative_root}index.html" aria-label="San Diego Palm Protection home">
      <img src="{relative_root}logo.png" alt="" width="54" height="54">
      <span><strong>San Diego</strong><small>Palm Protection</small></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span class="sr-only">Open navigation</span><span aria-hidden="true"></span></button>
    <nav id="primary-nav" class="primary-nav" aria-label="Primary navigation">
      <a href="{relative_root}palm-records-monitoring-verification.html">Services</a>
      <a href="{relative_root}residential-palm-assessment.html">Residential</a>
      <a href="{relative_root}managed-property-palm-services.html">Managed Properties</a>
      <a href="{relative_root}palm-removal-coordination.html">Palm Decline</a>
      <a href="{relative_root}palm-journal-new.html">Palm Journal</a>
      <a href="{relative_root}palm-proof-examples.html">Field Work</a>
      <a class="nav-phone" data-conversion="call" href="tel:2624923135">Call or Text</a>
      <a class="button button-small" data-conversion="homeowner-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry">Request Assessment</a>
    </nav>
  </div>
</header>"""


def credentials(marker: str) -> str:
    return render_credential_block(marker)


def homepage_credentials() -> str:
    return render_homepage_credential_block()


def about_credentials() -> str:
    return render_about_credential_block()


def three_pillars(relative_root: str = "./") -> str:
    items = [
        ("01", "Assessment, Monitoring & Documentation", "I visit the property, photograph the palm, write down what I find, and return when comparison over time will help.", "residential-palm-assessment.html"),
        ("02", "Protection & Treatment", "I assess the concern, explain the options, and provide protection and treatment services when they fit the palm and site.", "palm-stewardship-plans.html"),
        ("03", "Decline Response, Removal & Replacement", "When a palm is failing, I help organize the next steps, the contractor handoff, and what comes after removal.", "palm-removal-coordination.html"),
    ]
    return '<div class="pillar-grid">' + "".join(
        f'<article class="pillar"><span>{n}</span><h3>{escape(t)}</h3><p>{escape(d)}</p><a href="{relative_root}{href}">Explore this service</a></article>'
        for n, t, d, href in items
    ) + "</div>"


def inquiry(relative_root: str = "./", heading: str = "Request an on-site palm assessment.") -> str:
    return f"""<section class="conversion-band" id="request" aria-labelledby="request-heading">
  <div><p class="eyebrow">Private inquiry</p><h2 id="request-heading">{escape(heading)}</h2>
  <p>Tell me what you are seeing and what you need to decide. I work with single palms, small groups, and larger managed properties.</p></div>
  <div class="button-row"><a class="button" data-conversion="homeowner-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry">Homeowner Inquiry</a><a class="button button-quiet" data-conversion="organization-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#organization-inquiry">Request a Palm Portfolio Walkthrough</a><a class="text-link" data-conversion="call" href="tel:2624923135">Call or Text {PHONE}</a></div>
</section>"""


def footer(relative_root: str = "./") -> str:
    return f"""<footer class="site-footer">
  <div class="footer-grid">
    <div><a class="footer-brand" href="{relative_root}index.html">San Diego Palm Protection</a><p>John Krause personally assesses and photographs mature palms from Old Escondido.</p></div>
    <div><h2>Services</h2><a href="{relative_root}residential-palm-assessment.html">Residential assessment</a><a href="{relative_root}quarterly-palm-care-san-diego.html">Recurring monitoring</a><a href="{relative_root}managed-property-palm-services.html">Managed properties</a><a href="{relative_root}urban-forest-palm-documentation.html">Urban forest palm documentation</a></div>
    <div><h2>Resources</h2><a href="{relative_root}about.html">About</a><a href="{relative_root}palm-proof-examples.html">Field work</a><a href="{relative_root}palm-journal-new.html">Palm Journal</a><a href="{relative_root}palm-faq-san-diego.html">Palm FAQ</a><a href="{relative_root}report-a-palm.html">Report a palm</a></div>
  </div>
  <p class="footer-legal">John Krause, owner · California Qualified Applicator License No. 175295 · Category B — Landscape Maintenance · Insured</p>
</footer>
<script src="{relative_root}site-assets/site.js" defer></script>
{mobile_contact(relative_root)}"""


def mobile_contact(relative_root: str = "./") -> str:
    return f"""<aside class="mobile-contact-bar" aria-label="Quick contact">
  <a data-conversion="call" href="tel:2624923135">Call or Text</a>
  <a data-conversion="homeowner-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry">Request Assessment</a>
</aside>"""


def page(*, filename: str, title: str, description: str, eyebrow: str, h1: str,
         lede: str, body: str, image: str = "background.jpg",
         relative_root: str = "./", extra_schema: dict | None = None,
         publish_extra_schema: bool = False) -> str:
    public = public_credentials()
    hero_note = '<p class="hero-microcopy">Single palms and small groups welcome · On-site visit · Dated photographs · Written findings · Clear next steps</p>' if filename == "index.html" else ""
    hero_trust = '<p class="hero-trust-line">Owner-operated • California QAL, Category B</p>' if filename == "index.html" else ""
    residential_trust = (
        '<p class="hero-trust-line">Your assessment is completed by John Krause, owner of San Diego Palm Protection and holder of '
        f'{escape(public["individual_license"])}, {escape(public["category"])}. <strong>{escape(public["insurance"])}</strong></p>'
        if filename == "residential-palm-assessment.html" else ""
    )
    organization_trust = (
        '<div class="institutional-trust"><strong>Owner-led field work</strong><span>California Qualified Applicator License No. 175295</span>'
        '<span>Category B — Landscape Maintenance</span><span>Insured</span><span>Structured photographic and written reporting</span></div>'
        if filename in {"managed-property-palm-services.html", "urban-forest-palm-documentation.html"} else ""
    )
    organization_page = filename in {"managed-property-palm-services.html", "urban-forest-palm-documentation.html"}
    primary_href = f"{relative_root}palm-records-monitoring-verification.html#{'organization-inquiry' if organization_page else 'homeowner-inquiry'}"
    primary_label = "Request a Palm Portfolio Walkthrough" if organization_page else "Request a Palm Assessment"
    primary_event = "organization-inquiry-initiation" if organization_page else "homeowner-inquiry-initiation"
    return f"""<!doctype html>
<html lang="en">
<head>
  {head(title, description, filename, image, extra_schema=extra_schema, relative_root=relative_root, publish_extra_schema=publish_extra_schema)}
</head>
<body>
{header(relative_root)}
<main id="main">
  <section class="page-hero" style="--hero-image:url('/{image}')">
    <div class="hero-inner"><p class="eyebrow">{escape(eyebrow)}</p><h1>{escape(h1)}</h1><p class="lede">{escape(lede)}</p>{hero_note}{hero_trust}{residential_trust}
    <div class="button-row"><a class="button" data-conversion="{primary_event}" href="{primary_href}">{primary_label}</a><a class="button button-quiet" data-conversion="call" href="tel:2624923135">Call or Text {PHONE}</a></div></div>
  </section>
  <div class="trust-wrap trust-wrap--compact">{homepage_credentials() if filename == "index.html" else about_credentials() if filename == "about.html" else credentials("BUSINESS_CREDENTIALS")}{organization_trust}</div>
  {body}
  {inquiry(relative_root)}
</main>
{footer(relative_root)}
</body>
</html>
"""
