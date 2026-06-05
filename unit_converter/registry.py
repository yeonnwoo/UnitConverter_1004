"""Unit registry.

Responsibility (SRP): store and retrieve unit definitions (meters per unit).
Supports dynamic registration without modifying Converter (OCP).

Maps to: FR-03, NFR-01, EXT-02
"""

from unit_converter.constants import DEFAULT_UNITS


class UnitRegistry:
    def __init__(self, units: dict[str, float] | None = None) -> None:
        self._units = dict(units or DEFAULT_UNITS)

    def get(self, name: str) -> float:
        return self._units[name]
