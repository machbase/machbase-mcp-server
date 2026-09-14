# TAG 메타데이터

## Tag 메타데이터

### 개요

METADATA는 태그마다 한 행인 현재 속성입니다. 일반 TAG 조회에서는 같은 속성이 각
DATA 행에 함께 나타납니다. 현재 속성을 바꾸면 과거 DATA를 조회한 결과에도 새 속성이
보일 수 있으므로 발생 당시 속성이 필요하면 DATA나 별도 속성 이력에 보존합니다.

아래는 기본 메타데이터, JSON 메타데이터와 전체 예제를 서로 다른 테이블로 분리합니다.
태그의 정적 속성을 저장하는 영역으로 사용하며 센서 위치, 장비 상태, 설치 정보, 외부 식별자, JSON 문서형 속성을 메타데이터에 둘 수 있습니다.

메타데이터 전용 SQL로 다음 작업을 처리할 수 있습니다. 아래 예제의 `TAG`는 테이블 이름이며,
사용할 때 실제 TAG 테이블 이름으로 바꿉니다.

- 메타데이터 전용 조회
- 메타데이터 조건 기반 `UPDATE` / `DELETE`
- metadata row 마지막 변경 시각 조회
- ARRAY metadata 컬럼 ADD/DROP과 기존 row DEFAULT
- `JSON` 타입 메타데이터 컬럼 선언
- JSON path 조회와 JSON path 인덱스
- JSON 문서 일부만 수정하는 부분 갱신

사용자는 내부 저장 테이블을 직접 다룰 필요 없이 `TAG METADATA` 문법만 사용하면 됩니다.

### 메타데이터 컬럼 정의

메타데이터 컬럼은 `CREATE TAG TABLE` 의 `METADATA (...)` 절에서 정의합니다.

```sql
CREATE TAG TABLE ch5_meta (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    location VARCHAR(100),
    status VARCHAR(20),
    srcip IPV4
);
```

메타데이터 컬럼은 태그 이름별로 1행만 저장됩니다.

### ARRAY 메타데이터 컬럼 추가와 삭제

Standard Edition에서는 기존 TAG 테이블의 METADATA 영역에 고정 길이 숫자 ARRAY 컬럼을
추가하고 삭제할 수 있습니다.

```sql
INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_OLD', TO_DATE('2026-09-05 00:00:00'), 10.0);

ALTER TABLE ch5_meta METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_NEW', TO_DATE('2026-09-05 00:00:01'), 20.0);

SELECT name, limits
  FROM ch5_meta METADATA
 ORDER BY name;
```

ALTER 전에 존재한 `TEMP_OLD` metadata row에는 `[0.0000, NULL]`을 backfill합니다. ALTER
뒤 TAG DATA 입력으로 자동 등록된 `TEMP_NEW` metadata row에는 ADD COLUMN DEFAULT를 다시
적용하지 않으며 `limits`는 whole NULL입니다. DEFAULT가 없는 경우에는 ALTER 전 row도
whole NULL입니다.

추가한 ARRAY metadata 컬럼은 일반 TAG 조회의 명시 projection과 `SELECT *`에도
포함됩니다. ARRAY metadata 컬럼에는 자동 index를 만들지 않으며 다음과 같은 명시적
index도 지원하지 않습니다.

```sql
-- 지원하지 않으며 오류를 반환합니다.
CREATE INDEX idx_sensor_limits ON ch5_meta METADATA(limits);
```

컬럼을 제거할 때도 `METADATA`를 지정합니다.

```sql
ALTER TABLE ch5_meta METADATA DROP COLUMN (limits);
```

TAG DATA의 일반 ARRAY 컬럼은 `CREATE TAG TABLE`에서 선언할 수 있지만 ALTER로 추가할 수
없습니다. 지원 요소 타입, cardinality와 DEFAULT 규칙은
숫자 ARRAY 타입을 참고하십시오.

### 메타데이터 입력

메타데이터는 `INSERT INTO ... METADATA` 로 입력합니다.

```sql
INSERT INTO ch5_meta METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

컬럼 목록을 지정할 수도 있습니다.

```sql
INSERT INTO ch5_meta METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

주의사항:

- 컬럼 목록을 생략한 VALUES는 태그명 다음에 메타데이터 선언 순서를 따릅니다.
- 컬럼 목록을 지정했다면 그 목록의 순서대로 값을 전달합니다.
- 생략한 입력의 NULL·DEFAULT 처리는 해당 DDL과 입력 경로의 규칙을 따릅니다.
- 식별자는 TAG의 태그명 컬럼입니다. 이 예제에서는 그 이름을 `name`으로 선언했습니다.
- 메타데이터 행이 생성되면 `_LAST_UPDATE_TIME` 이 서버 시각으로 자동 기록됩니다.

