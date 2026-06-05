"""GREEN — Track A: U-OUT-01 (출력 3줄 이상)."""

import _approval

from unit_converter.cli import main

_U_OUT_GOLDEN = "u_out_01_meter_2_5.approved.txt"


def test_u_out_01_meter_input_outputs_three_or_more_lines(capsys) -> None:
    # Given: 입력 "meter:2.5"
    # When: python -m unit_converter "meter:2.5" 실행
    # Then: stdout 3줄 이상 출력 (스켈레톤)
    exit_code = main(["meter:2.5"])
    captured = capsys.readouterr()
    assert exit_code == 0
    lines = [line for line in captured.out.strip().splitlines() if line.strip()]
    assert len(lines) >= 3


def test_u_out_01_meter_input_golden_stdout(capsys) -> None:
    # Given: 입력 "meter:2.5"
    # When: CLI 실행
    # Then: stdout golden snapshot matches
    exit_code = main(["meter:2.5"])
    captured = capsys.readouterr()
    assert exit_code == 0
    stdout = captured.out
    if not stdout.endswith("\n"):
        stdout += "\n"
    _approval.assert_matches_golden(stdout, _U_OUT_GOLDEN)
