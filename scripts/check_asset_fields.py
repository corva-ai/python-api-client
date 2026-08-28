from __future__ import annotations

import re
import sys
from collections.abc import Iterable
from pathlib import Path

from corva_api_client.resources import (
    AssetField,
    AssetRelationship,
    CompanyField,
    ViewerLineField,
    ViewerPadField,
)


def _serializer_attributes(path: Path) -> set[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    attributes: set[str] = set()
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("attributes "):
            declaration = stripped
            while declaration.rstrip().endswith(",") and index + 1 < len(lines):
                index += 1
                declaration += " " + lines[index].strip()
            attributes.update(re.findall(r":([a-z][a-z0-9_]*)", declaration))
        elif stripped.startswith("attribute :"):
            match = re.match(r"attribute :([a-z][a-z0-9_]*)", stripped)
            if match:
                attributes.add(match.group(1))
        index += 1

    # JSON:API identifiers are emitted independently of sparse fieldsets.
    attributes.discard("id")
    return attributes


def _asset_relationships(path: Path) -> set[str]:
    source = path.read_text(encoding="utf-8")
    if "def index" not in source:
        raise ValueError(f"Could not find the index action in {path}")

    index_action = source.split("def index", maxsplit=1)[1]
    if "def show" not in index_action:
        raise ValueError(f"Could not find the end of the index action in {path}")

    index_action = index_action.split("def show", maxsplit=1)[0]
    if "serializer_options" not in index_action:
        raise ValueError(f"Could not find serializer_options in the index action in {path}")

    serializer_call = index_action.split("serializer_options", maxsplit=1)[1]
    match = re.search(r"%i\[([^]]+)]", serializer_call, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Could not find the asset relationship whitelist in {path}")
    return set(match.group(1).split())


def _enum_fields(values: Iterable[str], record_type: str) -> set[str]:
    prefix = f"{record_type}."
    return {value.removeprefix(prefix) for value in values}


def _compare(label: str, sdk: set[str], api: set[str]) -> list[str]:
    errors: list[str] = []
    missing = sorted(api - sdk)
    stale = sorted(sdk - api)
    if missing:
        errors.append(f"{label}: missing SDK values: {', '.join(missing)}")
    if stale:
        errors.append(f"{label}: stale SDK values: {', '.join(stale)}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_asset_fields.py /path/to/corva-api", file=sys.stderr)
        return 2

    api_root = Path(sys.argv[1]).expanduser().resolve()
    serializers = api_root / "app" / "serializers" / "v2"
    controllers = api_root / "app" / "controllers" / "v2"

    comparisons = (
        (
            "asset fields",
            _enum_fields(AssetField, "asset"),
            _serializer_attributes(serializers / "asset_serializer.rb"),
        ),
        (
            "asset relationships",
            _enum_fields(AssetRelationship, "asset"),
            _asset_relationships(controllers / "assets_controller.rb"),
        ),
        (
            "company fields",
            _enum_fields(CompanyField, "company"),
            _serializer_attributes(serializers / "company_serializer.rb"),
        ),
        (
            "viewer pad fields",
            _enum_fields(ViewerPadField, "pad"),
            _serializer_attributes(serializers / "pad_nested_serializer.rb"),
        ),
        (
            "viewer line fields",
            _enum_fields(ViewerLineField, "frac_fleet_line"),
            _serializer_attributes(serializers / "frac_fleet_line_nested_serializer.rb"),
        ),
    )

    errors = [
        error
        for label, sdk_fields, api_fields in comparisons
        for error in _compare(label, sdk_fields, api_fields)
    ]
    if errors:
        print("Asset field definitions are out of sync:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Asset field definitions match the Corva API serializers and whitelist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
