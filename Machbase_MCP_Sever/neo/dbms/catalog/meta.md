# 메타 테이블 사전

메타 테이블은 `M$` 접두사를 가지며 Machbase 스키마 정보(테이블 정의, 컬럼, 인덱스, 사용자 등)를 조회합니다. DDL 명령 실행 결과가 자동으로 반영되며 읽기 전용입니다.

8.7.0 Standard Edition의 다중 데이터베이스에서는 catalog-local metadata를 조인할 때
`DATABASE_ID`, `TABLESPACE_ID`와 parent object ID를 함께 사용해야 합니다. 논리
`DATABASE_ID`와 물리 `TABLESPACE_ID`는 서로 대체할 수 없습니다. database 운영 경계는
다중 데이터베이스 운영 가이드를
참고하십시오.

## 메타 테이블 목록

| 테이블 이름 | 설명 |
|------------|------|
| `M$SYS_TABLES` | 사용자가 생성한 테이블 목록과 타입 |
| `M$SYS_TABLE_PROPERTY` | 테이블에 적용된 속성 정보 |
| `M$SYS_COLUMNS` | 테이블 컬럼 정의 (타입, 길이 등) |
| `M$SYS_INDEXES` | 인덱스 정의 |
| `M$SYS_INDEX_COLUMNS` | 인덱스를 구성하는 컬럼 정보 |
| `M$SYS_TABLESPACES` | 테이블스페이스 목록 |
| `M$SYS_TABLESPACE_DISKS` | 테이블스페이스가 사용하는 디스크 경로 |
| `M$SYS_USERS` | 등록된 사용자 목록 |
| `M$SYS_VIEWS` | 뷰 정의 SQL 텍스트 |
| `M$SYS_USER_ACCESS` | 테이블별 사용자 권한 |
| `M$RETENTION` | Retention Policy 정보 |
| `M$TABLES` | M$ 메타 테이블 자체 목록 |
| `M$COLUMNS` | M$ 메타 테이블의 컬럼 목록 |

## M$SYS_TABLES

사용자가 생성한 테이블의 목록과 타입을 조회합니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `NAME` | VARCHAR | 테이블 이름 |
| `TYPE` | INTEGER | 테이블 타입 |
| `ID` | LONG | 테이블 식별자 |
| `DATABASE_ID` | LONG | 논리 데이터베이스 식별자 |
| `TABLESPACE_ID` | LONG | 물리 tablespace 식별자 |
| `USER_ID` | INTEGER | 테이블 생성 사용자 식별자 |
| `COLCOUNT` | INTEGER | 컬럼 수 |
| `FLAG` | INTEGER | 서브 타입 (1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat) |

**TYPE 값 의미:**

| 값 | 테이블 타입 |
|----|------------|
| `0` | Log 테이블 |
| `1` | Fixed 테이블 |
| `3` | Volatile 테이블 |
| `4` | Lookup 테이블 |
| `5` | Key Value 테이블 |
| `6` | Tag 테이블 |
| `7` | View |
| `8` | TRANSACTION 테이블 |

## M$SYS_COLUMNS

테이블 컬럼의 정의를 조회합니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `NAME` | VARCHAR | 컬럼명 |
| `TYPE` | INTEGER | 컬럼 데이터 타입 |
| `TABLE_ID` | LONG | 소속 테이블 식별자 |
| `DATABASE_ID` | LONG | 논리 데이터베이스 식별자 |
| `TABLESPACE_ID` | LONG | 물리 tablespace 식별자 |
| `LENGTH` | INTEGER | 컬럼 최대 길이 |
| `PART_PAGE_COUNT` | INTEGER | 파티션당 페이지 수 |
| `MINMAX_CACHE_SIZE` | LONG | MIN-MAX 캐시 크기 |

## M$SYS_INDEXES

인덱스 정의를 조회합니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `NAME` | VARCHAR | 인덱스 이름 |
| `TYPE` | INTEGER | 인덱스 타입 |
| `TABLE_ID` | LONG | 소속 테이블 식별자 |
| `DATABASE_ID` | LONG | 논리 데이터베이스 식별자 |
| `TABLESPACE_ID` | LONG | 물리 tablespace 식별자 |
| `COLCOUNT` | INTEGER | 인덱스 컬럼 수 |
| `MAX_LEVEL` | INTEGER | 최대 LSM 레벨 |

## M$SYS_USERS

등록된 사용자 목록을 조회합니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `USER_ID` | INTEGER | 사용자 식별자 |
| `NAME` | VARCHAR | 사용자 이름 |
| `PWD_POLICY_LEVEL` | INTEGER | 비밀번호 정책 수준 |
| `VALID_BEFORE` | VARCHAR | 계정 유효 기간 |

## M$RETENTION

Retention Policy 정보를 조회합니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `POLICY_NAME` | VARCHAR | 정책 이름 |
| `DURATION` | LONG | 보존 기간 (초) |
| `INTERVAL` | LONG | 삭제 실행 주기 (초) |

## SQL 예제

```sql
-- 전체 테이블 목록 (타입 포함)
SELECT name, type, colcount
  FROM m$sys_tables
 ORDER BY name;

-- Tag 테이블만 조회 (type = 6)
SELECT name FROM m$sys_tables WHERE type = 6;

-- 특정 테이블의 컬럼 목록
SELECT c.name AS col_name, c.type AS col_type, c.length
  FROM m$sys_columns c
  JOIN m$sys_tables  t
    ON c.database_id = t.database_id
   AND c.tablespace_id = t.tablespace_id
   AND c.table_id = t.id
 WHERE t.name = 'SENSOR_TAG'
 ORDER BY c.id;

-- 특정 테이블의 인덱스 목록
SELECT i.name AS idx_name, i.type AS idx_type, i.colcount
  FROM m$sys_indexes i
  JOIN m$sys_tables  t
    ON i.database_id = t.database_id
   AND i.tablespace_id = t.tablespace_id
   AND i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- 인덱스를 구성하는 컬럼 확인
SELECT ic.name AS col_name, ic.index_type
  FROM m$sys_index_columns ic
  JOIN m$sys_indexes i ON ic.index_id = i.id
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- 테이블스페이스 디스크 경로 확인
SELECT ts.name AS tbs_name, d.path, d.io_thread_count
  FROM m$sys_tablespace_disks d
  JOIN m$sys_tablespaces ts ON d.tablespace_id = ts.id;

-- 사용자 목록 조회
SELECT user_id, name, pwd_policy_level, valid_before
  FROM m$sys_users;

-- Retention Policy 목록
SELECT * FROM m$retention;
```

> 메타 테이블은 읽기 전용입니다. `INSERT`, `UPDATE`, `DELETE` 명령은 오류를 반환합니다. 스키마 변경은 `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` 등의 DDL 명령을 사용합니다.
