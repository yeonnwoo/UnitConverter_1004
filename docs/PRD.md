# PRD — Unit Converter CLI

| 항목 | 내용 |
|------|------|
| **프로젝트** | UnitConverter_1004 |
| **작성자** | 김연우 |
| **리뷰어** | 김명섭, 김민주, 김소민, 김정균, 김준호 |
| **문서 버전** | 초안 v0.1 |
| **근거** | `Report/UnitConverter_1004_ProblemDefinition_Report.md`, 교육과정 PRD 요약 |
| **관련 문서** | `docs/WORKBOOK.md`, `docs/DESIGN.md` |

---

## 1. 배경 및 목적

### 1.1 진짜 문제 (Mom Test)

> 계산기로 단위를 바꿀 때 단위 이름을 헷갈려 잘못 입력하면, 결과가 이상하게 나온 뒤에야 틀렸다는 걸 알고 다시 확인·재계산해야 한다.

### 1.2 주제

> 단위 이름을 명확히 넣었을 때만 변환하고, 틀리면 결과가 나오기 전에 바로 알 수 있게 한다.

### 1.3 제품 목표

PRD에서 추적 가능한 길이 단위 변환 CLI를 구현한다. 입력 검증·일괄 환산·명확한 오류로 Mom Test에서 확인된 **판정 지연**을 줄인다.

---

## 2. 사용자 및 사용 시나리오

### 2.1 페르소나

- 길이 단위 변환 시 **계산기**를 주로 사용
- **단위 이름** 혼동 경험 (예: mm ↔ m)
- 잘못 입력 시 결과가 이상해 보일 때까지 오류를 모름

### 2.2 핵심 시나리오

```bash
$ python -m unit_converter "meter:2.5"
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

사용자는 한 번의 입력으로 모든 등록 단위 결과를 대조해 이상 여부를 판정한다.

---

## 3. 기능 요구사항 (FR) — P0

| ID | 요구사항 | Given | Then | 성공 기준 |
|----|----------|-------|------|-----------|
| **FR-01** | 입력 파싱 | `meter:2.5` | `value=2.5`, `unit=meter` 추출 | — |
| **FR-02** | 전체 단위 환산·출력 | `meter:2.5` | feet, yard 등 등록 단위 전체 결과 표시 | SC-03 |
| **FR-03** | 미등록 단위 처리 | `cubit:1` | 명확한 오류 메시지 | SC-01 |
| **FR-04** | 음수 거부 | `meter:-1` | 거부 또는 예외 | SC-02 |
| **FR-05** | 형식 오류 처리 | `meter / abc` | 형식 오류 메시지 | SC-02 |

### 3.1 입력 형식

- 형식: `단위이름:숫자` (예: `meter:2.5`)
- 값: 0 이상

### 3.2 기본 지원 단위

| 단위 | meter 대비 비율 | 참고 |
|------|-----------------|------|
| `meter` | 1.0 | 기준 단위 |
| `feet` | 0.3048 | 1 m = 3.28084 ft |
| `yard` | 0.9144 | 1 m = 1.09361 yd |

### 3.3 환산 규칙

- 모든 환산은 **meter를 허브**로 한다.
- feet ↔ yard 등 비기준 단위 간 변환도 meter를 경유한다.

```
source_value → to_meter → meter_value → from_meter → target_value
```

---

## 4. 비기능 요구사항 (NFR) — P0

| ID | 요구사항 | 설명 | 설계 대응 |
|----|----------|------|-----------|
| **NFR-01** | OCP (개방-폐쇄 원칙) | 새 단위(예: `inch`) 추가 시 기존 Converter 코드 수정 없이 등록만으로 동작 | `UnitRegistry` + `units.json` / `register()` |
| **NFR-02** | SRP (단일 책임 원칙) | Parser / Registry / Converter / Printer 분리 | 모듈 1:1 대응 (`docs/DESIGN.md`) |

### 4.1 입력 검증 (품질)

| 항목 | 요구 |
|------|------|
| 음수 | 거부 (FR-04) |
| 잘못된 형식 | 거부 (FR-05) |
| 미등록 단위 | 거부 (FR-03) |
| 오류 메시지 | 원인(형식·음수·미등록) 구분 |

---

## 5. 확장 요구사항 (EXT) — P1

| ID | 요구사항 | 설명 | 예시 |
|----|----------|------|------|
| **EXT-01** | 설정 파일 로드 | `units.json` 또는 YAML에서 환산율 로드 | `--config path/to/units.json` |
| **EXT-02** | 동적 단위 등록 | 런타임에 단위 추가 후 즉시 변환 | `1 cubit = 0.4572 meter` |
| **EXT-03** | 출력 형식 | `--format` 플래그 | `json` \| `csv` \| `table` |

---

## 6. CLI 인터페이스

### 6.1 기본 사용 (P0)

```bash
python -m unit_converter "meter:2.5"
```

### 6.2 확장 옵션 (P1)

```bash
python -m unit_converter "meter:2.5" --format json
python -m unit_converter "meter:2.5" --format csv
python -m unit_converter "meter:2.5" --format table
python -m unit_converter "meter:2.5" --config path/to/units.yaml
```

### 6.3 기대 출력 (table)

```
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

