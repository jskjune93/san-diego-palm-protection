from __future__ import annotations

from html import escape
from hashlib import sha256
from pathlib import Path
import json

from business_credentials import (
    load_business_status,
    render_about_credential_block,
    render_compact_credential_block,
    render_credential_block,
    render_homepage_credential_block,
    public_credentials,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.sandiegopalmprotection.com"
PHONE = "262-492-3135"
EMAIL = "sandiegopalmprotection@gmail.com"
CUSTOMER_MAP = "images/palm-journal/where-we-care-for-palms-october-2026/sdpp-customer-map-2026-10-03.webp"
INQUIRY = json.loads((ROOT / "site-config" / "inquiry.json").read_text(encoding="utf-8"))

def species_reference_gallery(relative_root: str = "./") -> str:
    """Show priority palms with provenance stated for each photograph."""
    return f'''<div class="species-reference-gallery" aria-label="Canary Island date, Chilean wine, and Bismarck palm photographs">
  <figure class="species-reference-gallery__lead"><img src="{relative_root}mansion_healthy_cidp_poway_three.jpg" alt="Mature Canary Island date palms with complete crowns visible in a Poway property landscape" loading="lazy" decoding="async"><figcaption><strong>Canary Island date palm</strong><span>Photographed by SDPP in San Diego County.</span></figcaption></figure>
  <div class="species-reference-gallery__support" aria-label="Supporting species references">
    <figure><img src="{relative_root}images/species-reference/chilean-wine-palm-california.webp" alt="Grove of mature Chilean wine palms with complete crowns visible in a cultivated landscape" loading="lazy" decoding="async" width="1800" height="1198"><figcaption><strong>Chilean wine palm</strong><span>Species reference.</span></figcaption></figure>
    <figure><img src="{relative_root}images/species-reference/bismarck-crown-property-october-2026.webp" alt="Silver Bismarck palm with its complete crown visible in a San Diego County residential landscape" loading="lazy" decoding="async" width="1600" height="1200"><figcaption><strong>Bismarck palm</strong><span>Photographed by SDPP in San Diego County.</span></figcaption></figure>
  </div>
</div>
<p class="species-reference-credit">Chilean wine palm reference photograph: <a href="https://commons.wikimedia.org/wiki/File:Jubaea_chilensis_kz05.jpg" target="_blank" rel="noopener noreferrer">Krzysztof Ziarnek, Kenraiz</a> (<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>); resized for web. Canary Island date and Bismarck palm photographs by SDPP.</p>'''


def asset_version(path: str) -> str:
    return sha256((ROOT / path).read_bytes()).hexdigest()[:12]


def customer_map(relative_root: str = "./") -> str:
    """Reuse the existing maintained map; never create a per-page copy."""
    return f'''<section class="section customer-map-section" id="sdpp-customer-map" aria-labelledby="customer-map-heading">
  <div class="section-intro"><h2 id="customer-map-heading">Where we treat for palm weevil</h2><p>San Diego County</p></div>
  <figure><a href="{relative_root}{CUSTOMER_MAP}" aria-label="View the SDPP treatment map at full size"><img src="{relative_root}{CUSTOMER_MAP}" alt="San Diego County map with yellow dots showing SDPP palm weevil treatment locations" width="2000" height="1440" loading="lazy" decoding="async"></a></figure>
</section>'''


def asset_prefix(relative_root: str) -> str:
    return relative_root


def head(title: str, description: str, path: str, image: str = "Old-Escondido_full-CIDP.jpg",
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
        "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "/#website", "name": "San Diego Palm Protection", "alternateName": "SDPP", "url": BASE_URL},
        "publisher": {
            "@type": "Organization",
            "@id": BASE_URL + "/#business",
            "name": "San Diego Palm Protection",
            "url": BASE_URL,
            "description": credential["licensing_statement"],
        },
    }]
    if path == "index.html":
        schemas.extend([
            {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE_URL + "/#website",
             "url": BASE_URL + "/", "name": "San Diego Palm Protection", "alternateName": "SDPP"},
            {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE_URL + "/#business",
             "name": "San Diego Palm Protection", "alternateName": "SDPP", "legalName": "San Diego Palm Protection LLC",
             "url": BASE_URL + "/", "logo": BASE_URL + "/logo.png", "image": image_url,
             "telephone": "+1-262-492-3135", "email": EMAIL,
             "description": description, "areaServed": ["San Diego County", "North County San Diego", "Escondido"],
             "founder": {"@type": "Person", "name": "John Krause", "url": BASE_URL + "/about.html"}}
        ])
    if path != "index.html":
        schemas.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": canonical},
            ],
        })
    if extra_schema and (load_business_status()["mode"] == "commercial" or publish_extra_schema):
        schemas.append(extra_schema)
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
{('<meta name="google-site-verification" content="j22OLD5tPSCDJbZptb41c_NojwR6N0oC3p0H2yoK0Ck">' if path == 'index.html' else '')}
  <meta name="business-status" content="{escape(credential["status_label"])}">
  <meta name="business-credentials" content="{escape(credential["licensing_statement"])}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{image_url}">
  <link rel="icon" href="{relative_root}logo.png" type="image/png">
  <link rel="stylesheet" href="{relative_root}site-assets/site.css?v={asset_version('site-assets/site.css')}">
  <link rel="stylesheet" href="{relative_root}site-assets/credentials.css?v={asset_version('site-assets/credentials.css')}">
  <script type="application/ld+json">{json.dumps(schemas, ensure_ascii=False)}</script>
  <!-- SDPP analytics integration point: existing measurement configuration is preserved; no identifier is invented here. -->"""


def header(relative_root: str = "./", residential_primary: bool = False) -> str:
    action_label = "Request Assessment"
    action_anchor = "homeowner-inquiry"
    action_event = "homeowner-inquiry-initiation"
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
      <a href="{relative_root}palm-proof-examples.html">Field Work</a>
      <a href="{relative_root}palm-journal-new.html">Palm Journal</a>
      <a href="{relative_root}about.html">About</a>
      <a class="nav-phone" data-conversion="call" href="tel:2624923135">Call or Text</a>
      <a class="button button-small" data-conversion="{action_event}" href="{relative_root}palm-records-monitoring-verification.html#{action_anchor}">{action_label}</a>
    </nav>
  </div>
</header>"""


