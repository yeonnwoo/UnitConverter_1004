"""GREEN — Track B: D-CFG-01 (broken json)."""

import pytest

from unit_converter.config.loader import ConfigError, load_json


def test_d_cfg_01_broken_json_raises_config_error(tmp_path) -> None:
    # Given: 깨진 JSON 설정 파일
    # When: load_json(path) 호출
    # Then: ConfigError
    broken = tmp_path / "units.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_json(broken)
