"""RED skeleton — Track A: U-OUT-01 (출력 3줄 이상)."""

import pytest


def test_u_out_01_meter_input_outputs_three_or_more_lines() -> None:
    # Given: 입력 "meter:2.5"
    # When: python -m unit_converter "meter:2.5" 실행
    # Then: stdout 3줄 이상 출력 (스켈레톤)
    pytest.fail("RED: U-OUT-01 — 환산 출력 3줄 이상 미구현, 의도적 실패")
