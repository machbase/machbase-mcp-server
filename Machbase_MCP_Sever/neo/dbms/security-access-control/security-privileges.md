# 권한 관리

Machbase 권한은 활성 데이터베이스 범위의 관리 권한과 특정 테이블의 DML 권한으로 나뉩니다.
사용자는 데이터베이스에 연결할 `CONNECT` 권한과, 실제 작업 대상에 필요한 권한을 모두 가져야
합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

## 권한 모델

| 범위 | 권한 | 용도 |
|---|---|---|
| 활성 데이터베이스 | `CONNECT` | 연결 및 `USE` |
| 활성 데이터베이스 | `CREATE`, `DROP`, `ALTER` | 객체 생성·삭제·변경 |
| 활성 데이터베이스 | `BACKUP` | 데이터베이스 백업 |
| 활성 데이터베이스 | `DDL` | `CREATE`와 `DROP` 묶음 |
| 활성 데이터베이스 | `ALL` | `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP` |
| 마운트된 데이터베이스 | `USAGE` | 마운트된 데이터베이스 탐색 |
| 관리 데이터베이스 | `MOUNT` | `MOUNT DATABASE`, `UMOUNT DATABASE` |
| 테이블 | `SELECT`, `INSERT`, `DELETE`, `UPDATE` | 특정 테이블 DML |
| 테이블 | `ALL` | 네 가지 테이블 DML 권한 |

데이터베이스의 `ALL`은 테이블 DML이나 `MOUNT`를 포함하지 않습니다. 테이블의 `ALL`도 데이터베이스
관리 권한을 포함하지 않습니다. 권한이 있어도 해당 테이블 타입이 지원하지 않는 DML은 실행할
수 없습니다. 예를 들어 LOG 테이블은 `UPDATE`를 지원하지 않습니다.

## GRANT / REVOKE

```sql
GRANT privilege_list ON target TO user_name;
REVOKE privilege_list ON target FROM user_name;
```

다음 예제는 사용자에게 데이터베이스 연결과 한 테이블의 읽기·쓰기를 허용합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM app_user;
REVOKE CONNECT ON DATABASE factory_a FROM app_user;
```

테이블은 현재 데이터베이스의 `owner.table` 또는 `database.owner.table`로 지정할 수 있습니다.
데이터베이스 전체에 `SELECT` 같은 DML 권한을 주는 구문은 지원하지 않습니다.

현재 권한 기록은 `M$SYS_USER_ACCESS`에서 확인합니다.

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY DB_NAME, OWNER_NAME, TABLE_NAME;
```

`OWNER_NAME`과 `TABLE_NAME`이 `NULL`이면 데이터베이스 범위, 값이 있으면 테이블 범위의
기록입니다. `PRIV`는 복수 권한을 표현하는 비트 마스크이므로 화면에 나온 숫자 하나를 권한명
하나로 해석하거나 운영 스크립트에 고정하지 마십시오.

## 데이터베이스 권한

논리 데이터베이스는 사용자를 만든 것만으로 연결할 수 없습니다. 대상 데이터베이스에 `CONNECT`를
명시적으로 부여하고 필요한 관리 권한을 최소 단위로 추가합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO deploy_user;
GRANT DDL ON DATABASE factory_a TO deploy_user;
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

새 사용자에게 기본으로 기록되는 호환 권한은 기본 데이터베이스인 `MACHBASEDB` 범위입니다.
다른 논리 데이터베이스까지 자동으로 확장되지 않습니다.

### SELECT / INSERT / DELETE / UPDATE

DML 권한은 특정 테이블을 대상으로 부여합니다.

```sql
GRANT SELECT ON sys.sensor_log TO reader_user;
GRANT INSERT ON sys.sensor_log TO writer_user;
GRANT DELETE ON sys.device_config TO maint_user;
GRANT UPDATE ON sys.device_config TO maint_user;
```

