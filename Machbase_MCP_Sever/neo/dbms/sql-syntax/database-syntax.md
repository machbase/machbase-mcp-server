# DATABASE

Machbase 8.7.0 Standard Edition의 논리 데이터베이스 lifecycle과 session 선택 구문입니다.
데이터베이스 이름은 catalog 이름이며, 서버 인스턴스의 물리 저장소를 관리하는
`machadmin -c`, `machadmin -d`와는 구분합니다.

## CREATE DATABASE

```sql
create_database_stmt ::=
    'CREATE DATABASE' ['IF NOT EXISTS'] database_name
```

`CREATE DATABASE`는 현재 Machbase 인스턴스에 active logical database를 만듭니다.
새 데이터베이스의 기본 access mode는 `READ WRITE`입니다. 사용자와 인증 정보는
인스턴스 전체에서 공유되며, 테이블·view·index와 객체 권한은 데이터베이스별로 관리됩니다.

```sql
CREATE DATABASE factory_a;
CREATE DATABASE IF NOT EXISTS factory_b;
```

## ALTER DATABASE

```sql
alter_database_stmt ::=
    'ALTER DATABASE' database_name ( 'READ ONLY' | 'READ WRITE' )
```

`READ ONLY` 데이터베이스는 조회할 수 있지만 쓰기 DML, append와 변경 DDL을 실행할 수
없습니다. 실행 중인 쓰기 작업을 정리한 뒤 mode를 변경하십시오.

```sql
ALTER DATABASE factory_a READ ONLY;
ALTER DATABASE factory_a READ WRITE;
```

## DROP DATABASE

```sql
drop_database_stmt ::=
    'DROP DATABASE' ['IF EXISTS'] database_name
    [ 'RESTRICT' | 'CASCADE' | 'FORCE' | 'CASCADE FORCE' | 'FORCE CASCADE' ]
```

- `RESTRICT`는 객체나 사용 중인 참조가 있으면 삭제하지 않습니다.
- `CASCADE`는 대상 데이터베이스의 객체, metadata와 database-local grant를 정리합니다.
- `FORCE`는 종료 가능한 session, statement, cursor와 job 참조를 정리한 뒤 삭제를 진행합니다.
- 객체와 참조를 함께 정리해야 하면 `CASCADE FORCE`를 사용합니다.

기본 데이터베이스 `MACHBASEDB`는 삭제할 수 없습니다. 현재 session의 database도 삭제할 수
없으므로 먼저 `USE MACHBASEDB` 또는 다른 active database를 실행해야 합니다.

## USE

```sql
use_database_stmt ::= 'USE' ['DATABASE'] database_name
```

`USE`와 `USE DATABASE`는 같은 동작을 합니다. 현재 session의 database만 변경하며 다른
연결에는 영향을 주지 않습니다. transaction이 진행 중이거나 대상 database가 mounted
database인 경우에는 실패합니다.

```sql
USE factory_a;
USE DATABASE factory_b;
```

## 현재 데이터베이스 확인

```sql
SELECT CURRENT_DATABASE();
SELECT DATABASE();
SELECT CURRENT_CATALOG;
SHOW CURRENT DATABASE;
SHOW DATABASES;
```

권장 확인 방법은 `CURRENT_DATABASE()`입니다. client 연결 옵션으로 초기 database를
지정했더라도 연결 직후 이 값을 확인하여 실제 server catalog를 검증하십시오.

## 객체 이름

테이블·view와 DML 대상은 다음 형식으로 지정할 수 있습니다.

```text
table_name                         -- 현재 DB, 현재 사용자
owner.table_name                   -- 현재 DB, 지정 owner
database_name.owner.table_name    -- 지정 DB, 지정 owner
```

두 부분 이름은 항상 `owner.table`입니다. 따라서 `factory_a.sensor_log`를 database와
table의 두 부분 이름으로 해석하지 않으며, 명시적으로 다른 database를 지정하려면
`factory_a.sys.sensor_log`처럼 세 부분을 사용합니다.

```sql
SELECT * FROM factory_a.sys.sensor_log;
INSERT INTO factory_b.app.orders VALUES (1, 'ready');
```

다른 database를 직접 참조하려면 대상 database의 `CONNECT`와 대상 table의 필요한 DML
권한이 모두 필요합니다. index 이름, `LOAD DATA` 대상 등은 각 구문의 별도 qualifier
제약을 따릅니다.

## 권한 구문과 database 범위

database 권한과 table 권한은 서로 별개입니다. 기본 형태는 다음과 같습니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_a;
GRANT CREATE, ALTER ON DATABASE factory_a TO deployer;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_a;
REVOKE CONNECT ON DATABASE factory_a FROM app_a;
```

mounted database를 조회할 때는 대상 database의 `USAGE`와 table `SELECT`가 모두 필요합니다.
`MOUNT DATABASE`와 `UMOUNT DATABASE`를 실행하는 운영 권한은 USER/AUTH 문법과
다중 데이터베이스 운영 가이드를
참조하십시오.

## BACKUP/RESTORE와의 관계

논리 database 백업·복원 구문은 BACKUP / RESTORE / MOUNT에
정리되어 있습니다. 단일 active catalog를 대상으로 한 named backup만 logical MOUNT 또는
RESTORE 입력으로 사용할 수 있으며, 여러 active database가 포함된 full-instance image는
logical catalog로 mount/restore할 수 없습니다.
