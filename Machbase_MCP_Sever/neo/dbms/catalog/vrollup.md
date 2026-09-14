# V$ROLLUP 사전

`V$ROLLUP`은 Tag 데이터의 Rollup 작업 상태를 실시간으로 표시하는 가상 테이블입니다. Rollup이 정상 작동하는지 확인하거나 실행 주기와 소요 시간을 모니터링할 때 사용합니다.

## 컬럼 상세

| 컬럼 이름 | 타입 | 설명 |
|----------|------|------|
| `ID` | INTEGER | Rollup 작업 ID |
| `ROLLUP_NAME` | VARCHAR | Rollup 작업 이름 |
| `ROLLUP_TABLE` | VARCHAR | Rollup 결과가 저장되는 테이블 이름 |
| `SOURCE_TABLE` | VARCHAR | 집계 대상 원본 TAG 테이블 이름 |
| `COLUMN_NAME` | VARCHAR | 집계 대상 컬럼 이름 |
| `INTERVAL_TIME` | ULONG | 데이터 집계 간격 (밀리초) |
| `WAKEUP_INTERVAL` | ULONG | Rollup 작업의 실행 주기 (밀리초) |
| `LAST_WAKEUP_TIME` | DATETIME | 최근 실행 시각 |
| `ENABLED` | INTEGER | 활성화 여부 (1: 활성, 0: 비활성) |
| `LAST_ELAPSED_MSEC` | DOUBLE | 직전 실행에 걸린 시간 (밀리초) |
| `RUN_STATE` | VARCHAR | 스레드 상태 (I: 초기화, S: 대기, R: 실행중) |

## RUN_STATE 값

| 값 | 설명 |
|----|------|
| `I` | 초기화(Initializing) 중 |
| `S` | 다음 실행을 대기(Sleeping) 중 |
| `R` | 현재 실행(Running) 중 |

## SQL 예제

```sql
-- Rollup 작업 전체 상태 확인
SELECT rollup_name, rollup_table, source_table, column_name,
       interval_time, wakeup_interval, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- 마지막 실행 시각 확인
SELECT rollup_name, rollup_table, last_wakeup_time, last_elapsed_msec, run_state
  FROM v$rollup;

-- 비활성화된 Rollup 확인
SELECT rollup_name, rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;

-- 실행 시간이 오래 걸리는 Rollup 확인
SELECT rollup_name, rollup_table, wakeup_interval, last_elapsed_msec,
       last_elapsed_msec * 100.0 / wakeup_interval AS usage_ratio
  FROM v$rollup
 WHERE last_elapsed_msec > 0
   AND wakeup_interval > 0
 ORDER BY last_elapsed_msec DESC;
```

## 주의 사항

- `INTERVAL_TIME`은 데이터 집계 간격이며, `WAKEUP_INTERVAL`은 Rollup 작업의 실행 주기입니다.
- `LAST_ELAPSED_MSEC`가 `WAKEUP_INTERVAL`보다 크면 직전 실행에 걸린 시간이 설정된 실행 주기를 초과한 것입니다.
  집계 대상 데이터 양과 실행 주기를 점검하십시오. 예제의 `usage_ratio`는 실행 주기 대비 직전 실행 소요시간의 비율(%)입니다.
- `ENABLED = 0`이면 Rollup이 비활성화된 상태입니다. `ALTER ROLLUP rollup_name START` 명령으로 다시 활성화합니다.
  `rollup_name`에는 조회한 `ROLLUP_NAME` 값을 지정합니다.
- Rollup 생성과 관리는 TAG 테이블과 Rollup 섹션을 참고하십시오.
