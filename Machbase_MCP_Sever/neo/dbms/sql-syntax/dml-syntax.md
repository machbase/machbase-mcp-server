# DML

DML(Data Manipulation Language)은 테이블에 데이터를 삽입·수정·삭제하는 구문입니다.

## 테이블 유형별 DML 지원

| 구문 | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| INSERT | O | O | O | O | O |
| INSERT SELECT | O | O | O | O | O |
| UPDATE | - | O(태그/축 조건 또는 메타데이터) | O(일반 조건식) | O(PK 조건) | O |
| DELETE | O(보존 조건/전체) | O(시간/이름 조건) | O(일반 조건식/전체) | O(PK 조건) | O |
| DELETE WHERE | - | O(태그/축 조건) | O(일반 조건식) | O(PK equality) | O |
| TRUNCATE | O | - | - | - | O |

> LOG 테이블의 UPDATE는 지원하지 않습니다. 데이터 수정이 필요하면 LOOKUP 또는 VOLATILE 테이블을 사용하거나 TRANSACTION 테이블을 선택하십시오.

---

## INSERT INTO

```sql
insert_stmt ::=
    'INSERT INTO' table_name
    [ 'METADATA' ]
    [ '(' insert_column_list ')' ]
    'VALUES' '(' value_list ')'
    [ 'ON DUPLICATE KEY UPDATE' [ 'SET' set_list ] ]

insert_column_list ::= insert_target ( ',' insert_target )*
insert_target      ::= column_name | array_column_name '[' position ']'
value_list         ::= value ( ',' value )*
set_list           ::= column_name '=' value ( ',' column_name '=' value )*
```

지정하지 않은 컬럼에는 NULL이 입력됩니다. `METADATA`는 TAG 테이블의 메타데이터 컬럼에 삽입할 때 사용합니다.

```sql
-- 기본 삽입
INSERT INTO sensor_log VALUES (1, 'sensor-01', 23.5, 'OK');

-- 컬럼 지정 삽입
INSERT INTO sensor_log (name, value) VALUES ('sensor-01', 23.5);

-- TAG 테이블 메타데이터 삽입
INSERT INTO sensors METADATA (name, location, unit)
VALUES ('sensor-01', 'building-A', 'celsius');
```

### ARRAY element target

Machbase DBMS 8.7.0에서는 `INSERT ... VALUES`의 컬럼 목록에 고정 길이 `ARRAY`의 위치를
지정할 수 있습니다. position은 0부터 시작합니다. 지정하지 않은 요소는 element NULL로
저장됩니다.

```sql
CREATE LOG TABLE array_input (
    id INTEGER,
    channels INT32[4]
);

INSERT INTO array_input (id, channels[0], channels[3])
VALUES (1, 10, 40);
```

같은 문장에서 whole ARRAY target과 element target을 함께 사용하거나 같은 위치를 두 번
지정할 수 없습니다. scalar 컬럼과 범위 밖 position도 element target으로 사용할 수
없습니다. indexed target은 `INSERT ... SELECT`와 `UPDATE SET`에서는 지원하지 않습니다.

ARRAY 값 생성, sparse 입력과 Append 선택 target은
숫자 ARRAY 타입과
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

### ON DUPLICATE KEY UPDATE

`INSERT ... VALUES`에서 duplicate key가 발생하면 기존 행을 UPDATE합니다. `INSERT ... SELECT`와
결합할 수 없습니다.

| 테이블 타입 | duplicate 판정 key | 지원 범위 |
|---|---|---|
| TRANSACTION | PRIMARY KEY, 단일·복합 UNIQUE INDEX | Standard Edition |
| LOOKUP | PRIMARY KEY | 지원 |
| VOLATILE | PRIMARY KEY | 지원 |
| TAG METADATA | tag name PRIMARY KEY | 지원 |
| TAG data, LOG | - | 미지원 |

`SET`을 생략하면 INSERT 입력값으로 기존 non-key 컬럼을 갱신합니다. `SET`이 있으면 오른쪽
표현식은 duplicate 기존 행을 기준으로 평가합니다. LOOKUP·VOLATILE·TRANSACTION에서는
PRIMARY KEY 자체를 갱신할 수 없습니다. TAG METADATA의 tag name과 시스템 관리 컬럼은
TAG 메타데이터의 변경 규칙을 따릅니다.

```sql
-- 키 중복 시 value 컬럼만 업데이트
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.1', 'ONLINE')
ON DUPLICATE KEY UPDATE SET status = 'ONLINE';

-- SET 절 없이 사용하면 모든 컬럼을 삽입 값으로 업데이트
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.2', 'ONLINE')
ON DUPLICATE KEY UPDATE;
```

duplicate를 판정할 key가 없는 table에서의 UPSERT, key 변경, `VALUES(col)`·`EXCLUDED.col` 같은
다른 DBMS 전용 표현은 오류입니다. TRANSACTION의 UNIQUE 충돌·transaction 예제는
TRANSACTION upsert를 참고하십시오.

---

## INSERT SELECT

