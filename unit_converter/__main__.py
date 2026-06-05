"""Entry point for `python -m unit_converter`.

Orchestration is delegated to cli.main() (implemented in TDD phase).
"""

from unit_converter.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
