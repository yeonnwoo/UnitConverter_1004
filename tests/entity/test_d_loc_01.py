"""GREEN — D-LOC-01 (FR-LOC-01 = FR-01): Parser.parse 유효 입력."""

from unit_converter.parser import Parser


def test_d_loc_01_blank_coords_row_major(grid_g1: list[dict[str, str | float]]) -> None:
    # Given: G1 격자 (0이 2개), row-major — D-LOC-01-01~03 입력
    # When: Parser().parse(raw) 호출 (grid_g1 각 행)
    # Then: expected_unit·expected_value 추출 (1-index row-major 순)
    parser = Parser()
    for row in grid_g1:
        result = parser.parse(str(row["raw"]))
        assert result.unit == row["expected_unit"]
        assert result.value == row["expected_value"]


def test_d_loc_01_meter_colon_2_5_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "meter:2.5"
    # When: Parser().parse("meter:2.5") 호출
    # Then: unit=meter, value=2.5
    result = Parser().parse("meter:2.5")
    assert result.unit == "meter"
    assert result.value == 2.5


def test_d_loc_01_feet_colon_3_0_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "feet:3.0"
    # When: Parser().parse("feet:3.0") 호출
    # Then: unit=feet, value=3.0
    result = Parser().parse("feet:3.0")
    assert result.unit == "feet"
    assert result.value == 3.0


def test_d_loc_01_yard_colon_0_parses_unit_and_value() -> None:
    # Given: 입력 문자열 "yard:0" (경계: 0 허용)
    # When: Parser().parse("yard:0") 호출
    # Then: unit=yard, value=0.0
    result = Parser().parse("yard:0")
    assert result.unit == "yard"
    assert result.value == 0.0
