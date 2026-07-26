from __future__ import annotations

from pathlib import Path
from hashlib import sha256
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
