# ROLLUP_REBUILD

ROLLUP_REBUILD는 원본의 과거 값 보정 이후 집계를 다시 계산하는 프로시저이며
Standard Edition 전용입니다. FORCE와 달리 영향 버킷을 삭제·재생성합니다. 모든 ROLLUP 정의를
임의로 재구성하는 범용 명령은 아닙니다.

## 지원 대상을 먼저 확인

| 대상 | 현행 경로 |
|---|---|
| WITH ROLLUP으로 만든 완전한 SEC→MIN→HOUR 계층 | 기본 숫자·확장·문서 전체 JSON 경로 |
| 원본에 연결된 지원 Custom 트리 | 1 SEC·1 MIN·1 HOUR 간격과 재구성 경계에 맞는 SELECT 확인 |
| 임의 이름·간격의 수동 일반 ROLLUP | 자동 계층과 같은 지원을 가정하지 않음 |
| SEC가 없는 MIN/HOUR만의 자동 계층 | 완전한 기본 계층으로 간주하지 않음 |
| 10 MIN 등 다른 간격의 Custom | 현행 시간 경계 생성 경로에 지원되지 않음 |
| Cluster Edition | 미지원 |

Custom의 SELECT가 만드는 버킷과 INTERVAL, 기준 시간대가 재구성 경계와 일치해야 합니다.
지원하지 않는 작업이 트리에 섞였는지 먼저 조사합니다. 함수가 모든 Custom 표현식·간격을
생성 가능하다는 이유만으로 재구성할 수 있다고 가정하지 마십시오.

## 시간 인수와 버킷 경계

문자열 시각 또는 상수 문자열을 사용하는 TO_DATE를 지정합니다. 일반 DATETIME 식 전체를
평가하는 경로가 아니므로 NOW 산술식이나 바인딩 매개변수로 예제를 작성하지 않습니다.

시작과 종료 시각이 속한 버킷을 모두 포함하고 버킷 전체로 넓힙니다. 1분 단계에서
00:00:30~00:01:00을 지정하면 00:00과 00:01 두 버킷, 즉
[00:00:00, 00:02:00) 범위가 재계산됩니다. 시작=종료도 그 시각의 버킷을 재계산하며
시작이 종료보다 크면 오류입니다. 상위 시간 단계는 더 넓은 버킷으로 확장됩니다.

## 기본 계층과 Custom 정정 실습

### 1. 준비와 최초 집계

```sql
CREATE TAG TABLE ch6_rebuild (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
CREATE TAG TABLE ch6_rebuild_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, sum_value DOUBLE, cnt LONG
);
CREATE ROLLUP ch6_rebuild_custom INTO (ch6_rebuild_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time, SUM(value), COUNT(value)
      FROM ch6_rebuild GROUP BY name, time
) INTERVAL 1 MIN;

INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:00'), 1);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), 200);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:00'), 300);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:30'), 4);
EXEC TABLE_FLUSH(ch6_rebuild);

SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME FROM V$ROLLUP
 WHERE ROOT_TABLE = 'CH6_REBUILD' ORDER BY INTERVAL_TIME, ROLLUP_NAME;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_SEC FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_MIN FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_HOUR FORCE;
ALTER ROLLUP ch6_rebuild_custom FORCE;
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

제어 명령의 자동 생성 이름은 위 V$ROLLUP 결과와 일치하는지 확인합니다.
다른 객체의 이름을 추측해 실행하지 않습니다. 최초 분 평균은 100.5와 152입니다.

### 2. 원본 보정과 재구성

```sql
UPDATE ch6_rebuild SET value = 20
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:00:30');
UPDATE ch6_rebuild SET value = 30
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:01:00');
EXEC ROLLUP_REBUILD(ch6_rebuild, 'S1',
    TO_DATE('2026-01-01 00:00:30'),
    TO_DATE('2026-01-01 00:01:00'));
```

### 3. 원본·일반·Custom 결과 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT rollup('min', 1, time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT time, SUM(sum_value), SUM(cnt), SUM(sum_value) / SUM(cnt)
  FROM ch6_rebuild_dst WHERE name = 'S1'
 GROUP BY time ORDER BY time;
SHOW ROLLUPGAP;
```

세 결과는 00:00에 합계 21·건수 2·평균 10.5, 00:01에 합계 34·건수 2·평균 17입니다.
종료 시각 뒤의 00:01:30 값 4도 같은 버킷을 재계산할 때 포함되어야 합니다.

## 운영 영향과 실패 복구

관련 작업은 처리 위치를 따라잡고 중지·재계산·재시작됩니다. 원본의 안정적인 조회를 위한
내부 처리도 수행하므로 “재구성 중 정상 작업이 그대로 계속된다”고 설명하지 않습니다.
사용자 쿼리·수집의 허용 지연과 중지 시간을 검증 환경에서 먼저 측정합니다.

여러 단계가 하나의 원자적 트랜잭션으로 취소된다고 가정하지 않습니다. 실패 시 상태 복구는
최선 시도로 수행되므로 실제 데이터와 V$ROLLUP을 확인합니다. 원래 중지 상태를 그대로
복원해 준다는 보장도 없습니다. 재실행 전 지원 대상·원본 잔존 여부·재집계 범위를 확인합니다.

존재하지 않는 태그는 유효한 재구성 대상이 준비된 상황에서 no-op일 수 있습니다.
성공 응답만으로 의도한 태그를 처리했다고 판단하지 말고 실제 결과를 비교합니다.
원본이 삭제되어 없으면 원래 통계를 복원할 수 없습니다.

## 정리

```sql
DROP ROLLUP ch6_rebuild_custom;
DROP TABLE ch6_rebuild_dst;
DROP TABLE ch6_rebuild CASCADE;
```

Custom 대상은 따로 제거합니다. 일반 정의 자체를 바꿔야 하거나 이 프로시저 범위를 벗어나면
지원되는 새 정의·데이터 이전 절차를 마련합니다. 내부 저장 테이블을 임의로 삭제하는 SQL을
대체 절차로 제시하지 않습니다. 정확한 인수는
REBUILD 레퍼런스를 참고합니다.
