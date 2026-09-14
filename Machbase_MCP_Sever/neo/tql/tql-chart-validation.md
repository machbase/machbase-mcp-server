# TQL Chart Validation Guide

## Overview

TQL로 차트를 만들 때 빈 차트, 런타임 오류, 잘못된 시각화를 유발하는 흔한 문제들이 있습니다. 이 문서는 실행 전에 그런 문제를 찾아 고치기 위해 TQL 차트 스크립트를 검증하는 방법을 설명합니다.

**핵심 개념**: `chartID`가 담긴 HTTP 200 응답이 차트가 제대로 그려진다는 것을 보장하지는 **않습니다**. 데이터 불일치나 잘못된 컬럼 참조 때문에 차트가 비어 있을 수 있습니다.

---

## 흔한 TQL 차트 문제

### 문제 유형과 상태 코드

| 문제 유형 | 설명 | 상태 코드 |
|------------|-------------|-------------|
| **데이터 없음** | SQL 쿼리가 0건을 반환 | `NO_DATA` |
| **잘못된 컬럼** | 실제 컬럼 수 이상의 `column(N)` | `INVALID_COLUMN` |
| **음수 인덱스** | `column(-1)` 등 음수 인덱스 사용 | `NEGATIVE_INDEX` |
| **빈 차트** | `chartOption({})` 이거나 series 정의 누락 | `EMPTY_CHART` |
| **정상** | 모든 검사 통과 | `OK` |
| **오류** | 실행 또는 파싱 오류 | `ERROR` |

---

## 4단계 검증 절차

### 1단계: 데이터 존재 확인

**목적**: 데이터 소스가 실제 레코드를 반환하는지 확인합니다.

**확인할 것**:
- SQL 쿼리가 최소 1건을 반환해야 합니다
- FAKE 데이터의 차원이 유효해야 합니다
- 컬럼 수를 판별할 수 있어야 합니다

**SQL Data Sources**:

```js
// Extract and execute the SQL query
SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)

// Validation checks:
// 1. Execute: SELECT COUNT(*) FROM (original query)
// 2. If count = 0 → STATUS: NO_DATA
// 3. Execute: SELECT * FROM (original query) LIMIT 1
// 4. Count columns in result set
```

**FAKE 데이터 소스**:

```js
// Validation analyzes the FAKE() patterns
FAKE(arrange(0, 100, 1))
MAPVALUE(1, sin(value(0)))
MAPVALUE(2, cos(value(0)))

// Detection patterns:
// - arrange(start, end, step) → rows = (end-start)/step
// - linspace(start, end, count) → rows = count
// - MAPVALUE(N, ...) → columns include index N+1
```

**결과**:
- ✓ 조회 데이터: 100행 × 3컬럼
- ✗ 쿼리가 데이터를 반환하지 않음 (STATUS: NO_DATA)

---

### 2단계: 컬럼 참조 검증

**목적**: 모든 `column(N)` 참조가 유효한 범위 안에 있는지 검증합니다.

**확인할 것**:
- `CHART()` 구역의 모든 `column(N)` 호출을 찾습니다
- Verify `0 ≤ N < column_count`
- `column(-1)` 같은 음수 인덱스를 찾아냅니다

**유효한 컬럼 참조**:
```js
SQL(`SELECT time, value FROM example LIMIT 10`)
// Returns: 2 columns (time, value)
// Valid range: column(0) to column(1)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },  // ✓ Valid
        series: [{ data: column(1) }]              // ✓ Valid
    })
)
```

**잘못된 컬럼 참조**:
```js
SQL(`SELECT time, value FROM example LIMIT 10`)
// Returns: 2 columns (time, value)
// Valid range: column(0) to column(1)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(2) }]              // ✗ Invalid: column(2) doesn't exist
    })
)
```

**음수 인덱스 검출**:
```js
FAKE(linspace(0, 10, 5))
CHART(
    chartOption({
        series: [{ data: column(-1) }]             // ✗ Invalid: negative index
    })
)
```

