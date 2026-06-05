"""GREEN — Track A: U-IN-02 (콜론 없음)."""

import pytest

from unit_converter.errors import InvalidFormatError
from unit_converter.parser import Parser


def test_u_in_02_meter_without_colon_format_error() -> None:
    # Given: 입력 "meter" (콜론 없음)
    # When: CLI 또는 Parser에 "meter" 전달
    # Then: 형식 오류
    with pytest.raises(InvalidFormatError, match="format"):
        Parser().parse("meter")
