from __future__ import annotations

from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "site-config" / "business_status.json"

REQUIRED_ACTIVE_FIELDS = (
    "qal_issued_and_active",
    "pest_control_business_license_issued_and_active",
    "financial_responsibility_active",
    "owner_activation_approved",
)
REQUIRED_PUBLIC_FIELDS = (
    "status_label",
    "service_summary",
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
        missing_active = [field for field in REQUIRED_ACTIVE_FIELDS if status.get(field) is not True]
        if missing_active:
            raise ValueError(f"Public credential claims are blocked; inactive fields: {', '.join(missing_active)}")
    elif any(status.get(field) is True for field in REQUIRED_ACTIVE_FIELDS):
        raise ValueError("Prelicense status cannot represent license, QAL, insurance, or owner activation as active.")
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
        '<div class="business-credentials" aria-label="Current business service status">\n'
        f'  <p class="business-credentials__label">{escape(credentials["status_label"])}</p>\n'
        f'  <p class="business-credentials__summary">{escape(credentials["service_summary"])}</p>\n'
        f'  <p class="business-credentials__detail">{escape(credentials["exact_status"])}</p>\n'
        f'  <p class="business-credentials__note">{escape(credentials["scope_note"])}</p>\n'
        '</div>\n'
        f'<!-- {marker}:END -->'
    )


def footer_line() -> str:
    return escape(public_credentials()["exact_status"])
