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


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    reason: str


RULES = [
    Rule(
        "booking_or_quote_for_disabled_field_service",
        re.compile(
            r"\b(schedule|book|appointment|request\s+(?:a\s+)?(?:quote|assessment|service|visit)|ask\s+about|plan\s+questions)\b"
            r".{0,90}\b(treatment|pesticide|sapw|weevil|palm\s+care|quarterly|removal|installation|planting|pruning|property\s+visit|stewardship\s+visit)\b",
            re.I,
        ),
        "Prelicense mode cannot solicit booking, quotes, assessments, or visits for unavailable field services.",
    ),
    Rule(
        "reverse_booking_or_quote_for_disabled_field_service",
        re.compile(
            r"\b(treatment|pesticide|sapw|weevil|palm\s+care|quarterly|removal|installation|planting|pruning|property\s+visit|stewardship\s+visit)\b"
            r".{0,90}\b(schedule|book|appointment|request\s+(?:a\s+)?(?:quote|assessment|service|visit)|ask\s+about|plan\s+questions)\b",
            re.I,
        ),
        "Prelicense mode cannot solicit booking, quotes, assessments, or visits for unavailable field services.",
    ),
    Rule(
        "price_for_disabled_field_service",
        re.compile(
            r"(\$\s*\d|starting\s+at|typical\s+investment|price(?:s|d|range|ing)?)"
            r".{0,120}\b(treatment|visit|quarterly|care\s+plan|assessment|removal|installation|planting|pruning)\b"
            r"|\b(treatment|visit|quarterly|care\s+plan|assessment|removal|installation|planting|pruning)\b.{0,120}"
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


ALLOW_PATTERNS = [
    re.compile(r"not currently offered", re.I),
    re.compile(r"appropriately licensed|licensed provider|licensed tree contractor|qualified arborist|pest-control business", re.I),
    re.compile(r"education(?:al)?|documentation|field note|photographic|visible-condition|not a diagnosis|photos alone|historical", re.I),
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
        if is_allowed(compact):
            continue
        for rule in RULES:
            if rule.pattern.search(compact):
                diagnostics.append(f"{rel}:{line_no}: {rule.name}: {rule.reason} :: {compact[:220]}")
    return diagnostics


def validate_repository(root: Path = ROOT) -> list[str]:
    config = load_config(root)
    mode = config.get("mode")
    if mode != "prelicense":
        return []
    diagnostics: list[str] = []
    if config.get("pesticide_services_enabled") or config.get("tree_palm_contracting_enabled") or config.get("commercial_field_services_enabled"):
        diagnostics.append("site-config/business_status.json: prelicense mode cannot enable pesticide, contracting, or commercial field services")
    for path in iter_scan_files(root):
        rel = path.relative_to(root).as_posix()
        diagnostics.extend(validate_text(path.read_text(encoding="utf-8-sig", errors="replace"), rel))
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
    }
    failed = []
    for name, (text, should_pass) in fixtures.items():
        passed = not validate_text(text, f"fixture:{name}")
        if passed != should_pass:
            failed.append(f"{name}: expected {should_pass}, got {passed}")
    if failed:
        print("PRELICENSE_SELF_TEST_FAILED")
        for item in failed:
            print(f" - {item}")
        return 1
    print("PRELICENSE_SELF_TEST_OK")
    print(f"fixtures_checked={len(fixtures)}")
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