### 메타데이터 조회

#### 메타데이터만 조회

메타데이터 전용 조회는 `FROM TAG METADATA` 를 사용합니다.

```sql
SELECT name, location, status, srcip
  FROM ch5_meta METADATA
 ORDER BY name;
```

이 조회는 태그 이름당 1행을 반환합니다.

```sql
SELECT *
  FROM ch5_meta METADATA
 ORDER BY name;
```

`SELECT *` 와 `table_alias.*` 는 `NAME` 과 메타데이터 컬럼만 반환합니다.

`_LAST_UPDATE_TIME` 같은 시스템 관리 컬럼은 `SELECT *` 결과에 표시되지 않습니다. 필요한 경우 컬럼명을 명시합니다.

#### 마지막 변경 시각 조회

TAG metadata에는 각 metadata row의 마지막 변경 시각을 나타내는 시스템 관리 컬럼 `_LAST_UPDATE_TIME` 이 있습니다.

`_LAST_UPDATE_TIME` 은 tag data row의 마지막 입력 시각이 아니라, tag metadata row가 생성되거나 실제 metadata 값이 변경된 시각입니다.

##### 조회 방법

`_LAST_UPDATE_TIME` 은 명시적으로 컬럼명을 지정해서 조회합니다.

```sql
SELECT name, _last_update_time
  FROM ch5_meta METADATA;
```

다른 metadata 컬럼과 함께 조회하거나 조건에 사용할 수 있습니다.

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

`SELECT *` 와 `table_alias.*` 결과에는 `_LAST_UPDATE_TIME` 이 표시되지 않습니다.

##### 자동 기록 및 갱신 규칙

metadata row가 새로 생성되면 `_LAST_UPDATE_TIME` 이 자동으로 기록됩니다.

```sql
INSERT INTO ch5_meta METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

사용자 metadata 값이 실제로 변경되면 `_LAST_UPDATE_TIME` 이 갱신됩니다.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

같은 값으로 update하거나 JSON missing path 제거처럼 저장 결과가 바뀌지 않는 update는 실제 변경으로 보지 않습니다. 이 경우 `_LAST_UPDATE_TIME` 은 유지됩니다.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

JSON의 존재하지 않는 경로 제거도 저장값을 바꾸지 않으면 no-op입니다. 실행 예제는
아래 JSON 테이블을 생성한 뒤 확인합니다.

##### 직접 입력 및 수정 제한

`_LAST_UPDATE_TIME` 은 시스템 관리 컬럼이므로 사용자가 직접 값을 넣거나 수정할 수 없습니다.

다음 문장은 허용되지 않습니다.

```sql
INSERT INTO ch5_meta METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE ch5_meta METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

또한 TAG name 컬럼명, TAG metadata 컬럼명, `ALTER TABLE ... METADATA ADD COLUMN` 대상 컬럼명으로 `_LAST_UPDATE_TIME` 을 사용할 수 없습니다. `ALTER TABLE ... METADATA DROP COLUMN` 으로 `_LAST_UPDATE_TIME` 을 삭제할 수도 없습니다.

```sql
CREATE TAG TABLE invalid_sensor (
    _last_update_time VARCHAR(128) PRIMARY KEY,
    time              DATETIME BASETIME,
    value             DOUBLE
);
```

```sql
CREATE TAG TABLE invalid_sensor_meta (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    _last_update_time DATETIME
);
```

`_LAST_UPDATE_TIME2` 처럼 prefix만 같은 이름은 별도 사용자 컬럼으로 사용할 수 있습니다.

##### 시간 조건 조회 및 자동 인덱스

`_LAST_UPDATE_TIME` 에는 시간 조건 조회를 위한 인덱스가 자동으로 제공됩니다.

```sql
SELECT name, location, _last_update_time
  FROM ch5_meta METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

따라서 같은 컬럼에 사용자가 별도 인덱스를 중복 생성할 필요가 없습니다.

##### machloader / tagmetaimport 사용 시 주의사항

TAG metadata를 import할 때 입력 파일이나 form 파일에는 `NAME` 과 사용자 metadata 컬럼만 포함합니다. 내부 컬럼인 `_ID` 와 시스템 관리 컬럼 `_LAST_UPDATE_TIME` 은 입력 대상이 아닙니다.

metadata가 `location`, `status` 인 경우 입력 데이터는 다음 형태를 사용합니다.

```text
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

`_LAST_UPDATE_TIME` 은 import 시 서버가 자동으로 채웁니다.