```sql
insert_select_stmt ::=
    'INSERT INTO' table_name
    [ '(' insert_column_list ')' ]
    [ with_clause ]
    select_stmt
```

SELECT 결과를 테이블에 삽입합니다. Standard Edition에서는 대상 테이블과 컬럼 목록 뒤에
`WITH` 절을 둘 수 있습니다. 문장 선두의 `WITH ... INSERT INTO ...` 형식은 지원하지
않습니다.

```sql
-- 조회 결과를 다른 테이블에 복사
INSERT INTO sensor_log_copy SELECT * FROM sensor_log;

-- _arrival_time 명시 삽입 (시간 순서 보장 필요)
INSERT INTO sensor_log_copy (_arrival_time, id, name, value)
SELECT _arrival_time, id, name, value FROM sensor_log ORDER BY _arrival_time;

-- CTE 결과 삽입
INSERT INTO sensor_log_copy (id, name, value)
WITH filtered AS (
    SELECT id, name, value
    FROM sensor_log
    WHERE value >= 80
)
SELECT id, name, value FROM filtered;
```

주의사항:
- `_ARRIVAL_TIME`을 명시하지 않으면 INSERT 실행 시점의 시간이 자동 입력됩니다.
- LOG의 명시 시각 복사는 빈 대상에 오름차순으로 입력하고, 다른 입력 작업과 분리하세요.
  대상에 더 최신 시각이 있으면 원본을 정렬했더라도 역전 입력이 됩니다.
  기본 `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1`에서는 역전된 값을 직전 저장
  시각+1ns로 보정하고, 0에서는 거부합니다. 따라서 명시 입력이 원본 시각 보존을
  무조건 보장하지는 않습니다.
- VARCHAR 컬럼에서 삽입 값이 최대 길이를 초과하면 자동으로 잘라서 입력됩니다.
- LOG/TAG 입력은 TRANSACTION 테이블 트랜잭션의 ROLLBACK 대상이 아닙니다.

---

## UPDATE

```sql
update_stmt ::=
    'UPDATE' table_name [ 'METADATA' ]
    'SET' update_expr_list
    [ 'WHERE' predicate ]

update_expr_list ::= column_name '=' value ( ',' column_name '=' value )*
```

TRANSACTION 테이블은 WHERE 절을 생략하면 모든 행을 수정합니다. LOOKUP 테이블은 기본 키 또는 일반
조건식을 사용하고, VOLATILE 테이블은 기본 키 일치 조건을 사용합니다. TAG data UPDATE는 태그
선택자와 시간축 조건을 함께 사용합니다.

```sql
-- LOOKUP 테이블 레코드 수정
UPDATE devices SET status = 'OFFLINE' WHERE device_id = 'dev-001';

-- 여러 컬럼 동시 수정
UPDATE devices SET ip = '10.0.0.1', status = 'ONLINE' WHERE device_id = 'dev-002';

-- LOOKUP 일반 조건식으로 여러 행 수정
UPDATE devices SET status = 'OFFLINE' WHERE site = 'SEOUL' AND status = 'READY';

```

### TAG data UPDATE

TAG 테이블의 실제 시계열 데이터는 태그 선택 조건과 BASETIME 조건을 함께 지정해 수정합니다.

```sql
UPDATE sensors
   SET value = 101,
       status = 1
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

`name`(PRIMARY KEY), `time`(BASETIME), 메타데이터 컬럼은 data UPDATE의 SET 대상이 아닙니다.

### UPDATE METADATA (TAG 테이블)

TAG 테이블의 메타데이터 컬럼은 별도 `UPDATE ... METADATA` 구문으로 수정합니다.

```sql
-- 메타데이터 조건으로 여러 행 수정
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';

-- tag name 기준으로 수정
UPDATE sensors METADATA
   SET location = 'building-B'
 WHERE name = 'sensor-01';
```

---

## DELETE

```sql
-- LOG 테이블용 삭제 (시간/행 수 기반)
delete_stmt ::=
    'DELETE FROM' table_name
    [ 'OLDEST' number 'ROWS'
    | 'EXCEPT' number ( 'ROWS' | time_unit )
    | 'BEFORE' datetime_expression ]
    [ 'NO WAIT' ]

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

LOG 테이블에서는 임의 위치 삭제를 지원하지 않으며, 가장 오래된 데이터부터 연속으로만 삭제할 수 있습니다.

현재 LOG의 `BEFORE t`는 `_arrival_time <= t`인 행을 삭제합니다.
이름만 보고 경계를 제외한다고 생각하기 쉬우므로 사전 조회도 같은 비교 조건을 사용하세요.
`EXCEPT n DAY` 등의 기간은 서버 현재 시각을 기준으로 계산하며 마지막 입력 시각을
기준으로 하지 않습니다. 일반 사용자 DATETIME 컬럼의 값은 이 삭제 기준이 아닙니다.
실제 전후 결과는 LOG 보존형 삭제에서
확인할 수 있습니다.

