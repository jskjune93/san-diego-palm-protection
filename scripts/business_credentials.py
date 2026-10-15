from __future__ import annotations

from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "site-config" / "business_status.json"

REQUIRED_COMMERCIAL_FIELDS = (
    "qal_issued_and_active",
    "pest_control_business_license_issued_and_active",
    "financial_responsibility_active",
    "owner_activation_approved",
)
REQUIRED_PUBLIC_FIELDS = (
    "status_label",
    "service_summary",
    "business_license",
    "individual_license",
    "category",
    "insurance",
    "licensing_statement",
    "exact_status",
    "scope_note",
    "effective_date",
)
REQUIRED_SCOPE_FIELDS = (
    "primary_growth_path",
    "residential_path",
    "authority_path",
    "regulated_work_boundary",
    "excluded_direct_work",
    "outcome_boundary",
)


def load_business_status() -> dict:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    mode = status.get("mode")
    if mode != "commercial":
        raise ValueError("Production business status must remain commercial; no alternate production mode is supported.")
    missing_active = [field for field in REQUIRED_COMMERCIAL_FIELDS if status.get(field) is not True]
    if missing_active:
        raise ValueError(f"Public credential claims are blocked; inactive fields: {', '.join(missing_active)}")
    qualification = status.get("individual_qualification") or {}
    business_license = status.get("business_license") or {}
    owner = status.get("owner") or {}
    insurance = status.get("insurance") or {}
    operating_scope = status.get("operating_scope") or {}
    if (
        qualification.get("license_number") != "175295"
        or qualification.get("category_code") != "B"
        or qualification.get("category_name") != "Landscape Maintenance"
        or qualification.get("issued_and_active") is not True
        or status.get("qal_issued_and_active") is not True
    ):
        raise ValueError("Authoritative individual QAL configuration is incomplete or inconsistent.")
    if (
        business_license.get("license_number") != "47756"
        or business_license.get("issued_and_active") is not True
        or status.get("pest_control_business_license_issued_and_active") is not True
    ):
        raise ValueError("Authoritative Pest Control Business License configuration is incomplete or inconsistent.")
    if owner.get("name") != "John Krause" or owner.get("owner_operated") is not True:
        raise ValueError("Authoritative owner configuration is incomplete.")
    if insurance.get("insured") is not True or status.get("financial_responsibility_active") is not True:
        raise ValueError("Authoritative insurance configuration is incomplete or inconsistent.")
    missing_scope = [field for field in REQUIRED_SCOPE_FIELDS if not operating_scope.get(field)]
    if missing_scope:
        raise ValueError(f"Authoritative operating scope is incomplete: {', '.join(missing_scope)}")
    credentials = status.get("public_credentials") or {}
    missing_public = [field for field in REQUIRED_PUBLIC_FIELDS if not credentials.get(field)]
    if missing_public:
        raise ValueError(f"Public credential wording is incomplete: {', '.join(missing_public)}")
    return status


def public_credentials() -> dict[str, str]:
    return load_business_status()["public_credentials"]


def render_credential_block(marker: str = "BUSINESS_CREDENTIALS") -> str:
    credentials = public_credentials()
    return (
        f'<!-- {marker}:START -->\n'
        '<div class="business-credentials" aria-label="Owner qualification and current business service status">\n'
        f'  <p class="business-credentials__label">{escape(credentials["status_label"])}</p>\n'
        f'  <p class="business-credentials__summary">{escape(credentials["service_summary"])}</p>\n'
        f'  <p class="business-credentials__credential">{escape(credentials["business_license"])}<br>{escape(credentials["individual_license"])}<br>{escape(credentials["category"])}<br><strong>{escape(credentials["insurance"])}</strong></p>\n'
        f'  <p class="business-credentials__note">{escape(credentials["scope_note"])}</p>\n'
        '</div>\n'
        f'<!-- {marker}:END -->'
    )


def render_compact_credential_block(marker: str = "BUSINESS_CREDENTIALS") -> str:
    credentials = public_credentials()
    return (
        f'<!-- {marker}:START -->\n'
        '<div class="business-credentials business-credentials--strip" aria-label="Owner qualification and current business service status">\n'
        f'  <p class="business-credentials__label">{escape(credentials["status_label"])}</p>\n'
        f'  <p class="business-credentials__summary">{escape(credentials["service_summary"])}</p>\n'
        '  <p class="business-credentials__credential">'
        f'<span>{escape(credentials["business_license"])}</span>'
        f'<span>{escape(credentials["individual_license"])}</span>'
        f'<span>{escape(credentials["category"])}</span>'
        f'<strong>{escape(credentials["insurance"])}</strong></p>\n'
        f'  <p class="business-credentials__note">{escape(credentials["scope_note"])}</p>\n'
        '</div>\n'
        f'<!-- {marker}:END -->'
    )