**결과**:
- ✓ 모든 컬럼 참조 유효: [0, 1]
- ✗ 잘못된 컬럼 참조 발견: [2, 5]
- ✗ 음수 컬럼 인덱스 발견: [-1]

---

### 3단계: 빈 차트 옵션 확인

**목적**: 비어 있거나 불완전한 차트 설정을 찾아냅니다.

**빈 패턴:**

```js
// Pattern 1: Completely empty chartOption
CHART(
    chartOption({})                                // ✗ Empty
)

// Pattern 2: No series defined
CHART(
    chartOption({
        xAxis: { type: "category" },
        yAxis: {}
        // Missing: series
    })
)
```

**유효한 차트 옵션**:
```js
CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [                                   // ✓ Series defined
            { type: "line", data: column(1) }
        ]
    })
)
```

**결과**:
- ✓ 차트 옵션 존재
- ✗ 빈 chartOption 감지

---

### 4단계: 자동 수정 기능

**목적**: 수정된 TQL 스크립트를 자동으로 생성합니다.

**수정 1: 음수 인덱스 → 0**

```js
// Original (INVALID)
CHART(
    chartOption({
        series: [{ data: column(-1) }]
    })
)

// Fixed
CHART(
    chartOption({
        series: [{ data: column(0) }]  // Fixed: was column(-1)
    })
)
```

**Fix 2: Out of Range → Nearest Valid Column**

```js
// Data: 3 columns (0, 1, 2)

// Original (INVALID)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(5) }  // Out of range
        ]
    })
)

// Fixed
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(2) }  // Fixed: was column(5)
        ]
    })
)
```

**Fix 3: Empty Chart → Default Time-Series Template**

```js
// Data: 2 columns (time, value)

// Original (EMPTY)
CHART(chartOption({}))

// Fixed: Complete time-series chart with data transformation
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)

CHART(
    chartOption({
        title: { text: "Time Series Chart" },
        xAxis: { 
            type: "time",
            name: "Time"
        },
        yAxis: { 
            type: "value",
            name: "Value"
        },
        tooltip: { trigger: "axis" },
        series: [{ 
            type: "line", 
            data: column(0),
            smooth: true
        }]
    })
)
```

**Fix 4: Add Data Transformation (when needed)**

3컬럼 데이터 `[name, time, value]`의 경우:

```js
// Added transformation
MAPVALUE(0, list(value(1), value(2)))
POPVALUE(1, 2)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(0) }]
    })
)
```

---

## 검증 리포트 형식

### 리포트 구조

```
=== TQL CHART VALIDATION REPORT ===

[STEP 1] DATA EXISTENCE CHECK
✓ Query data: 100 rows × 2 columns

[STEP 2] COLUMN REFERENCE VALIDATION
✓ All column references valid: [0, 1]
  Valid range: column(0) to column(1)

[STEP 3] EMPTY CHART OPTION CHECK
✓ Chart options present

=== VALIDATION RESULT ===
STATUS: OK
DATA: 100 rows × 2 columns

=== ORIGINAL TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(1) }]
    })
)
```
```

### 문제가 있는 리포트

```
=== TQL CHART VALIDATION REPORT ===

[STEP 1] DATA EXISTENCE CHECK
✓ Query data: 100 rows × 2 columns

[STEP 2] COLUMN REFERENCE VALIDATION
✗ Invalid column references found: [3]
  Valid range: column(0) to column(1)

[STEP 3] EMPTY CHART OPTION CHECK
✓ Chart options present

=== VALIDATION RESULT ===
STATUS: INVALID_COLUMN
DATA: 100 rows × 2 columns
ISSUES: Out of range: [3]
FIXED: Yes

=== ORIGINAL TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(3) }
        ]
    })
)
```

=== FIXED TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(1) }  // Fixed: was column(3)
        ]
    })
)
```