일반 LOG, LOOKUP, VOLATILE 테이블에서 사용자가 `_LAST_UPDATE_TIME` 이라는 이름의 컬럼을 정의한 경우에는 일반 사용자 컬럼으로 동작합니다. 예약 동작은 TAG metadata 시스템 컬럼에만 적용됩니다.

#### 데이터와 함께 조회

메타데이터 조건으로 시계열 데이터를 조회할 때는 일반 `FROM TAG` 를 사용합니다.

```sql
SELECT name, status, time, value
  FROM ch5_meta
 WHERE status = 'READY'
 ORDER BY name, time;
```

이 조회는 데이터 row 기준으로 반환되므로, 같은 tag의 메타데이터 값은 각 데이터 row마다 반복됩니다.

주의사항:

- `FROM TAG METADATA` 에서는 `TIME`, `VALUE` 같은 데이터 컬럼을 조회할 수 없습니다.
- `FROM TAG` 는 데이터 조회 모드이고, `FROM TAG METADATA` 는 메타데이터 조회 모드입니다.
- `TAG METADATA` 에서는 내부 컬럼 `_ID`, `_RID` 를 사용할 수 없습니다.

### 메타데이터 수정

메타데이터 수정은 `UPDATE TAG METADATA` 를 사용합니다.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

메타데이터 조건으로 여러 태그를 한 번에 수정할 수도 있습니다.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

주의사항:

- 수정 대상은 `NAME` 과 메타데이터 컬럼입니다.
- `TIME`, `VALUE` 같은 데이터 컬럼은 `UPDATE ... METADATA` 에서 수정할 수 없습니다.
- 내부 컬럼은 수정할 수 없습니다.
- 실제 metadata 값이 바뀐 경우에만 `_LAST_UPDATE_TIME` 이 갱신됩니다.

### 메타데이터 삭제

메타데이터 삭제는 `DELETE FROM TAG METADATA` 를 사용합니다.

특정 태그의 메타데이터를 삭제하려면 `WHERE` 절에서 tag name 조건을 지정합니다.

```sql
DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_002';
```

메타데이터 조건으로 여러 태그를 한 번에 삭제할 수도 있습니다.

```sql
DELETE FROM ch5_meta METADATA
 WHERE status = 'STOP';
```

`WHERE` 절을 생략하면 전체 메타데이터가 대상입니다. 이 실습에는 앞서 입력한
TEMP_OLD·TEMP_NEW의 DATA가 남아 있으므로 아래 전체 삭제는 의도적으로 실패합니다.

```sql
DELETE FROM ch5_meta METADATA;
```

주의사항:

- 삭제 대상 중 하나라도 실제 데이터 row를 가지고 있으면 문장 전체가 실패합니다.
- 즉, 사용 중인 tag의 메타데이터는 삭제할 수 없습니다.
- 전체 삭제 시에도 사용 중인 tag가 하나라도 있으면 일부만 삭제하지 않고 문장 전체가 실패합니다.

사용 중인 tag의 메타데이터를 삭제하려면 먼저 해당 tag의 데이터 row를 삭제한 뒤
메타데이터 삭제를 다시 수행합니다.

