from __future__ import annotations

from html import escape
from pathlib import Path
import json

from business_credentials import render_credential_block, public_credentials

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.sandiegopalmprotection.com"
PHONE = "262-492-3135"
EMAIL = "sandiegopalmprotection@gmail.com"


def asset_prefix(relative_root: str) -> str:
    return relative_root


def head(title: str, description: str, path: str, image: str = "background.jpg",
         schema_type: str = "WebPage", extra_schema: dict | None = None,
         relative_root: str = "./") -> str:
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
        "serviceStatus": credential["status_label"],
    }]
    if extra_schema:
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
      <a href="{relative_root}palm-proof-examples.html">Sample Work</a>
      <a class="button button-small" href="{relative_root}palm-records-monitoring-verification.html#request">Request Assessment</a>
    </nav>
  </div>
</header>"""


def credentials(marker: str) -> str:
    return render_credential_block(marker)


def three_pillars(relative_root: str = "./") -> str:
    items = [
        ("01", "Monitoring & Documentation", "Assessments, photographic baselines, recurring visits, inventories, and written condition reporting.", "palm-records-monitoring-verification.html"),
        ("02", "Protection & Treatment", "Qualified, insured protection planning and regulated treatment when the site, diagnosis, label, and authorization support it.", "palm-stewardship-plans.html"),
        ("03", "Response, Removal & Replacement", "Clear records and coordination when a palm declines, urgent contractor work is needed, or replacement planning begins.", "palm-removal-coordination.html"),
    ]
    return '<div class="pillar-grid">' + "".join(
        f'<article class="pillar"><span>{n}</span><h3>{escape(t)}</h3><p>{escape(d)}</p><a href="{relative_root}{href}">Explore this service</a></article>'
        for n, t, d, href in items
    ) + "</div>"


def inquiry(relative_root: str = "./", heading: str = "Start with the palm, property, and decision in front of you.") -> str:
    return f"""<section class="conversion-band" id="request" aria-labelledby="request-heading">
  <div><p class="eyebrow">Private inquiry</p><h2 id="request-heading">{escape(heading)}</h2>
  <p>Tell us whether you need a residential assessment, recurring monitoring, a managed-property inventory, treatment planning, or decline response. Email is opened in your device; sending remains under your control.</p></div>
  <div class="button-row"><a class="button" data-conversion="email-assessment" href="mailto:{EMAIL}?subject=SDPP%20Palm%20Assessment%20Inquiry">Email an inquiry</a><a class="button button-quiet" data-conversion="call" href="tel:2624923135">Call or text {PHONE}</a></div>
</section>"""


def footer(relative_root: str = "./") -> str:
    return f"""<footer class="site-footer">
  <div class="footer-grid">
    <div><a class="footer-brand" href="{relative_root}index.html">San Diego Palm Protection</a><p>Assessment, documentation, monitoring, protection, and response for significant palms across North County San Diego.</p></div>
    <div><h2>Services</h2><a href="{relative_root}residential-palm-assessment.html">Residential assessment</a><a href="{relative_root}quarterly-palm-care-san-diego.html">Recurring monitoring</a><a href="{relative_root}managed-property-palm-services.html">Managed properties</a></div>
    <div><h2>Resources</h2><a href="{relative_root}palm-proof-examples.html">Sample work</a><a href="{relative_root}palm-journal-new.html">Palm Journal</a><a href="{relative_root}palm-faq-san-diego.html">Palm FAQ</a><a href="{relative_root}report-a-palm.html">Report a palm</a></div>
  </div>
  {credentials("BUSINESS_CREDENTIALS_FOOTER")}
  <p class="footer-legal">Insurance does not guarantee outcomes. Findings and recommendations are limited by access, available evidence, and the documented scope.</p>
</footer>
<script src="{relative_root}site-assets/site.js" defer></script>"""


def page(*, filename: str, title: str, description: str, eyebrow: str, h1: str,
         lede: str, body: str, image: str = "background.jpg",
         relative_root: str = "./", extra_schema: dict | None = None) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  {head(title, description, filename, image, extra_schema=extra_schema, relative_root=relative_root)}
</head>
<body>
{header(relative_root)}
<main id="main">
  <section class="page-hero" style="--hero-image:url('{relative_root}{image}')">
    <div class="hero-inner"><p class="eyebrow">{escape(eyebrow)}</p><h1>{escape(h1)}</h1><p class="lede">{escape(lede)}</p>
    <div class="button-row"><a class="button" href="#request">Discuss your palms</a><a class="text-link" href="{relative_root}palm-proof-examples.html">See the public proof format</a></div></div>
  </section>
  <div class="trust-wrap">{credentials("BUSINESS_CREDENTIALS")}</div>
  {body}
  {inquiry(relative_root)}
</main>
{footer(relative_root)}
</body>
</html>
"""