---

## 7. 성공 기준 (Mom Test 연동)

| ID | 기준 | Mom Test 증거 | FR |
|----|------|---------------|-----|
| **SC-01** | 미등록 단위 → 즉시 오류, 변환 결과 없음 | ③ mm/m 혼동 시 이상한 숫자 방지 | FR-03 |
| **SC-02** | 형식·음수 → 거부 | ② 단위 이름·값 검증 | FR-04, FR-05 |
| **SC-03** | 한 번에 모든 등록 단위 출력 → 대조·판정 | ③ 「너무 작다」 조기 발견 | FR-02 |

---

## 8. 테스트 추적성 매트릭스

| ID | Given | Then | Priority |
|----|-------|------|----------|
| FR-01 | `meter:2.5` | `value=2.5`, `unit=meter` | P0 |
| FR-02 | `meter:2.5` | feet=8.2021, yard=2.7340 등 | P0 |
| FR-03 | `cubit:1` | 명확한 오류 | P0 |
| FR-04 | `meter:-1` | 거부/예외 | P0 |
| FR-05 | `meter / abc` | 형식 오류 | P0 |
| NFR-01 | `inch` 등록 후 변환 | Converter 코드 무변경 | P0 |
| NFR-02 | 구조 검토 | Parser/Registry/Converter/Printer 분리 | P0 |
| EXT-01 | `units.json` 로드 | Registry 초기화 | P1 |
| EXT-02 | `cubit` 런타임 등록 | 즉시 변환 가능 | P1 |
| EXT-03 | `--format json\|csv\|table` | 형식별 출력 검증 | P1 |

---

## 9. 범위

### 9.1 포함 (In Scope)

- `unit:value` 파싱 및 검증
- meter, feet, yard 기본 환산
- OCP/SRP 준수 패키지 구조
- P1: 설정 파일, 동적 등록, 출력 형식

### 9.2 제외 (Out of Scope)

- GUI·모바일 앱
- 질량·온도 등 길이 외 물리량
- 범용 계산기 기능
- Mom Test 증거 없는 부가 기능

---

## 10. 문서·구현 추적

| 문서 | 역할 |
|------|------|
| `Report/UnitConverter_1004_ProblemDefinition_Report.md` | Mom Test · R-G-I-O · 성공 기준 |
| `docs/PRD.md` | 본 문서 — FR/NFR/EXT |
| `docs/DESIGN.md` | OCP/SRP 패키지 구조 |
| `docs/WORKBOOK.md` | Rule · Command · Test Loop |
| `tests/` | TDD — 요구사항별 테스트 (다음 단계) |
