"""RED skeleton — D-LOC-01 (FR-LOC-01 = FR-01): Parser.parse 유효 입력."""

import pytest


def test_d_loc_01_blank_coords_row_major(grid_g1: list[dict[str, str | float]]) -> None:
    # Given: G1 격자 (0이 2개), row-major — D-LOC-01-01~03 입력
    # When: Parser().parse(raw) 호출 (grid_g1 각 행)
    # Then: expected_unit·expected_value 추출 (1-index row-major 순)
    _ = grid_g1
    pytest.fail("RED: D-LOC-01 — Parser.parse 미구현, 의도적 실패")


def test_d_loc_01_meter_colon_2_5_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "meter:2.5"
    # When: Parser().parse("meter:2.5") 호출
    # Then: unit=meter, value=2.5
    pytest.fail("RED: D-LOC-01 — D-LOC-01-01 Parser.parse 미구현, 의도적 실패")


def test_d_loc_01_feet_colon_3_0_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "feet:3.0"
    # When: Parser().parse("feet:3.0") 호출
    # Then: unit=feet, value=3.0
    pytest.fail("RED: D-LOC-01 — D-LOC-01-02 Parser.parse 미구현, 의도적 실패")


def test_d_loc_01_yard_colon_0_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "yard:0" (경계: 0 허용)
    # When: Parser().parse("yard:0") 호출
    # Then: unit=yard, value=0.0
    pytest.fail("RED: D-LOC-01 — D-LOC-01-03 Parser.parse 미구현, 의도적 실패")
