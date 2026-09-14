# V$STORAGE_MOUNT_DATABASES 사전

`V$STORAGE_MOUNT_DATABASES`는 현재 인스턴스에 읽기 전용으로 연결된 backup database를
표시합니다.

## 컬럼

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `NAME` | VARCHAR | backup database 이름 |
| `PATH` | VARCHAR | backup 이미지 원본 경로 |
| `BACKUP_TBSID` | LONG | backup의 tablespace 식별자 |
| `BACKUP_SCN` | LONG | backup SCN |
| `MOUNTDB` | VARCHAR | MOUNT할 때 지정한 database 별칭 |
| `DB_BEGIN_TIME` | VARCHAR | backup 데이터의 시작 시각 |
| `DB_END_TIME` | VARCHAR | backup 데이터의 종료 시각 |
| `BACKUP_BEGIN_TIME` | VARCHAR | backup 작업 시작 시각 |
| `BACKUP_END_TIME` | VARCHAR | backup 작업 종료 시각 |
| `FLAG` | INTEGER | 내부 상태 플래그. 값의 의미를 임의로 해석하지 않음 |

## 조회

```sql
SELECT NAME, PATH, MOUNTDB,
       DB_BEGIN_TIME, DB_END_TIME,
       BACKUP_BEGIN_TIME, BACKUP_END_TIME
  FROM V$STORAGE_MOUNT_DATABASES
 ORDER BY MOUNTDB;
```

## MOUNT와 조회 예제

```sql
MOUNT DATABASE '/data/backup/sc15_snapshot' TO backup_check;

SELECT *
  FROM backup_check.sys.target_table
 LIMIT 10;

UMOUNT DATABASE backup_check;
```

피연산자는 backup 경로, `TO`, 별칭 순서입니다. mounted database의 객체는
`mount_alias.owner.table` 세 부분 이름으로 조회합니다. 전체 권한과 안전 제한은
BACKUP/RESTORE/MOUNT 문법을
참고하십시오.
