# 인덱스와 성능

인덱스는 조회 속도뿐 아니라 데이터의 고유성을 결정하기도 합니다.
업무 키를 보장할 인덱스와 읽기를 줄일 인덱스를 구분해야,
성능 정리 과정에서 필요한 제약을 실수로 없애지 않습니다.

## 인덱스 유형

| 종류 | 용도 | 복합 컬럼 | NULL |
|---|---|---|---|
| PRIMARY KEY | 행 식별, 테이블당 하나 | 미지원 | 불허 |
| UNIQUE INDEX | 업무 키의 고유성 | 지원 | NULL 포함 키끼리는 중복 아님 |
| 일반 인덱스 | 조건 조회의 접근 경로 | 지원 | 고유성 검사 없음 |

TRANSACTION 인덱스는 BTREE로 표시됩니다.
컬럼의 PRIMARY KEY 또는 사후 CREATE PRIMARY KEY INDEX를 사용할 수 있습니다.
LOG의 LSM·KEYWORD 인덱스 구문을 TRANSACTION에 그대로 적용하지 마세요.

## UNIQUE INDEX와 NULL

```sql
CREATE TRANSACTION TABLE ch8_index_account (
    id      LONG PRIMARY KEY,
    email   VARCHAR(120),
    tenant  INTEGER NOT NULL,
    login   VARCHAR(64)
);
INSERT INTO ch8_index_account VALUES (1, 'a@example.com', 1, 'alpha');
INSERT INTO ch8_index_account VALUES (2, 'b@example.com', 1, 'beta');
INSERT INTO ch8_index_account VALUES (3, NULL, 2, NULL);
INSERT INTO ch8_index_account VALUES (4, NULL, 2, NULL);

CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
CREATE UNIQUE INDEX ch8_index_login ON ch8_index_account(tenant, login);

SELECT id FROM ch8_index_account WHERE email IS NULL ORDER BY id;
SHOW INDEX ch8_index_email;
```

3·4번이 모두 존재하고 인덱스도 생성됩니다.
반드시 값이 있어야 하는 업무 키라면 UNIQUE뿐 아니라 각 컬럼의 NOT NULL도 필요합니다.
CREATE TABLE 내부에 UNIQUE를 붙이는 대신 별도 CREATE UNIQUE INDEX를 사용하세요.

다음 두 문장은 각각 고유성 위반을 확인하는 선택 실습입니다.

```sql
-- 의도적으로 실패: email 중복
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
UPDATE ch8_index_account SET email = 'a@example.com' WHERE id = 2;
```

실패 후에는 네 행과 2번의 b@example.com이 유지되어야 합니다.
현재 일반 UNIQUE 위반은 ERR-01418로 보고됩니다.
오류 메시지만 보고 어떤 업무 키가 중복되었는지 단정하지 말고 인덱스와 입력값을 함께
확인하세요.

## UNIQUE INDEX 삭제

```sql
DROP INDEX ch8_index_email;
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
SELECT id, email FROM ch8_index_account WHERE email = 'a@example.com' ORDER BY id;
```

이제 1·5번이 모두 저장됩니다.
중복이 있는 상태에서 인덱스를 재생성하면 실패합니다.

```sql
-- 의도적으로 실패: 기존 데이터에 중복이 있습니다.
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
```

실습 중 추가한 5번을 제거한 뒤 다시 생성합니다.

```sql
DELETE FROM ch8_index_account WHERE id = 5;
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
SELECT COUNT(*) AS remaining_rows FROM ch8_index_account;
```

건수는 4입니다.
운영에서는 인덱스를 없애기 전에 이것이 성능용인지 고유성 보장용인지부터 확인해야 합니다.

## 일반·복합 인덱스

```sql
CREATE TRANSACTION TABLE ch8_index_event (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME,
    state   JSON
);
INSERT INTO ch8_index_event VALUES (
    1, 'OPEN', TO_DATE('2026-01-01', 'YYYY-MM-DD'), '{"status":"ALARM","code":500}');
INSERT INTO ch8_index_event VALUES (
    2, 'CLOSED', TO_DATE('2026-01-02', 'YYYY-MM-DD'), '{"status":"NORMAL","code":200}');
INSERT INTO ch8_index_event VALUES (
    3, 'OPEN', TO_DATE('2026-01-03', 'YYYY-MM-DD'), '{"code":500}');

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

CREATE INDEX ch8_index_status_time ON ch8_index_event(status, created);

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
 ORDER BY id;
```

결과는 생성 전후 의미가 같아야 하며 마지막 조회는 1·3번입니다.
선두 컬럼을 조건에 맞추되 모든 복합 조건이 반드시 해당 인덱스를 사용한다고
단정하지 마세요. Machbase의 계획 선택과 지원되는 조건 모양을 EXPLAIN으로 확인합니다.
세 행의 실행 시간은 성능 벤치마크가 아닙니다.

## JSON path 인덱스

```sql
CREATE INDEX ch8_index_json_status ON ch8_index_event(state->'$.status');
CREATE INDEX ch8_index_json_code ON ch8_index_event(state->'$.code');

EXPLAIN SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM';
SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM' ORDER BY id;
SELECT id FROM ch8_index_event WHERE state->'$.code' = '500' ORDER BY id;
```

상태 조회는 1번, code 조회는 1·3번입니다.
인덱스를 만들었다고 모든 JSON 함수 표현식이 이 경로를 사용하는 것은 아닙니다.
화살표 경로와 숫자 추출 함수는 결과 타입과 비교 의미를 구분하세요.
복잡한 조건이 자주 반복되면 일반 컬럼으로 분리한 설계도 비교할 수 있습니다.

JSON path UNIQUE INDEX를 만들 수 있는 경우에도 TRANSACTION UPSERT의 충돌 선택 키로는
사용하지 않습니다. UPSERT 제약을 확인하세요.

## 읽기·쓰기 비용

인덱스 생성 전후에 같은 데이터량·조건값·동시 입력률을 사용하세요.
조회 시간뿐 아니라 INSERT·UPDATE·DELETE 처리량과 인덱스 공간도 함께 비교합니다.
LIMIT은 반환량을 줄이지만 어떤 행을 반환할지 고정하려면 ORDER BY가 필요합니다.

```sql
DROP TABLE ch8_index_event;
DROP TABLE ch8_index_account;
```

성능 때문에 UNIQUE INDEX를 일반 인덱스로 바꾸면 고유성 보장은 사라집니다.
튜닝 전후에 결과와 제약이 같은지 먼저 확인하는 것이 좋은 출발점입니다.
