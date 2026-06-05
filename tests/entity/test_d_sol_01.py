"""GREEN — Track B: D-SOL-01 (entity solution golden master)."""

import _approval

from unit_converter.converter import convert_all
from unit_converter.models import ParsedInput

_GOLDEN = "d_sol_01_g1_step_a.approved.txt"


def _format_d_sol_01_snapshot(parsed: ParsedInput) -> str:
    """Canonical golden format: status line + 1-index conversion lines."""
    results = convert_all(parsed)
    lines = ["status:OK"]
    for idx, result in enumerate(results, start=1):
        lines.append(f"{idx},{result.target_unit},{result.target_value:.7f}")
    return "\n".join(lines) + "\n"


def test_d_sol_01_step_a_success() -> None:
    # Given: G1 step A — meter:2.5
    # When: convert_all (entity solution)
    # Then: golden snapshot matches
    parsed = ParsedInput("meter", 2.5)
    actual = _format_d_sol_01_snapshot(parsed)
    _approval.assert_matches_golden(actual, _GOLDEN)