✓ Use the fixed TQL above to avoid chart errors
```

---

## 런타임 검증 스크립트

런타임 검증을 켜면 TQL 앞에 검증 코드가 삽입됩니다:

```js
// === Auto-generated validation script ===
SCRIPT({
    console.log("Validating chart data dimensions...");
    console.log("Expected columns: 3");
}, {
    if ($.values.length < 3) {
        console.warn("Data has only " + $.values.length + " columns, expected 3");
    }
    $.yield.apply($, $.values);
})

SQL(`SELECT name, time, value FROM example`)
CHART(
    chartOption({
        xAxis: { data: column(1) },
        series: [{ data: column(2) }]
    })
)
```

데이터 차원이 예기치 않게 바뀌는 운영 환경 문제를 디버깅할 때 도움이 됩니다.

---

## 권장 사항

### 1. 실행 전에 항상 검증하기

**진행 순서**:

```
1. Write TQL script
2. Validate script (check for issues)
3. If issues found:
   - Use auto-fixed version
   - Or manually correct the script
4. Execute validated TQL
5. Verify chart renders correctly
```

### 2. column()과 value()의 차이 이해하기

**핵심 차이**:

| 함수 | 사용 위치 | 반환 | 예시 |
|----------|-------|---------|---------|
| `value(N)` | 파이프라인 중간 | 현재 레코드의 단일 값 | `value(0)` = `10` |
| `column(N)` | CHART() 내부 전용 | 컬럼 N의 모든 값 배열 | `column(0)` = `[1,2,3,4,5]` |

**예제**:
```js
SQL(`SELECT time, value FROM example`)
// During pipeline: each record has 2 values
// value(0) = time of current record
// value(1) = value of current record

MAPVALUE(1, value(1) * 100)  // ✓ Correct: transforms each record

CHART(
    chartOption({
        xAxis: { data: column(0) },  // ✓ Correct: collects all time values
        series: [{ data: column(1) }]  // ✓ Correct: collects all value values
    })
)
```

### 3. 데이터 구조를 먼저 확인하기

`CHART()`를 작성하기 전에 데이터 구조를 확인하세요:

```js
SQL(`SELECT time, value FROM example LIMIT 10`)
CSV()  // Preview: see actual columns and values
```

Output:
```csv
1699920000000000000,10.5
1699920001000000000,11.3
1699920002000000000,9.8
...
```

Now you know:
- 컬럼 0: 시간(타임스탬프)
- 컬럼 1: 값(숫자)
- 유효 범위: `column(0)` ~ `column(1)`

### 4. 다중 컬럼 데이터를 올바르게 다루기

**For 3-column data** `[name, time, value]`:

```js
SQL(`SELECT name, time, value FROM example`)
// 3 columns: column(0)=name, column(1)=time, column(2)=value

// Option 1: Transform to [time, value] pairs
MAPVALUE(0, list(value(1), value(2)))
POPVALUE(1, 2)
CHART(
    chartOption({
        xAxis: { type: "time" },
        series: [{ data: column(0) }]  // Now column(0) = [time, value]
    })
)

// Option 2: Use separate columns
CHART(
    chartOption({
        xAxis: { type: "time", data: column(1) },
        series: [{ data: column(2) }]
    })
)
```

### 5. 흔한 실수 피하기

**❌ 잘못됨: CHART() 밖에서 column() 사용**

```js
SQL(`SELECT time, value FROM example`)
MAPVALUE(1, column(1) * 100)  // ERROR: column() not available here
```

**✓ 올바름: 파이프라인에서 value() 사용**

```js
SQL(`SELECT time, value FROM example`)
MAPVALUE(1, value(1) * 100)   // ✓ Correct
```

**❌ 잘못됨: 금지된 문법 - column(N, M)**

```js
CHART(
    chartOption({
        series: [{ data: column(0, 1) }]  // ERROR: column(N, M) doesn't exist
    })
)
```

**✓ 올바름: 파이프라인에서 list() 사용**

```js
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    chartOption({
        series: [{ data: column(0) }]  // ✓ column(0) now contains [time, value] pairs
    })
)
```

**❌ 잘못됨: 데이터 구조를 가정**

```js
// Assuming 3 columns without verification
SQL(`SELECT * FROM example`)
CHART(
    chartOption({
        series: [
            { data: column(1) },
            { data: column(2) }
        ]
    })
)
```

**✓ 올바름: 먼저 확인한 뒤 사용**

```js
// Step 1: Check structure
SQL(`SELECT * FROM example LIMIT 1`)
CSV()  // See actual columns

