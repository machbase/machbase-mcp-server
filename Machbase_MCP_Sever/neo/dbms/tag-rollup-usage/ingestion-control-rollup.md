# ROLLUP 제어와 상태 확인

## 작업 상태와 처리 완료

ROLLUP은 생성 시 자동 시작됩니다. START를 즉시 반복하거나 이미 중지한 작업을 다시
STOP하면 상태 오류가 날 수 있습니다. 아래 실습은 생성 → STOP → 입력 → START →
WAKEUP → FORCE 순서로 상태를 구분합니다.

```sql
CREATE TAG TABLE ch6_control (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_control_ru ON ch6_control(value)
  INTERVAL 1 MIN WAKEUP INTERVAL 10 SEC;
ALTER ROLLUP ch6_control_ru STOP;
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_control);

SELECT DISTINCT ROLLUP_NAME, ENABLED, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';

ALTER ROLLUP ch6_control_ru START;
ALTER ROLLUP ch6_control_ru WAKEUP;
ALTER ROLLUP ch6_control_ru FORCE;

SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_control WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

중지 상태의 ENABLED는 0, INTERVAL_TIME은 60000ms, WAKEUP_INTERVAL은 10000ms입니다.
마지막 조회는 TEMP_01의 00:00 평균 15와 00:01 평균 30을 반환합니다.

| 명령 | 목적 | 완료 의미 |
|---|---|---|
| STOP | 작업 중지 | 이후 처리하지 않은 입력분은 남아 있음 |
| START | 중지한 작업 재개 | 처리 위치부터 계속 진행 |
| WAKEUP | 작업을 깨움 | 처리 완료를 기다리지 않음 |
| FORCE | 대상 소스의 처리 범위를 따라잡도록 기다림 | 과거 수정분의 재계산이나 미래 입력 완료는 아님 |
| ROLLUP_REBUILD | 지원 대상의 과거 버킷 재계산 | 원본 보정 후 집계를 다시 구성 |

SQL ALTER 대신 이름을 지정한 `EXEC ROLLUP_START(name)`, `ROLLUP_STOP(name)`,
`ROLLUP_FORCE(name)`도 사용할 수 있습니다. 동일 전환을 두 형식으로 연속 실행하지 않습니다.
이름 없는 일괄 제어와 특정 작업 제어의 범위를 혼동하지 마십시오.

## WAKEUP INTERVAL

생략하면 생성 INTERVAL과 같습니다. 양수이고 집계 간격보다 크지 않아야 하며 집계 간격을
나누어떨어지게 해야 합니다. 더 자주 깨우면 지연을 줄일 수 있지만 처리 부하도 증가합니다.

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 5 SEC;
SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';
```

WAKEUP_INTERVAL이 5000ms로 바뀝니다. 다음은 60초의 약수가 아닌 의도적 오류입니다.

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 7 SEC;
```

## V$ROLLUP 읽기

| 컬럼 | 해석 |
|---|---|
| ROLLUP_NAME | 제어할 작업 이름 |
| ROLLUP_TABLE | 집계 대상 테이블; Custom은 사용자 대상 TAG |
| SOURCE_TABLE, ROOT_TABLE | 직접 소스와 작업을 해석할 원본 관계 |
| COLUMN_NAME | 일반·경로 집계 대상 컬럼 |
| INTERVAL_TIME, WAKEUP_INTERVAL | 밀리초 단위 생성·실행 간격 |
| LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME | 직전에 깨어난 시각과 다음 예정 시각 |
| EXT_TYPE | 0 일반, 1 확장, 2 Custom |
| PREDICATE | 일반 조건식 또는 Custom SELECT 본문 |
| ENABLED | 작업 활성화 여부 |
| RUN_STATE | `I` 초기, `S` 대기, `R` 처리 중 |
| END_RID | 소스 처리 위치 |
| LAST_ELAPSED_MSEC | 직전 처리 시간(ms) |
| DATABASE_NAME, USER_ID | 데이터베이스·소유자 구분 |

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, SOURCE_TABLE, ROOT_TABLE,
       INTERVAL_TIME, WAKEUP_INTERVAL, LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME,
       ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU'
 ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP은 machsql 전용 클라이언트 명령이며 SDK의 일반 SQL API에 보내지 않습니다.
GAP은 소스와 ROLLUP 처리 RID의 차이입니다. 시간 지연 자체가 아니고, 모든 계층·관련 노드의
상태와 함께 봅니다. gap=0이어도 이미 집계한 원본 보정이 반영되었다는 뜻은 아닙니다.
지속 입력 중의 값은 관측 시점에 따라 변하므로 재현 실습에서는 입력을 멈춘 상태로 비교합니다.

중지 기간에 원본이 보존 정책으로 삭제되면 START만으로 그 데이터를 되살릴 수 없습니다.
FORCE는 하위에서 상위 순서로 실행하고, 실패하면 최초 오류·상태·소스 접근 가능성을 확인합니다.

## 정리

```sql
DROP ROLLUP ch6_control_ru;
DROP TABLE ch6_control;
```

자세한 명령 계약은 EXEC 레퍼런스와
ROLLUP 문제 해결을 참고합니다.
