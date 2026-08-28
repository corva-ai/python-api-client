from pathlib import Path
from runpy import run_path
from typing import Callable, cast

import pytest

_asset_relationships = cast(
    Callable[[Path], set[str]],
    run_path("scripts/check_asset_fields.py")["_asset_relationships"],
)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("class AssetsController\nend\n", "Could not find the index action"),
        ("def index\nend\n", "Could not find the end of the index action"),
        (
            "def index\n  render json: []\nend\ndef show\nend\n",
            "Could not find serializer_options",
        ),
    ],
)
def test_asset_relationship_parser_reports_controller_layout_errors(
    tmp_path: Path,
    source: str,
    message: str,
) -> None:
    controller = tmp_path / "assets_controller.rb"
    controller.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        _asset_relationships(controller)
