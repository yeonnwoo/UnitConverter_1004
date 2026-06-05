"""GREEN — Track A: U-IN-03 (음수)."""

import pytest

from unit_converter.errors import NegativeValueError
from unit_converter.parser import Parser


def test_u_in_03_meter_negative_one_rejected() -> None:
    # Given: 입력 "meter:-1"
    # When: CLI 또는 Parser에 "meter:-1" 전달
    # Then: 음수 거부
    with pytest.raises(NegativeValueError, match="Negative"):
        Parser().parse("meter:-1")