def credentials(marker: str) -> str:
    return render_credential_block(marker)


def compact_credentials(marker: str) -> str:
    return render_compact_credential_block(marker)


def homepage_credentials() -> str:
    return render_homepage_credential_block()


def about_credentials() -> str:
    return render_about_credential_block()


def stewardship_functions(relative_root: str = "./") -> str:
    items = [
        ("01", "Stewardship & Palm Health", "The overall relationship: palm identities, priorities, recurring care, service history, planning, and direct owner involvement across the property.", "palm-records-monitoring-verification.html"),
        ("02", "Protection & Treatment", "Preventive protection, South American palm weevil awareness, treatment when appropriate, and early response to visible decline.", "palm-stewardship-plans.html"),
        ("03", "Documentation & Portfolio Management", "Palm inventories, condition records, photographs, treatment and work history, recurring schedules, and budgeting support.", "palm-records-monitoring-verification.html"),
        ("04", "Response, Removal & Renewal", "Decline response, pruning or removal coordination, replacement planning, sourcing, and long-term landscape continuity.", "palm-removal-coordination.html"),
    ]
    return '<div class="pillar-grid pillar-grid--4">' + "".join(
        f'<article class="pillar"><span>{n}</span><h3>{escape(t)}</h3><p>{escape(d)}</p><a href="{relative_root}{href}">Explore this service</a></article>'
        for n, t, d, href in items
    ) + "</div>"


def three_pillars(relative_root: str = "./") -> str:
    """Backward-compatible name for the shared stewardship model."""
    return stewardship_functions(relative_root)


