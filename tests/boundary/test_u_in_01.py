"""RED skeleton — Track A: U-IN-01 (빈 입력)."""

import pytest


def test_u_in_01_empty_input_format_error() -> None:
    # Given: 입력 ""
    # When: CLI 또는 Parser에 빈 문자열 전달
    # Then: 형식 오류 메시지
    pytest.fail("RED: U-IN-01 — 빈 입력 형식 오류 미구현, 의도적 실패")
