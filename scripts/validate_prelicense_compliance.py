from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "site-config" / "business_status.json"

PUBLIC_PATTERNS = ("*.html", "*.json")
PUBLIC_DIRS = [ROOT, ROOT / "palm-journal", ROOT / "journal-data", ROOT / "journal-data" / "articles"]

STATUS_NOTICE = (
    "San Diego Palm Protection currently focuses on palm documentation, "
    "photographic condition records, and educational resources."
)

REGULATED_SERVICE_FLAGS = (
    "pesticide_services_enabled",
    "tree_palm_contracting_enabled",
    "commercial_field_services_enabled",
)

READINESS_FIELDS = (
    "qal_issued_and_active",
    "pest_control_business_license_issued_and_active",
    "financial_responsibility_active",
    "workers_compensation_requirement_addressed",
    "county_registration_current",
    "equipment_registered_and_ready",
    "reporting_system_ready",
    "storage_transport_ppe_systems_ready",
    "label_sds_notice_consent_emergency_systems_ready",
    "owner_activation_approved",
)

PERMANENT_REQUIREMENTS = ("job_application_preflight_required",)


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    reason: str


RULES = [
    Rule(
        "booking_or_quote_for_disabled_field_service",
        re.compile(
            r"\b(schedule|book|appointment|request\s+(?:a\s+)?(?:quote|photographic condition review|service|visit)|ask\s+about|plan\s+questions)\b"
            r".{0,90}\b(treatment|pesticide|sapw|weevil|palm\s+care|quarterly|removal|installation|planting|pruning|property\s+visit|stewardship\s+visit)\b",
            re.I,
        ),
        "Prelicense mode cannot solicit booking, quotes, photographic condition reviews, or visits for unavailable field services.",
    ),
    Rule(
        "reverse_booking_or_quote_for_disabled_field_service",
        re.compile(
            r"\b(treatment|pesticide|sapw|weevil|palm\s+care|quarterly|removal|installation|planting|pruning|property\s+visit|stewardship\s+visit)\b"
            r".{0,90}\b(schedule|book|appointment|request\s+(?:a\s+)?(?:quote|photographic condition review|service|visit)|ask\s+about|plan\s+questions)\b",
            re.I,
        ),
        "Prelicense mode cannot solicit booking, quotes, photographic condition reviews, or visits for unavailable field services.",
    ),
    Rule(
        "price_for_disabled_field_service",
        re.compile(
            r"(\$\s*\d|starting\s+at|typical\s+investment|price(?:s|d|range|ing)?)"
            r".{0,120}\b(treatment|visit|quarterly|care\s+plan|photographic condition review|removal|installation|planting|pruning)\b"
            r"|\b(treatment|visit|quarterly|care\s+plan|photographic condition review|removal|installation|planting|pruning)\b.{0,120}"
            r"(\$\s*\d|starting\s+at|typical\s+investment|price(?:s|d|range|ing)?)",
            re.I,
        ),
        "Prelicense mode cannot publish pricing for unavailable regulated or field services.",
    ),
    Rule(
        "sdpp_pesticide_or_treatment_claim",
        re.compile(
            r"\b(SDPP|San Diego Palm Protection|owner)\b.{0,80}"
            r"\b(apply|spray|drench|treat|perform|provide|offer|protect|prevent|control)\w*\b.{0,80}"
            r"\b(Safari|dinotefuran|imidacloprid|bifenthrin|pesticide|insecticide|SAPW|weevil|treatment)\b",
            re.I,
        ),
        "Prelicense mode cannot claim SDPP performs pesticide treatment, prevention, or pest-control work.",
    ),
    Rule(
        "we_apply_pesticide_claim",
        re.compile(r"\bwe\b.{0,60}\b(apply|spray|drench|treat)\w*\b.{0,80}\b(Safari|dinotefuran|imidacloprid|bifenthrin|pesticide|insecticide|SAPW|weevil|treatment)\b", re.I),
        "Prelicense mode cannot claim SDPP performs pesticide treatment, prevention, or pest-control work.",
    ),
    Rule(
        "sdpp_tree_contracting_claim",
        re.compile(
            r"\b(SDPP|San Diego Palm Protection)\b.{0,80}"
            r"\b(remove|prune|trim|install|plant|coordinate|subcontract|grind)\w*\b.{0,80}"
            r"\b(palm|tree|stump|contractor|installation|removal|pruning|planting)\b",
            re.I,
        ),
        "Prelicense mode cannot claim SDPP performs or sells tree/palm contracting, removal, installation, or coordination.",
    ),
    Rule(
        "we_tree_contracting_claim",
        re.compile(r"\bwe\b.{0,60}\b(remove|prune|trim|install|plant|coordinate|subcontract|grind)\w*\b.{0,80}\b(palm|tree|stump|installation|removal|pruning|planting)\b", re.I),
        "Prelicense mode cannot claim SDPP performs or sells tree/palm contracting, removal, installation, or coordination.",
    ),
    Rule(
        "false_credential_claim",
        re.compile(r"\b(SDPP|San Diego Palm Protection|we|owner)\b.{0,80}\b(licensed|certified|insured|credentialed|authorized)\b", re.I),
        "No verified credential is configured; do not claim SDPP is licensed, certified, insured, or authorized.",
    ),
    Rule(
        "structured_data_offer_or_price",
        re.compile(r'"@type"\s*:\s*"(?:Offer|OfferCatalog)"|"price"\s*:|"priceRange"\s*:', re.I),
        "Offer, OfferCatalog, price, and priceRange structured data are disabled in prelicense mode.",
    ),
    Rule(
        "structured_data_disabled_service",
        re.compile(r'"@type"\s*:\s*"Service"|serviceType"\s*:', re.I),
        "Service structured data is disabled in prelicense mode to avoid implying unavailable field services.",
    ),
]

