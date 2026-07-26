from __future__ import annotations

from pathlib import Path
from hashlib import sha256
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proof-data"
SCHEMA = json.loads((PROOF / "schema.json").read_text(encoding="utf-8"))
WINDOWS_PATH = re.compile(r"[A-Za-z]:\\")


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def validate(path: Path) -> list[str]:
    errors = []
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in SCHEMA["required_manifest_fields"]:
        if key not in data:
            errors.append(f"{path.name}: missing {key}")
    if data.get("schema_version") != SCHEMA["schema_version"]:
        errors.append(f"{path.name}: unsupported schema_version")
    if data.get("product_type") not in SCHEMA["allowed_product_types"]:
        errors.append(f"{path.name}: unapproved product_type")
    if data.get("status") != "approved" or data.get("publication_approval") != "approved":
        errors.append(f"{path.name}: separate public approval is not current")
    if data.get("artifact_fingerprint") != data.get("approved_fingerprint"):
        errors.append(f"{path.name}: approved fingerprint does not match artifact")
    public_filename = data.get("content", {}).get("public_filename")
    if public_filename:
        artifact = ROOT / public_filename
        if artifact.parent != ROOT or not artifact.is_file():
            errors.append(f"{path.name}: approved public artifact is missing or outside the public root")
        else:
            actual_fingerprint = sha256(artifact.read_bytes()).hexdigest()
            if actual_fingerprint != data.get("artifact_fingerprint"):
                errors.append(
                    f"{path.name}: public artifact bytes do not match the approved fingerprint"
                )
    if data.get("privacy") not in SCHEMA["allowed_privacy"]:
        errors.append(f"{path.name}: privacy must be sanitized or public")
    if data.get("publication_target") != "website" or data.get("privacy_scan_passed") is not True:
        errors.append(f"{path.name}: website target or privacy scan gate failed")
    forbidden = set(SCHEMA["forbidden_keys"]).intersection(walk_keys(data))
    if forbidden:
        errors.append(f"{path.name}: forbidden keys: {', '.join(sorted(forbidden))}")
    raw = json.dumps(data)
    if WINDOWS_PATH.search(raw):
        errors.append(f"{path.name}: local Windows path detected")
    for media in data.get("media", []):
        if media.get("approved_for_public") is not True:
            errors.append(f"{path.name}: media lacks public-use approval")
        filename = media.get("filename")
        expected = media.get("sha256")
        if filename and expected:
            candidates = list((ROOT / "images").rglob(filename))
            if len(candidates) != 1:
                errors.append(f"{path.name}: approved media must resolve exactly once: {filename}")
            elif sha256(candidates[0].read_bytes()).hexdigest() != expected:
                errors.append(f"{path.name}: approved media hash mismatch: {filename}")
    if path.name == "old-escondido-urban-forest-documentation.json":
        resource = json.loads((ROOT / "site-config" / "ufmp_resource.json").read_text(encoding="utf-8"))
        package_fingerprint = "6b000803ddd52b377e3a85365ae4f0072b253d0de100de6809ea04d0099f0386"
        business_fingerprint = "aee886c262d3a4b2eb7a3dbd407c65b5ddb41f5d5d0b7331c301a501a31ec1e1"
        if data.get("approved_package_fingerprint") != package_fingerprint:
            errors.append(f"{path.name}: approved package fingerprint changed")
        if data.get("business_status_fingerprint") != business_fingerprint:
            errors.append(f"{path.name}: approved business-status fingerprint changed")
        if resource.get("approval", {}).get("substantive_copy_locked") is not True:
            errors.append(f"{path.name}: substantive-copy lock is missing")
        if resource.get("page_action") != {
            "label": "Review the documentation method",
            "href": "./palm-records-monitoring-verification.html",
            "supporting_copy": "See how stable palm IDs, dated photographs, and evidence boundaries support reviewable records.",
        }:
            errors.append(f"{path.name}: approved page action changed")
        urban_page = ROOT / "urban-forest-palm-documentation.html"
        if urban_page.is_file():
            rendered = urban_page.read_text(encoding="utf-8")
            approved_text = [resource["title"], resource["summary"]]
            approved_text.extend(item["body"] for item in resource["sections"])
            approved_text.extend(resource["large_property_civic_capability"])
            approved_text.append(resource["palm_journal"]["heading"])
            approved_text.extend(resource["palm_journal"]["paragraphs"])
            approved_text.extend(item["caption"] for item in resource["media"])
            approved_text.extend(item["alt"] for item in resource["media"])
            for text in approved_text:
                if escape(text) not in rendered:
                    errors.append(f"{path.name}: approved substantive copy is missing or changed: {text[:54]}")
        else:
            errors.append(f"{path.name}: urban-forest integration page is missing")
    return errors


def main() -> int:
    errors = []
    files = sorted((PROOF / "approved").glob("*.json"))
    for path in files:
        errors.extend(validate(path))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Proof boundary valid: {len(files)} approved public bundle(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
