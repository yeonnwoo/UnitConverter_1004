"""CLI orchestration layer.

Responsibility (SRP): parse CLI arguments and wire Parser, Registry,
Converter, and Printer. Does not contain parsing, conversion, or formatting logic.

Maps to: FR-02 (E2E), EXT-03 (--format), EXT-01 (--config)
"""

import sys

from unit_converter.converter import convert_all
from unit_converter.errors import UnitConverterError
from unit_converter.parser import Parser
from unit_converter.printer.table import TablePrinter


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m unit_converter \"unit:value\"", file=sys.stderr)
        return 1

    try:
        parsed = Parser().parse(args[0])
        results = convert_all(parsed)
        print(TablePrinter().print(parsed, results))
        return 0
    except UnitConverterError as exc:
        print(str(exc), file=sys.stderr)
        return 1
