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
    "individual_license",
    "category",
    "insurance",
    "exact_status",
    "scope_note",
    "effective_date",
)


def load_business_status() -> dict:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    mode = status.get("mode")
    if mode not in {"prelicense", "commercial"}:
        raise ValueError("Business status mode must be prelicense or commercial.")
    if mode == "commercial":
        missing_active = [field for field in REQUIRED_COMMERCIAL_FIELDS if status.get(field) is not True]
        if missing_active:
            raise ValueError(f"Public credential claims are blocked; inactive fields: {', '.join(missing_active)}")
    elif status.get("pest_control_business_license_issued_and_active") is not False or status.get("owner_activation_approved") is not False:
        raise ValueError("Prelicense status cannot represent business-level pesticide authorization or owner activation as active.")
    qualification = status.get("individual_qualification") or {}
    owner = status.get("owner") or {}
    insurance = status.get("insurance") or {}
    if (
        qualification.get("license_number") != "175295"
        or qualification.get("category_code") != "B"
        or qualification.get("category_name") != "Landscape Maintenance"
        or qualification.get("issued_and_active") is not True
        or status.get("qal_issued_and_active") is not True
    ):
        raise ValueError("Authoritative individual QAL configuration is incomplete or inconsistent.")
    if owner.get("name") != "John Krause" or owner.get("owner_operated") is not True:
        raise ValueError("Authoritative owner configuration is incomplete.")
    if insurance.get("insured") is not True or status.get("financial_responsibility_active") is not True:
        raise ValueError("Authoritative insurance configuration is incomplete or inconsistent.")
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
        f'  <p class="business-credentials__credential">{escape(credentials["individual_license"])}<br>{escape(credentials["category"])}<br><strong>{escape(credentials["insurance"])}</strong></p>\n'
        f'  <p class="business-credentials__detail">{escape(credentials["exact_status"])}</p>\n'
        f'  <p class="business-credentials__note">{escape(credentials["scope_note"])}</p>\n'
        '</div>\n'
        f'<!-- {marker}:END -->'
    )


def render_homepage_credential_block() -> str:
    credentials = public_credentials()
    owner = load_business_status()["owner"]["name"]
    return (
        '<!-- BUSINESS_CREDENTIALS:START -->\n'
        '<div class="business-credentials business-credentials--homepage" aria-label="Owner qualification and current business service status">\n'
        '  <p class="business-credentials__label">Qualified, insured, and owner-led</p>\n'
        f'  <p class="business-credentials__credential"><strong>{escape(owner)}, Owner</strong><br>{escape(credentials["individual_license"])}<br>{escape(credentials["category"])}<br>{escape(credentials["insurance"])}</p>\n'
        f'  <p class="business-credentials__detail"><strong>Current service scope:</strong> Assessment, documentation, monitoring, reporting, sourcing, and coordination are available now. {escape(credentials["exact_status"])}</p>\n'
        '</div>\n'
        '<!-- BUSINESS_CREDENTIALS:END -->'
    )


def render_about_credential_block() -> str:
    credentials = public_credentials()
    owner = load_business_status()["owner"]["name"]
    return (
        '<!-- BUSINESS_CREDENTIALS:START -->\n'
        '<div class="business-credentials business-credentials--about" aria-label="John Krause qualification and insurance">\n'
        '  <p class="business-credentials__label">Qualifications</p>\n'
        f'  <p class="business-credentials__credential"><strong>{escape(owner)}</strong><br>Owner, San Diego Palm Protection<br>{escape(credentials["individual_license"])}<br>{escape(credentials["category"])}<br>{escape(credentials["insurance"])}</p>\n'
        "  <p class=\"business-credentials__detail\">The license shown is John Krause's individual credential. It is not a Pest Control Business License.</p>\n"
        '</div>\n'
        '<!-- BUSINESS_CREDENTIALS:END -->'
    )


def footer_line() -> str:
    return escape(public_credentials()["exact_status"])
