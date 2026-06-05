---
name: unit-converter-arr-cycle
description: >-
  Runs one full ARRR (RED→GREEN→REFACTOR) TDD cycle for UnitConverter_1004:
  write a failing test for a single FR/NFR, minimal implementation, SRP/OCP
  refactor, and verification. Use when the user asks for TDD, ARRR, RED-GREEN-REFACTOR,
  or to implement FR-01 through NFR-02 one requirement at a time.
---

# UnitConverter ARRR Cycle Skill

UnitConverter_1004에서 **요구사항 1개**에 대해 RED→GREEN→REFACTOR 전체 사이클을 수행한다.

## 사전 조건

- 근거 문서: `docs/PRD.md`, `docs/DESIGN.md`, `docs/WORKBOOK.md`, `.cursorrules`
- **1사이클 = FR/NFR 1개** (또는 밀접한 1쌍). 여러 FR 동시 구현 금지.
- P0 미완료 시 P1(EXT) 선구현 금지.

## 입력 (사용자가 지정)

| 항목 | 예시 |
|------|------|
| 요구 ID | `FR-01`, `FR-04`, `NFR-01` |
| 대상 모듈 | `parser.py`, `registry.py` |
| RED 시나리오 | `meter:2.5` 파싱 |

미지정 시 `.cursorrules` ARRR 표의 **다음 미완료 사이클**부터 진행한다.

---

## 사이클 워크플로

### 0. 범위 확인 (Mom Test 게이트)

새 코드가 Mom Test 증거 3줄과 무관하면 **중단**하고 사용자에게 알린다.

### 1. RED — 실패 테스트

1. `docs/DESIGN.md` §8에서 **올바른 테스트 파일** 선택.
2. Given / When / Then 형식으로 테스트 **1개**만 추가.
3. 함수명에 요구 ID 포함: `test_parser_fr01_valid_input`.
4. Command 실행 — **반드시 실패** 확인:

```bash
pytest tests/test_<module>.py -v -k <test_name>
```

RED 완료 조건: `FAILED` 또는 `ImportError`/`AttributeError`(아직 미구현). **통과하면 RED 실패** — 테스트가 잘못됨.

### 2. GREEN — 최소 구현

1. **해당 모듈만** 수정 (`docs/DESIGN.md` SRP 표 준수).
2. 테스트 통과에 필요한 **최소** 코드만 작성.
3. 다른 FR·P1 기능·범위 밖 리팩터 금지.
4. Command 실행 — **통과** 확인:

```bash
pytest tests/test_<module>.py -v -k <test_name>
```

### 3. REFACTOR — 구조 정리

1. SRP 위반(파싱+환산+출력 혼합) 제거.
2. OCP 위반(단위 추가 시 `converter.py` 수정) 없는지 확인.
3. 중복·네이밍만 정리. **동작 변경·추가 기능 금지**.
4. 전체 관련 테스트 재실행:

```bash
pytest tests/test_<module>.py -v
```

### 4. 마감

- [ ] RED 실패 확인했음
- [ ] GREEN 최소 구현으로 통과
- [ ] REFACTOR 후 테스트 유지
- [ ] 커밋 메시지에 FR/NFR/SC ID 포함 (사용자 요청 시)

커밋 메시지 예:

```
feat(parser): FR-01 unit:value 파싱 구현

Given meter:2.5, extract unit=meter and value=2.5.
```

---

## 모듈 · 테스트 파일 매핑

| 요구 | 테스트 파일 | 구현 모듈 |
|------|-------------|-----------|
| FR-01, FR-04, FR-05 | `tests/test_parser.py` | `parser.py` |
| FR-03, EXT-02, NFR-01 | `tests/test_registry.py` | `registry.py` |
| FR-02 | `tests/test_converter.py` | `converter.py` |
| FR-02 출력, EXT-03 | `tests/test_printer.py` | `printer/` |
| EXT-01 | `tests/test_config_loader.py` | `config/loader.py` |
| E2E | `tests/test_cli.py` | `cli.py`, `__main__.py` |

---

## 권장 사이클 순서 (불편 우선)

| # | RED | ID |
|---|-----|-----|
| 1 | `meter:2.5` 파싱 | FR-01 |
| 2 | `meter:-1` 거부 | FR-04, SC-02 |
| 3 | `meter / abc` 거부 | FR-05, SC-02 |
| 4 | `cubit:1` 미등록 | FR-03, SC-01 |
| 5 | `meter:2.5` → feet, yard | FR-02, SC-03 |
| 6 | table 출력 | FR-02, SC-03 |
| 7 | inch 등록, Converter 무변경 | NFR-01 |
| 8 | SRP 분리 검토 | NFR-02 |

---

## REFACTOR 체크 (SRP · OCP)

| 모듈 | 이 모듈에 있으면 안 됨 |
|------|------------------------|
| `parser.py` | 환산율, Registry 조회, 출력 포맷 |
| `registry.py` | 입력 파싱, 환산 연산 |
| `converter.py` | 파싱, 출력, 단위 등록 |
| `printer/` | 환산 로직, 단위 등록 |
| `cli.py` | 파싱·환산·포맷 내부 로직 |

NFR-01: 새 단위는 `registry.register()` 또는 `units.json`만. `converter.py` 수정 시 **사이클 실패**.

---

## 예시: FR-01 사이클

**RED** — `tests/test_parser.py`:

```python
def test_parser_fr01_valid_input():
    # Given: meter:2.5
    # When: parse
    # Then: unit=meter, value=2.5
    result = Parser().parse("meter:2.5")
    assert result.unit == "meter"
    assert result.value == 2.5
```

```bash
pytest tests/test_parser.py -v -k fr01   # → FAILED 확인
```

**GREEN** — `parser.py` + `models.py` 최소 구현 → `pytest` 통과.

**REFACTOR** — `ParsedInput` dataclass 정리, parser에 환산 로직 없음 확인.

---

## Command 요약 (Skill 내부 단계용)

```bash
pytest tests/test_<module>.py -v -k <test_name>   # RED/GREEN
pytest tests/test_<module>.py -v                   # REFACTOR
pytest                                             # 전체 (사이클 마감 선택)
python -m unit_converter "meter:2.5"               # E2E (FR-02 이후)
```

---

## 하지 않을 것

- RED 없이 구현
- 한 사이클에 FR 여러 개
- Mom Test 증거 없는 기능
- P1(EXT)을 P0보다 먼저
- 테스트 파일 매핑 무시 (parser 테스트에 converter 검증 등)

## 추가 참고

- 상세 규칙: `.cursorrules`
- 사이클 체크리스트: `docs/WORKBOOK.md` § Test Loop