`DELETE`와 `UPDATE`를 부여하기 전에는 대상 테이블 타입의 조건 제약을 함께 검토합니다.
TAG 데이터 변경은 태그와 시간 조건이 필요하고, VOLATILE 변경은 기본 키 조건이 필요합니다.

### CREATE / DROP

```sql
GRANT CREATE ON DATABASE factory_a TO deploy_user;
GRANT DROP ON DATABASE factory_a TO deploy_user;
```

`DROP`은 복구하기 어려운 변경을 허용하므로, 단순 적재·조회 계정에는 부여하지 마십시오.
객체 소유권만으로 다른 데이터베이스에 접속할 수 있는 것은 아닙니다.

### ALTER

```sql
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

`ALTER`는 테이블 구조와 운영 설정 변경에 영향을 줄 수 있습니다. 애플리케이션 계정과 분리한
배포·운영 계정에만 부여하고, 변경 후 현재 설정과 스키마를 다시 조회하십시오.

### BACKUP

```sql
GRANT BACKUP ON DATABASE factory_a TO backup_user;
```

백업 경로에 대한 Machbase 서버 프로세스 OS 계정의 쓰기 권한과 여유 공간은 SQL 권한과
별도로 필요합니다. 백업용 DB 사용자에는 DML이나 DDL 권한을 함께 주지 않는 구성을 권장합니다.

### MOUNT

```sql
GRANT MOUNT ON DATABASE MACHBASEDB TO recovery_user;
```

MOUNT/UMOUNT는 관리 작업입니다. 마운트된 데이터베이스를 탐색할 `USAGE`와 그 안의 테이블을
읽을 `SELECT`는 별도 권한입니다. 실제 복구 절차는
백업, 복구, 마운트를 따르십시오.

### DDL / ALL 합성 권한

```sql
-- CREATE + DROP
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- active database의 CONNECT, CREATE, DROP, ALTER, BACKUP
GRANT ALL ON DATABASE factory_a TO database_admin;

-- 한 테이블의 SELECT, INSERT, DELETE, UPDATE
GRANT ALL ON TABLE factory_a.sys.sensor_log TO table_admin;
```

합성 권한은 편리하지만 최소 권한 검토를 어렵게 할 수 있습니다. 자동화 계정에는 가능한 한
개별 권한을 부여하십시오.

## 기본 부여 권한과 제외 권한

`CREATE USER`가 만든 사용자는 `MACHBASEDB`에 대한 호환 기본 권한 기록을 가집니다.
논리 데이터베이스에서는 다음처럼 필요한 범위를 명시하는 구성을 기준으로 삼으십시오.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

`ALTER`, `BACKUP`, `MOUNT`, `USAGE`와 다른 논리 데이터베이스의 권한은 업무 역할을 검토한 뒤
별도로 부여합니다.

## 테이블 권한

테이블 권한은 반드시 대상 객체와 함께 관리합니다.

```sql
GRANT SELECT ON TABLE factory_a.sys.sensor_log TO reader_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO ingest_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM ingest_user;
```

테이블을 삭제할 때 기존 테이블 grant도 정리되며, 같은 이름으로 만든 새 객체에 승계되지
않습니다. 필요한 권한을 다시 부여한 뒤 `M$SYS_USER_ACCESS`에서 확인하십시오.

## 권한 진단 체크리스트

사용자와 권한 현황을 다음 순서로 검토합니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

- 사용하지 않는 계정이 남아 있지 않은지 확인합니다.
- 읽기 계정에 쓰기·DDL·관리 권한이 없는지 확인합니다.
- 임시 권한은 승인된 기간이 끝나면 `REVOKE`하고 결과를 다시 조회합니다.
- 사용자를 삭제하기 전 소유 객체와 실행 중인 세션을 확인합니다.
- 숫자 `PRIV`를 해석해야 하는 감사 도구는 사용 중인 버전의 권한 정의와 함께 검증합니다.
