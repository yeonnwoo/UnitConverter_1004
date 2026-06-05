"""Unit converter.

Responsibility (SRP): perform meter-based conversion using Registry.
All non-meter conversions go through meter as the hub unit.

Maps to: FR-02
"""

from unit_converter.registry import UnitRegistry

_default_registry = UnitRegistry()


def to_meter(value: float, unit: str, registry: UnitRegistry | None = None) -> float:
    reg = registry or _default_registry
    return value * reg.get(unit)