// Step 2: Validate before CHART()
// Use validation to confirm column count

// Step 3: Use confirmed indices
SQL(`SELECT * FROM example`)
CHART(
    chartOption({
        series: [
            { data: column(1) },  // ✓ Verified safe
            { data: column(2) }   // ✓ Verified safe
        ]
    })
)
```

---

## 빈 차트 디버깅

### 흔한 원인과 해결책

**1. HTTP 200 + chartID인데 차트가 빈 경우**

**문제**: 응답은 성공으로 보이지만 차트가 그려지지 않습니다.

**진단**:
- 검증을 실행해 컬럼 참조를 확인하세요
- 가장 흔한 원인: 실제 컬럼 수 이상의 `column(N)`

**해결**:
```js
// Check validation report for INVALID_COLUMN status
// Use auto-fixed version or correct manually
```

**2. 데이터는 있는데 차트에 아무것도 안 나오는 경우**

**문제**: SQL은 데이터를 반환하는데 시리즈가 비어 있습니다.

**진단**:
- 데이터 변환이 필요한지 확인하세요
- xAxis 타입이 데이터 형식과 맞는지 확인하세요

**해결**:
```js
// For time-series data
MAPVALUE(0, list(value(0), value(1)))  // Create [time, value] pairs
POPVALUE(1)
CHART(
    chartOption({
        xAxis: { type: "time" },       // Match data type
        series: [{ data: column(0) }]
    })
)
```

**3. 빈 chartOption**

**문제**: `chartOption({})` or missing series.

**진단**:
- 검증 리포트에 EMPTY_CHART 상태가 표시됩니다

**해결**:
```js
// Use auto-fixed version with default template
// Or manually add complete chart configuration
CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [{ type: "line", data: column(1) }]
    })
)
```

---

## Examples

### 예제 1: 정상적인 단순 차트

**TQL Script**:

```js
FAKE(linspace(0, 10, 11))
MAPVALUE(1, value(0) * value(0))

CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            { type: "line", data: column(1) }
        ]
    })
)
```

**검증 결과**:

```
STATUS: OK
DATA: 11 rows × 2 columns
```

---

### 예제 2: 잘못된 컬럼 참조

**TQL Script**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(2) },  // Invalid!
            { data: column(3) }   // Invalid!
        ]
    })
)
```

**검증 결과**:

```
STATUS: INVALID_COLUMN
DATA: 100 rows × 2 columns
ISSUES: Out of range: [2, 3]
```

**수정 버전**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(1) },  // Fixed: was column(2)
            { data: column(1) }   // Fixed: was column(3)
        ]
    })
)
```

---

### 예제 3: 빈 차트 옵션

**TQL Script**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(chartOption({}))
```

**검증 결과**:

```
STATUS: EMPTY_CHART
DATA: 100 rows × 2 columns
ISSUES: Empty chartOption (no series or completely empty)
```

**수정 버전**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)

