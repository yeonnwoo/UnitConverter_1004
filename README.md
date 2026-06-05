# UnitConverter_1004

길이 단위 변환 CLI — Mom Test 기반 문제 정의부터 TDD까지 추적 가능하게 구현하는 교육 프로젝트.

| | |
|---|---|
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **상태** | spec 완료 · **TDD RED** 진행 중 |

---

## 무엇을 만드는가

> **단위 이름을 명확히 넣었을 때만 변환하고, 틀리면 결과가 나오기 전에 바로 알 수 있게 한다.**

계산기로 단위를 바꿀 때 단위 이름(mm ↔ m 등)을 헷갈려 잘못 입력하면, 결과가 이상해 보일 때까지 오류를 모르는 불편을 줄이는 CLI다.

```bash
$ python -m unit_converter "meter:2.5"
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

---

## 프로젝트 진행 단계

```
Mom Test ✅ → R-G-I-O ✅ → PRD ✅ → Design ✅ → TDD RED 🔄 → GREEN → REFACTOR
```

| 단계 | 산출물 | 경로 |
|------|--------|------|
| 문제 정의 | Problem Definition Report | [`Report/UnitConverter_1004_ProblemDefinition_Report.md`](Report/UnitConverter_1004_ProblemDefinition_Report.md) |
| 요구사항 | PRD | [`docs/PRD.md`](docs/PRD.md) |
| 워크북 | R-G-I-O · Rule · Test Loop | [`docs/WORKBOOK.md`](docs/WORKBOOK.md) |
| 설계 | OCP/SRP 패키지 구조 | [`docs/DESIGN.md`](docs/DESIGN.md) |
| 구현 | Python 패키지 | [`unit_converter/`](unit_converter/) |

---

## 패키지 구조 (요약)

```
unit_converter/
├── parser.py       # 입력 파싱 (FR-01, FR-04, FR-05)
├── registry.py     # 단위 등록·조회 (FR-03, NFR-01)
├── converter.py    # meter 경유 환산 (FR-02)
├── printer/        # table / json / csv 출력 (EXT-03)
├── config/         # units.json, YAML/JSON 로더 (EXT-01)
└── cli.py          # CLI 오케스트레이션
```

상세: [`docs/DESIGN.md`](docs/DESIGN.md)

---

## 요구사항 요약

### P0 — 핵심

| ID | 내용 |
|----|------|
| FR-01 | `unit:value` 파싱 |
| FR-02 | 등록된 모든 단위로 환산·출력 |
| FR-03 | 미등록 단위 오류 |
| FR-04 | 음수 거부 |
| FR-05 | 형식 오류 처리 |
| NFR-01 | OCP — 단위 추가 시 Converter 비수정 |
| NFR-02 | SRP — Parser / Registry / Converter / Printer 분리 |

### P1 — 확장

| ID | 내용 |
|----|------|
| EXT-01 | `units.json` / YAML 설정 로드 |
| EXT-02 | 런타임 단위 등록 |
| EXT-03 | `--format json \| csv \| table` |

---

## 성공 기준 (Mom Test)

| ID | 기준 |
|----|------|
| SC-01 | 미등록 단위 → 즉시 오류 (이상한 숫자 방지) |
| SC-02 | 형식·음수 → 거부 |
| SC-03 | 한 번에 모든 단위 출력 → 대조·판정 |

---

## TDD — Dual-Track RED

ARRR RED 단계에서 **Track(역할)** 과 **Layer(계층)** 를 분리한다.  
동일한 C2C 추적(Rule 1~3)과 RED 설계표 형식을 쓰고, **Layer만 바꿔 재사용**한다.

| Track | Layer | 대상 | 테스트 경로 예 |
|-------|-------|------|----------------|
| **B (Logic)** | entity | `Parser`, `ParsedInput` | `tests/entity/test_d_loc_01.py` |
| **A (UI)** | boundary | `cli`, `__main__` (CLI 진입) | `tests/boundary/test_u_in_01.py` |

- **Rule 1:** PRD FR ↔ Test ID 1:1 연결
- **Rule 2:** To-Do 1개 (판단 포함)
- **Rule 3:** Given / When / Then 명시
- Logic Track → Domain Mock 금지 · entity emit 금지
- RED: `pytest.fail()` 스켈레톤 · skip/xfail 금지

ARRR 전체 순서: [`docs/WORKBOOK.md`](docs/WORKBOOK.md) · Skill: [`.cursor/skills/unit-converter-arr-cycle/`](.cursor/skills/unit-converter-arr-cycle/SKILL.md)

---

### Track A (UI) — boundary Layer

```
Phase: red | Layer: boundary | Track: UI
```

| Test ID | Given | Then (Expected RED) |
|---------|-------|----------------------|
| U-IN-01 | `""` | 형식 오류 메시지 |
| U-IN-02 | `meter` (콜론 없음) | 형식 오류 |
| U-IN-03 | `meter:-1` | 음수 거부 |
| U-OUT-01 | `meter:2.5` | 3줄 이상 출력 (스켈레톤) |

```bash
python -m pytest tests/boundary/ -v
```

---

### Track B (Domain) — entity Layer

```
Phase: red | Layer: entity | Track: Logic
```

| Test ID | 함수 | Given / Then |
|---------|------|--------------|
| D-CNV-01 | `to_meter` | 1 feet → 0.3048 m (±ε) |
| D-CNV-02 | `convert_all` | 2.5 m → 8.20210 ft (소수 5자리) |
| D-CNV-03 | `convert_all` | feet → yard, meter 경유 일치 |
| D-REG-01 | `register` | cubit 0.4572 → 변환 가능 |
| D-CFG-01 | `load json` | 깨진 파일 → ConfigError |

```bash
python -m pytest tests/entity/test_d_cnv_01.py -v
python -m pytest tests/entity/ -v
```

> Track A = 입력·출력 경계. Track B = 환산·등록·설정 로직. 모두 `pytest.fail` RED 스켈레톤.

---

## 개발 명령

```bash
# RED (Track B)
python -m pytest tests/entity/test_d_loc_01.py -v

# RED (Track A)
python -m pytest tests/boundary/ -v

# 전체 (구현 후)
pytest
python -m unit_converter "meter:2.5"
```

---

## 기본 단위 (meter 기준)

| 단위 | 비율 |
|------|------|
| meter | 1.0 |
| feet | 0.3048 |
| yard | 0.9144 |

---

## 라이선스

교육 과정용 프로젝트.
