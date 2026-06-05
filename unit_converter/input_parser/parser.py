"""Input string parser implementation.

Responsibility (SRP): validate and parse `unit:value` strings into ParsedInput.
Does not know conversion rates or output formats.

Maps to: FR-01, FR-04, FR-05
"""

from unit_converter.errors import InvalidFormatError, NegativeValueError
from unit_converter.models import ParsedInput


class Parser:
    def parse(self, raw: str) -> ParsedInput:
        if not raw or ":" not in raw:
            raise InvalidFormatError("Invalid format: expected unit:value")
        unit, value_str = raw.split(":", maxsplit=1)
        value = float(value_str)
        if value < 0:
            raise NegativeValueError("Negative values are not allowed")
        return ParsedInput(unit=unit, value=value)
