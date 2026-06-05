# UnitConverter_1004 — Golden Master · REFACTOR Report

| 항목 | 내용 |
|------|------|
| **프로젝트** | UnitConverter_1004 |
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **문서 버전** | **v0.2** |
| **Phase** | Golden Master 완료 → **Safe Refactor (P0+P1) 완료** |
| **브랜치** | `refactoring` (Golden Master + `/refactor-safe` 4회, uncommitted) |
| **관련 문서** | `Report/UnitConverter_1004_GREEN_Report.md`, `docs/WORKBOOK.md`, `Prompting/UnitConverter_1004_GoldenMaster_REFACTOR_Transcript.md` |

---

## 1. Executive Summary

GREEN 13건 PASS → **Golden Master 3건** → `/refactor-smell` → **`/refactor-safe` 4회** 완료.

- **Golden Master:** 16 tests PASSED · golden **matched** (기준선 고정)
- **Safe Refactor:** P0 2건(`input_parser/`, `registry/`) + P1 2건(format 통합, `_resolve_registry`) — **tests/ 무변경**
- **회귀:** `python -m pytest tests/ -v` → **16 passed** · golden 3건 **matched** (UPDATE_GOLDEN 없음)
- **미완료:** P1 잔여(Magic Number `.4f`, FR-03 `UnknownUnitError`), P2, ECB boundary→CLI 정렬

---

## 2. Golden Master 완료 체크리스트

> REFACTOR 직전 게이트: TC PASS + 승인된 입·출력 스냅샷

### Harness

- [x] `tests/_approval.py` — `assert_matches_golden(actual, relative)` + `UPDATE_GOLDEN=1` 지원
- [x] `tests/conftest.py` — `_approval` import 경로 (`sys.path`)

### Golden baseline (3건)

| Test ID | Layer | Golden 파일 | REFACTOR 후 matched |
|---------|-------|-------------|---------------------|
| **D-SOL-01** | entity | `tests/golden/d_sol_01_g1_step_a.approved.txt` | ✅ |
| **U-OUT-01** | boundary | `tests/golden/u_out_01_meter_2_5.approved.txt` | ✅ |
| **U-IN-01** | boundary | `tests/golden/u_in_01_empty_input.approved.txt` | ✅ |

### 커밋 · merge

| 항목 | 내용 |
|------|------|
| Golden 커밋 | `89d0a51` — `test(green): Golden Master baselines for D-SOL-01, U-OUT-01, U-IN-01` |
| merge | `staging` (`70afe2e`) — Golden Master 통합 |

---

## 3. REFACTOR 완료 체크리스트

> `docs/WORKBOOK.md` § Test Loop · NFR-02 SRP · Change Budget 준수

### `/refactor-safe` 실행 이력

| # | 우선순위 | 스멜 | 변경 | Budget | Golden |
|---|----------|------|------|--------|--------|
| 1 | **P0** | SRP / 패키지 미분리 | `input_parser/` 추출 + `parser.py` shim | 파일 3 · `Parser` 1 · `parse` 1 | matched |
| 2 | **P0** | SRP / 패키지 미분리 | `registry/` 추출 · `registry.py` 삭제 | 파일 3 · `UnitRegistry` 1 | matched |
| 3 | **P1** | Duplicated Code | `Parser.parse` format 검증 통합 (`not raw or ":" not in raw`) | 파일 1 · 메서드 1 | matched |
| 4 | **P1** | Duplicated Code | `converter._resolve_registry()` 헬퍼 추출 | 파일 1 · 함수 1 · 호출 3 | matched |

### REFACTOR 게이트

- [x] **pytest:** `python -m pytest tests/ -v` → **16 passed**
- [x] **Golden:** 3건 UPDATE_GOLDEN 없이 **matched**
- [x] **tests/ 무변경** (assert 완화·skip 없음)
- [x] **동작 불변** (예외 타입·메시지·stdout·entity 스냅샷 동일)
- [ ] **커밋** (사용자 요청 시)
- [ ] **staging merge** (사용자 요청 시)

---

## 4. 구현 파일 구조 (REFACTOR 후)

