# TRANSACTION INSERT ON DUPLICATE KEY UPDATE

“없으면 추가하고 있으면 수정”하는 작업은 간단해 보이지만, 무엇을 중복으로 보는지에
따라 다른 행이 바뀔 수 있습니다. 특히 카운터 증가를 재전송하면 같은 이벤트가 두 번
반영될 수 있습니다. 키와 갱신 대상, 재시도 정책을 함께 확인하세요.

TRANSACTION의 `INSERT ... ON DUPLICATE KEY UPDATE`는 PRIMARY KEY 또는 일반 UNIQUE INDEX
충돌 시 기존 행을 갱신합니다. 아래 실습은 페이지 안에서 필요한 객체를 직접 준비합니다.
오류 확인 SQL은 정상 흐름과 분리하고, 마지막 정리까지 실행한 뒤 재실행하세요.

## 지원 문법

TRANSACTION 테이블에서는 `INSERT ... VALUES ...` 형태의 upsert를 지원합니다.

```text
INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];
```

충돌 판정 키로 인정되는 대상은 다음과 같습니다.

- TRANSACTION PRIMARY KEY
- TRANSACTION UNIQUE INDEX
- TRANSACTION 복합 UNIQUE INDEX

## 기본 동작

중복이 없으면 일반 INSERT와 같이 새 행을 추가합니다.

```sql
CREATE TRANSACTION TABLE ch8_up_device_state (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    alarm_count INTEGER,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_state
VALUES (1, 'NORMAL', 0, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'NORMAL',
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

PRIMARY KEY가 중복되면 기존 행을 UPDATE합니다.

```sql
INSERT INTO ch8_up_device_state
VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        alarm_count = alarm_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

`SET` 절에서는 PRIMARY KEY를 변경할 수 없습니다. 오른쪽 식은 충돌한 기존 행을
기준으로 평가됩니다. 따라서 `alarm_count = alarm_count + 1`은 INSERT하려던 값이
아니라 기존 행의 alarm_count에 1을 더합니다.

```sql
SELECT device_id, status, alarm_count, updated_at
FROM ch8_up_device_state
WHERE device_id = 1;
```

예상 결과 형태는 다음과 같습니다.

```text
DEVICE_ID  STATUS  ALARM_COUNT  UPDATED_AT
---------  ------  -----------  -----------------------------
1          ALARM   1            2026-07-10 09:05:00 000:000:000
```

`ON DUPLICATE KEY UPDATE` 뒤에 `SET` 절을 쓰지 않을 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_asset_cache (
    asset_id INTEGER PRIMARY KEY,
    asset_name VARCHAR(80),
    location VARCHAR(80),
    keep_value INTEGER
);

INSERT INTO ch8_up_asset_cache VALUES (1, 'compressor-a', 'plant-1', 100);

INSERT INTO ch8_up_asset_cache(asset_id, asset_name, location)
VALUES (1, 'compressor-a-renamed', 'plant-2')
    ON DUPLICATE KEY UPDATE;
