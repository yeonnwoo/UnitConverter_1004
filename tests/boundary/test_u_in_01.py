"""GREEN — Track A: U-IN-01 (빈 입력)."""

import pytest

import _approval

from unit_converter.errors import InvalidFormatError
from unit_converter.parser import Parser

_U_IN_GOLDEN = "u_in_01_empty_input.approved.txt"


def test_u_in_01_empty_input_format_error() -> None:
    # Given: 입력 ""
    # When: CLI 또는 Parser에 빈 문자열 전달
    # Then: 형식 오류 메시지
    with pytest.raises(InvalidFormatError, match="format"):
        Parser().parse("")


def test_u_in_01_empty_input_golden_error_code() -> None:
    # Given: 입력 ""
    # When: Parser.parse
    # Then: error code golden snapshot matches
    try:
        Parser().parse("")
    except InvalidFormatError as exc:
        actual = f"status:ERR,{type(exc).__name__}\n"
    else:
        raise AssertionError("Expected InvalidFormatError")
    _approval.assert_matches_golden(actual, _U_IN_GOLDEN)
