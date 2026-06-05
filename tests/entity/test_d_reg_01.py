"""GREEN — Track B: D-REG-01 (register cubit)."""

import pytest

from unit_converter.converter import convert_all
from unit_converter.models import ParsedInput
from unit_converter.registry import UnitRegistry


def test_d_reg_01_register_cubit_convertible() -> None:
    # Given: cubit = 0.4572 m
    # When: registry.register("cubit", 0.4572) 후 변환
    # Then: 변환 가능
    registry = UnitRegistry()
    registry.register("cubit", 0.4572)
    results = convert_all(ParsedInput("cubit", 1.0), registry)
    meter = next(r for r in results if r.target_unit == "meter")
    assert meter.target_value == pytest.approx(0.4572)
