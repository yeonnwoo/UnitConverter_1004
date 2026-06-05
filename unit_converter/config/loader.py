"""External config file loader (JSON / YAML).

Responsibility (SRP): read unit definitions from files and return data
for Registry initialization. OCP: new loaders implement the same interface.

Maps to: EXT-01
"""

import json
from pathlib import Path


class ConfigError(Exception):
    """Raised when a config file cannot be loaded or parsed."""


def load_json(path: Path | str) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ConfigError(str(exc)) from exc
