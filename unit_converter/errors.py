"""Domain-specific exceptions.

Maps to: FR-03 (UnknownUnitError), FR-04 (NegativeValueError), FR-05 (InvalidFormatError)
"""


class UnitConverterError(Exception):
    """Base exception for unit converter domain errors."""


class InvalidFormatError(UnitConverterError):
    """Raised when input does not match unit:value format (FR-05)."""


class NegativeValueError(UnitConverterError):
    """Raised when input value is negative (FR-04)."""


class UnknownUnitError(UnitConverterError):
    """Raised when unit is not registered (FR-03)."""
