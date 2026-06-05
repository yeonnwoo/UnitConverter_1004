# UnitConverter_1004 — RED Skeleton Report

| 항목 | 내용 |
|------|------|
| **프로젝트** | UnitConverter_1004 |
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **문서 버전** | v0.2 |
| **Phase** | RED (Skeleton) — **Dual-Track 완료** |
| **브랜치** | RED |
| **관련 문서** | `Report/UnitConverter_1004_RED_TestPlan_Report.md`, `docs/WORKBOOK.md`, `Prompting/UnitConverter_1004_Session_Transcript.md` |

---

## 1. Executive Summary

Dual-Track RED 설계표 기준으로 **Track A 4건 + Track B 5건** 스켈레톤을 작성하고 의도적 실패를 확인했다.

- **설계표 ID:** 9개 (U-IN/U-OUT, D-CNV/D-REG/D-CFG)
- **추가:** D-LOC-01 4건 (파싱 보조 스켈레톤)
- **결과:** 13 tests **FAILED** (의도적 `pytest.fail`)
- **범위:** `tests/`만 변경 · `unit_converter/` 미수정

---

## 2. RED 완료 체크리스트

### Dual-Track 스켈레톤

- [x] **Track A (boundary):** U-IN-01 ~ U-OUT-01 (4)
- [x] **Track B (entity):** D-CNV-01 ~ D-CFG-01 (5)
- [x] AAA 주석 (Given / When / Then)
- [x] Then = `pytest.fail("RED: …")` 한 줄만
- [x] assert 본문 · skip · xfail · 통과 더미 **없음**
- [x] `unit_converter/` **미수정**

### 검증

- [x] `python -m pytest tests/` → **13 failed** (의도적 RED)
- [x] `Report/UnitConverter_1004_RED_TestPlan_Report.md` 작성
- [x] `Report/UnitConverter_1004_RED_Skeleton_Report.md` (본 문서)
- [x] `Prompting/UnitConverter_1004_Session_Transcript.md` Export
- [x] `README.md` Dual-Track 표 반영

### ECB · Mock

- [x] Logic Track → Domain Mock 금지
- [x] entity emit 금지 (side effect 없음)

### 다음 (RED 범위 밖)

- [x] **GREEN** — 1커밋 = RED 1묶음 → `Report/UnitConverter_1004_GREEN_Report.md`
- [ ] **REFACTOR** — SRP/OCP 유지
- [x] Git 커밋 (GREEN 10커밋, `GREEN` 브랜치)

> ARRR 1사이클 체크리스트(RED/GREEN/REFACTOR)는 `docs/WORKBOOK.md` § Test Loop 참고.

---

## 3. Dual-Track Test ID · 파일 매핑

### Track A — `tests/boundary/`

| Test ID | Given | Then | 파일 |
|---------|-------|------|------|
| U-IN-01 | `""` | 형식 오류 메시지 | `test_u_in_01.py` |
| U-IN-02 | `meter` (콜론 없음) | 형식 오류 | `test_u_in_02.py` |
| U-IN-03 | `meter:-1` | 음수 거부 | `test_u_in_03.py` |
| U-OUT-01 | `meter:2.5` | 3줄 이상 출력 | `test_u_out_01.py` |

### Track B — `tests/entity/`

| Test ID | 함수 | Given / Then | 파일 |
|---------|------|--------------|------|
| D-CNV-01 | `to_meter` | 1 feet → 0.3048 m (±ε) | `test_d_cnv_01.py` |
| D-CNV-02 | `convert_all` | 2.5 m → 8.20210 ft | `test_d_cnv_02.py` |
| D-CNV-03 | `convert_all` | feet → yard, meter 경유 | `test_d_cnv_03.py` |
| D-REG-01 | `register` | cubit 0.4572 → 변환 가능 | `test_d_reg_01.py` |
| D-CFG-01 | `load json` | 깨진 파일 → ConfigError | `test_d_cfg_01.py` |

### 추가 (설계표 외)

| Test ID | 파일 | 비고 |
|---------|------|------|
| D-LOC-01 (×4) | `test_d_loc_01.py` | FR-01 파싱 보조 · `grid_g1` 픽스처 |

---

## 4. 생성 파일 목록

```
tests/
├── conftest.py              # grid_g1 픽스처
├── boundary/
│   ├── test_u_in_01.py
│   ├── test_u_in_02.py
│   ├── test_u_in_03.py
│   └── test_u_out_01.py
└── entity/
    ├── constants.py         # G1_GRID_ROWS=34, COLS=16, CASE_COUNT=4
    ├── test_d_cnv_01.py
    ├── test_d_cnv_02.py
    ├── test_d_cnv_03.py
    ├── test_d_reg_01.py
    ├── test_d_cfg_01.py
    └── test_d_loc_01.py     # 추가 4함수
```

---

## 5. pytest 실행 결과

```bash
python -m pytest tests/ -v
```

| 항목 | 값 |
|------|-----|
| 수집 | 13 items |
| 통과 | 0 |
| 실패 | 13 (의도적 RED) |
| exit code | 1 |

**대표 FAIL 한 줄:**

```
Failed: RED: U-IN-01 — 빈 입력 형식 오류 미구현, 의도적 실패
```

---

## 6. 다음 단계 (GREEN)

| 우선순위 | RED 묶음 | GREEN 대상 |
|----------|----------|------------|
| 1 | U-IN-01 ~ 03 | `parser.py` + `errors.py` (형식·음수) |
| 2 | D-CNV-01 ~ 03 | `converter.py` + `registry.py` |
| 3 | U-OUT-01 | `cli.py` + `printer/` |
| 4 | D-REG-01 | `registry.py` (OCP) |
| 5 | D-CFG-01 | `config/loader.py` (P1) |

GREEN 시: `pytest.fail` 제거 → assert 추가 · When에 실제 호출.

---

## 7. 문서 추적성

```
Dual-Track RED 설계표
  → tests/boundary/ (Track A ×4)
  → tests/entity/ (Track B ×5)
  → pytest 13 failed ✅
  → GREEN (다음 단계)

WORKBOOK Test Loop
  → docs/WORKBOOK.md (ARRR 사이클 체크리스트)
```
