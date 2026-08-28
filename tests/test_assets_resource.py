from __future__ import annotations

from typing import Any, cast
from unittest.mock import Mock

import httpx
import pytest

from corva_api_client.resources import (
    AssetField,
    AssetRelationship,
    AssetsClient,
    AssetStatus,
    CompanyField,
)


def test_search_includes_visibility() -> None:
    client = Mock()
    client.get.return_value = {"data": []}
    assets = AssetsClient(client)

    result = assets.search(visibility="company")

    assert result == {"data": []}
    client.get.assert_called_once_with(
        "/v2/assets",
        params={
            "fields": "asset.name,asset.asset_type,asset.status",
            "sort": "-last_active_at",
            "visibility": "company",
        },
    )


@pytest.mark.parametrize(
    ("types", "expected"),
    [
        ("well", ["well"]),
        (["well", "rig"], ["well", "rig"]),
        ("well, rig", ["well", "rig"]),
    ],
)
def test_search_serializes_types(types, expected: list[str]) -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(types=types)

    params = client.get.call_args.kwargs["params"]
    assert params["types[]"] == expected


def test_search_encodes_multiple_types_as_repeated_array_parameters() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(types=["well", "rig"])

    params = httpx.QueryParams(client.get.call_args.kwargs["params"])
    assert params.multi_items() == [
        ("types[]", "well"),
        ("types[]", "rig"),
        ("fields", "asset.name,asset.asset_type,asset.status"),
        ("sort", "-last_active_at"),
    ]


def test_search_omits_empty_types_collection() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(types=[])

    assert "types[]" not in client.get.call_args.kwargs["params"]


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (AssetStatus.ACTIVE, ["active"]),
        ([AssetStatus.ACTIVE, AssetStatus.PAUSED], ["active", "paused"]),
        ("active, paused", ["active", "paused"]),
    ],
)
def test_search_serializes_statuses(status, expected: list[str]) -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(status=status)

    params = client.get.call_args.kwargs["params"]
    assert params["status[]"] == expected


def test_search_encodes_multiple_statuses_as_repeated_array_parameters() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(status=[AssetStatus.ACTIVE, AssetStatus.PAUSED])

    params = httpx.QueryParams(client.get.call_args.kwargs["params"])
    assert params.multi_items() == [
        ("status[]", "active"),
        ("status[]", "paused"),
        ("fields", "asset.name,asset.asset_type,asset.status"),
        ("sort", "-last_active_at"),
    ]


def test_search_rejects_invalid_status_before_request() -> None:
    client = Mock()
    assets = AssetsClient(client)

    with pytest.raises(ValueError, match="Invalid asset status 'all'"):
        assets.search(status=cast(Any, "all"))

    client.get.assert_not_called()


def test_search_omits_empty_status_collection() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(status=[])

    assert "status[]" not in client.get.call_args.kwargs["params"]


def test_search_serializes_discoverable_fields() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(
        fields=[
            AssetField.NAME,
            AssetField.ASSET_TYPE,
            AssetRelationship.COMPANY,
            CompanyField.NAME,
        ]
    )

    assert client.get.call_args.kwargs["params"]["fields"] == (
        "asset.name,asset.asset_type,asset.company,company.name"
    )


def test_search_accepts_custom_fields_for_forward_compatibility() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(fields=[AssetField.NAME, "asset.future_field"])

    assert client.get.call_args.kwargs["params"]["fields"] == ("asset.name,asset.future_field")


def test_search_normalizes_comma_separated_field_string() -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(fields=" asset.name, asset.status, ,asset.last_active_at ")

    assert client.get.call_args.kwargs["params"]["fields"] == (
        "asset.name,asset.status,asset.last_active_at"
    )


@pytest.mark.parametrize("fields", ["*", "all"])
def test_search_supports_explicit_full_fieldsets(fields: str) -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(fields=fields)

    assert client.get.call_args.kwargs["params"]["fields"] == fields


@pytest.mark.parametrize("fields", [None, []])
def test_search_omits_empty_fields(fields) -> None:
    client = Mock()
    assets = AssetsClient(client)

    assets.search(fields=fields)

    assert "fields" not in client.get.call_args.kwargs["params"]
