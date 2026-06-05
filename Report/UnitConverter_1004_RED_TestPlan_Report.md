# UnitConverter_1004 — RED Test Plan Report

| 항목 | 내용 |
|------|------|
| **프로젝트** | UnitConverter_1004 |
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **문서 버전** | v0.1 |
| **Phase** | RED |
| **브랜치** | RED |
| **관련 문서** | `docs/PRD.md`, `docs/DESIGN.md`, `README.md`, `Prompting/UnitConverter_1004_Session_Transcript.md` |

---

## 1. Executive Summary

ARRR **RED** 단계에서 Dual-Track 테스트 설계를 완료했다.

- **Track B (Logic / entity):** `D-LOC-01` — FR-01 (`unit:value` 파싱)
- **Track A (UI / boundary):** `U-IN-01`, `U-IN-02` — CLI 입출력 경계

테스트 파일·스켈레톤은 `/red-skeleton` 단계에서 생성 예정. 본 보고서는 **설계·플랜만** 포함한다.

---

## 2. C2C 추적 (Rule 1~3)

### Rule 적용

| Rule | 내용 |
|------|------|
| Rule 1 | PRD FR ↔ Test ID 1:1 연결 |
| Rule 2 | To-Do 1개 (판단 포함) |
| Rule 3 | Given / When / Then 명시 |

### PRD FR-LOC-01 인용

| ID | 요구사항 | Given | Then |
|----|----------|-------|------|
| **FR-01** (FR-LOC-01) | 입력 파싱 | `meter:2.5` | `value=2.5`, `unit=meter` 추출 |

### To-Do (판단 1개)

| # | To-Do | 결정 |
|---|-------|------|
| T-01 | `Parser.parse()` 반환 타입을 `ParsedInput` dataclass로 고정할지 | **YES** — entity Layer·FR-02 이후 추적성 |

### Test ID → Given / When / Then (Track B)

| Test ID | Given | When | Then |
|---------|-------|------|------|
| D-LOC-01-01 | `"meter:2.5"` | `Parser().parse(...)` | `unit=meter`, `value=2.5` |
| D-LOC-01-02 | `"feet:3.0"` | `Parser().parse(...)` | `unit=feet`, `value=3.0` |
| D-LOC-01-03 | `"yard:0"` | `Parser().parse(...)` | `unit=yard`, `value=0.0` |

---

## 3. Track B — RED 설계표 (Logic / entity)

```
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01 = FR-01)
```

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|---------|-----------|------------|-----------|----------------------|
| D-LOC-01-01 | `Parser.parse` | `"meter:2.5"` → `unit=meter`, `value=2.5` | Parser는 Registry/Converter/Printer 미참조 | `ImportError` / `AssertionError` |
| D-LOC-01-02 | `Parser.parse` | `"feet:3.0"` → `unit=feet`, `value=3.0` | 단위 이름 콜론 앞 문자열 그대로 보존 | 동일 |
| D-LOC-01-03 | `Parser.parse` | `"yard:0"` → `unit=yard`, `value=0.0` | 0은 거부하지 않음 (FR-04는 음수만) | 동일 |

### 테스트 플랜

| 항목 | 내용 |
|------|------|
| 파일 | `tests/entity/test_d_loc_01.py` |
| 함수명 | `test_d_loc_01_meter_colon_2_5_parses_unit_and_value` 등 3개 |
| conftest | `g1_valid_unit_value_grid` (G1 격자, 로직 없음) |
| RED 묶음 | D-LOC-01-01 ~ 03 |
| pytest | `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_meter_colon_2_5_parses_unit_and_value -v` |

### G1 격자 (conftest 데이터)

| row | raw_input | expected_unit | expected_value |
|-----|-----------|---------------|----------------|
| G1-1 | `"meter:2.5"` | `"meter"` | `2.5` |
| G1-2 | `"feet:3.0"` | `"feet"` | `3.0` |
| G1-3 | `"yard:0"` | `"yard"` | `0.0` |

---

## 4. Track A — RED 설계표 (UI / boundary)

```
Phase: red | Layer: boundary | Track: UI
이번 RED 묶음: U-IN-01, U-IN-02
```

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| U-IN-01 | `python -m unit_converter` (인자 없음) | 사용법 안내 또는 non-zero exit | `ModuleNotFoundError` / `SystemExit` |
| U-IN-02 | `python -m unit_converter "meter:2.5"` | stdout에 `feet`·`yard` 환산 줄 | `ImportError` / `AssertionError` |

| 항목 | 내용 |
|------|------|
| 파일 | `tests/boundary/test_u_in_01.py`, `test_u_in_02.py` |
| pytest | `python -m pytest tests/boundary/ -v` |

> Track A는 CLI 경계만 검증. 파싱 내부 로직은 Track B에 둔다.

---

## 5. ECB · Mock 점검

| 점검 | Track B | Track A |
|------|---------|---------|
| Logic Track → Domain Mock 금지 | ✅ Registry/Converter Mock 없음 | — |
| entity E001~E005 emit 금지 | ✅ ParsedInput/Parser만, side effect 없음 | boundary는 stdout/exit만 |
| skip / xfail | ✅ 금지 | ✅ 금지 |
| src/ 수정 (RED 단계) | ✅ 금지 | ✅ 금지 |

---

## 6. ①~⑧ 개발 활동 · Cursor 요소 매핑 (ARRR RED)

| # | 활동 | ARRR | Cursor 요소 |
|---|------|------|-------------|
| ① | Mom Test · 문제 정의 | — | Report, WORKBOOK |
| ② | PRD · FR/NFR | — | `docs/PRD.md` |
| ③ | OCP/SRP 설계 | — | `docs/DESIGN.md` |
| ④ | Rule 정의 | RED 준비 | `.cursorrules` |
| ⑤ | Command | RED 검증 | `pytest`, `python -m unit_converter` |
| ⑥ | Skill | RED→GREEN→REFACTOR | `.cursor/skills/unit-converter-arr-cycle/` |
| ⑦ | Test Loop | **RED** (현재) | Dual-Track 설계표 |
| ⑧ | Review Loop | REFACTOR 이후 | ECB·계약 (사이클 8) |

---

## 7. 다음 단계

| 순서 | 작업 | 상태 |
|------|------|------|
| 1 | `/red-test-plan` (본 보고서) | ✅ |
| 2 | `/red-skeleton` — `pytest.fail()` 스켈레톤 | ✅ |
| 3 | RED 실행 — 실패 확인 (13 failed) | ✅ |
| 4 | GREEN (1커밋 = RED 1묶음) | 🔜 |

> RED 완료 체크리스트: `Report/UnitConverter_1004_RED_Skeleton_Report.md` §2

---

## 8. 문서 추적성

```
Dual-Track RED 설계표 (9 ID)
  → tests/boundary/ U-IN-01~03, U-OUT-01 ✅
  → tests/entity/ D-CNV-01~03, D-REG-01, D-CFG-01 ✅

RED Skeleton Report
  → Report/UnitConverter_1004_RED_Skeleton_Report.md

Prompting Transcript
  → Prompting/UnitConverter_1004_Session_Transcript.md
```