def inquiry(relative_root: str = "./", residential_primary: bool = False) -> str:
    heading = "Request an on-site palm assessment." if residential_primary else "Discuss a property or palm stewardship plan."
    description = (
        "Tell me what you are seeing and what you need to decide. I work with homeowners protecting important mature palms."
        if residential_primary else
        "Tell me about the property, the palms, and what you are responsible for. I work with managed palm portfolios, large estates, and homeowners protecting important mature palms."
    )
    primary = f'<a class="button" data-conversion="organization-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#organization-inquiry">Discuss Your Palm Portfolio</a>'
    secondary = f'<a class="button button-quiet" data-conversion="homeowner-inquiry-initiation" href="{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry">Homeowner Inquiry</a>'
    if residential_primary:
        primary, secondary = secondary.replace("button button-quiet", "button").replace("Homeowner Inquiry", "Request a Palm Assessment"), primary.replace('class="button"', 'class="button button-quiet"')
    return f"""<section class="conversion-band" id="request" aria-labelledby="request-heading">
  <div><p class="eyebrow">Private inquiry</p><h2 id="request-heading">{escape(heading)}</h2>
  <p>{description}</p></div>
  <div class="button-row">{primary}{secondary}<a class="text-link" data-conversion="call" href="tel:2624923135">Call or Text {PHONE}</a></div>
</section>"""


def footer(relative_root: str = "./", residential_primary: bool = False) -> str:
    licensing_statement = escape(public_credentials()["licensing_statement"])
    return f"""<footer class="site-footer">
  <div class="footer-grid">
    <div><a class="footer-brand" href="{relative_root}index.html">San Diego Palm Protection</a><p>Owner-led South American palm weevil prevention, licensed treatment, and continuing care in San Diego County.</p></div>
    <div><h2>Services</h2><a href="{relative_root}jacksonville-palm-health.html">Jacksonville-area inquiries</a><a href="{relative_root}palm-records-monitoring-verification.html">All palm services</a><a href="{relative_root}south-american-palm-weevil-treatment-san-diego.html">Palm weevil prevention &amp; treatment</a><a href="{relative_root}quarterly-palm-care-san-diego.html">Recurring stewardship</a><a href="{relative_root}urban-forest-palm-documentation.html">Urban forest support</a></div>
    <div><h2>Resources</h2><a href="{relative_root}sapw.html">SAPW &amp; CIDP Photos</a><a href="{relative_root}about.html">About</a><a href="{relative_root}palm-proof-examples.html">Field work</a><a href="{relative_root}palm-journal-new.html">Palm Journal</a><a href="{relative_root}palm-faq-san-diego.html">Palm FAQ</a><a href="{relative_root}report-a-palm.html">Report a palm</a></div>
  </div>
  <p class="footer-service-areas">Based in Old Escondido · Serving North County and San Diego County. <a href="{relative_root}palm-care-escondido.html">Escondido palm care</a> · <a href="{relative_root}palm-care-poway.html">Poway palm care</a> · <a href="{relative_root}palm-care-rancho-santa-fe.html">Rancho Santa Fe palm care</a></p>
  <p class="footer-legal">{licensing_statement}</p>
</footer>
<script src="{relative_root}site-assets/site.js?v={asset_version('site-assets/site.js')}" defer></script>
{mobile_contact(relative_root, residential_primary)}"""


def mobile_contact(relative_root: str = "./", residential_primary: bool = False) -> str:
    action_label = "Request Assessment" if residential_primary else "Discuss Your Palms"
    action_anchor = "homeowner-inquiry" if residential_primary else "organization-inquiry"
    action_event = "homeowner-inquiry-initiation" if residential_primary else "organization-inquiry-initiation"
    return f"""<aside class="mobile-contact-bar" aria-label="Quick contact">
  <a data-conversion="call" href="tel:2624923135">Call or Text</a>
  <a data-conversion="{action_event}" href="{relative_root}palm-records-monitoring-verification.html#{action_anchor}">{action_label}</a>
</aside>"""