def render_homepage_credential_block() -> str:
    credentials = public_credentials()
    owner = load_business_status()["owner"]["name"]
    return (
        '<!-- BUSINESS_CREDENTIALS:START -->\n'
        '<div class="business-credentials business-credentials--strip business-credentials--homepage" aria-label="Owner qualification and current business service status">\n'
        f'  <p class="business-credentials__label">{escape(credentials["status_label"])}</p>\n'
        '  <p class="business-credentials__credential">'
        f'<strong>{escape(owner)}, Owner</strong>'
        f'<span>{escape(credentials["business_license"])}</span>'
        f'<span>{escape(credentials["individual_license"])}</span>'
        f'<span>{escape(credentials["category"])}</span>'
        f'<strong>{escape(credentials["insurance"])}</strong></p>\n'
        '</div>\n'
        '<!-- BUSINESS_CREDENTIALS:END -->'
    )


def render_about_credential_block() -> str:
    credentials = public_credentials()
    owner = load_business_status()["owner"]["name"]
    return (
        '<!-- BUSINESS_CREDENTIALS:START -->\n'
        '<div class="business-credentials business-credentials--strip business-credentials--about" aria-label="John Krause qualification and insurance">\n'
        '  <p class="business-credentials__label">Qualifications</p>\n'
        '  <p class="business-credentials__credential">'
        f'<strong>{escape(owner)}, Owner</strong>'
        f'<span>{escape(credentials["business_license"])}</span>'
        f'<span>{escape(credentials["individual_license"])}</span>'
        f'<span>{escape(credentials["category"])}</span>'
        f'<strong>{escape(credentials["insurance"])}</strong></p>\n'
        f'  <p class="business-credentials__detail">{escape(credentials["service_summary"])}</p>\n'
        '</div>\n'
        '<!-- BUSINESS_CREDENTIALS:END -->'
    )


def footer_line() -> str:
    return escape(public_credentials()["licensing_statement"])


def government_buyer_block() -> str:
    status = load_business_status()
    cert = status["state_certification"]
    return f'''<section class="section section-tint" id="government-buyers" aria-labelledby="government-buyers-heading">
  <div class="section-intro"><p class="eyebrow">Government &amp; institutional services</p><h2 id="government-buyers-heading">A palm specialist for your property or project.</h2><p>I work directly with the palms: reviewing visible condition, carrying out appropriate licensed treatment, and keeping dated photographs and service records. Send me the site, palm count, required work and procurement schedule.</p></div>
  <div class="service-lines"><article><h3>California certified</h3><p>{escape(cert["legal_name"])}<br>{escape(cert["programs"])}<br>Certification ID {escape(cert["certification_id"])}<br>Approved through {escape(cert["expires"])}</p><p><a href="https://caleprocure.ca.gov/pages/PublicSearch/supplier-search.aspx">Verify in Cal eProcure</a> using the certification ID.</p></article><article><h3>What I perform</h3><p>Palm assessments, visible-condition monitoring, photographic records, preventive SAPW protection and appropriate pesticide treatment within the agreed Category B scope.</p><p>When removal, pruning or replacement needs another contractor, I can help coordinate the next step. The proposal identifies who performs each part.</p></article><article><h3>Location and availability</h3><p>{escape(status["government_service_area"])}</p><p>Contact John Krause: <a href="mailto:sandiegopalmprotection@gmail.com">sandiegopalmprotection@gmail.com</a> or <a href="tel:2624923135">262-492-3135</a>.</p></article></div>
  <div class="button-row"><a class="button" href="./SDPP-Commercial-Palm-Stewardship.pdf" target="_blank" rel="noopener noreferrer">View capability overview <span class="sr-only">(PDF, opens in a new tab)</span></a><a class="button" href="./palm-proof-examples.html">Review Field Work</a><a href="./san-diego-palm-protection-sample-assessment.pdf" target="_blank" rel="noopener noreferrer">View a public documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a></div>
  <p class="note">{escape(status["operating_scope"]["regulated_work_boundary"])}</p>
</section>'''