ALWAYS_BLOCK_RULES = [
    Rule(
        "monitoring_as_commercial_service",
        re.compile(r"\b(palm\s+monitoring|monitoring)\s+services?\s+(?:available|offered|provided|for\s+hire)\b|\bprofessional\s+(?:palm\s+)?monitoring\b", re.I),
        "Prelicense mode cannot present palm monitoring as a current commercial SDPP service.",
    ),
    Rule(
        "professional_inspection_solicitation",
        re.compile(r"\b(schedule|book|request)\b.{0,80}\bprofessional\s+(?:palm\s+)?inspection\b|\bprofessional\s+(?:palm\s+)?inspection\b.{0,80}\b(schedule|book|request)\b", re.I),
        "Prelicense mode cannot solicit professional inspections by SDPP.",
    ),
    Rule(
        "photo_based_treatment_recommendation",
        re.compile(r"\b(send|text|email|submit)\b.{0,80}\bphotos?\b.{0,100}\b(treatment|pesticide|chemical|insecticide)\s+recommendation\b", re.I),
        "Photo submission cannot be offered in exchange for treatment or pesticide recommendations.",
    ),
    Rule(
        "contingent_future_treatment_offer",
        re.compile(r"\b(treatment|sapw|pesticide|weevil)\b.{0,80}\b(waitlist|reserve|prebook|pre-book|deposit|coming\s+soon|after\s+licens(?:e|ing)|pending\s+licens(?:e|ing)|future\s+treatment)\b|\b(waitlist|reserve|prebook|pre-book|deposit|coming\s+soon|after\s+licens(?:e|ing)|pending\s+licens(?:e|ing)|future\s+treatment)\b.{0,80}\b(treatment|sapw|pesticide|weevil)\b", re.I),
        "Prelicense mode cannot solicit future, contingent, waitlisted, reserved, or post-licensing treatment work.",
    ),
    Rule(
        "site_specific_pesticide_prescription",
        re.compile(r"\b(prescribe|prescription|site-specific|specific)\b.{0,80}\b(pesticide|chemical|insecticide|treatment|Safari|dinotefuran|imidacloprid|bifenthrin)\b|\b(pesticide|chemical|insecticide|treatment|Safari|dinotefuran|imidacloprid|bifenthrin)\b.{0,80}\b(prescribe|prescription|site-specific)\b", re.I),
        "Prelicense mode cannot provide site-specific pesticide prescriptions or recommendations.",
    ),
]



