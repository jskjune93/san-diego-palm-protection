"""Validate SDPP's sole supported production state: active commercial service."""

from __future__ import annotations

import argparse
import re
import sys

from validate_operational_status import FORBIDDEN, main as validate_operational_status


def has_obsolete_status(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in FORBIDDEN)


def run_self_test() -> int:
    allowed = (
        "San Diego Palm Protection provides pesticide treatment when appropriate.",
        "Treatment follows the pesticide label, applicable law, site conditions, and agreed scope.",
        "Some pruning, removal, or specialist work may require a different contractor or license.",
    )
    # Construct regression samples from tokens so obsolete public copy is not
    # retained as a reusable fixture or production variant.
    prohibited = tuple(" ".join(parts) for parts in (
        ("SDPP is not currently", "offering pesticide applications."),
        ("Pesticide application is", "not currently offered."),
        ("Regulated work must be discussed with an", "appropriately licensed treatment provider."),
        ("Documentation, monitoring, reporting, sourcing, and coordination", "are available now."),
        ("Production", "pre-license status."),
        ("The QAL does not establish", "business-level pesticide authorization."),
        ("Treatment must be performed by a", "third-party provider."),
        ("SDPP is awaiting", "its license."),
    ))
    failures = [text for text in allowed if has_obsolete_status(text)]
    failures.extend(text for text in prohibited if not has_obsolete_status(text))
    if failures:
        print("ACTIVE_LICENSE_SELF_TEST_FAILED")
        for failure in failures:
            print(f" - {failure}")
        return 1
    print("ACTIVE_LICENSE_SELF_TEST_OK")
    print(f"fixtures_checked={len(allowed) + len(prohibited)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SDPP active-license website safeguards.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    return run_self_test() if args.self_test else validate_operational_status()


if __name__ == "__main__":
    sys.exit(main())
