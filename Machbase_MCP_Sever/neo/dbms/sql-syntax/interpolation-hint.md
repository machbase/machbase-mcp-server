# INTERPOLATION hint

`INTERPOLATION` 힌트는 TAG 테이블의 시계열 데이터에서 누락된 시간 구간을 수학적으로 보간해 채워 반환합니다. 센서 오류, 네트워크 장애 등으로 빠진 데이터 구간을 연속적인 시계열로 처리할 때 사용합니다.

> TAG 테이블 전용 힌트입니다. LOG, LOOKUP, VOLATILE 테이블에는 적용되지 않습니다.

## 문법

```sql
SELECT /*+ INTERPOLATION(time_column [method interval_ns]) */ col1, col2, ...
  FROM tag_table
 WHERE ...;
```

| 매개변수 | 설명 |
|----------|------|
| `time_column` | BASETIME 컬럼 이름 |
| `method` | 보간 방법: `LINEAR` (선형, 기본값), `PREV` (이전 값 유지) |
| `interval_ns` | 보간 간격 (나노초 단위) |

## 예시

### 기본 선형 보간

```sql
-- 1분 간격 데이터에서 누락 구간을 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN NOW - 1h AND NOW;
```

### 보간 방법 명시

```sql
-- LINEAR: 앞뒤 값 사이를 직선으로 보간 (60초 간격)
SELECT /*+ INTERPOLATION(value LINEAR 60000000000) */
       name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- PREV: 이전 값으로 채우기 (60초 간격)
SELECT /*+ INTERPOLATION(status_code PREV 60000000000) */
       name, time, status_code
  FROM sensor_tag
 WHERE name = 'STATUS-01'
   AND time BETWEEN NOW - 1h AND NOW;
```

### 인라인 뷰와 CTE 제한

`INTERPOLATION`은 인라인 뷰에 적용할 수 없습니다. CTE도 실행 시 인라인 뷰 형태로
전개되므로 CTE 본문에서 `INTERPOLATION`을 사용하면 다음 오류가 발생합니다.

```text
ERR-02304: Interpolation is not applicable on (INLINE-VIEW).
```

보간 결과를 PIVOT하거나 여러 단계에서 재사용해야 하면 보간 쿼리를 먼저 실행해 별도
테이블에 저장한 후 다음 쿼리에서 처리합니다.

## 보간 방법

| 방법 | 설명 |
|------|------|
| `LINEAR` | 누락 구간의 앞뒤 실제 값을 직선으로 연결해 보간 |
| `PREV` | 누락 구간을 직전 실제 값으로 채움 |

- 누락 구간의 시작 또는 끝에 실제 데이터가 없으면 보간을 수행하지 않습니다.
- 시간 범위는 `WHERE` 절에서 BASETIME 컬럼에 대한 조건으로 지정합니다.
  예를 들어 최근 1시간은 `time BETWEEN NOW - 1h AND NOW`로 조회합니다.
  `DURATION`은 TAG 테이블에 사용할 수 없습니다.
  시간 범위 없이 사용하면 전체 데이터를 대상으로 하여 성능에 영향을 줄 수 있습니다.

## INTERPOLATION vs SERIES BY

| 항목 | INTERPOLATION 힌트 | SERIES BY |
|------|--------------------|-----------|
| 용도 | 누락 시간 구간 채우기 | 연속 조건 만족 구간 추출 |
| 대상 | TAG 테이블 | 모든 테이블 |
| 결과 | 보간된 행 자동 추가 | 조건 만족 행만 반환 |

## 관련 문서

- SAMPLING hint — 비율 기반 샘플링
- SELECT hint syntax — 전체 힌트 목록
- SERIES BY syntax — 연속 구간 추출
- WITH / CTE syntax — CTE의 인라인 뷰 전개와 제한
