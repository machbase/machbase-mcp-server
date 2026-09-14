# 활용 패턴과 시나리오

실제 분석에서는 시간, 호스트, 오류 등급, 메시지를 함께 봅니다.
각 기능을 따로 실행해 보았다면 이제 “어느 서버에서 어떤 오류가 늘었는가?”라는 질문으로
연결해 보겠습니다. 이 실습은 앞 절의 테이블 없이도 실행할 수 있습니다.

## 원본 이벤트와 현재 상태

LOG에는 사건이 발생할 때마다 새 행을 추가합니다.
장비의 현재 이름·위치처럼 변경 가능한 기준 정보는 LOOKUP에 분리할 수 있지만,
과거 상태까지 필요하다면 당시 값을 이벤트에 남기거나 이력을 별도로 설계해야 합니다.

보안 이벤트나 작업 추적에도 같은 접근을 사용할 수 있습니다.
센서 이름별 계측 집계가 중심이라면 TAG를, 업무 행의 수정·트랜잭션이 중심이라면
TRANSACTION을 먼저 검토하세요.

## 로그와 인덱스 생성

시간 조건을 실행 날짜와 무관하게 비교하기 위해 도착 시각을 명시합니다.
빈 테이블에 오름차순으로 입력하는 실습이며, 일반 수집에서는 원본 발생 시각을
별도 DATETIME 컬럼에 보관하는 편이 좋습니다.

```sql
CREATE LOG TABLE ch7_app (
    event_id INTEGER,
    host     VARCHAR(32),
    level    VARCHAR(16),
    message  TEXT
);
CREATE INDEX ch7_app_message ON ch7_app(message) INDEX_TYPE KEYWORD;

INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'web-01', 'INFO', 'service started');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:10:00', 'YYYY-MM-DD HH24:MI:SS'),
        2, 'web-01', 'WARN', 'slow response');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:20:00', 'YYYY-MM-DD HH24:MI:SS'),
        3, 'web-02', 'ERROR', 'database timeout');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:30:00', 'YYYY-MM-DD HH24:MI:SS'),
        4, 'web-02', 'ERROR', 'connection refused');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        5, 'web-01', 'INFO', 'normal service');

EXEC TABLE_FLUSH(ch7_app);
EXEC INDEX_FLUSH(ch7_app);
SELECT COUNT(*) AS received_rows FROM ch7_app;
```

입력 건수는 5입니다. 실습을 반복하기 전에 마지막 DROP까지 실행했는지 확인하세요.
단순 재전송은 중복 행이 될 수 있습니다.

## 오류와 시간대별 조회

```sql
SELECT event_id, host, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND message SEARCH 'timeout'
 ORDER BY event_id;

SELECT event_id, host, level, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND level = 'ERROR'
 ORDER BY event_id;
```

첫 쿼리는 web-02의 3번, 두 번째는 3·4번을 선택합니다.
특정 단어로 시작하되 분석할 때는 같은 호스트·시간대의 다른 오류도 함께 확인하는
흐름입니다. 검색 범위를 넓힐 때는 시간 조건을 통째로 제거하기보다 필요한 구간만 늘리세요.

## 시간별·등급별 집계

```sql
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS event_hour,
       level, COUNT(*) AS event_count
  FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
 ORDER BY event_hour, level;
```

| event_hour | level | event_count |
|---|---|---|
| 2026-01-01 10 | ERROR | 2 |
| 2026-01-01 10 | INFO | 1 |
| 2026-01-01 10 | WARN | 1 |
| 2026-01-01 11 | INFO | 1 |

이 쿼리는 원본 LOG를 읽어 수행하는 집계입니다. TAG의 ROLLUP을 자동으로 사용하는
쿼리가 아닙니다. 데이터가 커지면 조회 구간과 실행 계획을 확인하고, 사전 집계가 필요한지
별도로 판단하세요.

실수하기 쉬운 부분은 고정 시각 데이터에 `DURATION 1 HOUR`를 적용하는 것입니다.
그 조건은 현재 시각 기준이므로 실행 날짜가 바뀌면 표본이 선택되지 않을 수 있습니다.
운영의 최근 로그 조회와 재현용 고정 시각 조회를 구분하세요.

## 수집과 보존 관리

지속 수집은 Append 입력에서 이어서 구성할 수 있습니다.
장기 운영에서는 보존 정책을 함께 정하세요.
원본 로그, 백업, 별도로 만드는 집계 데이터는 필요한 보관 기간이 다를 수 있습니다.

```sql
DROP TABLE ch7_app;
```

여기까지 결과가 맞으면 실제 로그 몇 건으로 필드와 메시지를 바꾸어 보세요.
한 번에 전체 수집을 옮기기보다 작은 표본으로 같은 질문에 답할 수 있는지 확인하는 편이
문제를 찾기 쉽습니다.