```sql
-- 모든 데이터 삭제
DELETE FROM sensor_log;

-- 가장 오래된 N건 삭제
DELETE FROM sensor_log OLDEST 1000 ROWS;

-- 최근 N건을 제외하고 모두 삭제
DELETE FROM sensor_log EXCEPT 10000 ROWS;

-- 최근 N일 데이터를 제외하고 모두 삭제
DELETE FROM sensor_log EXCEPT 7 DAY;

-- 특정 시각까지의 데이터 삭제 (경계 시각 포함)
DELETE FROM sensor_log BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

### DELETE WHERE (LOOKUP/VOLATILE 테이블)

```sql
delete_where_stmt ::=
    'DELETE FROM' table_name 'WHERE' predicate
```

LOOKUP 테이블은 기본 키 또는 일반 조건식을 사용합니다. VOLATILE 테이블은 기본 키 일치 조건을
사용합니다. LOOKUP 테이블은 WHERE 절을 생략하여 모든 행을 삭제할 수도 있습니다.

```sql
DELETE FROM devices WHERE device_id = 'dev-001';

-- LOOKUP 일반 조건식으로 여러 행 삭제
DELETE FROM devices WHERE status = 'EXPIRED' OR site = 'RETIRED';

-- LOOKUP 전체 삭제
DELETE FROM devices;
```

### DELETE (TAG 테이블)

```sql
-- TAG 테이블: 이름 또는 시간 조건으로 삭제
delete_from_tag_where_stmt ::=
    'DELETE FROM' table_name [ 'ROLLUP' ]
    'WHERE' predicate
    -- predicate: tag_name 조건, tag_time 조건, 또는 두 조건의 AND 조합
```

시간 조건에는 `=`, `<`, `<=`, `BETWEEN`을 사용할 수 있습니다.

```sql
-- TAG 이름 기준 삭제
DELETE FROM tag WHERE name = 'sensor-01';

-- TAG 이름 + 시간 기준 삭제
DELETE FROM tag WHERE name = 'sensor-01' AND time < TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 시간 조건만으로 삭제
DELETE FROM tag WHERE time <= TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- ROLLUP 데이터 삭제
DELETE FROM tag ROLLUP WHERE name = 'sensor-01';
DELETE FROM tag ROLLUP WHERE time BETWEEN TO_DATE('2024-01-01','YYYY-MM-DD') AND TO_DATE('2024-02-01','YYYY-MM-DD');
```

### DELETE FROM TAG METADATA

```sql
DELETE FROM table_name METADATA [ WHERE predicate ]
```

TAG 테이블의 메타데이터 행을 삭제합니다. WHERE를 생략하면 모든 메타데이터를 삭제합니다. 실제 데이터가 있는 태그의 메타데이터는 삭제할 수 없습니다.

```sql
DELETE FROM sensors METADATA WHERE name = 'sensor-01';
DELETE FROM sensors METADATA WHERE status = 'STOP';
DELETE FROM sensors METADATA;  -- 모든 메타데이터 삭제 (실제 데이터 없는 태그만)
```

---

## UPDATE/DELETE 영향 행 수

`UPDATE`와 `DELETE`를 실행한 클라이언트는 해당 문장의 영향 행 수(affected rows)를
확인할 수 있습니다. Direct execution과 prepared statement 모두 같은 기준을 사용합니다.

`UPDATE`는 실제로 값이 달라진 행 수가 아니라 `WHERE` 조건에 일치한 행 수를 반환합니다.
따라서 기존 값과 같은 값을 다시 설정해도 대상 행이 조건에 일치하면 영향 행 수에
포함됩니다. `WHERE` 절을 생략할 수 있는 테이블에서는 모든 대상 행이 일치한 것으로
계산합니다.

`DELETE`는 조건에 일치해 실제로 삭제된 행 수를 반환합니다. 같은 `DELETE`를 반복하면
첫 실행에서 행이 제거되므로 다음 실행은 `0`을 반환합니다.

```sql
CREATE LOOKUP TABLE device_state (
    id INTEGER PRIMARY KEY,
    value INTEGER
);

INSERT INTO device_state VALUES (1, 10);
INSERT INTO device_state VALUES (2, 10);

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated.

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated. (동일 값 반복 UPDATE)

UPDATE device_state SET value = 20 WHERE id = 999;
-- No row updated.

DELETE FROM device_state WHERE id = 1;
-- 1 row(s) deleted.

DELETE FROM device_state WHERE id = 1;
-- No row deleted.
```

`No row updated.` 또는 영향 행 수 `0`은 설정한 값이 기존 값과 같다는 의미가 아니라,
조건에 일치한 행이 없다는 의미입니다.

트랜잭션에서 반환된 영향 행 수는 각 문장을 실행한 시점의 결과입니다. 이후
`ROLLBACK`하더라도 이미 반환된 영향 행 수의 의미는 바뀌지 않습니다.

---

## 관련 문서

- DDL 문법 사전 - 테이블 생성 및 스키마 변경
- SELECT 문법 사전 - 데이터 조회
- WITH / CTE syntax - CTE를 사용한 INSERT SELECT
- LOOKUP predicate UPDATE - 일반 조건식 갱신
- LOOKUP predicate DELETE - 일반 조건식 삭제
- LOAD DATA INFILE - CSV 파일 일괄 입력