FORBIDDEN_PUBLIC_PHRASES = (
    "every treatment is personally performed",
    "professional palm fertilization",
    "apply professional palm nutrition",
    "limited client roster",
    "quarterly care clients",
    "first-time customers",
    "enrolling in quarterly care",
    "we serve homeowners",
    "care handled consistently",
    "looked after year-round",
    "one-time palm photo review & treatment",
    "single professional visit",
    "approved production draft",
    "editorial review required",
    "approval required",
    "production draft",
    "unpublished",
    "internal note",
    "machine status",
    "fingerprint",
    "approval gate",
)

ALLOW_PATTERNS = [
    re.compile(r"not currently offered", re.I),
    re.compile(r"appropriately licensed|licensed provider|licensed tree contractor|qualified arborist|pest-control business", re.I),
    re.compile(r"education(?:al)?|documentation|field note|photographic|visible-condition|not a definitive diagnosis|not establish a diagnosis|photos alone|historical", re.I),
    re.compile(r"does not perform|not perform|not provide|not offered|not currently", re.I),
    re.compile(r"according to|reportedly|had recently been removed|was cut down", re.I),
    re.compile(r"not a substitute for formal arboricultural consulting|municipal determinations|laboratory testing", re.I),
    re.compile(r"serviceType\"\s*:\s*\"Canary Island Date Palm Risk Checklist", re.I),
]