def page(*, filename: str, title: str, description: str, eyebrow: str, h1: str,
         lede: str, body: str, image: str = "Old-Escondido_full-CIDP.jpg",
         hero_position: str = "center center", hero_position_mobile: str | None = None,
         relative_root: str = "./", extra_schema: dict | None = None,
         publish_extra_schema: bool = False) -> str:
    public = public_credentials()
    hero_note = ""
    hero_trust = ""
    residential_trust = (
        '<p class="hero-trust-line">Your assessment is completed by John Krause, owner of San Diego Palm Protection and holder of '
        f'{escape(public["business_license"])} and {escape(public["individual_license"])}, {escape(public["category"])}. <strong>{escape(public["insurance"])}</strong></p>'
        if filename == "residential-palm-assessment.html" else ""
    )
    residential_page = filename in {
        "index.html", "residential-palm-assessment.html", "palm-records-monitoring-verification.html", "sapw.html",
        "south-american-palm-weevil-treatment-san-diego.html",
        "palm-stewardship-plans.html", "quarterly-palm-care-san-diego.html",
        "canary-island-date-palm-care-san-diego.html", "palm-care-escondido.html",
        "palm-care-poway.html", "palm-care-rancho-santa-fe.html",
    }
    organization_page = not residential_page
    primary_href = f"{relative_root}palm-records-monitoring-verification.html#{'homeowner-inquiry' if residential_page else 'organization-inquiry'}"
    primary_label = "Request a Palm Assessment" if residential_page else "Discuss Your Palm Portfolio"
    primary_event = "homeowner-inquiry-initiation" if residential_page else "organization-inquiry-initiation"
    if filename == "index.html":
        primary_href = f"{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry"
        primary_label = "Request a Palm Assessment"
        primary_event = "homeowner-inquiry-initiation"
        secondary_action = f'<a class="button button-quiet" data-conversion="call" href="tel:2624923135">Call or Text {PHONE}</a><a class="text-link" href="{relative_root}palm-proof-examples.html">View Field Work</a>'
    else:
        secondary_action = f'<a class="button button-quiet" data-conversion="call" href="tel:2624923135">Call or Text {PHONE}</a>'
    report_page = filename == "report-a-palm.html"
    if report_page:
        primary_href = "https://sdpp-community-palm-map.san-diego-pa-2324.chatgpt.site/?report=1"
        primary_label = "Report a palm"
        primary_event = "palm-report-map-open"
        secondary_action = ""
    if filename == "palm-removal-coordination.html":
        primary_href = f"{relative_root}palm-records-monitoring-verification.html#homeowner-inquiry"
        primary_label = "Discuss a removal"
        primary_event = "removal-inquiry-initiation"
    inquiry_band = "" if filename in {"palm-records-monitoring-verification.html", "report-a-palm.html"} else "  " + inquiry(relative_root, residential_page)
    if filename == "index.html":
        page_variant = "home"
    elif filename == "about.html":
        page_variant = "profile"
    elif filename == "palm-proof-examples.html":
        page_variant = "evidence"
    elif filename == "specimen-palms-cycads.html":
        page_variant = "species"
    else:
        page_variant = "service"
    main_classes = f"site-main site-main--{page_variant}"
    if filename == "index.html":
        main_classes += " homepage-content"
    credential_rail = ""
    if not report_page:
        credential_block = homepage_credentials() if filename == "index.html" else (
            about_credentials() if filename == "about.html" else compact_credentials("BUSINESS_CREDENTIALS")
        )
        credential_rail = f'  <div class="trust-wrap trust-wrap--compact trust-wrap--{page_variant}">{credential_block}</div>'
    return f"""<!doctype html>
<html lang="en">
<head>
  {head(title, description, filename, image, extra_schema=extra_schema, relative_root=relative_root, publish_extra_schema=publish_extra_schema)}
</head>
<body>
{header(relative_root, residential_page)}
<main id="main" class="{main_classes}">
  <section class="page-hero page-hero--{page_variant}" style="--hero-image:url('/{image}');--hero-position:{escape(hero_position)};--hero-position-mobile:{escape(hero_position_mobile or hero_position)}">
    <div class="hero-inner"><div class="hero-copy"><p class="eyebrow">{escape(eyebrow)}</p><h1>{escape(h1)}</h1><p class="lede">{escape(lede)}</p>{hero_note}{hero_trust}{residential_trust}
    <div class="button-row"><a class="button" data-conversion="{primary_event}" href="{primary_href}">{primary_label}</a>{secondary_action}</div></div></div>
  </section>
{credential_rail}
  {body}
{inquiry_band}
</main>
{footer(relative_root, residential_page)}
</body>
</html>
"""
