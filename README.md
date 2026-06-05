# UnitConverter_1004

길이 단위 변환 CLI — Mom Test 기반 문제 정의부터 TDD까지 추적 가능하게 구현하는 교육 프로젝트.

| | |
|---|---|
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **상태** | 설계 완료 · TDD 진행 예정 |

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
Mom Test ✅ → R-G-I-O ✅ → PRD ✅ → Design ✅ → TDD (ARRR) 🔜
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

## 개발 (TDD 예정)

```bash
# 테스트 (구현 후)
pytest

# CLI 실행 (구현 후)
python -m unit_converter "meter:2.5"
```

ARRR 1사이클 순서: [`docs/WORKBOOK.md`](docs/WORKBOOK.md) § Test Loop 참고.

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
