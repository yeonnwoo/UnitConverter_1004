"""Shared pytest fixtures."""

import pytest

from tests.entity.constants import G1_CASE_COUNT, G1_GRID_COLS, G1_GRID_ROWS


@pytest.fixture
def grid_g1() -> list[dict[str, str | float]]:
    """G1 격자 — row-major 파싱 입력 (0이 2개).

    Dimensions: G1_GRID_ROWS × G1_GRID_COLS (fixture 메타).
    Active cases: G1_CASE_COUNT rows.
    """
    _ = (G1_GRID_ROWS, G1_GRID_COLS)  # fixture dimension constants
    return [
        {"raw": "meter:2.5", "expected_unit": "meter", "expected_value": 2.5},
        {"raw": "feet:3.0", "expected_unit": "feet", "expected_value": 3.0},
        {"raw": "yard:0", "expected_unit": "yard", "expected_value": 0.0},
        {"raw": "meter:0", "expected_unit": "meter", "expected_value": 0.0},
    ][:G1_CASE_COUNT]
