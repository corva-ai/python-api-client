from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from corva_api_client.client import CorvaClient


class AssetStatus(StrEnum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    IDLE = "idle"
    DELETING = "deleting"
    DELETION_PAUSED = "deletion_paused"
    ARCHIVED = "archived"


class AssetField(StrEnum):
    """Sparse fieldset values supported by the v2 asset serializer."""

    NAME = "asset.name"
    ASSET_TYPE = "asset.asset_type"
    STATUS = "asset.status"
    TYPE = "asset.type"
    STATS = "asset.stats"
    LAST_ACTIVE_AT = "asset.last_active_at"
    LAST_DRILLING_AT = "asset.last_drilling_at"
    LAST_COMPLETION_AT = "asset.last_completion_at"
    CREATED_AT = "asset.created_at"
    SETTINGS = "asset.settings"
    VISIBILITY = "asset.visibility"
    COUNTY = "asset.county"
    BASIN = "asset.basin"
    API_NUMBER = "asset.api_number"
    TIMEZONE = "asset.timezone"
    TOP_HOLE = "asset.top_hole"
    BOTTOM_HOLE = "asset.bottom_hole"
    CONTRACTOR_NAME = "asset.contractor_name"
    DIRECTIONAL_DRILLER = "asset.directional_driller"
    MUD_COMPANY = "asset.mud_company"
    COMPANY_ID = "asset.company_id"
    COMPANY_NAME = "asset.company_name"
    ROOT_ASSET_ID = "asset.root_asset_id"
    ROOT_ASSET_NAME = "asset.root_asset_name"
    PARENT_ASSET_ID = "asset.parent_asset_id"
    PARENT_ASSET_NAME = "asset.parent_asset_name"
    CUSTOM_PROPERTIES = "asset.custom_properties"
    STRING_DESIGN = "asset.string_design"
    TARGET_FORMATION = "asset.target_formation"
    AREA = "asset.area"
    ENABLE_ALERTS = "asset.enable_alerts"
    VISIBLE_RERUN_ID = "asset.visible_rerun_id"
    DAY_SHIFT_START_TIME = "asset.day_shift_start_time"
    LON_LAT = "asset.lon_lat"
    QC_BY = "asset.qc_by"
    QC_AT = "asset.qc_at"
    STANDARD_TARGET_FORMATION = "asset.standard_target_formation"
    RIG_CLASSIFICATION = "asset.rig_classification"
    CUSTOMER_WELL_ID = "asset.customer_well_id"
    AIR_GAP = "asset.air_gap"
    GROUND_ELEVATION = "asset.ground_elevation"
    WATER_DEPTH = "asset.water_depth"
    ORIGINAL_WELL_ID = "asset.original_well_id"
    ORIGINAL_WELL_CREATED_AT = "asset.original_well_created_at"
    ALTERNATIVE_NAMES = "asset.alternative_names"
    ALTERNATIVE_WELLBORE_NAMES = "asset.alternative_wellbore_names"
    STATE = "asset.state"
    EDR_PROVIDER = "asset.edr_provider"
    WELLBORE_NAME = "asset.wellbore_name"
    WELL_ID = "asset.well_id"
    FLOATING_VESSEL_SUBTYPE = "asset.floating_vessel_subtype"
    PLATFORM_RIG_TYPE = "asset.platform_rig_type"
    LAST_INTERVENTION_AT = "asset.last_intervention_at"
    COUNTRY = "asset.country"
    FORCE_ALERT_NOTIFICATIONS = "asset.force_alert_notifications"
    SOURCE_WELL = "asset.source_well"
    CREATED_BY = "asset.created_by"
    RERUN_ORIGINAL_MANDATORY_FIELDS = "asset.rerun_original_mandatory_fields"
    RIG_CHANGED_AT = "asset.rig_changed_at"
    MERGING_RERUN_AS_SOURCE = "asset.merging_rerun_as_source"
    MERGING_RERUN_AS_TARGET = "asset.merging_rerun_as_target"
    RUNNING_RERUN_AS_SOURCE = "asset.running_rerun_as_source"
    RUNNING_RERUN_AS_TARGET = "asset.running_rerun_as_target"
    RIG_ID = "asset.rig_id"
    VIEWER_PAD_ID = "asset.viewer_pad_id"
    VIEWER_PAD_NAME = "asset.viewer_pad_name"


class AssetRelationship(StrEnum):
    """Asset relationship fields that opt related records into the response."""

    COMPANY = "asset.company"
    PARENT_ASSET = "asset.parent_asset"
    CHILDREN = "asset.children"
    ACTIVE_CHILD = "asset.active_child"
    LAST_ACTIVE_CHILD = "asset.last_active_child"
    VIEWER_PAD = "asset.viewer_pad"
    VIEWER_LINES = "asset.viewer_lines"


class CompanyField(StrEnum):
    """Company fields usable when ``asset.company`` is requested."""

    NAME = "company.name"
    TIME_ZONE = "company.time_zone"
    LANGUAGE = "company.language"
    PROVIDER = "company.provider"
    UNIT_SYSTEM = "company.unit_system"
    DEV_CENTER_ENABLED = "company.dev_center_enabled"
    COMPETITOR_ANALYSIS_ENABLED = "company.competitor_analysis_enabled"
    ALERT_WORKFLOW_ID = "company.alert_workflow_id"
    ALERT_RBAC_ENABLED = "company.alert_rbac_enabled"
    TOOL_ORDERING_ENABLED = "company.tool_ordering_enabled"
    WITH_SUBSCRIPTION = "company.with_subscription"


class ViewerPadField(StrEnum):
    """Pad fields usable when ``asset.viewer_pad`` is requested."""

    NAME = "pad.name"
    LON_LAT = "pad.lon_lat"
    CURRENT_FRAC_FLEET_ID = "pad.current_frac_fleet_id"
    LAST_ACTIVE_AT = "pad.last_active_at"
    CREATED_AT = "pad.created_at"
    UPDATED_AT = "pad.updated_at"


class ViewerLineField(StrEnum):
    """Viewer-line fields usable when ``asset.viewer_lines`` is requested."""

    NAME = "frac_fleet_line.name"
    LINE_TYPE = "frac_fleet_line.line_type"
    PAD_FRAC_FLEET_ID = "frac_fleet_line.pad_frac_fleet_id"


AssetFieldValue = (
    AssetField | AssetRelationship | CompanyField | ViewerPadField | ViewerLineField | str
)

DEFAULT_ASSET_FIELDS: tuple[AssetField, ...] = (
    AssetField.NAME,
    AssetField.ASSET_TYPE,
    AssetField.STATUS,
)


def _serialize_asset_fields(
    fields: str | Sequence[AssetFieldValue] | None,
) -> str | None:
    if fields is None or isinstance(fields, str):
        return fields

    return ",".join(value for field in fields if (value := str(field).strip())) or None


def _serialize_asset_types(types: str | Sequence[str] | None) -> list[str]:
    if types is None:
        return []

    raw_types = types.split(",") if isinstance(types, str) else types
    return [value for raw_type in raw_types if (value := str(raw_type).strip())]


def _serialize_asset_status(
    status: AssetStatus | Sequence[AssetStatus] | None,
) -> list[str]:
    if status is None:
        return []

    raw_statuses = status.split(",") if isinstance(status, str) else status
    statuses: list[str] = []
    for raw_status in raw_statuses:
        value = str(raw_status).strip()
        if not value:
            continue
        try:
            statuses.append(AssetStatus(value).value)
        except ValueError as error:
            valid_values = ", ".join(item.value for item in AssetStatus)
            raise ValueError(
                f"Invalid asset status {value!r}. Expected one or more of: "
                f"{valid_values}. Omit status to search all statuses."
            ) from error

    return statuses


class AssetsClient:
    def __init__(self, client: "CorvaClient") -> None:
        self._client = client

    def list(self, query_parameters: dict[str, Any] | None = None):
        return self._client.get("/v2/assets", params=query_parameters)

    def get(
        self,
        id: int | None = None,
        query_parameters: dict[str, Any] | None = None,
    ):
        return self._client.get(f"/v2/assets/{id}", params=query_parameters)

    def ancestor_ids(self, id: int, query_parameters: dict[str, Any] | None = None):
        return self._client.get(f"/v2/assets/{id}/ancestor_ids", params=query_parameters)

    # Backwards-compatible helper for the current CLI command style.
    def search(
        self,
        query: str | None = None,
        types: str | Sequence[str] | None = None,
        status: AssetStatus | Sequence[AssetStatus] | None = None,
        company_id: int | None = None,
        fields: str | Sequence[AssetFieldValue] | None = DEFAULT_ASSET_FIELDS,
        start: int | None = None,
        end: int | None = None,
        sort: str | None = "-last_active_at",
        page: int | None = None,
        per_page: int | None = None,
        order: str | None = None,
        visibility: str | None = None,
    ):
        """Search assets using a discoverable JSON:API sparse fieldset.

        ``fields`` accepts enum members, arbitrary ``<record_type>.<field>``
        strings, comma-separated strings, or the explicit full-payload values
        ``"*"`` and ``"all"``. Relationships are included only when their
        :class:`AssetRelationship` value is selected. For example, request both
        ``AssetRelationship.COMPANY`` and ``CompanyField.NAME`` to include the
        related company's name. Pass ``None`` to omit the parameter and use the
        server default.

        The default fieldset contains only the asset name, type, and status to
        keep responses suitable for interactive tools and agents. Requesting
        ``"*"`` or ``"all"`` can produce a substantially larger payload.
        """
        params: dict[str, Any] = {}

        if query:
            params["search"] = query
        serialized_types = _serialize_asset_types(types)
        if serialized_types:
            params["types[]"] = serialized_types
        serialized_status = _serialize_asset_status(status)
        if serialized_status:
            params["status[]"] = serialized_status
        if company_id is not None:
            params["company_id"] = company_id
        serialized_fields = _serialize_asset_fields(fields)
        if serialized_fields:
            params["fields"] = serialized_fields
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if visibility:
            params["visibility"] = visibility
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        return self.list(params or None)
