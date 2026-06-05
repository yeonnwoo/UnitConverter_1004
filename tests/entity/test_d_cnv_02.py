"""GREEN — Track B: D-CNV-02 (convert_all)."""

import pytest

from unit_converter.converter import convert_all
from unit_converter.models import ParsedInput


def test_d_cnv_02_2_5_meter_to_feet_five_decimals() -> None:
    # Given: 2.5 meter
    # When: convert_all(ParsedInput("meter", 2.5)) 호출
    # Then: 8.20210 ft (소수 5자리)
    results = convert_all(ParsedInput("meter", 2.5))
    feet = next(r for r in results if r.target_unit == "feet")
    assert feet.target_value == pytest.approx(8.20210, abs=1e-5)
