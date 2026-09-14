# INDEX

인덱스 문법과 테이블 타입별 지원 범위를 설명합니다. 인덱스는 조회 비용을 줄이는 대신
입력과 변경 때 유지 비용이 발생하므로 실제 조건과 실행 계획을 확인한 뒤 추가하십시오.

## CREATE INDEX

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

```sql
create_index_stmt ::=
    'CREATE' index_modifier? 'INDEX' [ 'IF NOT EXISTS' ] index_name
    'ON' index_target '(' index_column_list ')'
    [ 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' | 'TAG' ) ]
    [ 'TABLESPACE' tablespace_name ]
    [ index_property_list ]

index_modifier ::= 'UNIQUE' | 'PRIMARY KEY'

index_target ::= table_name | table_name 'METADATA'

index_column_list ::=
    column_name ( ',' column_name )*
  | column_name json_path

index_property_list ::=
    ( 'MAX_LEVEL'        '=' number
    | 'PAGE_SIZE'        '=' number
    | 'BITMAP_ENCODE'    '=' ( 'EQUAL' | 'RANGE' )
    | 'PART_VALUE_COUNT' '=' number )
    ( ',' index_property_list )*
```

### IF NOT EXISTS

`IF NOT EXISTS`를 지정하면 같은 database와 owner에 동일한 index name이 있을 때 오류 없이
성공하고 기존 index를 유지합니다.

- 동일한 이름이 없으면 table, column, index type, property와 권한을 기존 CREATE INDEX와
  동일하게 검증한 뒤 생성합니다.
- 동일한 이름이 있으면 table, column, index type, JSON path와 property를 비교하거나
  변경하지 않습니다.
- 중복 판정 namespace는 `database + owner + index name`입니다. 다른 database나 owner의 같은
  이름은 별도 index입니다.
- 옵션을 생략한 CREATE INDEX는 기존 duplicate-name 오류를 그대로 반환합니다.

> **주의**
> `IF NOT EXISTS`는 index 정의를 일치시키는 기능이 아닙니다. 같은 이름이 있으면 statement의
> target table이나 column이 없거나 정의가 달라도 no-op으로 성공합니다. 반복 배포 뒤에는
> `SHOW INDEX` 또는 system catalog에서 실제 table, column, type과 property를 확인하십시오.

```sql
CREATE LOG TABLE sensor_log_ifne (
    sensor_id INTEGER,
    value     DOUBLE
);

CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(sensor_id);

-- 같은 이름이 있으므로 성공하고 기존 SENSOR_ID mapping을 유지합니다.
CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(value);

SHOW INDEX sensor_log_ifne_idx;

DROP TABLE sensor_log_ifne;
```

### 조건부 생성 지원 형태

| 형식 | 지원 범위 |
|---|---|
| 일반 `CREATE INDEX IF NOT EXISTS` | 해당 table type에서 지원하는 일반 index |
| `CREATE UNIQUE INDEX IF NOT EXISTS` | Standard Edition TRANSACTION table |
| `CREATE PRIMARY KEY INDEX IF NOT EXISTS` | Standard Edition TRANSACTION table |
| TAG data JSON path / TAG METADATA index | Standard Edition, Cluster Edition |
| 일반 문법의 `INDEX_TYPE` 절 | 해당 table type과 index type의 기존 지원 범위 |

deprecated `CREATE BITMAP INDEX`, `CREATE KEYWORD INDEX`, `CREATE REDBLACK INDEX` 전용 문법에는
`IF NOT EXISTS`를 사용할 수 없습니다. 일반 문법을 사용합니다.

```sql
CREATE INDEX IF NOT EXISTS idx_message
    ON app_log(message) INDEX_TYPE KEYWORD;
```

## 테이블 타입별 지원 범위

