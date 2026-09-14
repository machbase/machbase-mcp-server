# SELECT hint

SELECT 힌트는 `/*+ ... */` 형식의 주석 블록으로 옵티마이저 동작을 제어하거나 보간, 샘플링 등의 데이터 처리 기능을 지정합니다.

## 힌트 문법

```sql
SELECT /*+ hint_clause */ ...
SELECT /*+ hint1 hint2 */ ...
```

힌트는 `SELECT` 키워드 바로 뒤의 `/*+ ... */` 블록에 작성합니다.

## 주요 힌트 목록

### 실행 계획 제어 힌트

| 힌트 | 문법 | 설명 |
|------|------|------|
| `PARALLEL` | `/*+ PARALLEL(table, n) */` | 병렬 처리 계수 지정 |
| `NOPARALLEL` | `/*+ NOPARALLEL(table) */` | 병렬 처리 비활성화 |
| `FULL` | `/*+ FULL(table) */` | 인덱스 스캔 대신 풀 스캔 강제 |
| `NO_INDEX` | `/*+ NO_INDEX(table, index) */` | 특정 인덱스 사용 안 함 |
| `ROLLUP_TABLE` | `/*+ ROLLUP_TABLE(rollup_table) */` | 특정 ROLLUP 테이블 강제 선택 |
| `RID_RANGE` | `/*+ RID_RANGE(table, start, end) */` | RID 범위 지정 |
| `SCAN_FORWARD` | `/*+ SCAN_FORWARD(table) */` | 오래된 레코드부터 스캔 (LOG 테이블) |
| `SCAN_BACKWARD` | `/*+ SCAN_BACKWARD(table) */` | 최신 레코드부터 스캔 (LOG 테이블) |

### 데이터 처리 힌트

| 힌트 | 문법 | 설명 |
|------|------|------|
| `INTERPOLATION` | `/*+ INTERPOLATION(time_col) */` | 누락 시간 구간 자동 보간 |
| `SAMPLING` | `/*+ SAMPLING(SamplingRate) */` | 실수 값으로 지정한 비율에 따라 데이터 추출 |

## 예시

```sql
-- 병렬 처리 8개 스레드
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor, AVG(value)
  FROM sensor_log
 WHERE ts BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-31', 'YYYY-MM-DD')
 GROUP BY sensor;

-- 특정 인덱스 미사용
SELECT /*+ NO_INDEX(sensor_log, idx_ts) */ *
  FROM sensor_log
 WHERE ts > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- ROLLUP 테이블 강제 선택
SELECT /*+ ROLLUP_TABLE(_rollup_tag_value_min) */
       name, rollup('min', 5, time) AS t, AVG(value)
  FROM tag
 WHERE name = 'TEMP-01'
 GROUP BY name, t;

-- 누락 구간 보간 (TAG 테이블 전용)
SELECT /*+ INTERPOLATION(time) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN NOW - 1h AND NOW;

-- 조건에 맞는 행을 최대 100,000행으로 제한한 범위에서 1% 비율로 추출
SELECT /*+ SAMPLING(0.01) */ t_name, time, value
  FROM tag
 WHERE t_name = 'TAG_99'
 LIMIT 100000;
```

## 하위 항목

- INTERPOLATION hint — 누락 시간 구간 보간 힌트 상세
- SAMPLING hint — 비율 기반 샘플링 힌트 상세

## 관련 문서

- 쿼리 성능 튜닝 — 실행 계획과 힌트 적용 기준
