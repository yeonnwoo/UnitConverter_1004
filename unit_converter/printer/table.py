"""Default table-style output formatter.

Example: `2.5 meter = 8.2021 feet`

Maps to: FR-02, EXT-03 (table)
"""

from unit_converter.models import ConversionResult, ParsedInput


class TablePrinter:
    def print(self, source: ParsedInput, results: list[ConversionResult]) -> str:
        lines = [
            f"{source.value:g} {source.unit} = {source.value:g} {source.unit}",
        ]
        lines.extend(
            f"{source.value:g} {source.unit} = {result.target_value:.4f} {result.target_unit}"
            for result in results
        )
        return "\n".join(lines)
