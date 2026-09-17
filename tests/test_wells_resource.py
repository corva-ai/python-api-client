from __future__ import annotations

from unittest.mock import Mock

import pytest

from corva_api_client.resources import DEFAULT_WELL_FIELDS, WellField, WellsClient


def test_search_serializes_company_id_as_company() -> None:
    client = Mock()
    client.get.return_value = {"data": []}
    wells = WellsClient(client)

    result = wells.search(company_id=80)

    assert result == {"data": []}
    client.get.assert_called_once_with(
        "/v2/wells",
        params={"company": 80, "fields": "*"},
    )


@pytest.mark.parametrize(
    ("fields", "expected"),
    [
        (DEFAULT_WELL_FIELDS, "well.asset_id,well.name,well.status,well.state"),
        ([WellField.NAME, " well.identifier "], "well.name,well.identifier"),
        (["well.name", "", "  "], "well.name"),
        ("well.name,well.status", "well.name,well.status"),
        ("*", "*"),
        ("all", "all"),
    ],
)
def test_search_serializes_sparse_fields(fields, expected) -> None:
    client = Mock()
    WellsClient(client).search(fields=fields)

    client.get.assert_called_once_with("/v2/wells", params={"fields": expected})


@pytest.mark.parametrize("fields", [None, ""])
def test_search_can_omit_fields_for_compatibility(fields) -> None:
    client = Mock()
    WellsClient(client).search(fields=fields)

    client.get.assert_called_once_with("/v2/wells", params=None)


@pytest.mark.parametrize("fields", [[], (), ["", "  "]])
def test_search_rejects_empty_field_sequences(fields) -> None:
    client = Mock()
    with pytest.raises(ValueError, match="at least one field"):
        WellsClient(client).search(fields=fields)

    client.get.assert_not_called()


def test_well_fields_only_advertise_unconditional_attributes() -> None:
    values = {field.value for field in WellField}
    assert "well.rerun" in values
    assert "well.rerun_original_mandatory_fields" in values
    assert values.isdisjoint(
        {
            "well.distance",
            "well.archivation",
            "well.has_completed_idle_paused_stream",
            "well.company",
        }
    )
