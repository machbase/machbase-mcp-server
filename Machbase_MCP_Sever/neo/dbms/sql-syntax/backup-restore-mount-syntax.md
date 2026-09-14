# BACKUP / RESTORE / MOUNT

Machbase의 백업·복원·마운트 구문은 데이터를 안전하게 보호하고 필요 시 복구하거나 과거 데이터를 조회할 때 사용합니다.

> **권한**: 일반 사용자가 백업·마운트를 실행하려면 별도 권한이 필요합니다.
> ```sql
> GRANT BACKUP ON DATABASE database_name TO user_name;
> GRANT MOUNT  ON DATABASE MACHBASEDB TO user_name;
> ```

---

## BACKUP

### 논리 데이터베이스 백업

8.7.0 Standard Edition에서는 대상 catalog를 명시하는 logical backup을 사용할 수 있습니다.

```sql
backup_logical_database_stmt ::=
    'BACKUP DATABASE' database_name
    [ 'AFTER' 'backup_path_or_lsn' ]
    'INTO DISK' '=' 'backup_path'
```

```sql
BACKUP DATABASE factory_a INTO DISK = '/backup/factory_a_20260806';
BACKUP DATABASE factory_a AFTER '/backup/factory_a_20260806'
  INTO DISK = '/backup/factory_a_inc';
```

논리 backup은 하나의 active database catalog를 대상으로 합니다. 여러 active database가
포함된 전체 인스턴스 image는 logical `MOUNT` 또는 `RESTORE` 입력으로 사용할 수 없습니다.

### 전체 백업

```sql
backup_database_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    [ 'IMPORT MODE' ]
```

현재 데이터베이스 전체를 지정한 경로에 저장합니다. 서버를 중단하지 않고 실행하는 온라인 백업입니다.

```sql
-- 절대 경로로 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 상대 경로 ($MACHBASE_HOME/dbs 기준)
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

- `backup_path`가 이미 존재하면 오류가 발생합니다. 날짜 등을 포함한 고유한 이름을 사용하십시오.
- 백업이 완료될 때까지 명령이 블로킹됩니다.

### 증분 백업

```sql
backup_incremental_stmt ::=
    'BACKUP DATABASE AFTER' 'backup_path_or_lsn'
    'INTO DISK' '=' 'backup_path'
```

마지막 전체 또는 증분 백업을 기준으로 백업합니다.
테이블 타입별 저장 방식은 구분해야 합니다. TRANSACTION 저장소는 증분 이미지에도
해당 백업 시점의 전체 스냅샷으로 포함되므로, 변경 행만의 델타나 변경량만큼의 공간으로
계산하면 안 됩니다. TRANSACTION 백업 검증에서
백업과 현재 데이터의 조회를 비교할 수 있습니다.

```sql
-- 전체 백업 이후 변경분 증분 백업
BACKUP DATABASE AFTER '/backup/machbase_20240101'
INTO DISK = '/backup/incr_20240102';
```

### 기간 백업

```sql
backup_period_stmt ::=
    'BACKUP DATABASE'
    'FROM' datetime_expr 'TO' datetime_expr
    'INTO DISK' '=' 'backup_path'
```

지정한 시간 범위에 해당하는 데이터만 백업합니다.

```sql
BACKUP DATABASE
FROM TO_DATE('2024-01-01','YYYY-MM-DD')
TO   TO_DATE('2024-02-01','YYYY-MM-DD')
INTO DISK = '/backup/period_jan';
```

### 테이블 백업

```sql
backup_table_stmt ::=
    'BACKUP TABLE' table_name 'INTO DISK' '=' 'backup_path'
```

전체 데이터베이스가 아닌 특정 테이블만 선택적으로 백업합니다.

```sql
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';
```

---

## RESTORE

기존 `machadmin -r` 복원은 서버를 중단한 오프라인 인스턴스 복원입니다. 8.7.0 Standard
Edition에서는 논리 database를 새 catalog로 복원하거나 READ ONLY target을 교체하는
online `RESTORE DATABASE`도 지원합니다.

```sql
restore_database_stmt ::=
    'RESTORE DATABASE' database_name 'FROM DISK' '=' 'backup_path'
    [ 'REMAP OWNER' old_owner 'TO' new_owner ]
    [ 'REPLACE' ]
```

```sql
RESTORE DATABASE factory_a_copy
  FROM DISK = '/backup/factory_a_20260806'
  REMAP OWNER APP_A TO APP_ARCHIVE;