CHART(
    chartOption({
        title: { text: "Time Series Chart" },
        xAxis: { 
            type: "time",
            name: "Time"
        },
        yAxis: { 
            type: "value",
            name: "Value"
        },
        tooltip: { trigger: "axis" },
        series: [{ 
            type: "line", 
            data: column(0),
            smooth: true
        }]
    })
)
```

---

### 예제 4: 데이터 없음

**TQL Script**:

```js
SQL(`SELECT time, value FROM example WHERE name = 'nonexistent'`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

**검증 결과**:

```
STATUS: NO_DATA
REASON: SQL query returned 0 rows
SQL: SELECT time, value FROM example WHERE name = 'nonexistent'
```

**해결**: WHERE 절이나 데이터 입력을 고칩니다.

---

### 예제 5: 음수 컬럼 인덱스

**TQL Script**:

```js
FAKE(linspace(0, 10, 5))

CHART(
    chartOption({
        series: [{ data: column(-1) }]
    })
)
```

**검증 결과**:

```
STATUS: NEGATIVE_INDEX
DATA: 5 rows × 1 columns
ISSUES: Negative indices: [-1]
```

**수정 버전**:

```js
FAKE(linspace(0, 10, 5))

CHART(
    chartOption({
        series: [{ data: column(0) }]  // Fixed: was column(-1)
    })
)
```

---

## 실제 검증 워크플로

### 전체 개발 사이클

**Step 1: Write initial TQL**

```js
SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

**Step 2: Validate the script**

```
Request validation check
→ Receives validation report
→ Check STATUS field
```

**Step 3: Handle validation result**

**If STATUS: OK**
```
→ Execute TQL directly
→ Verify chart renders
```

**If STATUS: INVALID_COLUMN, NEGATIVE_INDEX, or EMPTY_CHART**
```
→ Review FIXED TQL section
→ Use fixed version
→ Execute fixed TQL
→ Verify chart renders
```

**If STATUS: NO_DATA**
```
→ Check SQL query
→ Verify table name and WHERE conditions
→ Check if data exists in database
→ Fix query and revalidate
```

**If STATUS: ERROR**
```
→ Review error message
→ Check TQL syntax
→ Fix errors and revalidate
```

**Step 4: Production deployment**

```js
// Optional: Add runtime validation for debugging
// This logs warnings if data dimensions change

// === Auto-generated validation script ===
SCRIPT({
    console.log("Validating chart data dimensions...");
    console.log("Expected columns: 2");
}, {
    if ($.values.length < 2) {
        console.warn("Data has only " + $.values.length + " columns, expected 2");
    }
    $.yield.apply($, $.values);
})

SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

---

## Summary

### 핵심 정리

1. **TQL 차트 스크립트는 실행 전에 항상 검증**해 빈 차트와 런타임 오류를 예방하세요

2. **HTTP 200 + chartID가 차트 성공을 뜻하지 않습니다** — 올바른 렌더링을 보장하려면 검증이 필요합니다

3. **검증 절차를 이해하세요**:
   - 1단계: 데이터 존재 확인(행과 컬럼)
   - 2단계: 컬럼 참조(유효한 인덱스)
   - 3단계: 빈 차트 옵션(series 누락)
   - 4단계: 자동 수정(교정된 TQL)

4. **차이를 알아두세요**:
   - `value(N)`: 파이프라인 처리 중의 단일 값
   - `column(N)`: CHART() 안에서만 쓰는 값 배열

5. **흔한 수정**:
   - 음수 인덱스 → `column(0)`
   - 범위 초과 → 가장 가까운 유효 컬럼
   - 빈 chartOption → 기본 시계열 템플릿

6. **권장 워크플로**:
   - TQL 작성 → 검증 → 필요 시 수정 → 실행 → 확인

7. 운영 환경에서 차원 불일치를 디버깅할 때는 **런타임 검증을 사용**하세요

---

## 관련 문서

- TQL 가이드 - TQL 언어 전체 레퍼런스
- TQL 레퍼런스 - TQL 문법과 연산자  
- 선 차트 예제 - 실용적인 차트 예제
- CHART() 함수 - CHART() 함수 상세 문서
- SCRIPT() 함수 - TQL에서의 JavaScript 처리