```
unit_converter/
├── constants.py           # DEFAULT_UNITS SSOT
├── models.py              # ParsedInput, ConversionResult (E001)
├── errors.py
├── input_parser/          # E002 — FR-01, FR-04, FR-05  [NEW]
│   ├── __init__.py
│   └── parser.py          # Parser.parse
├── parser.py              # shim → input_parser.Parser
├── registry/              # E003 — FR-03, NFR-01       [NEW]
│   ├── __init__.py
│   └── registry.py        # UnitRegistry
├── converter.py           # to_meter, from_meter, convert_all + _resolve_registry
├── cli.py                 # E2E orchestration
├── config/loader.py
└── printer/table.py       # E005
```

### 변경 파일 요약 (`unit_converter/`)

| 파일 | 변경 |
|------|------|
| `input_parser/parser.py` | **신규** — `Parser` 구현 |
| `input_parser/__init__.py` | **신규** — export |
| `parser.py` | shim (re-export) |
| `registry/registry.py` | **신규** — `UnitRegistry` 구현 |
| `registry/__init__.py` | **신규** — export |
| `registry.py` | **삭제** (패키지 충돌 방지) |
| `converter.py` | `_resolve_registry()` 추출 |

---

## 5. Track · pytest 검증

```bash
python -m pytest tests/ -v
# → 16 passed
```

| Track | 명령 | REFACTOR 후 |
|-------|------|-------------|
| **Logic** | `python -m pytest tests/entity -v` | **10 passed** |
| **UI** | `python -m pytest tests/boundary -v` | **6 passed** |

---

## 6. `/refactor-smell` 잔여 (미적용)

### P1 — 후속 사이클

| 스멜 | 위치 | 비고 |
|------|------|------|
| Duplicated Code | `test_d_loc_01.py` L17–41 | meter/feet/yard 개별 테스트 — **tests/ Scope** |
| Magic Number | `printer/table.py:print` | `.4f` → `constants.py` SSOT (**golden 영향 주의**) |
| 설계–구현 갭 | `registry/registry.py:get` | FR-03 `UnknownUnitError` (**동작 변경 → GREEN**) |

### P2

| 스멜 | 위치 |
|------|------|
| ECB 위반 | `test_u_in_01~03.py` — boundary→Parser 직접 |
| Long Method | `tests/_approval.py:assert_matches_golden` |
| Duplicated Code | `test_u_out_01.py` — capsys 셋업 2회 |
| Mysterious Name | `test_d_loc_01_blank_coords_row_major` |

---

## 7. 브랜치 · 작업 이력

| 이벤트 | 내용 |
|--------|------|
| Golden Master | `89d0a51` on GREEN → staging merge |
| refactor 시행·롤백 | refactoring 브랜치 1차 시도 → 정리 후 재개 |
| Safe Refactor 4회 | P0×2 + P1×2 완료 (로컬 uncommitted) |
| Report v0.2 | 본 문서 (REFACTOR P0+P1 마감) |

---

## 8. 다음 단계

| 순서 | 작업 | 비고 |
|------|------|------|
| 1 | REFACTOR 커밋 | `refactor: extract input_parser and registry packages (NFR-02)` |
| 2 | `staging` merge | 사용자 요청 시 |
| 3 | P1 Magic Number (`.4f`) | golden U-OUT-01 영향 검토 |
| 4 | FR-03 `UnknownUnitError` | 별도 GREEN 사이클 |

---

## 9. 문서 추적성

```
GREEN Report (13 passed)
  → Golden Master 3건 (16 passed, matched) — 89d0a51
  → staging merge (70afe2e)
  → /refactor-smell
  → /refactor-safe #1 input_parser ✅
  → /refactor-safe #2 registry ✅
  → /refactor-safe #3 Parser.parse format ✅
  → /refactor-safe #4 _resolve_registry ✅
  → Report v0.2 (본 문서)
  → 커밋 · merge (다음)

Prompting/UnitConverter_1004_GoldenMaster_REFACTOR_Transcript.md
  → Turn 23~28 (Safe Refactor Export)
```
