# ROLLUP 활용 시나리오

## 센서별 원본과 구간 통계

두 센서가 같은 시각에 측정해도 단위가 다르면 평균을 섞지 않습니다. 아래는 현재 단위를
메타데이터로 관리하고 태그별 집계를 조회하는 독립 실습입니다.

### 1. 생성과 입력

```sql
CREATE TAG TABLE ch6_scenario (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
) METADATA (unit VARCHAR(16));
INSERT INTO ch6_scenario METADATA VALUES ('TEMP_01', 'celsius');
INSERT INTO ch6_scenario METADATA VALUES ('PRESS_01', 'bar');
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:00'), 20);
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:30'), 22);
INSERT INTO ch6_scenario VALUES ('PRESS_01', TO_DATE('2026-01-01 10:00:00'), 1.02);
CREATE ROLLUP ch6_scenario_ru ON ch6_scenario(value) INTERVAL 1 MIN;
EXEC TABLE_FLUSH(ch6_scenario);
ALTER ROLLUP ch6_scenario_ru FORCE;
```

원본 입력 뒤 ROLLUP을 만들었어도 남아 있는 데이터를 초기 집계합니다.
생성 완료만으로 초기 집계까지 끝났다고 판단하지 않습니다.

### 2. 결과 확인

```sql
SELECT name, unit FROM ch6_scenario METADATA ORDER BY name;
SELECT name, DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SELECT name, rollup('min', 1, time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SHOW ROLLUPGAP;
```

TEMP_01은 2건·평균 21°C, PRESS_01은 1건·평균 1.02bar입니다.
메타데이터 조회는 현재 단위이며 과거 단위 변경 이력을 자동 보존하지 않습니다.

### 3. 개별 관측 확인

고정 시각 데이터를 입력했으므로 같은 고정 범위를 조회합니다. 이 데이터에 현재 시각의
“최근 5분” 조건을 적용하면 실행 날짜에 따라 빈 결과가 됩니다.

```sql
SELECT name, time, value FROM ch6_scenario
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 10:00:00')
   AND time < TO_DATE('2026-01-01 10:01:00')
 ORDER BY time;
```

두 원본 값은 20과 22입니다. 통계 평균 21에서 각 관측이나 발생 순서를 복원할 수는 없습니다.

### 4. 정리

```sql
DROP ROLLUP ch6_scenario_ru;
DROP TABLE ch6_scenario;
```

## 업무별 적용

| 요구 | 확인할 설계 |
|---|---|
| 정상 품질 통계 | 조건 필터와 후보 힌트를 고정해 원본과 비교 |
| OHLC | 확장 ROLLUP의 FIRST/LAST 또는 Custom의 보조 시각 재집계 |
| 다중 센서 비교 | 태그별 단위와 같은 버킷·조회 범위 사용 |
| 누적 계량기 소비량 | 경계 차이, 초기화·교체·누락 규칙; 표본 평균과 구분 |
| 가동률 | 표본 비율과 시간 비율 구분, 결측 구간 정책 |
| 최신 원본과 장기 집계 결합 | 집계 완료가 확인된 기준점에서 구간을 겹치지 않게 분리 |

원본과 ROLLUP 결과를 UNION ALL로 합칠 때는 경계의 중복·누락과 서로 다른 표본 수를
확인합니다. “최근 2분은 언제나 미집계” 같은 고정 지연을 보장으로 사용하지 않습니다.
부분 결과를 다시 합쳐 평균을 구한다면 합계와 유효 건수를 전달합니다.

기능별 완결 실습은 조건, 확장,
JSON, Custom에 있습니다.
문제가 생기면 진단 순서로 상태와 의미를 먼저 확인합니다.
