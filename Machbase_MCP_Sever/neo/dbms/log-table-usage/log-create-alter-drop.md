# 생성, 변경, 삭제

컬럼을 추가하는 SQL은 짧지만, 운영에서는 “기존 행에 어떤 값이 보이는가?”와
“기존 입력 프로그램이 계속 동작하는가?”까지 확인해야 합니다.
이 절에서는 데이터를 넣어 둔 상태에서 스키마를 바꾸고 그 결과를 살펴봅니다.

## LOG 테이블 생성

테이블 타입을 생략한 `CREATE TABLE`은 TRANSACTION 테이블을 만듭니다.
이 실습에서는 `CREATE LOG TABLE`을 사용하세요.

```sql
CREATE LOG TABLE ch7_ddl (
    event_id INTEGER,
    category VARCHAR(32),
    severity SHORT,
    message  VARCHAR(128)
);
INSERT INTO ch7_ddl VALUES (1, 'network', 3, 'connection timeout');
```

자동 컬럼 `_arrival_time`은 DDL에 다시 선언하지 않습니다.
실제 발생 시각이 필요하면 별도 DATETIME 컬럼을 두세요.
PRIMARY KEY·UNIQUE 제약은 LOG에서 지원하지 않습니다.

## 컬럼 추가와 기본값

```sql
ALTER TABLE ch7_ddl ADD COLUMN (host_name VARCHAR(64));
ALTER TABLE ch7_ddl ADD COLUMN (source_kind VARCHAR(16) DEFAULT 'agent');
ALTER TABLE ch7_ddl ADD COLUMN (channels INT32[3] DEFAULT [1, NULL, 3]);

SELECT event_id, host_name, source_kind, channels
  FROM ch7_ddl
 ORDER BY event_id;
```

기존 1번 행의 `host_name`은 NULL, `source_kind`는 `agent`,
`channels`는 `[1, NULL, 3]`으로 조회됩니다.
DEFAULT가 있는 컬럼과 없는 컬럼의 차이를 여기서 확인하세요.
ARRAY DEFAULT는 요소 수가 선언한 길이와 같아야 합니다.

이어서 컬럼 이름을 바꾸고 문자열 길이를 늘립니다.

```sql
ALTER TABLE ch7_ddl RENAME COLUMN category TO event_category;
ALTER TABLE ch7_ddl MODIFY COLUMN (message VARCHAR(4096));
ALTER TABLE ch7_ddl MODIFY COLUMN severity SET MINMAX_CACHE_SIZE = 1048576;

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

기존 행의 값은 유지됩니다. 이름을 바꾼 뒤에는 조회 SQL도 `event_category`를 사용해야
합니다. MINMAX 예제는 숫자 컬럼에 1MiB를 지정한 것으로, 모든 테이블에 적용할 권장값은
아닙니다.

실수하기 쉬운 부분은 타입 변경입니다. VARCHAR 길이 확장은 TEXT를 VARCHAR로 변환하는
명령이 아닙니다. `MINMAX_CACHE_SIZE` 역시 VARCHAR·TEXT 같은 가변 길이 컬럼에는
설정할 수 없습니다.

## NOT NULL과 기존 데이터

현재 `event_category`에는 값이 있으므로 다음 변경이 가능합니다.

```sql
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NOT NULL;
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NULL;
```

옵션 없는 `NOT NULL`은 기존 행을 검사합니다.
NULL이 있는 `host_name`에는 적용할 수 없습니다. 아래 SQL은 실패를 확인하고 싶을 때만
따로 실행하세요.

```sql
-- 의도적으로 실패: 기존 행의 host_name이 NULL입니다.
ALTER TABLE ch7_ddl MODIFY COLUMN host_name NOT NULL;
```

`NOT NULL NOCHECK`는 기존 NULL 검사를 생략합니다.
기존 NULL을 채우거나 과거 데이터까지 조건을 만족한다고 보장하는 옵션은 아닙니다.
이 실습의 정상 흐름에서는 사용하지 않습니다.

## 인덱스와 컬럼 삭제

```sql
CREATE INDEX ch7_ddl_host_idx ON ch7_ddl(host_name) INDEX_TYPE LSM;
DROP INDEX ch7_ddl_host_idx;
ALTER TABLE ch7_ddl DROP COLUMN (host_name);
ALTER TABLE ch7_ddl DROP COLUMN (source_kind);
ALTER TABLE ch7_ddl DROP COLUMN (channels);

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

인덱스가 참조하는 컬럼은 인덱스를 먼저 삭제해야 합니다.
내부 컬럼 `_ARRIVAL_TIME`·`_RID`는 삭제·이름 변경·속성 변경 대상이 아니며,
사용자 컬럼은 최소 하나가 남아 있어야 합니다.
VARCHAR 길이는 기존보다 크게만 변경할 수 있고 최대 32,767바이트 범위여야 합니다.

## 데이터 삭제와 테이블 삭제

주의: 다음 명령은 실습 데이터를 지웁니다.
LOG 데이터는 TRANSACTION 테이블의 `ROLLBACK`으로 되돌릴 수 없습니다.

```sql
TRUNCATE TABLE ch7_ddl;
SELECT COUNT(*) AS remaining_rows FROM ch7_ddl;
DROP TABLE ch7_ddl;
```

TRUNCATE 뒤 건수는 0이고 정의는 남습니다. 마지막 DROP은 정의도 삭제합니다.
일부 오래된 데이터만 정리하려면 보존형 삭제를 사용하세요.

## DDL 운영 주의사항

변경 전에는 입력 작업과 DDL 시점을 조정하고, 변경 후에는 SQL·Appender·파일 매핑의
컬럼 이름·순서·타입을 확인합니다. 리소스 사용 중 오류가 나면 반복 실행하기보다
대상 테이블을 사용하는 작업부터 확인하세요.

어느 변경에서 막혔는지 모르겠다면 변경 전 DDL과 실패한 SQL을 함께 준비해 보세요.
그 두 가지가 있으면 원인을 훨씬 빠르게 좁힐 수 있습니다.
