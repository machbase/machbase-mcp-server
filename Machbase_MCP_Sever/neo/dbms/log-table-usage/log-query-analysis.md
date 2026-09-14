# 조회와 분석

시간 범위를 조금만 다르게 잡아도 조회 건수가 달라집니다.
특히 하루씩 나누어 집계할 때 끝 시각을 양쪽 구간에 모두 포함하면 경계의 행이 중복됩니다.
이 절에서는 고정 시각 데이터로 범위와 결과 순서를 확인한 뒤 기준 정보를 조인합니다.

## 실습 데이터 준비

```sql
CREATE LOG TABLE ch7_query (
    event_id INTEGER,
    device   VARCHAR(32),
    value    DOUBLE
);

INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'DEV-01', 10);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 'DEV-01', 20);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'DEV-02', 30);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 'DEV-02', 40);

SELECT _arrival_time, event_id, device, value
  FROM ch7_query
 ORDER BY _arrival_time, event_id;
```

결과는 1·2·3·4번 순서입니다. 2·3번처럼 같은 시각의 행도 있으므로
순서를 고정하려면 시간뿐 아니라 이벤트 번호까지 정렬 기준에 넣습니다.
이 번호는 예제에서 직접 관리하는 값이며 LOG의 자동 고유 키가 아닙니다.

## 연속 구간과 시간 경계

```sql
SELECT event_id, value
  FROM ch7_query
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

1·2·3번이 선택됩니다. 다음 구간을 12:00부터 시작하면 4번은 그 구간에서만 집계됩니다.
`BETWEEN`은 양 끝을 포함하므로 이런 연속 구간과 의미가 다릅니다.
사용자 정의 `event_time`을 기준으로 분석할 때도 같은 WHERE 패턴을 사용하면 됩니다.

## DURATION 조회

```sql
SELECT event_id FROM ch7_query
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION 1 HOUR AFTER TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

| 쿼리 | 시간 범위 | 선택되는 event_id |
|---|---|---|
| 12:00 이전 1시간 | 11:00~12:00, 양 끝 포함 | 2, 3, 4 |
| 10:00 이후 1시간 | 10:00~11:00, 양 끝 포함 | 1, 2, 3 |
| 10:00부터 12:00까지 | 양 끝 포함 | 1, 2, 3, 4 |

`DURATION 1 HOUR`처럼 기준 시각을 생략하면 현재 시각을 기준으로 합니다.
따라서 오래된 고정 시각 실습에 그대로 사용하면 결과가 없을 수 있습니다.
문법 위치는 WHERE 다음, GROUP BY·ORDER BY 앞입니다.

실수하기 쉬운 부분은 DURATION이 모든 시간 컬럼에 적용되는 조건이라고 생각하는 것입니다.
DURATION은 LOG 전용이며 `_arrival_time`을 사용합니다. TAG의 시간 컬럼이나 사용자
DATETIME 조건은 WHERE로 지정하세요. 자세한 문법은
상대 시간·DURATION 사전을 참고하세요.

## 스캔 방향과 정렬

DURATION의 BEFORE는 최신 쪽부터, AFTER는 오래된 쪽부터 읽는 방향을 지정합니다.
FROM … TO는 두 시각의 순서에 따라 방향이 달라집니다.
아래는 역순 범위와 같은 시각의 경계를 확인하는 예제입니다.

```sql
SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id DESC;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

첫 결과는 4·3·2·1번이고, 같은 시각을 지정한 두 번째 결과는 2·3번입니다.
여기서는 스캔 방향과 별개로 ORDER BY를 명시해 출력 순서를 고정했습니다.

하지만 집계·조인 등까지 포함한 최종 결과의 순서가 필요하다면 ORDER BY를 명시하세요.
특히 LIMIT만 사용해서 어떤 행이 나올지 추측하지 않는 것이 좋습니다.

전역 `TABLE_SCAN_DIRECTION`은 다른 쿼리에도 영향을 줄 수 있습니다.
화면 출력 순서를 바꾸기 위해 서버 설정부터 바꾸지는 마세요.
쿼리 튜닝에서 실행 계획을 확인한 뒤
필요한 접근 경로를 조정하세요.

## LOOKUP 조인

```sql
CREATE LOOKUP TABLE ch7_query_device (
    device VARCHAR(32) PRIMARY KEY,
    label  VARCHAR(64)
);
INSERT INTO ch7_query_device VALUES ('DEV-01', 'Boiler');
INSERT INTO ch7_query_device VALUES ('DEV-02', 'Pump');

SELECT q.event_id, d.label, q.value
  FROM ch7_query q
  JOIN ch7_query_device d ON q.device = d.device
 WHERE q._arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND q._arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY q.event_id;
```

결과는 `(1, Boiler, 10)`, `(2, Boiler, 20)`, `(3, Pump, 30)`입니다.
LOG와 LOOKUP을 섞은 쿼리이므로 DURATION 대신 LOG 컬럼의 WHERE 범위를 사용합니다.
이 INNER JOIN에서는 기준 정보가 없는 이벤트가 결과에서 빠진다는 점도 확인하세요.

또한 현재 LOOKUP 값을 조인한다고 과거 시점의 장치 설명이 복원되는 것은 아닙니다.
이력이 필요하면 당시 설명을 이벤트에 저장하거나 유효 기간을 가진 별도 이력을 설계해야 합니다.

```sql
DROP TABLE ch7_query_device;
DROP TABLE ch7_query;
```

조회 건수가 예상과 다르면 시간 경계와 조인 전 건수를 먼저 확인하세요.
조건을 하나씩 추가하면 어디에서 행이 빠지는지 찾기 쉽습니다.
