"""RED skeleton — Track A: U-IN-02 (콜론 없음)."""

import pytest


def test_u_in_02_meter_without_colon_format_error() -> None:
    # Given: 입력 "meter" (콜론 없음)
    # When: CLI 또는 Parser에 "meter" 전달
    # Then: 형식 오류
    pytest.fail("RED: U-IN-02 — 콜론 없는 입력 형식 오류 미구현, 의도적 실패")