```sql
DELETE FROM ch5_meta
 WHERE name = 'TEMP_001';

DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

### JSON 메타데이터 컬럼

메타데이터에 `JSON` 컬럼을 선언할 수 있습니다.

```sql
CREATE TAG TABLE ch5_meta_json (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

JSON 메타데이터 입력 예:

```sql
INSERT INTO ch5_meta_json METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

주의사항:

- `JSON` 메타데이터 컬럼은 길이를 지정하지 않습니다.
- 유효하지 않은 JSON 문자열은 오류가 발생합니다.
- raw JSON 컬럼 자체에는 자동 인덱스가 생성되지 않습니다.

### JSON 값이 바뀌지 않는 경우

```sql
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'SHIP_001';
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
```

경로가 없어 저장값이 그대로이면 변경 시각도 유지됩니다.

### JSON path 조회

JSON 메타데이터는 `->` 연산자로 조회할 수 있습니다.

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ch5_meta_json METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

데이터 조회에서도 같은 방식으로 사용할 수 있습니다.

```sql
SELECT name, time, value
  FROM ch5_meta_json
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

#### 경로 표기 규칙

조회와 부분 갱신에서 사용하는 path는 full JSONPath를 사용합니다.

- 일반 key: `$.name`
- 중첩 key: `$.ship.status`
- key 이름에 `.` 또는 `-` 가 포함되면 bracket 표기 사용

```sql
SELECT info->'$[''ship.owner'']'
  FROM ch5_meta_json METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ch5_meta_json METADATA;
```

### JSON path 인덱스

#### 테이블 생성 시 함께 선언

자주 조회하는 JSON path는 메타데이터 정의 시 함께 인덱싱할 수 있습니다.

```sql
CREATE TAG TABLE ch5_meta_json_indexed (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

`INDEX(...)` 안의 문자열은 다음 규칙으로 해석합니다.

- `'name'` 은 `$.name`
- `'ship.status'` 는 `$.ship.status`
- 특수 문자가 있는 key나 복잡한 경로는 full JSONPath를 직접 사용

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

#### 생성 후 인덱스 추가

테이블 생성 후에도 JSON path 인덱스를 추가할 수 있습니다.

```sql
CREATE INDEX idx_ship_owner
ON ch5_meta_json METADATA (info->'$.owner');
```

#### 인덱스 삭제

인덱스 이름만으로 삭제합니다.

```sql
SHOW INDEX idx_ship_owner;
DROP INDEX idx_ship_owner;
```

명시적으로 만든 인덱스는 생성 시 정한 이름으로 관리합니다. `SHOW INDEX idx_ship_owner;`는
DROP 전에 실행합니다. 삭제 후 같은 이름을 조회하면 존재하지 않는 객체입니다.

#### 인덱스 사용 시 주의사항

현재 JSON path 인덱스는 문자열 비교 중심으로 동작합니다.

```sql
SELECT name
  FROM ch5_meta_json METADATA
 WHERE info->'$.status' = 'READY';
```

문자열 literal 비교는 인덱스를 사용할 수 있습니다. 반면 숫자 literal 비교는 full scan으로 처리될 수 있습니다.

예:

- `info->'$.num' = '10'` : 인덱스 사용 가능
- `info->'$.num' = 10` : full scan 가능

### JSON 부분 갱신

JSON 함수는 지정 경로를 바꾼 새 문서 값을 반환합니다. UPDATE는 그 결과를 컬럼에 저장합니다.
이는 경로 단위의 논리적 갱신이며 저장 파일 일부만 제자리에서 수정한다는 성능 보장은 아닙니다.

#### JSON_SET

SQL scalar 값을 JSON scalar로 저장합니다.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

#### JSON_SET_JSON

입력 문자열을 JSON으로 해석해 object 또는 array를 저장합니다.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

#### JSON_REMOVE

특정 멤버 또는 하위 경로를 삭제합니다.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

#### 부분 갱신 규칙

- `JSON_SET(..., path, NULL)` 은 JSON `null` 을 저장합니다.
- `JSON_SET_JSON(..., path, NULL)` 의 결과는 SQL `NULL` 입니다.
- JSON 문서 인자가 `NULL` 이면 함수 결과는 SQL `NULL` 입니다.
- path 가 `NULL` 이거나 빈 문자열이면 오류가 발생합니다.
- 존재하지 않는 경로에 대한 `JSON_REMOVE` 는 오류가 아니라 no-op 입니다.
- `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.
- 부분 갱신은 object 경로 중심으로 지원합니다.
- array element 경로 갱신 예: `$.items[0]` 는 지원하지 않습니다.

### 전체 예제

```sql
CREATE TAG TABLE ch5_meta_complete (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ch5_meta_complete METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ch5_meta_complete VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ch5_meta_complete METADATA;

SELECT name, time, value
  FROM ch5_meta_complete
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ch5_meta_complete METADATA (info->'$.owner');

UPDATE ch5_meta_complete METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

### 요약

- 메타데이터 전용 조회는 `FROM TAG METADATA`
- 데이터 조회는 `FROM TAG`
- 메타데이터 수정/삭제는 `UPDATE/DELETE ... METADATA`
- ARRAY metadata 컬럼 변경은 `ALTER TABLE ... METADATA ADD/DROP COLUMN`
- JSON 메타데이터는 `INFO JSON`
- `_LAST_UPDATE_TIME` 은 metadata row의 마지막 변경 시각이며 명시적으로 조회할 수 있습니다
- JSON path 인덱스는 `INFO JSON INDEX(...)` 또는 `CREATE INDEX ... ON TAG METADATA (...)`
- JSON 부분 갱신은 `JSON_SET`, `JSON_SET_JSON`, `JSON_REMOVE`
- `_LAST_UPDATE_TIME` 은 서버가 자동 관리하며 standard와 cluster 환경에서 동일하게 동작합니다

## 실습 정리

전체 삭제 실패 예제와 달리 DROP은 테이블과 DATA·METADATA를 모두 제거합니다.
아래 이름이 이번 실습에서 만든 객체인지 확인한 뒤 실행합니다.

```sql
DROP TABLE ch5_meta;
DROP TABLE ch5_meta_json;
DROP TABLE ch5_meta_json_indexed;
DROP TABLE ch5_meta_complete;
```
