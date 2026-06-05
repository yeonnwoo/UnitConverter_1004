"""GREEN — Track A: U-IN-01 (빈 입력)."""

import pytest

from unit_converter.errors import InvalidFormatError
from unit_converter.parser import Parser


def test_u_in_01_empty_input_format_error() -> None:
    # Given: 입력 ""
    # When: CLI 또는 Parser에 빈 문자열 전달
    # Then: 형식 오류 메시지
    with pytest.raises(InvalidFormatError, match="format"):
        Parser().parse("")
