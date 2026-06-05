"""Golden Master approval helper."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

_GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual output to a file under tests/golden/.

    Set UPDATE_GOLDEN=1 to write (or overwrite) the golden baseline.
    """
    path = _GOLDEN_ROOT / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not path.is_file():
        raise AssertionError(
            f"Golden file missing: {path}\nRun with UPDATE_GOLDEN=1 to create."
        )

    expected = path.read_text(encoding="utf-8")
    if actual != expected:
        diff = difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"golden/{relative}",
            tofile="actual",
        )
        raise AssertionError(
            f"Golden mismatch for {relative}:\n{''.join(diff)}"
        )
