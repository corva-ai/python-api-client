from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from corva_api_client.client import CorvaClient


class WellField(StrEnum):
    """Unconditional attribute fieldsets supported by the v2 well serializer."""

    ASSET_ID = "well.asset_id"
    NAME = "well.name"
    IDENTIFIER = "well.identifier"
    STATUS = "well.status"
    STATE = "well.state"
    VISIBILITY = "well.visibility"
    AREA = "well.area"
    LON_LAT = "well.lon_lat"
    CUSTOM_PROPERTIES = "well.custom_properties"
    SETTINGS = "well.settings"
    STATS = "well.stats"
    CREATED_AT = "well.created_at"
    UPDATED_AT = "well.updated_at"
    LAST_ACTIVE_AT = "well.last_active_at"
    LAST_DRILLING_AT = "well.last_drilling_at"
    LAST_INTERVENTION_AT = "well.last_intervention_at"
    QC_BY = "well.qc_by"
    QC_AT = "well.qc_at"
    ENABLE_ALERTS = "well.enable_alerts"
    RIG_CLASSIFICATION = "well.rig_classification"
    CUSTOMER_WELL_ID = "well.customer_well_id"
    AIR_GAP = "well.air_gap"
    GROUND_ELEVATION = "well.ground_elevation"
    WATER_DEPTH = "well.water_depth"
    ALTERNATIVE_NAMES = "well.alternative_names"
    ALTERNATIVE_WELLBORE_NAMES = "well.alternative_wellbore_names"
    ORIGINAL_WELL_ID = "well.original_well_id"
    ORIGINAL_WELL_CREATED_AT = "well.original_well_created_at"
    WELLBORE_NAME = "well.wellbore_name"
    PAD_ID = "well.pad_id"
    PROGRAM_ID = "well.program_id"
    FRAC_FLEET_ID = "well.frac_fleet_id"
    RIG_ID = "well.rig_id"
    FLOATING_VESSEL_SUBTYPE = "well.floating_vessel_subtype"
    PLATFORM_RIG_TYPE = "well.platform_rig_type"
    COUNTRY = "well.country"
    FORCE_ALERT_NOTIFICATIONS = "well.force_alert_notifications"
    RIG_CHANGED_AT = "well.rig_changed_at"
    RERUN = "well.rerun"
    RERUN_ORIGINAL_MANDATORY_FIELDS = "well.rerun_original_mandatory_fields"


DEFAULT_WELL_FIELDS: tuple[WellField, ...] = (
    WellField.ASSET_ID,
    WellField.NAME,
    WellField.STATUS,
    WellField.STATE,
)


def _serialize_well_fields(
    fields: str | Sequence[WellField | str] | None,
) -> str | None:
    if fields is None:
        return None
    if isinstance(fields, str):
        return fields or None

    serialized = ",".join(value for field in fields if (value := str(field).strip()))
    if not serialized:
        raise ValueError("Well fields must contain at least one field.")
    return serialized


class WellsClient:
    def __init__(self, client: "CorvaClient") -> None:
        self._client = client

    def list(self, query_parameters: dict[str, Any] | None = None):
        return self._client.get("/v2/wells", params=query_parameters)

    def get(
        self,
        id: int | None = None,
        query_parameters: dict[str, Any] | None = None,
    ):
        return self._client.get(f"/v2/wells/{id}", params=query_parameters)

    def search(
        self,
        *,
        ids: str | None = None,
        company_id: int | None = None,
        fields: str | Sequence[WellField | str] | None = "*",
        sort: str | None = None,
        pad: int | None = None,
        status: str | None = None,
        state: str | None = None,
        identifier: str | None = None,
        area: str | None = None,
        search: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ):
        """Search wells with optional JSON:API sparse field selection.

        ``fields`` accepts a comma-separated string or a sequence of
        :class:`WellField` members and raw ``<record_type>.<field>`` strings.
        The existing full-payload default ``"*"`` is retained for compatibility.
        Pass :data:`DEFAULT_WELL_FIELDS` for compact discovery responses, or
        ``None`` to use the server default. Empty sequences raise ``ValueError``
        rather than silently falling back to broader server defaults.
        """
        params: dict[str, Any] = {}

        if ids:
            params["ids"] = ids
        if company_id is not None:
            params["company"] = company_id
        serialized_fields = _serialize_well_fields(fields)
        if serialized_fields:
            params["fields"] = serialized_fields
        if sort:
            params["sort"] = sort
        if pad is not None:
            params["pad"] = pad
        if status:
            params["status"] = status
        if state:
            params["state"] = state
        if identifier:
            params["identifier"] = identifier
        if area:
            params["area"] = area
        if search:
            params["search"] = search
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page

        return self.list(params or None)
