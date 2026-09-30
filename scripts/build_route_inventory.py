from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CORE_ROLES = {
    "index.html": ("restructured", "Commercial orientation and three-pillar gateway"),
    "about.html": ("created", "Owner identity, qualifications, field process, and trust"),
    "urban-forest-palm-documentation.html": ("created", "Municipal, public-agency, institutional, and urban-forest palm documentation support"),
    "palm-proof-examples.html": ("created", "Approved sanitized proof presentation and privacy boundary"),
    "palm-records-monitoring-verification.html": ("restructured", "Canonical service overview and inquiry"),
    "quarterly-palm-care-san-diego.html": ("restructured", "Annual mature-palm protection and recurring treatment pathway; URL preserved"),
    "palm-removal-coordination.html": ("restructured", "Decline, removal, documented loss, and replacement pathway"),
    "palm-stewardship-plans.html": ("restructured", "Protection and treatment planning"),
    "report-a-palm.html": ("restructured", "Permissioned private observation handoff"),
    "sapw.html": ("restructured", "SAPW education, risk, and assessment gateway"),
    "south-american-palm-weevil-treatment-san-diego.html": ("consolidated in place", "Treatment-specific discovery route into canonical protection pathway"),
    "canary-island-date-palm-care-san-diego.html": ("restructured", "Species-specific discovery route"),
    "cidp-risk-checklist.html": ("restructured", "Educational observation checklist"),
    "old-escondido-palm-preservation.html": ("restructured", "Community documentation and exact UFMP context"),
    "palm-care-escondido.html": ("consolidated in place", "Escondido local discovery route"),
    "palm-care-poway.html": ("consolidated in place", "Poway local discovery route"),
    "palm-care-rancho-santa-fe.html": ("consolidated in place", "Rancho Santa Fe local discovery route"),
    "palm-faq-san-diego.html": ("restructured", "Educational decision support"),
    "palm-sourcing-installation.html": ("restructured", "Replacement sourcing and installation planning"),
    "specimen-palms-cycads.html": ("restructured", "Specimen selection and replacement education"),
    "palm-journal-new.html": ("restructured", "Field evidence library and Journal gateway"),
    "palm-journal/documented-loss/index.html": ("restructured", "Confirmed-loss collection with attribution boundaries"),
}

LEGACY_REDIRECTS = {
    "managed-property-palm-services.html": "palm-records-monitoring-verification.html#organization-inquiry",
    "residential-palm-assessment.html": "palm-records-monitoring-verification.html#homeowner-inquiry",
}


def main() -> None:
    entries = json.loads((ROOT / "journal-data" / "journal_entries.json").read_text(encoding="utf-8"))
    rows = [(route, *CORE_ROLES[route]) for route in CORE_ROLES]
    for entry in entries:
        if entry.get("status") == "published" and entry.get("page"):
            suffix = f"{entry['slug']}/" if entry.get("directory_route") else f"{entry['slug']}.html"
            rows.append((f"palm-journal/{suffix}", "preserved / regenerated", f"Palm Journal evidence: {entry['category']}"))
    rows.sort()
    lines = [
        "# Route inventory and disposition",
        "",
        f"{len(rows)} public HTML routes are generated and validated. Two superseded audience routes are preserved through permanent redirects into the canonical service and inquiry page.",
        "",
        "| Route | Disposition | Commercial or educational purpose |",
        "|---|---|---|",
    ]
    lines.extend(f"| `/{route.replace('index.html', '')}` | {status} | {purpose} |" for route, status, purpose in rows)
    lines += [
        "",
        "## Permanent redirects",
        "",
        "| Legacy route | Canonical destination |",
        "|---|---|",
    ]
    lines.extend(f"| `/{source}` | `/{destination}` |" for source, destination in LEGACY_REDIRECTS.items())
    lines += [
        "",
        "## Consolidation policy",
        "",
        "Local and species pages retain search/discovery roles but point into the canonical service architecture. They do not define competing service names, navigation, credential wording, or design systems. Superseded audience pages redirect to the matching inquiry on the canonical service page.",
    ]
    (ROOT / "docs" / "route-inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Documented {len(rows)} public routes.")


if __name__ == "__main__":
    main()
