"""GREEN — Track B: D-CNV-01 (to_meter)."""

import pytest

from unit_converter.converter import to_meter


def test_d_cnv_01_one_feet_to_meter() -> None:
    # Given: 1 feet
    # When: to_meter(1, "feet") 호출
    # Then: 0.3048 m (±ε)
    assert to_meter(1, "feet") == pytest.approx(0.3048)
