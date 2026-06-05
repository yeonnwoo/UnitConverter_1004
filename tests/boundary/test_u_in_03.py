"""RED skeleton — Track A: U-IN-03 (음수)."""

import pytest


def test_u_in_03_meter_negative_one_rejected() -> None:
    # Given: 입력 "meter:-1"
    # When: CLI 또는 Parser에 "meter:-1" 전달
    # Then: 음수 거부
    pytest.fail("RED: U-IN-03 — 음수 거부 미구현, 의도적 실패")
