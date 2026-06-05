"""Unit converter.

Responsibility (SRP): perform meter-based conversion using Registry.
All non-meter conversions go through meter as the hub unit.

Maps to: FR-02
"""

from unit_converter.models import ConversionResult, ParsedInput
from unit_converter.registry import UnitRegistry

_default_registry = UnitRegistry()


def _resolve_registry(registry: UnitRegistry | None) -> UnitRegistry:
    return registry or _default_registry


def to_meter(value: float, unit: str, registry: UnitRegistry | None = None) -> float:
    reg = _resolve_registry(registry)
    return value * reg.get(unit)


def from_meter(meter_value: float, unit: str, registry: UnitRegistry | None = None) -> float:
    reg = _resolve_registry(registry)
    return meter_value / reg.get(unit)


def convert_all(
    parsed: ParsedInput,
    registry: UnitRegistry | None = None,
) -> list[ConversionResult]:
    reg = _resolve_registry(registry)
    meter_value = to_meter(parsed.value, parsed.unit, reg)
    return [
        ConversionResult(
            source_unit=parsed.unit,
            source_value=parsed.value,
            target_unit=target_unit,
            target_value=from_meter(meter_value, target_unit, reg),
        )
        for target_unit in reg.all_units()
        if target_unit != parsed.unit
    ]