```

`SET` 절이 없으면 INSERT 대상 컬럼 중 PRIMARY KEY가 아닌 컬럼만 기존 행에 반영됩니다. 위 예에서는 `asset_name`, `location`이 갱신되고, 컬럼 목록에 없던 `keep_value`는 기존 값을 유지합니다.

```sql
SELECT asset_id, asset_name, location, keep_value
FROM ch8_up_asset_cache
ORDER BY asset_id;
```

예상 결과 형태는 다음과 같습니다.

```text
ASSET_ID  ASSET_NAME            LOCATION  KEEP_VALUE
--------  --------------------  --------  ----------
1         compressor-a-renamed  plant-2   100
```

PRIMARY KEY 컬럼만 있는 테이블에서 중복 행에 `SET` 없는 upsert를 실행하면 갱신 대상 컬럼이 없으므로 행은 변경되지 않습니다.

## UNIQUE INDEX 중복 처리

PRIMARY KEY뿐 아니라 UNIQUE INDEX 충돌도 갱신 경로를 실행합니다.

```sql
CREATE TRANSACTION TABLE ch8_up_account_profile (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    display_name VARCHAR(80),
    login_count INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_account_profile_email
ON ch8_up_account_profile(email);

INSERT INTO ch8_up_account_profile
VALUES (1, 'ops@example.com', 'ops-user', 1);

INSERT INTO ch8_up_account_profile
VALUES (2, 'ops@example.com', 'ops-renamed', 1)
    ON DUPLICATE KEY UPDATE SET
        display_name = 'ops-renamed',
        login_count = login_count + 1;

SELECT id, email, display_name, login_count
FROM ch8_up_account_profile
ORDER BY id;
```

`email` UNIQUE INDEX가 중복되므로 `id = 1` 행이 UPDATE됩니다. INSERT하려던 `id = 2` 행은 새로 추가되지 않습니다.

복합 UNIQUE INDEX는 키 조합 전체가 같은 경우 중복으로 처리됩니다.

```sql
CREATE TRANSACTION TABLE ch8_up_daily_device_summary (
    id INTEGER PRIMARY KEY,
    device_id INTEGER,
    summary_day VARCHAR(10),
    event_count INTEGER,
    last_status VARCHAR(16)
);

CREATE UNIQUE INDEX ch8_up_uidx_daily_device_summary
ON ch8_up_daily_device_summary(device_id, summary_day);

INSERT INTO ch8_up_daily_device_summary
VALUES (1, 101, '2026-07-10', 3, 'NORMAL');

INSERT INTO ch8_up_daily_device_summary
VALUES (2, 101, '2026-07-10', 1, 'ALARM')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1,
        last_status = 'ALARM';

INSERT INTO ch8_up_daily_device_summary
VALUES (3, 101, '2026-07-11', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1;
```

첫 번째 upsert는 `(device_id, summary_day) = (101, '2026-07-10')` 행을 UPDATE합니다. 두 번째 upsert는 날짜가 다르므로 새 행을 INSERT합니다.

UNIQUE KEY에 NULL이 포함된 행끼리는 중복으로 처리하지 않습니다.
다음 두 입력은 서로 덮어쓰지 않고 각각 새 행이 됩니다.

```sql
INSERT INTO ch8_up_daily_device_summary VALUES (4, NULL, '2026-07-10', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE;
INSERT INTO ch8_up_daily_device_summary VALUES (5, NULL, '2026-07-10', 2, 'ALARM')
    ON DUPLICATE KEY UPDATE;
SELECT id, device_id, summary_day, event_count
  FROM ch8_up_daily_device_summary ORDER BY id;
```

결과 id는 1·3·4·5이며 event_count는 각각 4·1·1·2입니다.
필수 업무 키라면 UNIQUE INDEX뿐 아니라 구성 컬럼의 NOT NULL도 필요합니다.

## 활용 예제

TAG 테이블에는 시간순 측정값이 계속 쌓이고, TRANSACTION 테이블에는 장비별 최신 상태만 유지할 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_latest_device_status (
    device_name VARCHAR(80) PRIMARY KEY,
    last_value DOUBLE,
    last_state VARCHAR(16),
    event_count LONG,
    updated_at DATETIME
);

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 72.5, 'NORMAL', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 72.5,
        last_state = 'NORMAL',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 91.2, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 91.2,
        last_state = 'ALARM',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

이 패턴은 대시보드가 최신 상태만 빠르게 조회해야 할 때 사용할 수 있습니다.

외부 시스템에서 같은 업무 키로 기준 데이터를 반복 전송할 때 UNIQUE INDEX를 기준으로 upsert할 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_customer_device (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    external_device_id VARCHAR(64),
    device_name VARCHAR(80),
    owner_name VARCHAR(80),
    enabled INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_customer_device_external_id
ON ch8_up_customer_device(external_device_id);

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a', 'line-1', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a',
        owner_name = 'line-1',
        enabled = 1;

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a-renamed', 'line-2', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a-renamed',
        owner_name = 'line-2',
        enabled = 1;
```

첫 INSERT는 새 행을 생성하고, 두 번째 INSERT는 `external_device_id` UNIQUE INDEX 충돌로 기존 행을 UPDATE합니다. 내부 `id`는 유지됩니다.

소스 데이터의 컬럼 값을 그대로 최신 캐시에 반영하고 싶으면 `SET` 절 없는 upsert를 사용할 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_tag_alias_cache (
    alias_name VARCHAR(80) PRIMARY KEY,
    tag_name VARCHAR(80),
    unit VARCHAR(16),
    description VARCHAR(160),
    manually_checked INTEGER
);

INSERT INTO ch8_up_tag_alias_cache
VALUES ('compressor-a-temp', 'comp_a.temp', 'celsius', 'main compressor temp', 1);

INSERT INTO ch8_up_tag_alias_cache(alias_name, tag_name, unit, description)
VALUES ('compressor-a-temp', 'comp_a.temperature', 'celsius', 'renamed tag')
    ON DUPLICATE KEY UPDATE;
```

위 구문은 `tag_name`, `unit`, `description`만 갱신합니다. 컬럼 목록에 없는 `manually_checked`는 기존 값을 유지합니다.

집계 테이블에서 키별 발생 횟수를 누적할 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_alarm_counter (
    alarm_code VARCHAR(32) PRIMARY KEY,
    first_seen DATETIME,
    last_seen DATETIME,
    hit_count LONG
);

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;
```

`hit_count = hit_count + 1`은 기존 행 기준으로 계산되므로 누적 카운터 구현에 사용할 수 있습니다.

JSON 컬럼도 update 대상 컬럼으로 사용할 수 있습니다.

```sql
CREATE TRANSACTION TABLE ch8_up_device_json_state (
    device_id INTEGER PRIMARY KEY,
    state JSON,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"NORMAL","score":10}',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"NORMAL","score":10}',
    updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"ALARM","score":90}',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"ALARM","score":90}',
    updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT JSON_EXTRACT_STRING(state, '$.status') AS status,
       JSON_EXTRACT_INTEGER(state, '$.score') AS score
FROM ch8_up_device_json_state
WHERE device_id = 1;
```

제한: JSON path UNIQUE INDEX는 충돌 판정 키 후보에서 제외됩니다. JSON path UNIQUE INDEX
충돌은 upsert 갱신 경로로 전환되지 않고 고유성 제약 오류로 처리됩니다.

## 트랜잭션과 권한

TRANSACTION upsert는 일반 INSERT/UPDATE와 같이 트랜잭션 안에서 COMMIT 또는 ROLLBACK됩니다.

```sql
CREATE TRANSACTION TABLE ch8_up_tx_device_state (
    id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    count_value INTEGER
);

INSERT INTO ch8_up_tx_device_state VALUES (1, 'NORMAL', 10);

BEGIN;

INSERT INTO ch8_up_tx_device_state VALUES (2, 'NORMAL', 1)
    ON DUPLICATE KEY UPDATE SET count_value = count_value + 1;

INSERT INTO ch8_up_tx_device_state VALUES (1, 'ALARM', 1)
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        count_value = count_value + 1;

ROLLBACK;

SELECT id, status, count_value
FROM ch8_up_tx_device_state
ORDER BY id;
```

위 예에서는 삽입 경로와 갱신 경로가 모두 ROLLBACK됩니다.

일반 제약 위반으로 중복 갱신 문장이 실패해도 명시적 트랜잭션의 앞선 성공 변경은
남을 수 있습니다. 응용 프로그램은 오류를 확인한 뒤 후속 처리를 결정하거나
ROLLBACK으로 업무 변경을 취소해야 합니다.

TRANSACTION upsert 문장에는 `INSERT` 권한과 `UPDATE` 권한이 모두 필요합니다. 실제 실행 결과가
삽입 경로가 되더라도 문장에 갱신 경로가 포함되므로 두 권한을 모두 부여해야 합니다.

아래는 권한 형식만 보여 주는 예입니다. 실제 소유자·테이블·기존 애플리케이션 계정에
맞춰 별도의 관리 작업으로 적용하세요.

```text
GRANT INSERT ON owner.table_name TO app_user;
GRANT UPDATE ON owner.table_name TO app_user;
```

`SELECT` 권한은 TRANSACTION upsert 문장 실행 자체에는 필요하지 않습니다. 단, 응용 프로그램이 결과 확인을 위해 `SELECT`를 실행한다면 별도로 `SELECT` 권한이 필요합니다.

## 지원 타입과 제약

`SET` 절에서 갱신할 수 있는 컬럼 타입은 일반 TRANSACTION `UPDATE`와 같은 공개 타입
지원 범위를 따릅니다.

| 분류 | 타입 |
| --- | --- |
| 정수 | `SHORT`, `INT16`, `USHORT`, `UINT16`, `INT`, `INTEGER`, `INT32`, `UINTEGER`, `UINT32`, `LONG`, `INT64`, `ULONG`, `UINT64` |
| 실수 | `FLOAT`, `DOUBLE` |
| 고정소수 | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| 문자열/LOB | `VARCHAR`, `TEXT`, `CLOB`, `BINARY`, `BLOB` |
| 기타 | `DATETIME`, `IPV4`, `IPV6`, `JSON` |

위 표는 TRANSACTION에서 사용하는 스칼라 타입을 정리한 것입니다. 숫자 ARRAY의 지원 범위는
데이터 타입 사전을 참고하십시오.

충돌 판정 키가 되는 키·인덱스 타입은 TRANSACTION PRIMARY KEY 및 UNIQUE INDEX의 타입 정책을
따릅니다. 이 기능은 key 타입의 지원 범위를 확장하지 않습니다.

다음 구문은 지원하지 않습니다.

```text
-- 지원하지 않는 문법을 보여 주는 설명용 구역입니다.
-- INSERT SELECT와 ON DUPLICATE KEY UPDATE 결합은 지원하지 않습니다.
INSERT INTO ch8_up_device_state(device_id, status, alarm_count, updated_at)
SELECT device_id, status, alarm_count, updated_at
FROM staging_device_state
ON DUPLICATE KEY UPDATE SET status = 'UPDATED';

-- MySQL VALUES(col) 함수는 지원하지 않습니다.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = VALUES(status);

-- EXCLUDED alias는 지원하지 않습니다.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = EXCLUDED.status;

-- conflict target syntax는 지원하지 않습니다.
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON CONFLICT (device_id) DO UPDATE SET status = 'ALARM';
```

대상 테이블 제한은 다음과 같습니다.

- 이 페이지는 TRANSACTION의 PRIMARY KEY·UNIQUE 충돌 동작만 다룹니다. 같은 SQL 형태는
  LOOKUP과 VOLATILE의 PRIMARY KEY 충돌에도 지원되며 공통 문법은
  DML 사전을
  정본으로 사용합니다.
- LOG와 TAG DATA 행에는 지원하지 않습니다. TAG METADATA의 태그 이름 충돌 처리는
  DML 사전을
  참고합니다.
- TRANSACTION 테이블이라도 PRIMARY KEY 또는 UNIQUE INDEX가 없으면 사용할 수 없습니다.
- JSON path UNIQUE INDEX는 충돌 판정 키로 사용하지 않습니다.

## 충돌과 오류 처리

여러 UNIQUE INDEX가 같은 기존 행을 가리키면 해당 행을 한 번 UPDATE합니다.
반면 서로 다른 기존 행과 충돌하면 어느 행을 갱신해야 할지 결정할 수 없어 문장이
실패합니다.

다음은 두 업무 키가 서로 다른 행과 충돌하는 표본입니다.

```sql
CREATE TRANSACTION TABLE ch8_up_user_contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    phone VARCHAR(40),
    note VARCHAR(80)
);

CREATE UNIQUE INDEX ch8_up_uidx_user_contact_email ON ch8_up_user_contact(email);
CREATE UNIQUE INDEX ch8_up_uidx_user_contact_phone ON ch8_up_user_contact(phone);

INSERT INTO ch8_up_user_contact VALUES (1, 'a@example.com', '010-0000-0001', 'user-a');
INSERT INTO ch8_up_user_contact VALUES (2, 'b@example.com', '010-0000-0002', 'user-b');

```

다음 INSERT만 의도적으로 실패하는 선택 실습입니다.

```sql
-- email은 id=1과 충돌하고 phone은 id=2와 충돌합니다.
-- 서로 다른 row와 충돌하므로 갱신 경로를 선택하지 않고 실패합니다.
INSERT INTO ch8_up_user_contact VALUES (3, 'a@example.com', '010-0000-0002', 'ambiguous')
ON DUPLICATE KEY UPDATE SET note = 'updated';
```

`SET` 결과가 다른 UNIQUE 제약 또는 `NOT NULL` constraint를 위반해도 문장은 실패하며 기존 행은 보존됩니다.

## 재전송과 최신 상태

카운터 증가 UPSERT는 자동 중복 제거가 아닙니다.
같은 이벤트를 다시 실행하면 기존 카운터가 다시 증가합니다.
COMMIT 응답을 잃었다면 업무 키·이벤트 처리 기록으로 결과부터 확인하세요.

또한 “최신 상태”는 입력 순서와 이벤트 발생 순서가 같을 때만 단순 덮어쓰기로 유지됩니다.
늦게 도착한 과거 이벤트가 최신 값을 덮어쓰지 않도록 원본 시각 비교와 수집 정책을
별도로 정하세요. 여러 테이블을 함께 변경하는 작업은
트랜잭션의 장애 시 커밋 범위도 확인해야 합니다.

## 운영 권장 사항

- 업무 key가 명확하면 PRIMARY KEY 또는 UNIQUE INDEX를 먼저 정의합니다.
- 카운터 누적에는 `SET count_col = count_col + 1` 형태를 사용합니다.
- 소스 행의 값을 그대로 반영하려면 `SET` 없는 upsert를 사용할 수 있습니다. 이때 컬럼 목록에서 생략한 컬럼은 보존됩니다.
- 여러 UNIQUE INDEX가 있는 테이블에서는 서로 다른 행과 동시에 충돌할 수 있는 입력을 사전에 정리합니다.
- MySQL 호환 SQL을 이식할 때 `VALUES(col)`, `EXCLUDED`, `ON CONFLICT` 구문은 Machbase 지원 구문으로 바꿉니다.
- JSON path UNIQUE INDEX를 upsert key로 사용하는 설계는 피하고, 필요한 경우 별도 일반 컬럼에 key 값을 저장한 뒤 UNIQUE INDEX를 생성합니다.

## 결과 확인과 정리

정상 실습이 끝났으면 대표 값과 건수를 다시 확인합니다.
아래 예상값은 의도적인 오류 외에 모든 정상 SQL을 한 번씩 실행한 기준입니다.

```sql
SELECT id, email, display_name, login_count
  FROM ch8_up_account_profile ORDER BY id;
SELECT device_name, last_state, event_count
  FROM ch8_up_latest_device_status;
SELECT external_device_id, device_name, owner_name
  FROM ch8_up_customer_device;
SELECT alias_name, tag_name, manually_checked FROM ch8_up_tag_alias_cache;
SELECT alarm_code, hit_count FROM ch8_up_alarm_counter;
SELECT id, status, count_value FROM ch8_up_tx_device_state ORDER BY id;
SELECT id, note FROM ch8_up_user_contact ORDER BY id;
```

| 표본 | 확인할 결과 |
|---|---|
| account_profile | id=1 유지, display_name=ops-renamed, login_count=2 |
| latest_device_status | ALARM, event_count=2 |
| customer_device | 외부 키 한 행, 이름 compressor-a-renamed, 소유 line-2 |
| tag_alias_cache | tag_name=comp_a.temperature, manually_checked=1 유지 |
| alarm_counter | OVER_TEMP의 hit_count=2 |
| tx_device_state | ROLLBACK 후 기존 id=1, NORMAL, count_value=10만 존재 |
| user_contact | id=1·2의 user-a·user-b가 그대로 유지 |

```sql
DROP TABLE ch8_up_user_contact;
DROP TABLE ch8_up_tx_device_state;
DROP TABLE ch8_up_device_json_state;
DROP TABLE ch8_up_alarm_counter;
DROP TABLE ch8_up_tag_alias_cache;
DROP TABLE ch8_up_customer_device;
DROP TABLE ch8_up_latest_device_status;
DROP TABLE ch8_up_daily_device_summary;
DROP TABLE ch8_up_account_profile;
DROP TABLE ch8_up_asset_cache;
DROP TABLE ch8_up_device_state;
```

DROP은 이 페이지의 실습 객체만 대상으로 합니다.
키가 복잡할수록 새 입력값과 기존 충돌 행을 나란히 비교해 보세요.
어느 행을 갱신하려 했는지 분명해지면 오류의 원인도 찾기 쉬워집니다.