| 테이블 타입 | 인덱스 | 주요 용도 |
|------------|--------|-----------|
| LOG | LSM, KEYWORD, BITMAP | 범위 조회, 텍스트 검색, 분석 조건 |
| TAG | TAG/KV secondary, JSON path | 값 컬럼과 JSON member 조건 |
| TAG METADATA | 자동 컬럼 인덱스, JSON path | 태그 속성 조건 |
| TRANSACTION | PRIMARY KEY, UNIQUE, 일반 BTREE | 관계형 키와 복합 조건 |
| VOLATILE | REDBLACK | 메모리 테이블의 키·조건 조회 |
| LOOKUP | REDBLACK | 메모리 테이블의 키·조건 조회 |

타입을 생략했을 때 적용되는 내부 인덱스는 테이블 타입에 따라 다릅니다. 다른 테이블 타입의
인덱스 이름을 지정해도 같은 구조가 생성된다고 가정하지 마십시오.

## LOG 인덱스

```sql
CREATE INDEX idx_ts ON sensor_log (ts);
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;
CREATE INDEX idx_status ON sensor_log (status)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;
```

| 타입 | 대상과 특징 |
|------|-------------|
| LSM | LOG의 기본 범위 인덱스 |
| KEYWORD | VARCHAR/TEXT의 `SEARCH`, `ESEARCH` |
| BITMAP | 반복 값 분석. VARCHAR, TEXT, BINARY에는 사용하지 않음 |

LSM의 `MAX_LEVEL`, `PAGE_SIZE`, BITMAP의 `BITMAP_ENCODE` 같은 속성은 데이터 분포와
조회 조건으로 측정해 결정하십시오.

## TAG 인덱스

TAG 이름과 시간 축의 기본 접근 구조는 자동으로 관리됩니다. 값 컬럼을 단독 조건으로 자주
사용할 때 TAG/KV secondary index를 검토합니다.

```sql
CREATE INDEX idx_value ON sensor_tag (value) INDEX_TYPE TAG;
```

JSON 값 컬럼은 path별 인덱스를 만들 수 있습니다.

```sql
CREATE INDEX idx_sensor ON tag_json (value.sensor.name);
CREATE INDEX idx_metric ON tag_json (value->'$.metric');
CREATE INDEX idx_item ON tag_json (value.items[0]."product-id");
```

TAG METADATA 일반 컬럼에는 인덱스가 자동 생성됩니다. METADATA JSON 컬럼의 path를
추가할 때는 다음 형식을 사용합니다.

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

지원 범위와 실행 계획 예시는
TAG 인덱스와 성능을 참고하십시오.

## TRANSACTION 인덱스

TRANSACTION은 PRIMARY KEY, UNIQUE INDEX와 일반 단일·복합 인덱스를 지원합니다.

```sql
CREATE PRIMARY KEY INDEX idx_pk_order ON orders (order_id);
CREATE UNIQUE INDEX uidx_account_email ON account (email);
CREATE UNIQUE INDEX uidx_tenant_login ON account (tenant_id, login_name);
CREATE INDEX idx_category_name ON product (category, product_name);
```

PRIMARY KEY는 테이블당 하나이며 단일 컬럼입니다. `CREATE UNIQUE INDEX`는 복합 컬럼을
지원하고, NULL이 포함된 키는 다른 NULL 포함 키와 중복으로 판정하지 않습니다. 상세 동작은
TRANSACTION 인덱스와 성능을 참고하십시오.

## VOLATILE과 LOOKUP 인덱스

VOLATILE과 LOOKUP은 REDBLACK 메모리 인덱스를 사용합니다.

```sql
CREATE INDEX idx_status ON device_status (status) INDEX_TYPE REDBLACK;
```

타입별 기본 키와 추가 인덱스 설계는 다음 문서를 참고하십시오.

- VOLATILE 인덱스와 성능
- LOOKUP 인덱스와 성능

## DROP INDEX

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

```sql
DROP INDEX idx_status;
```

대상 인덱스를 사용하는 세션이 있으면 삭제가 실패할 수 있습니다. 삭제 전 실행 계획과
해당 인덱스를 사용하는 운영 쿼리를 확인하십시오.

## 관련 문서

- SEARCH / ESEARCH / REGEXP
- 쿼리 성능 튜닝
