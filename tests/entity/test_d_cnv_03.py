"""GREEN — Track B: D-CNV-03 (feet→yard via meter)."""

import pytest

from unit_converter.converter import convert_all, from_meter, to_meter
from unit_converter.models import ParsedInput


def test_d_cnv_03_feet_to_yard_via_meter() -> None:
    # Given: feet 값
    # When: convert_all (feet → yard) 호출
    # Then: meter 경유 환산과 일치
    feet_value = 10.0
    results = convert_all(ParsedInput("feet", feet_value))
    yard = next(r for r in results if r.target_unit == "yard")
    meter_value = to_meter(feet_value, "feet")
    expected_yard = from_meter(meter_value, "yard")
    assert yard.target_value == pytest.approx(expected_yard)