RESTORE DATABASE factory_a
  FROM DISK = '/backup/factory_a_20260806'
  REPLACE;
```

`RESTORE DATABASE`는 SYS 전용입니다. `REPLACE` target은 READ ONLY이며 참조가 없어야
하고, restore 후 database/table 권한은 자동 승계되지 않으므로 다시 부여해야 합니다.
backup image의 unsupported object나 owner 충돌은 restore 전체를 실패시킬 수 있습니다.

### 기존 인스턴스 오프라인 복원 (`machadmin -r`)

복원 전 백업 SQL 파일을 준비해 검증한 뒤 실행합니다.

```sql
-- /secure/path/pre_restore_backup.sql
BACKUP DATABASE INTO DISK = '/backup/before_restore';
```

```bash
# 1. 복원 전 현재 데이터 백업
machsql -s 127.0.0.1 -P 5656 -u SYS \
  -f /secure/path/pre_restore_backup.sql

# 2. 서버 종료
machadmin -s

# 3. 현재 데이터베이스 삭제
machadmin -d

# 4. 백업 데이터로 복원
machadmin -r /backup/machbase_20240101

# 5. 서버 시작
machadmin -u
```

`machadmin -d`는 현재 database를 파기합니다. 복구 대상, 백업과 되돌림 계획을 확인하고
명시적으로 승인받은 뒤에만 실행하십시오. 복원을 실행하면 현재 database가 백업 시점으로
완전히 교체됩니다.

### 증분 백업 복원

복원할 최종 증분 백업 경로를 한 번 지정합니다. 증분 백업은 체인 정보를 포함하므로 전체 백업부터 반복 적용하지 않아도 됩니다.

```bash
machadmin -s
machadmin -d
machadmin -r /backup/incr_20240103
machadmin -u
```

### machadmin 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-s` (`--shutdown`) | 서버 정상 종료 |
| `-k` (`--kill`) | 서버 강제 종료 |
| `-u` (`--startup`) | 서버 시작 |
| `-d` (`--destroydb`) | 현재 데이터베이스 삭제 |
| `-r path` (`--restore`) | 지정한 백업 경로로 복원 |

---

## MOUNT DATABASE

```sql
mount_database_stmt ::=
    'MOUNT DATABASE' 'backup_database_path' 'TO' mount_name
```

서버를 중단하거나 active database를 교체하지 않고, 단일 catalog backup image를 현재 서버에
mounted database로 연결합니다. mounted database는 항상 READ ONLY이며 `USE`로 current
database가 될 수 없습니다.

- `backup_database_path`: DISK 방식으로 생성된 백업 디렉터리 경로
- `mount_name`: mounted database에 접근할 때 사용할 database alias

```sql
-- 절대 경로로 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 상대 경로 ($MACHBASE_HOME/dbs 기준)
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

### 마운트된 DB 조회

마운트된 데이터베이스의 테이블은 `mount_name.user_name.table_name` 형식으로 접근합니다.
조회하려면 mounted database의 `USAGE`와 대상 table의 `SELECT`가 모두 필요합니다.

```sql
-- 마운트 DB의 테이블 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- 현재 DB와 마운트 DB를 함께 조회 (JOIN)
SELECT a.name, a.value AS current_val, b.value AS backup_val
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name;
```

---

## UMOUNT DATABASE

```sql
umount_database_stmt ::=
    'UMOUNT DATABASE' mount_name
```

마운트된 데이터베이스를 해제합니다.

```sql
UMOUNT DATABASE backup_db;
```

마운트 DB를 참조 중인 열린 커서나 실행 중인 쿼리가 있으면 언마운트가 실패합니다. 해당 세션을 종료한 뒤 다시 실행하십시오.

---

## 제약 및 주의 사항

| 항목 | 설명 |
|------|------|
| 마운트 DB 쓰기 | 불가 (읽기 전용) |
| IBFILE 방식 백업 마운트 | 불가 (DISK 방식만 마운트 가능) |
| 버전 호환성 | 백업 DB와 현재 서버의 메타 버전이 호환되어야 함 |
| TAG 테이블 기간 복원 | 미지원 (전체 백업 또는 증분 백업으로만 복원 가능) |
| Cluster Edition | 다중 database와 MOUNT/UMOUNT 미지원 |

---

## 관련 문서

- 백업, 복원, 마운트 운영 가이드 - 상세 운영 절차 및 자동화 예시
- GRANT/REVOKE - 백업·마운트 권한 부여
