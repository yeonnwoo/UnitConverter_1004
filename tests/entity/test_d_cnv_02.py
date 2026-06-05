"""RED skeleton — Track B: D-CNV-02 (convert_all)."""

import pytest


def test_d_cnv_02_2_5_meter_to_feet_five_decimals() -> None:
    # Given: 2.5 meter
    # When: convert_all(ParsedInput("meter", 2.5)) 호출
    # Then: 8.20210 ft (소수 5자리)
    pytest.fail("RED: D-CNV-02 — convert_all 2.5m→ft 미구현, 의도적 실패")
