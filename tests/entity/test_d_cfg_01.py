"""RED skeleton — Track B: D-CFG-01 (broken json)."""

import pytest


def test_d_cfg_01_broken_json_raises_config_error() -> None:
    # Given: 깨진 JSON 설정 파일
    # When: load_json(path) 호출
    # Then: ConfigError
    pytest.fail("RED: D-CFG-01 — 깨진 JSON ConfigError 미구현, 의도적 실패")