def load_config(root: Path = ROOT) -> dict:
    path = root / "site-config" / "business_status.json"
    if not path.exists():
        raise FileNotFoundError(f"missing business status config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def iter_scan_files(root: Path = ROOT) -> list[Path]:
    files: set[Path] = set()
    for directory in PUBLIC_DIRS:
        if not directory.exists():
            continue
        for pattern in PUBLIC_PATTERNS:
            files.update(path for path in directory.glob(pattern) if path.is_file())
    return sorted(files)


def is_allowed(line: str) -> bool:
    return any(pattern.search(line) for pattern in ALLOW_PATTERNS)


def validate_text(text: str, rel: str) -> list[str]:
    diagnostics: list[str] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        compact = " ".join(line.strip().split())
        if not compact or "PRELICENSE_ALLOW" in compact:
            continue
        lower = compact.lower()
        for phrase in FORBIDDEN_PUBLIC_PHRASES:
            if phrase in lower:
                diagnostics.append(f"{rel}:{line_no}: forbidden_public_phrase: Public prelicense content cannot contain this current-service or internal workflow phrase: {phrase} :: {compact[:220]}")
        for rule in ALWAYS_BLOCK_RULES:
            if rule.pattern.search(compact):
                diagnostics.append(f"{rel}:{line_no}: {rule.name}: {rule.reason} :: {compact[:220]}")
        if is_allowed(compact):
            continue
        for rule in RULES:
            if rule.pattern.search(compact):
                diagnostics.append(f"{rel}:{line_no}: {rule.name}: {rule.reason} :: {compact[:220]}")
    return diagnostics


def validate_repository(root: Path = ROOT) -> list[str]:
    config = load_config(root)
    mode = config.get("mode")
    diagnostics = validate_config(config)
    if mode != "prelicense":
        return diagnostics
    for path in iter_scan_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        diagnostics.extend(validate_text(text, rel))
        if path.suffix.lower() == ".html":
            notice_count = text.count(STATUS_NOTICE)
            if notice_count > 1:
                diagnostics.append(f"{rel}: duplicate_prelicense_scope: prelicense scope notice appears {notice_count} times")
    index_path = root / "palm-journal-new.html"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8-sig", errors="replace")
        try:
            entries = json.loads((root / "journal-data" / "journal_entries.json").read_text(encoding="utf-8"))
            for entry in entries:
                if entry.get("public", True) is False and (entry.get("slug", "") in index_text or entry.get("legacy_anchor", "") in index_text):
                    diagnostics.append(f"palm-journal-new.html: held journal record is publicly rendered: {entry.get('slug')}")
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(f"journal-data/journal_entries.json: unable to verify held records: {exc}")
    return diagnostics


def validate_config(config: dict, rel: str = "site-config/business_status.json") -> list[str]:
    diagnostics: list[str] = []
    for field in REGULATED_SERVICE_FLAGS:
        if field not in config:
            diagnostics.append(f"{rel}: missing regulated service flag: {field}")
    for field in READINESS_FIELDS:
        if field not in config:
            diagnostics.append(f"{rel}: missing activation prerequisite: {field}")
    for field in PERMANENT_REQUIREMENTS:
        if field not in config:
            diagnostics.append(f"{rel}: missing permanent activation requirement: {field}")
        elif config.get(field) is not True:
            diagnostics.append(f"{rel}: permanent job/application preflight requirement must remain true: {field}")

    regulated_enabled = any(config.get(field) is True for field in REGULATED_SERVICE_FLAGS)
    if config.get("mode") == "prelicense" and regulated_enabled:
        diagnostics.append(f"{rel}: prelicense mode cannot enable pesticide, contracting, or commercial field services")
    if regulated_enabled:
        for field in READINESS_FIELDS:
            if config.get(field) is not True:
                diagnostics.append(f"{rel}: regulated services enabled before prerequisite is complete: {field}")
        if config.get("owner_activation_approved") is not True:
            diagnostics.append(f"{rel}: regulated services enabled without explicit owner activation approval")
    if config.get("qal_issued_and_active") is True and regulated_enabled:
        incomplete = [field for field in READINESS_FIELDS if config.get(field) is not True]
        if incomplete:
            diagnostics.append(f"{rel}: QAL issuance alone is not sufficient activation; incomplete prerequisites: {', '.join(incomplete)}")
    return diagnostics


def run_self_tests() -> int:
    fixtures = {
        "educational pesticide mention": ("This educational page explains dinotefuran and imidacloprid labels at a high level.", True),
        "historical treatment reference": ("Historical field note: the palm was treated twice before this observation.", True),
        "referral to licensed provider": ("Contact an appropriately licensed pest-control business for treatment options.", True),
        "schedule SAPW treatment": ("Schedule SAPW treatment with San Diego Palm Protection today.", False),
        "treatment price": ("Quarterly palm treatment starting at $500 per visit.", False),
        "We apply Safari": ("We apply Safari insecticide for South American palm weevil prevention.", False),
        "palm removal offer": ("San Diego Palm Protection can coordinate palm removal for your property.", False),
        "palm installation offer": ("We install specimen palms and planting upgrades.", False),
        "licensed and insured": ("San Diego Palm Protection is licensed and insured for palm treatment.", False),
        "prelicense notice": (STATUS_NOTICE + " Pesticide application and removal services are not currently offered.", True),
        "monitoring service": ("Palm monitoring services available for San Diego homeowners.", False),
        "professional inspection": ("Schedule a professional inspection for your Canary Island date palm.", False),
        "photos for treatment recommendation": ("Send photos for a treatment recommendation.", False),
        "sapw waitlist": ("Join the SAPW treatment waitlist.", False),
        "reserve after licensing": ("Reserve treatment after licensing is complete.", False),
        "site specific prescription": ("We can prescribe a site-specific pesticide treatment for this palm.", False),
        "historical visible record": ("This historical record documents visible changes over time.", True),
        "no photo diagnosis": ("Photographs do not establish a diagnosis.", True),
        "licensed provider evaluation": ("Contact an appropriately licensed provider for an in-person evaluation.", True),
        "educational monitoring techniques": ("This educational page explains general monitoring techniques for palms.", True),
        "educational pesticide labels": ("This educational page discusses pesticide labels and application methods generally.", True),
        "limited client roster": ("San Diego Palm Protection intentionally maintains a limited client roster.", False),
        "quarterly care clients": ("Our quarterly care clients receive direct attention.", False),
        "first time customers": ("Ideal for first-time customers enrolling in quarterly care.", False),
        "professional fertilization": ("Professional palm fertilization is included.", False),
        "apply nutrition": ("Apply professional palm nutrition to support growth.", False),
        "treatment personally performed": ("Every treatment is personally performed by the owner.", False),
        "internal editorial phrase": ("Legacy library reference; editorial review required before individual article migration.", False),
        "structured data service claim": ('{"@context":"https://schema.org","@type":"Service","serviceType":"SAPW treatment"}', False),
    }
    failed = []
    for name, (text, should_pass) in fixtures.items():
        passed = not validate_text(text, f"fixture:{name}")
        if passed != should_pass:
            failed.append(f"{name}: expected {should_pass}, got {passed}")
    base_config = {
        "mode": "prelicense",
        "pesticide_services_enabled": False,
        "tree_palm_contracting_enabled": False,
        "commercial_field_services_enabled": False,
        "qal_issued_and_active": False,
        "pest_control_business_license_issued_and_active": False,
        "financial_responsibility_active": False,
        "workers_compensation_requirement_addressed": False,
        "county_registration_current": False,
        "equipment_registered_and_ready": False,
        "reporting_system_ready": False,
        "storage_transport_ppe_systems_ready": False,
        "label_sds_notice_consent_emergency_systems_ready": False,
        "job_application_preflight_required": True,
        "owner_activation_approved": False,
    }
    config_fixtures = {
        "public prelicense config": (base_config, True),
        "workers compensation unresolved blocks activation": ({**base_config, "mode": "commercial", "pesticide_services_enabled": True, "workers_compensation_requirement_addressed": False, "owner_activation_approved": True}, False),
        "operating systems missing blocks activation": ({**base_config, "mode": "commercial", "pesticide_services_enabled": True, "qal_issued_and_active": True, "pest_control_business_license_issued_and_active": True, "financial_responsibility_active": True, "workers_compensation_requirement_addressed": True, "county_registration_current": True, "equipment_registered_and_ready": False, "reporting_system_ready": False, "storage_transport_ppe_systems_ready": False, "label_sds_notice_consent_emergency_systems_ready": False, "owner_activation_approved": True}, False),
        "job preflight disabled blocks activation": ({**base_config, "job_application_preflight_required": False}, False),
        "owner activation absent blocks activation": ({key: value for key, value in base_config.items() if key != "owner_activation_approved"}, False),
        "qal alone does not activate": ({**base_config, "mode": "commercial", "pesticide_services_enabled": True, "qal_issued_and_active": True}, False),
        "all prerequisites allow commercial flags": ({**base_config, "mode": "commercial", "pesticide_services_enabled": True, "qal_issued_and_active": True, "pest_control_business_license_issued_and_active": True, "financial_responsibility_active": True, "workers_compensation_requirement_addressed": True, "county_registration_current": True, "equipment_registered_and_ready": True, "reporting_system_ready": True, "storage_transport_ppe_systems_ready": True, "label_sds_notice_consent_emergency_systems_ready": True, "owner_activation_approved": True}, True),
    }
    for name, (config, should_pass) in config_fixtures.items():
        passed = not validate_config(config, f"fixture:{name}")
        if passed != should_pass:
            failed.append(f"{name}: expected {should_pass}, got {passed}")
    if failed:
        print("PRELICENSE_SELF_TEST_FAILED")
        for item in failed:
            print(f" - {item}")
        return 1
    print("PRELICENSE_SELF_TEST_OK")
    print(f"fixtures_checked={len(fixtures) + len(config_fixtures)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SDPP prelicense public website safeguards.")
    parser.add_argument("--self-test", action="store_true", help="run built-in fixture tests")
    args = parser.parse_args()
    if args.self_test:
        return run_self_tests()
    diagnostics = validate_repository(ROOT)
    if diagnostics:
        print("PRELICENSE_COMPLIANCE_FAILED")
        for item in diagnostics:
            print(f" - {item}")
        return 1
    print("PRELICENSE_COMPLIANCE_OK")
    print(f"files_checked={len(iter_scan_files(ROOT))}")
    print(f"mode={load_config(ROOT).get('mode')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
