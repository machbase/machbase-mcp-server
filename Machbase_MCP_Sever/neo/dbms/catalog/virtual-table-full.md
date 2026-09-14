# 전체 가상 테이블 레퍼런스

Virtual Table은 Machbase 서버의 운영 정보를 테이블 형태로 제공하는 읽기 전용 가상 테이블이며, 이름이 `V$`로 시작합니다. 서버 상태를 조회하거나 다른 테이블과 JOIN하여 운영 데이터를 분석하는 데 활용합니다. INSERT, UPDATE, DELETE는 지원하지 않습니다.

## 목차

* Session/System
  * V$PROPERTY
  * V$SESSION
  * V$SESMEM
  * V$SESSTAT
  * V$SESTIME
* V$SYSMEM
  * V$SYSSTAT
  * V$SYSTIME
  * V$STMT
  * V$VERSION
  * V$DATABASES
  * V$DATABASE_OPERATIONS
  * V$NEO\_SESSION
  * V$NEO\_STMT
* PVO Statement Cache
  * V$PVO\_CACHE\_STAT
  * V$PVO\_CACHE\_LIST
* Storage
  * V$STORAGE
  * V$STORAGE\_MOUNT\_DATABASES
  * V$CACHE
  * V$CACHE\_OBJECTS
  * V$STORAGE\_DC\_TABLESPACES
  * V$STORAGE\_DC\_TABLESPACE\_DISKS
  * V$STORAGE\_DC\_DWFILES
  * V$STORAGE\_DC\_PAGECACHE
  * V$STORAGE\_DC\_PAGECACHE\_LRU\_LST
  * V$STORAGE\_USAGE
  * V$STORAGE\_TABLES
* Log Table
  * V$STORAGE\_DC\_TABLES
  * V$STORAGE\_DC\_TABLES\_STAT
  * V$STORAGE\_DC\_TABLE\_COLUMNS
  * V$STORAGE\_DC\_TABLE\_COLUMN\_PARTS
  * V$STORAGE\_DC\_TABLE\_INDEXES
* LSM(Log Structured Merge) Index
  * V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS
  * V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS\_CACHE
  * V$STORAGE\_DC\_LSMINDEX\_LEVELS
  * V$STORAGE\_DC\_LSMINDEX\_FILES
  * V$STORAGE\_DC\_LSMINDEX\_AGER\_JOBS
* Volatile Table
  * V$STORAGE\_DC\_VOLATILE\_TABLE
* Tag Table
  * V$STORAGE\_TAG\_TABLES
  * V$STORAGE\_TAG\_CACHE
  * V$STORAGE\_TAG\_CACHE\_BASE
  * V$STORAGE\_TAG\_CACHE\_OBJECTS
  * V$STORAGE\_TAG\_TABLE\_FILES
  * V$STORAGE\_TAG\_INDEX
* Tag Rollup
  * V$ROLLUP
* License
  * V$LICENSE\_INFO
* Mutex
  * V$MUTEX
  * V$MUTEX\_WAIT\_STAT
* Cluster
  * V$NODE\_STATUS
  * V$DDL\_INFO
  * V$REPLICATION
  * V$REPL\_SENDER
  * V$REPL\_SENDER\_META
  * V$REPL\_RECEIVER
  * V$REPL\_RECEIVER\_META
  * V$REPL\_READER
  * V$REPL\_READER\_META
  * V$REPL\_WRITER
  * V$REPL\_WRITER\_META
* Others
  * V$TABLES
  * V$COLUMNS
  * V$RETENTION\_JOB
  * V$USER\_AUTH\_KEYS

## Session/System
### V$PROPERTY
---

서버에 설정된 프로퍼티 정보를 표시합니다.

| 컬럼 이름 | 설명           |
| ----- | ------------ |
| NAME  | 프로퍼티명        |
| VALUE | 프로퍼티 값       |
| TYPE  | 데이터 타입       |
| DEFLT | 기본 값         |
| MIN   | 설정할 수 있는 최소값 |
| MAX   | 설정할 수 있는 최대값 |

### V$SESSION
---

MACHBASE 서버에 접속된 세션 정보를 표시합니다.

| 컬럼 이름                              | 설명                                                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| HOSTNAME (Cluster Only)            | 세션 연결된 HOST 이름                                                                                                                   |
| ID                                 | 세션 식별자                                                                                                                           |
| CLOSED                             | 연결이 닫혀있는지 여부                                                                                                                     |
| USER_ID                            | 사용자 식별자                                                                                                                          |
| LOGIN_TIME                         | 접속 시각                                                                                                                            |
| CLIENT_TYPE                        | 접속 Client 타입                                                                                                                     |
| USER_NAME                          | 사용자 이름                                                                                                                           |
| CURRENT_DB_ID                     | 세션의 현재 논리 데이터베이스 식별자                                                                                                  |
| CURRENT_DB_NAME                   | 세션의 현재 데이터베이스 이름                                                                                                          |
| USER_IP                            | 사용자 IP                                                                                                                           |
| SQL_LOGGING                        | 해당 세션의 Trace Log 에 메시지를 남길지 여부<br>Parsing, Validation, Optimization 단계에서 발생하는 에러를 남깁니다.<br>DDL을 수행한 결과를 남깁니다.<br>(위의 두 케이스 모두 남깁니다) |
| SHOW_HIDDEN_COLS                   | SELECT 시, 숨겨진 컬럼을 나타낼 것인지 여부                                                                                                     |
| FEEDBACK_APPEND_ERROR              | APPEND 시 에러를 찾으면 곧바로 실패할 것인지 여부                                                                                                  |
| DEFAULT_DATE_FORMAT                | Datetime 입력 시 기본 입력 포맷                                                                                                           |
| MAX_QPX_MEM                        | 쿼리 수행 시 가용할 최대 메모리 크기                                                                                                            |
| IDLE_TIMEOUT                       | 세션 연결 후 해당 시간 동안 Client 가 아무일도 하지 않을 시 세션 종료                                                                                     |
| QUERY_TIMEOUT                      | 쿼리 수행 시 응답 대기 시간                                                                                                                 |
| DDL_LOCK_TIMEOUT (Standard Only)   | 충돌한 DDL 잠금을 기다릴 시간(초). `0`이면 즉시 오류를 반환합니다. |
| TRANSACTION_BUSY_TIMEOUT_MS                | TRANSACTION 쓰기 충돌 시 대기할 시간(밀리초). `-1`은 계속 대기하고 `0`은 즉시 오류를 반환합니다. |

### V$SESMEM
---

세션 메모리 정보를 표시합니다.

| 컬럼 이름 | 설명          |
| ----- | ----------- |
| SID   | 세션 식별자      |
| ID    | 메모리 매니저 식별자 |
| USAGE | 사용 크기       |

### V$SESSTAT
---

세션의 통계 정보를 표시합니다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| SID   | 세션 식별자    |
| ID    | 통계 정보 식별자 |
| VALUE | 통계 정보 값   |

### V$SESTIME
---

세션의 시간 정보를 표시합니다.

`ACCUM_MSEC`와 `MAX_MSEC`는 밀리초 단위의 `DOUBLE` 값입니다.

| 컬럼 이름      | 설명             |
| ---------- | -------------- |
| SID        | 세션 식별자         |
| ID         | 수행 단위 식별자      |
| ACCUM_MSEC | 누적 시간          |
| MAX_MSEC   | (각 수행 중) 최대 시간 |

### V$SYSMEM
---

시스템의 메모리 정보를 표시합니다.

| 컬럼 이름     | 설명           |
| --------- | ------------ |
| ID        | 메모리 매니저 식별자  |
| NAME      | 메모리 매니저 이름   |
| USAGE     | 현재 사용량       |
| MAX_USAGE | (기록된) 최대 사용량 |

### V$SYSSTAT
---

시스템의 통계 정보를 표시합니다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| ID    | 통계 정보 식별자 |
| NAME  | 통계 정보 이름  |
| VALUE | 통계 정보 값   |

### V$SYSTIME
---

시스템의 시간 정보를 표시합니다.

`ACCUM_MSEC`, `AVG_MSEC`, `MIN_MSEC`, `MAX_MSEC`는 밀리초 단위의 `DOUBLE` 값입니다.

| 컬럼 이름      | 설명             |
| ---------- | -------------- |
| ID         | 수행 단위 식별자      |
| NAME       | 수행 단위 이름       |
| ACCUM_MSEC | 누적 시간          |
| AVG_MSEC   | (각 수행 중) 평균 시간 |
| MIN_MSEC   | (각 수행 중) 최소 시간 |
| MAX_MSEC   | (각 수행 중) 최대 시간 |
| COUNT      | 수행 횟수          |

### V$STMT
---

사용자가 현재 실행중인 쿼리문에 대한 정보를 표시합니다.

| 컬럼 이름       | 설명                            |
| ----------- | ----------------------------- |
| ID          | 쿼리 식별자                        |
| SESS_ID     | 쿼리를 수행한 세션 식별자                |
| STATE       | 쿼리 상태                         |
| RECORD_SIZE | SELECT 구문 수행 중인 경우, 결과 레코드 크기 |
| QUERY       | 쿼리 구문                         |

### V$VERSION
---

MACHBASE 의 버전에 대한 정보를 표시합니다.

| 컬럼 이름                     | 설명                                       |
| ------------------------- | ---------------------------------------- |
| BINARY_DB_MAJOR_VERSION   | DB 메이저 버전                                |
| BINARY_DB_MINOR_VERSION   | DB 마이너 버전                                |
| BINARY_META_MAJOR_VERSION | META 메이저 버전                              |
| BINARY_META_MINOR_VERSION | META 마이너 버전                              |
| BINARY_CM_MAJOR_VERSION   | Client (Communication Level) 메이저 버전      |
| BINARY_CM_MINOR_VERSION   | Client (Communication Level) 마이너 버전      |
| BINARY_SIGNATURE          | DB서버 파일의 버전 명                            |
| FILE_DB_MAJOR_VERSION     | File DB 메이저 버전                           |
| FILE_DB_MINOR_VERSION     | File DB 메이저 버전                           |
| FILE_META_MAJOR_VERSION   | File META 메이저 버전                         |
| FILE_META_MINOR_VERSION   | File META 마이너 버전                         |
| FILE_CM_MAJOR_VERSION     | File Client (Communication Level) 메이저 버전 |
| FILE_CM_MINOR_VERSION     | File Client (Communication Level) 마이너 버전 |
| FILE_CREATE_TIME          | 파일 생성 시각                                 |
| EDITION                   | MACHBASE 유형                              |

### V$DATABASES
---

논리 active database와 mounted database의 상태를 표시합니다. `DATABASE_ID`는 논리
catalog 식별자이며 물리 `TABLESPACE_ID`와 동일하지 않습니다.

| 컬럼 이름 | 설명 |
|-----------|------|
| DATABASE_ID | 논리 데이터베이스 식별자 |
| SOURCE_DATABASE_ID | mounted backup 원본 데이터베이스 식별자 |
| NAME | 데이터베이스 이름 또는 mounted alias |
| KIND | `ACTIVE` 또는 `MOUNTED` |
| ACCESS_MODE | `READ_WRITE` 또는 `READ_ONLY` |
| CAN_USE | `USE`로 선택할 수 있는지 여부 |
| STATE | lifecycle 상태 |
| IS_DEFAULT | 기본 `MACHBASEDB` 여부 |

```sql
SELECT database_id, name, kind, access_mode, can_use, state, is_default
  FROM v$databases
 ORDER BY database_id;
```

### V$DATABASE_OPERATIONS
---

database lifecycle operation의 상태와 오류를 표시합니다.

| 컬럼 이름 | 설명 |
|-----------|------|
| OPERATION_ID | operation 식별자 |
| DATABASE_ID | 대상 논리 데이터베이스 식별자 |
| DATABASE_NAME | 대상 데이터베이스 이름 |
| STATE | operation 상태 |
| LAST_ERROR | 실패 원인 |
| CREATED_AT | 생성 시각 |
| UPDATED_AT | 마지막 변경 시각 |

```sql
SELECT operation_id, database_name, state, last_error
  FROM v$database_operations
 ORDER BY operation_id DESC;
```

### V$NEO_SESSION
---

Neo 프로토콜 클라이언트의 세션 상태를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| ID | 세션 식별자 |
| USER_ID | 사용자 식별자 |
| USER_NAME | 사용자 이름 |
| STMT_COUNT | 세션의 statement 수 |
| DISCONN_FLAG | 연결 해제 플래그 |

### V$NEO_STMT
---

Neo 프로토콜 클라이언트의 statement 상태를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| ID | statement 식별자 |
| SESS_ID | 세션 식별자 |
| STATE | statement 상태 |
| QUERY | statement 텍스트 |
| APPEND_SUCCESS_CNT | append 성공 건수 |
| APPEND_FAILURE_CNT | append 실패 건수 |

## PVO Statement Cache
Standard 에디션에서만 제공되는 글로벌 PVO Statement Cache 상태를 조회합니다.

### V$PVO_CACHE_STAT
---

PVO Statement Cache의 전체 통계를 보여줍니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| CACHE_ENTRY_COUNT | 캐시에 적재된 SQL 엔트리 수 |
| CACHE_HANDLE_COUNT | 모든 SQL에 대한 캐시된 플랜(핸들) 수 |
| CACHE_MEMORY_USAGE | 사용 중인 캐시 메모리 크기 |
| CACHE_MAX_MEMORY_SIZE | 설정된 캐시 메모리 한도 |
| CACHE_MAX_PLANS_PER_SQL | SQL당 허용되는 최대 플랜 수 |
| CACHE_MAX_SQL_ENTRIES | 허용되는 최대 SQL 엔트리 수 (0은 무제한) |
| CACHE_SHARD_COUNT | 캐시 샤드 개수 |
| CACHE_HIT | 캐시 히트 횟수 |
| CACHE_MISS | 캐시 미스 횟수 |
| SINGLEFLIGHT_WAIT | 동일 SQL 병행 빌드 대기 횟수 |
| BUILD_COUNT | 플랜 빌드 시도 횟수 |
| BUILD_FAIL | 빌드 실패 횟수 |
| INVALIDATE_COUNT | 무효화된 플랜 수 |
| EVICT_COUNT | 메모리 한도 등으로 인한 캐시 축출 횟수 |
| FLUSH_COUNT | 명시적/내부 플러시 횟수 |

### V$PVO_CACHE_LIST
---

PVO Statement Cache에 저장된 SQL별 상세 정보를 보여줍니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| TOUCH_TIME | 마지막 터치 시각 |
| USER_ID | SQL을 소유한 사용자 ID |
| QUERY | 원본 SQL 텍스트 |
| DEFAULT_DATE_FORMAT | 실행 당시의 날짜 포맷 |
| TIMEZONE_OFFSET | 실행 당시 타임존 오프셋 |
| SHOW_HIDDEN_COLS | 숨김 컬럼 표시 여부 |
| QUERY_PARALLEL_FACTOR | 병렬 실행 계수 |
| HANDLE_COUNT | 보유한 플랜(핸들) 수 |
| BUSY_COUNT | 동시에 사용 중인 핸들 수 |
| HIT_COUNT | 캐시 히트 횟수 |
| BUILD_IN_PROGRESS | 빌드 진행 중 여부 |

## Storage
### V$STORAGE
---

저장 시스템의 내부 정보를 표시합니다.

| 컬럼 이름                     | 설명                                   |
| ------------------------- | ------------------------------------ |
| DC_TABLE_FILE_SIZE        | 디스크 컬럼 데이터의 총 용량                     |
| DC_INDEX_FILE_SIZE        | 인덱스 파일 데이터의 총 용량                     |
| DC_TABLESPACE_DWFILE_SIZE | 모든 컬럼데이터를 위한 DWFILE의 총 용량            |
| DC_KV_TABLE_FILE_SIZE     | TAGDATA 테이블의 파티션 테이블이 가지는 데이터파일 총 용량 |

### V$STORAGE_MOUNT_DATABASES
---

마운트 기능을 이용하여 마운트한 백업 데이터베이스의 정보를 표시합니다.

| 컬럼 이름             | 설명                     |
| ----------------- | ---------------------- |
| NAME              | 마운트된 데이터베이스의 이름        |
| PATH              | 백업 파일의 위치              |
| BACKUP_TBSID      | 백업 데이터베이스의 테이블스페이스 식별자 |
| BACKUP_SCN        | 백업 데이터베이스의 식별자         |
| MOUNTDB           | MOUNT할 때 지정한 데이터베이스 별칭 |
| DB_BEGIN_TIME     | 백업 데이터베이스의 최초입력 시간     |
| DB_END_TIME       | 백업 데이터베이스의 최종 입력 시간    |
| BACKUP_BEGIN_TIME | 백업 실행시 시작 시간           |
| BACKUP_END_TIME   | 백업 실행시 종료 시간           |
| FLAG              | 프로퍼티 플래그               |

### V$CACHE
---

Storage Manager 에서 읽은 결과를 캐싱한, 캐시 객체에 대한 종합 정보를 표시합니다.

| 컬럼 이름     | 설명               |
| --------- | ---------------- |
| OBJ_COUNT | 결과집합 캐시 객체의 현재 수 |

### V$CACHE_OBJECTS
---

저장 시스템에서 읽은 결과를 캐싱한, 각 캐시 객체에 대한 정보를 표시합니다.

| 컬럼 이름     | 설명             |
| --------- | -------------- |
| OID       | 객체식별자          |
| REF_COUNT | 참조 카운트         |
| FLAG      | (서버 내부 사용 플래그) |

### V$STORAGE_DC_TABLESPACES
---

저장 시스템의 테이블스페이스 정보를 표시합니다.

| 컬럼 이름      | 설명                           |
| ---------- | ---------------------------- |
| NAME       | 테이블스페이스 이름                   |
| ID         | 테이블스페이스 식별자                  |
| FLAG       | 테이블스페이스 Property 를 나타내는 Flag |
| REF_COUNT  | 테이블스페이스 참조 횟수                |
| DISK_COUNT | 테이블스페이스에 속한 디스크 개수           |

### V$STORAGE_DC_TABLESPACE_DISKS
---

저장 시스템의 테이블스페이스 정보를 표시합니다.

| 컬럼 이름              | 설명                  |
| ------------------ | ------------------- |
| NAME               | 디스크 이름              |
| ID                 | 디스크 식별자             |
| TABLESPACE_ID      | 디스크가 속한 테이블스페이스 식별자 |
| PATH               | 디스크의 경로             |
| IO_THREAD_COUNT    | I/O Thread 개수       |
| IO_JOB_COUNT       | I/O Job 개수          |
| VIRTUAL_DISK_COUNT | 가상 디스크 개수           |

### V$STORAGE_DC_DWFILES
---

저장 시스템에서 운용하는 Double-write 파일 (DW File) 의 정보를 표시합니다.

| 컬럼 이름                | 설명                      |
| -------------------- | ----------------------- |
| TBS_ID               | 테이블스페이스 식별자             |
| DISK_ID              | 디스크 식별자                 |
| FILE                 | 파일의 경로                  |
| TABLE_ID             | 테이블 식별자                 |
| COLUMN_ID            | 컬럼 식별자                  |
| PARTITION_ID         | 파티션 식별자                 |
| PAGE_ID              | 페이지 식별자                 |
| DISK_OFFSET          | 디스크 오프셋                 |
| DISK_IMAGE_SIZE      | 디스크 이미지 크기              |
| HEAD_CRC32CODE_IMAGE | CRC32 Code 의 Head Image |
| TAIL_CRC32CODE_IMAGE | CRC32 Code 의 Tail Image |
| CRC32CODE_PAGE       | CRC32 Code 의 Page       |
| HEAD_TIMESTAMP_PAGE  | Timestamp 의 Head Page   |
| TAIL_TIMESTAMP_PAGE  | Timestamp 의 TailPage    |

### V$STORAGE_DC_PAGECACHE
---

저장 시스템에서 운용하는 Page Cache 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                     |
| ------------ | ---------------------- |
| MAX_MEM_SIZE | Page Cache 의 최대 메모리 크기 |
| CUR_MEM_SIZE | Page Cache 의 현재 메모리 크기 |
| PAGE_CNT     | 캐싱된 페이지 개수             |
| CHECK_TIME   | 검사 시간                  |

### V$STORAGE_DC_PAGECACHE_LRU_LST
---

저장 시스템에서 운용하는 Page Cache 의 LRU List 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                  |
| ------------ | ------------------- |
| SIZE         | 페이지 크기              |
| REF_CNT      | 참조 횟수               |
| PARTITION_ID | 파티션 식별자             |
| OFFSET       | Page Cache 의 Offset |
| OBJECT_ID    | 객체 식별자              |
| LEVEL        | 파티션 레벨              |

### V$STORAGE_USAGE
---

저장 시스템에서 사용 중인 스토리지의 사용량을 표시합니다.

| 컬럼 이름       | 설명                                                     |
| ----------- | ------------------------------------------------------ |
| TOTAL_SPACE | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 총 용량                |
| USED_SPACE  | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 사용량                 |
| USED_RATIO  | 사용량 비율(%)                                              |
| RATIO_CAP   | 스토리지 사용량 한계. USED_RATIO이 이 한계에 도달하면 데이터 입력/인덱스 구축이 멈춤. |

### V$STORAGE_TABLES
---

테이블의 상세 정보를 표시합니다.

| 컬럼 이름         | 설명                                                                                                                                                                                                         |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID            | 테이블의 ID                                                                                                                                                                                                    |
| TYPE          | 테이블 형태<br>Persistent: LOG 테이블과 TAG 테이블<br>Volatile: 휘발성(Volatile) 테이블<br>Key-Value: TAG 테이블의 부속 테이블                                                                                                        |
| STATUS        | 현재 상태<br>Creating...: CREATE TABLE로 테이블 생성 진행중<br>Normal: 정상<br>Predrop: DROP TABLE 명령 접수 상태<br>Dropping...: DROP TABLE 명령 수행 상태<br>Dropped: DROP TABLE 명령 완료 상태<br>Mounted: 백업된 데이터베이스를 mount 명령으로 불러온 상태 |
| STORAGE_USAGE | 해당 테이블이 스토리지에서 점유한 용량                                                                                                                                                                                      |

## Log Table
### V$STORAGE_DC_TABLES
---

Log Table 에 대한 내부 정보를 표시합니다.

| 컬럼 이름                | 설명                                         |
| -------------------- | ------------------------------------------ |
| ID                   | 테이블의 식별자                                   |
| TABLESPACE_ID        | 테이블스페이스 식별자                               |
| CREATE_SCN           | 생성 당시의 시스템 변경 번호 (System Change Number)    |
| UPDATE_SCN           | 최근 변경 당시의 시스템 변경 번호 (System Change Number) |
| DDL_REF_COUNT        | DDL 구문 수행으로, 해당 테이블을 참조하고 있는 세션의 개수.       |
| BEGIN_RID            | 테이블의 최소 RID                                |
| END_RID              | 테이블의 마지막 Row ID + 1                        |
| BEGIN_META_RID       | 메타 정보를 기록하기 시작한 시점의 ID                     |
| END_META_RID         | 메타 정보의 기록이 종료한 시점의 ID                      |
| END_SYNC_RID         | 디스크에 기록된 마지막 Row ID + 1                    |
| FLAG                 | Table Property 를 나타내는 Flag                 |
| COLUMN_COUNT         | 테이블의 컬럼 수                                  |
| INDEX_COUNT          | 테이블의 인덱스 수                                 |
| INDEX_MIN_END_RID    | 인덱스에 기록된 마지막 RID + 1                       |
| LAST_ARRIVAL_TIME    | 마지막으로 기록된 \_arrival_time 값                 |
| LAST_CHECKPOINT_TIME | 마지막으로 Checkpoint 를 지난 시점                   |
| TYPE                 | 테이블 유형                                     |

### V$STORAGE_DC_TABLES_STAT
---

Log Table 에 대한 내부 정보를 표시합니다.

| 컬럼 이름         | 설명          |
| ------------- | ----------- |
| TABLESPACE_ID | 테이블스페이스 식별자 |
| TABLE_ID      | 테이블 식별자     |
| COUNT         | 레코드 개수      |
| COLUMN_ID     | 컬럼 식별자      |

### V$STORAGE_DC_TABLE_COLUMNS
---

Log Table 의 컬럼에 대한 정보를 표시합니다.

| 컬럼 이름                     | 설명                              |
| ------------------------- | ------------------------------- |
| TABLE_ID                  | 테이블 식별자                         |
| TABLESPACE_ID             | 테이블스페이스 식별자                    |
| ID                        | 컬럼 식별자                          |
| FLAG                      | 프로퍼티 플래그                        |
| SIZE                      | 컬럼의 데이터 크기                      |
| PARTITION_VALUE_COUNT     | 파티션에 저장되는 최대 데이터 수              |
| PAGE_VALUE_COUNT          | 페이지에 저장되는 최대 데이터 수              |
| CACHE_VALUE_COUNT         | 캐시 값의 최대 수                      |
| MINMAX_CACHE_SIZE         | 컬럼 파티션에 대한 MIN/MAX 캐시의 최대 크기    |
| CUR_APPEND_PARTITION_ID   | 현재 입력을 진행중인 파티션의 식별자            |
| CUR_CACHE_PARTITION_COUNT | 현재 캐시에 데이터를 읽어들인 파티션의 수         |
| CUR_MINMAX_CACHE_SIZE     | 현재 MIN/MAX캐시의 크기                |
| END_RID_FOR_DEFAULT_VALUE | 이 값보다 작은 RID를 갖는 컬럼은 디폴트값으로 지정됨 |
| DISK_FILE_SIZE            | 해당 컬럼에 대한 컬럼 파티션 데이터 파일의 전체 크기  |
| MEMORY_TOTAL_SIZE         | 테이블이 사용 중인 메모리 크기               |
| MEMORY_ALLOC_SIZE         | 테이블이 할당받은 메모리 크기                |

### V$STORAGE_DC_TABLE_COLUMN_PARTS
---

Log Table 의 컬럼 파티션 정보를 표시합니다.

| 컬럼 이름                         | 설명                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| TABLE_ID                      | 테이블 식별자                                                                            |
| TABLESPACE_ID                 | 테이블스페이스 식별자                                                                       |
| COLUMN_ID                     | 컬럼 식별자                                                                             |
| ID                            | 파티션 식별자                                                                            |
| FLAG                          | 컬럼 Property 를 나타내는 Flag                                                            |
| BEGIN_RID                     | 파티션에 저장된 최소 RID                                                                    |
| END_RID                       | 파티션에 저장된 최종 RID                                                                    |
| END_SYNC_RID                  | SYNC가 끝난 최종 RID.<br>시작 RID 보다 크고 마지막 SYNC RID 보다 작은 RID 를 갖는 데이터는 파티션 파일에 기록되어 있습니다. |
| MIN_TIME                      | 컬럼 파티션에 최초로 데이터를 입력한 시간                                                            |
| MAX_TIME                      | 컬럼 파티션에 마지막으로 데이터를 입력한 시간                                                          |
| MAX_VALUE_COUNT_PER_PARTITION | 파티션의 최대 데이터 수                                                                      |
| MAX_VALUE_COUNT_PER_PAGE      | 페이지당 최대 데이터 수                                                                      |
| MAX_PAGE_COUNT                | 파티션당 최대 페이지의 수                                                                     |
| PAGE_SIZE                     | 컬럼 파티션에 저장된 페이지의 크기                                                                |
| PAGE_COUNT                    | 현재 컬럼 파티션에 생성된 페이지의 수                                                              |
| COMPRESS_RATIO                | 컬럼 파티션의 압축률. 0이면 아직 데이터 압축이 실행되지 않은 경우입니다.                                          |
| DISK_FILENAME                 | 파티션 파일의 이름                                                                         |
| EXTERNAL_PART_SIZE            | 데이터의 양이 큰 값은 외부 파티션 파일에 기록하는데, 그 파일의 크기를 표시                                        |
| MIN_VALUE                     | 컬럼 파티션의 최소값                                                                        |
| MAX_VALUE                     | 컬럼 파티션의 최대값                                                                        |

### V$STORAGE_DC_TABLE_INDEXES
---

Log Table 에 생성된 인덱스 정보를 표시합니다.

| 컬럼 이름                | 설명                           |
| -------------------- | ---------------------------- |
| TABLE_ID             | 테이블 식별자                      |
| TABLESPACE_ID        | 테이블스페이스 식별자                 |
| ID                   | 인덱스 식별자                      |
| FLAG                 | 인덱스 Property 를 나타내는 Flag     |
| TABLE_BEGIN_RID      | 테이블의 입력된 최소 RID              |
| TABLE_END_RID        | 테이블의 마지막 RID                 |
| BEGIN_RID            | 인덱스의 최소 RID                  |
| END_RID              | 인덱스의 최대 RID                  |
| END_SYNC_RID         | 파일에 기록된 최대 RID+1             |
| COLUMN_COUNT         | 인덱스 컬럼 수                     |
| BEGIN_PART_ID        | 인덱스의 최초 파티션 식별자              |
| END_PART_ID          | 인덱스의 최종 파티션 식별자              |
| FLUSH_REQUEST_COUNT  | 디스크에 반영요청된 인덱스 파티션의 수        |
| MAX_KEY_SIZE         | 최대 키 크기                      |
| INDEX_TYPE           | 인덱스 유형                       |
| DISK_FILE_SIZE       | 해당 인덱스에 대한 인덱스 파티션 파일의 전체 크기 |
| LAST_CHECKPOINT_TIME | 마지막으로 Checkpoint 를 지난 시점     |

## LSM(Log Structured Merge) Index
### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS
---

LSM Index 파티션에 대한 정보를 표시합니다.

| 컬럼 이름                      | 설명                                      |
| -------------------------- | --------------------------------------- |
| TABLE ID                   | 인덱스가 생성된 테이블의 식별자                       |
| TABLESPACE_ID              | 테이블스페이스 식별자                             |
| INDEX_ID                   | 인덱스 식별자                                 |
| LEVEL                      | 인데스 파티션의 LSM 레벨                         |
| PARTITION_ID               | 파티션 식별자                                 |
| BEGIN_RID                  | 파티션에 입력된 최소 RID                         |
| END_RID                    | 파티션에 입력된 최대 RID+1                       |
| KEY_VALUE_COUNT            | 파티션에 입력된 키값의 수                          |
| KEY_VALUE_TABLE_SIZE       | 키값을 저장하는 페이지 크기                         |
| KEY_VALUE_TABLE_PAGE_COUNT | 키값을 저장하는 페이지의 수                         |
| MIN_KEY_VALUE              | 최소 키 값                                  |
| MAX_KEY_VALUE              | 최대 키 값                                  |
| BITMAP_TABLE_SIZE          | 비트맵 값을 저장하는 페이지의 합계                     |
| BITMAP_TABLE_PAGE_COUNT    | 비트맵 값을 저장하는 페이지의 수                      |
| META_SIZE                  | 메타 정보를 저장하는 페이지의 합계                     |
| META_PAGE_COUNT            | 메타 정보를 저장하는 페이지의 수                      |
| TOTAL_BUILD_MSEC           | 해당 파티션을 완성하기 까지의 총 시간                   |
| KEYVAL_BUILD_MSEC          | KeyValue Mode 에서, 해당 파티션을 완성하기 까지의 총 시간 |
| BITMAP_BUILD_MSEC          | Bitmap Mode 에서, 해당 파티션을 완성하기 까지의 총 시간   |

### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS_CACHE
---

LSM Index 파티션 캐시에 대한 정보를 표시합니다.

| 컬럼 이름                      | 설명                          |
| -------------------------- | --------------------------- |
| BEGIN_RID                  | 파티션에 입력된 최소 RID             |
| BITMAP_TABLE_PAGE_COUNT    | 비트맵 값을 저장하는 페이지의 수          |
| BITMAP_TABLE_SIZE          | 비트맵 값을 저장하는 페이지의 합계         |
| END_RID                    | 파티션에 입력된 최대 RID+1           |
| INDEX_ID                   | 인덱스 식별자                     |
| KEY_VALUE_COUNT            | 파티션에 입력된 키값의 수              |
| KEY_VALUE_TABLE_PAGE_COUNT | 키값을 저장하는 페이지의 수             |
| KEY_VALUE_TABLE_SIZE       | 키값을 저장하는 페이지의 크기            |
| LEVEL                      | 인데스 파티션의 LSM 레벨             |
| MEMORY_SIZE                | 메모리 사용량                     |
| MEMORY_SIZE_RBTREE         | Redblack Tree 가 사용한 메모리 사용량 |
| META_PAGE_COUNT            | 메타 정보를 저장하는 페이지의 수          |
| META_SIZE                  | 메타 정보를 저장하는 페이지의 합계         |
| PARTITION_ID               | 파티션 식별자                     |
| TABLE_ID                   | 인덱스가 생성된 테이블의 식별자           |
| TABLESPACE_ID              | 테이블스페이스 식별자                 |

### V$STORAGE_DC_LSMINDEX_LEVELS
---

LSM 인덱스의 레벨에 관한 정보를 표시합니다.

| 컬럼 이름          | 설명                     |
| -------------- | ---------------------- |
| TABLE_ID       | 테이블 식별자                |
| TABLESPACE_ID  | 테이블스페이스 식별자           |
| INDEX_ID       | 인덱스 식별자                |
| LEVEL          | 레벨                     |
| BEGIN_RID      | 파티션의 첫번째 RID           |
| END_RID        | 파티션의 마지막 RID+1         |
| META_BEGIN_RID | 메타정보를 기록하기 시작한 시점의 RID |
| META_END_RID   | 메타정보의 기록이 끝난 시점의 RID   |
| DELETE_END_RID | 삭제된 RID 최대값 +1         |

### V$STORAGE_DC_LSMINDEX_FILES
---

LSM Index 를 구성하는 파일에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명              |
| ------------ | --------------- |
| TABLE_ID     | 테이블 식별자         |
| TABLESPACE_ID | 테이블스페이스 식별자    |
| INDEX_ID     | 인덱스 식별자         |
| LEVEL        | 인데스 파티션의 LSM 레벨 |
| PARTITION_ID | 파티션 식별자         |
| BEGIN_RID    | 파티션의 첫번째 RID    |
| END_RID      | 파티션의 마지막 RID+1  |
| PATH         | 인덱스 파일의 위치      |

### V$STORAGE_DC_LSMINDEX_AGER_JOBS
---

LSM Index 의 삭제를 담당하는 Ager 의 작업 상태를 표시합니다.

| 컬럼 이름     | 설명                 |
| --------- | ------------------ |
| TABLE_ID  | 테이블 식별자            |
| INDEX_ID  | 인덱스 식별자            |
| LEVEL     | 인데스 파티션의 LSM 레벨    |
| BEGIN_RID | 파티션의 첫번째 RID       |
| END_RID   | 파티션의 마지막 RID+1     |
| STATE     | Index Ager 의 작업 상태 |

## Volatile Table
### V$STORAGE_DC_VOLATILE_TABLE
---

Volatile Table 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                          |
| ------------ | --------------------------- |
| MAX_MEM_SIZE | Volatile Tablespace 의 최대 크기 |
| CUR_MEM_SIZE | Volatile Tablespace 의 현재 크기 |

## Tag Table
### V$STORAGE_TAG_TABLES
---

Tagdata Table 의 파티션 테이블에 대한 정보를 표시합니다.

| 컬럼 이름                | 설명                                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID                   | 테이블 식별자                                                                                                                                                                                      |
| TABLE_BEGIN_RID      | 테이블 시작 RID                                                                                                                                                                                   |
| TABLE_END_RID        | 테이블 끝 RID                                                                                                                                                                                    |
| WRITE_END_RID        | 데이터 파일에 기록된 마지막 RID                                                                                                                                                                          |
| EXT_ROW_COUNT        | VARCHAR 레코드 중 외부 파티션에 입력된 개수                                                                                                                                                                 |
| EXT_WRITE_COUNT      | VARCHAR 레코드 중 데이터파일에 기록된 개수                                                                                                                                                                  |
| DISK_INDEX_END_RID   | 스토리지에 저장된 인덱스의 끝 RID                                                                                                                                                                         |
| MEMORY_INDEX_END_RID | 메모리 인덱스에 상주한 테이블 끝 RID                                                                                                                                                                       |
| DELETE_MIN_DATE      | DELETE ... BETWEEN ... 수행시 삭제 대상의 최소 시각                                                                                                                                                      |
| DELETE_MAX_DATE      | DELETE ... BETWEEN ..., 혹은 DELETE ... BEFORE ... 수행시 삭제 대상의 최대 시각                                                                                                                            |
| INDEX_STATE          | 현재 인덱스 구축 상태<br>IDLE: 구축 완료, 대기중.<br>PROGRESS: 구축 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료                |
| DELETE_STATE         | 현재 DELETE 연산의 상태. DELETE 명령이 들어올 때에만 수행되므로 IDLE이 없습니다.<br>PROGRESS: 삭제 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기/쓰기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산이 진행되지 않습니다.<br>ABNORMAL: 비정상 종료 |
| SAVE_STATE           | 현재 테이블 저장 연산의 상태.<br>IDLE: 저장 완료, 대기중.<br>PROGRESS: 저장 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료           |
| VINDEX_STATE         | 현재 VARCHAR 인덱스 구축 상태<br>IDLE: 구축 완료, 대기중.<br>PROGRESS: 구축 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료                |

### V$STORAGE_TAG_CACHE
---

Tagdata Table 의 파티션 테이블에서 사용하는 캐시 정보를 표시합니다.

| 컬럼 이름       | 설명                       |
| ----------- | ------------------------ |
| POOL_ID     | 캐시 풀 식별자                 |
| CATEGORY    | 캐쉬되고 있는 객체 분류            |
| USED_MEMORY | 사용중인 메모리 크기              |
| BLOCK_COUNT | 데이터 캐시 개수                |
| CACHE_HIT   | 데이터 캐시 히트 횟수             |
| CACHE_MISS  | 데이터 캐시 미스 횟수             |
| FLUSHOUT    | 데이터 캐시 충돌로 페이지를 비운 횟수    |
| COLD_READ   | 스토리지에서 직접 읽어온 데이터 페이지 개수 |
| MEMORY_WAIT | 데이터 메모리가 캐시 충돌로 대기한 횟수   |
| IO_WAIT     | 데이터 읽기 연산 대기 횟수          |

### V$STORAGE_TAG_CACHE_BASE
---

태그 캐시 풀의 집계 정보를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| POOL_ID | 캐시 풀 식별자 |
| TOTAL_CACHE_MEMORY | 전체 캐시 메모리 |
| TOTAL_OBJECT_COUNT | 전체 캐시 객체 수 |
| TOTAL_LRU_LOOP_COUNT | 전체 LRU 루프 수 |

### V$STORAGE_TAG_CACHE_OBJECTS
---

Tagdata Table의 파티션 테이블에서 사용하는 각각의 캐시 블럭에 대한 상세정보를 표시합니다.

| 컬럼 이름      | 설명                                                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| CATEGORY   | 캐쉬되고 있는 객체 분류                                                                                                        |
| LATEST_HIT | 마지막 접근 시각                                                                                                            |
| STATUS     | 캐시 상태<br>None: 메모리 할당을 마친 상태<br>Resides: 캐시에 보존된 상태<br>Loading: 스토리지에서 테이블 데이터를 불러 오는 중<br>ERROR!: 데이터를 불러오는 중 오류 발생 |
| WAIT_COUNT | Loading 상태에서 해당 캐시를 읽지 못해 대기한 회수                                                                                     |
| REF_COUNT  | 현재 캐시 블럭을 참조 중인 세션 수                                                                                                 |
| HIT_COUNT  | 캐시 블럭을 참조한 회수                                                                                                        |
| TABLE_ID   | 테이블 식별자                                                                                                              |
| FILE_ID    | 파일 식별자                                                                                                               |
| PART_ID    | 데이터파일 내부의 파티션 식별자                                                                                                    |
| SAVE_SCN   | 테이블 저장 SCN                                                                                                           |
| VSAVE_SCN  | 테이블 저장 SCN                                                                                                           |
| DELETE_SCN | DELETE 연산 SCN                                                                                                        |
| OFFSET     | 데이터파일 오프셋                                                                                                            |
| DATA_SIZE  | 압축 이전 데이터 크기, 혹은 0                                                                                                   |

### V$STORAGE_TAG_TABLE_FILES
---

Tagdata Table 의 파티션 테이블의 파일 정보를 표시합니다.

| 컬럼 이름     | 설명                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| TABLE_ID  | 테이블 식별자                                                                                                                            |
| FILE_ID   | 파일 식별자                                                                                                                             |
| STATE     | 인덱싱 상태<br>COMPLETE: 데이터 저장, 인덱싱 완료<br>INDEXING: 인덱스 구축 중.<br>FILLED: 데이터가 꽉 찬 상태, 인덱싱 대기 중<br>PARTIAL: 아직 데이터가 꽉 차지 않았음. 인덱싱 대기 중. |
| REF_COUNT | 현재 파일을 참조 중인 세션 수                                                                                                                  |
| ROW_COUNT | 삭제됐던 레코드를 포함하여 파일에 저장된 레코드 개수                                                                                                      |
| DEL_COUNT | 파일에서 삭제된 레코드 개수                                                                                                                    |
| MIN_DATE  | 해당 파일에 기록된 데이터의 최소 일자                                                                                                              |
| MAX_DATE  | 해당 파일에 기록된 데이터의 최대 일자                                                                                                              |

### V$STORAGE_TAG_INDEX
---

Tagdata Table 에 생성된 인덱스 정보를 표시합니다.

| 컬럼 이름                | 설명                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| TABLE_ID             | 테이블 식별자                                                                                               |
| INDEX_ID             | 인덱스 식별자(INDEX_ID가 4294967295인 경우 tag테이블 생성시 자동으로 생성되는 기본 인덱스를 의미함)                                    |
| INDEX_STATE          | 인덱싱 상태<br>IDLE: 인덱싱이 완료되어 대기중인 상태<br>INDEXING: 인덱싱이 진행중인 상태<br>STORAGE FULL: Disk full상태로 인덱싱이 중단된 상태 |
| DISK_INDEX_END_RID   | 마지막으로 disk에 반영된 인덱스의 EndRID                                                                           |
| MEMORY_INDEX_END_RID | 마지막으로 memory에 반영된 인덱스의 EndRID                                                                         |
| TABLE_END_RID        | 테이블에 마지막으로 반영된 데이터의 EndRID                                                                            |

## Tag Rollup
### V$ROLLUP
---

Tagdata 테이블의 Rollup 정보를 표시합니다.

| 컬럼 이름          | 설명                                                      |
| -------------- | ------------------------------------------------------- |
| DATABASE_ID    | 논리 데이터베이스 식별자                                  |
| ID             | Rollup 작업 ID                                            |
| ROLLUP_TABLE   | Rollup 테이블 이름                                         |
| SOURCE_TABLE   | 집계 대상 테이블 이름(TAG/ROLLUP)                                |
| COLUMN_NAME    | 집계 대상 값 컬럼                                               |
| ROOT_TABLE     | 최상위 소스 태그 테이블 이름                                        |
| USER_ID        | 소유자 User ID                                             |
| INTERVAL_TIME  | 데이터 집계 간격(밀리초)                                         |
| WAKEUP_INTERVAL| Rollup 작업의 실행 주기(밀리초)                                  |
| LAST_WAKEUP_TIME| 최근 wakeup 시각                                            |
| NEXT_WAKEUP_TIME| 다음 wakeup 예정 시각                                         |
| ENABLED        | Rollup 활성화 여부(1/0)                                      |
| END_RID        | 이 Rollup이 처리한 Source Table의 마지막 RID                      |
| LAST_ELAPSED_MSEC | 직전 Rollup 실행에 걸린 시간(밀리초)                               |
| EXT_TYPE       | 확장(EXTENSION) 여부 플래그                                     |
| PREDICATE      | 조건 롤업의 필터 식(NULL이면 조건 없음)                              |
| RUN_STATE      | 스레드 상태: I=INIT, S=SLEEPING, R=RUNNING                      |

## License
### V$LICENSE_INFO
---

라이선스 정보를 표시합니다.

| 컬럼 이름            | 설명                     |
| ---------------- | ---------------------- |
| ID               | 라이선스 ID               |
| ISSUE_DATE       | 발행일                    |
| TYPE             | 라이선스 유형                |
| CUSTOMER         | 고객사 이름                 |
| PROJECT          | 프로젝트 이름                |
| COUNTRY_CODE     | 국가 코드                  |
| INSTALL_DATE     | 설치일                    |
| VIOLATE_STATUS   | 라이선스 위반 상태             |
| VIOLATE_MSG      | 라이선스 위반 메시지            |

`V$LICENSE_STATUS`는 Standard 8.5.4 서버에서 노출되지 않습니다. Standard 에디션에서
조회 가능한 라이선스 필드는 `V$LICENSE_INFO`를 사용하십시오.

## Mutex
### V$MUTEX
---

현재 뮤텍스 상태를 보여줍니다.

`WAIT_MSEC`, `WAIT_AVG_MSEC`, `HELD_MSEC`, `HELD_AVG_MSEC`는 밀리초 단위의 `DOUBLE` 값입니다.

| 필드명            | 설명                         | 비고                                                                                                         |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| OBJECT         | 뮤텍스 객체의 주소                 |                                                                                                            |
| NAME           | 뮤텍스 생성시 부여한 이름             |                                                                                                            |
| TYPE           | 뮤텍스 타입                     | Mutex: pmuMutex<br>RW Mutex: pmuRWMutex                                                                    |
| OWNER          | 뮤텍스를 획득한 스레드의 ID           | Mutex: 뮤텍스를 획득한 스레드가 없으면 0.<br>RW Mutex w/ Read-Lock: 0<br>RW Mutex w/ Write-Lock: Write Lock을 획득한 스레드의 ID |
| LOCK_COUNT     | 뮤텍스를 획득한 스레드 개수            | RW Mutex는 2 이상이 될 수 있습니다.                                                                                    |
| PEND_COUNT     | 뮤텍스를 획득하려고 대기 중인 스레드 개수    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| TRY_COUNT      | 뮤텍스를 획득하려고 시도한 회수          | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| CONFLICT_COUNT | 뮤텍스 획득에 실패한 회수             | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| WAIT_MSEC      | 뮤텍스 획득 대기 시간의 총합           | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| WAIT_AVG_MSEC  | 뮤텍스 획득 시도 후 성공까지의 평균 시간    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_MSEC      | 뮤텍스를 획득한 이후 해제할 때까지의 시간 총합 | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_AVG_MSEC  | 뮤텍스 획득 이후 해제까지의 시간 평균      | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |

### V$MUTEX_WAIT_STAT
---

현재 대기중인 뮤텍스의 콜스택을 보여줍니다.

| 필드        | 설명                  | 비고                               |
| --------- | ------------------- | -------------------------------- |
| THREAD_ID | 뮤텍스 획득 대기 중인 스레드 ID |                                  |
| OBJECT    | 획득 시도 중인 뮤텍스의 주소    | V$MUTEX의 OBJECT와 동일              |
| DEPTH     | 호출 깊이               | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |
| SYMBOL    | 뮤텍스 획득을 호출한 함수의 심볼  | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |

## Cluster

다음 가상 테이블은 클러스터 에디션용이며 Standard 서버에서는 노출되지 않습니다.
실행 중인 에디션에서 조회 가능한지 `V$TABLES`로 확인한 뒤 사용하십시오.

### V$NODE_STATUS
---

Cluster 각 Node 의 상태를 표시합니다. 1건만 표시됩니다.

| 컬럼 이름    | 설명                                                            |
| -------- | ------------------------------------------------------------- |
| NODETYPE | Node 의 유형. 쿼리로 조회 가능한 Type 은 두 가지 뿐입니다.<br>Broker<br>Warehouse |
| STATE    | Node 의 상태                                                     |

### V$DDL_INFO
---

Cluster 에서 수행한 DDL 정보를 표시합니다.

| 컬럼 이름          | 설명                      |
| -------------- | ----------------------- |
| SEQUENCENUMBER | DDL 순서 번호               |
| TIME           | DDL 수행 시간               |
| VALUE          | DDL 쿼리 결과 값 (서버 내부 사용)  |
| CLIENT         | 클라이언트 이름                |
| BROKER         | Leader Broker 의 Node 이름 |
| USER           | 사용자 이름                  |
| SQL            | DDL 쿼리 값                |

### V$REPLICATION
---

Replication 작동에 대한 정보를 표시합니다.

| 컬럼 이름            | 설명                                 |
| ---------------- | ---------------------------------- |
| HOSTNAME         | Replication 이 작동되는 Node 의 Hostname |
| MODE             | (서버 내부 사용)                         |
| STATE            | Node 의 상태                          |
| ADDR             | Replication Manager 의 주소           |
| PORT_NO          | Replication Manager 의 포트번호         |
| MAX_SENDER_COUNT | 생성 가능한 Sender 최대 개수                |
| RUN_SENDER_COUNT | 작동중인 Sender 최대 개수                  |

### V$REPL_SENDER
---

Replication 작동 시, Sender 의 정보를 표시합니다.

| 컬럼 이름              | 설명                                 |
| ------------------ | ---------------------------------- |
| HOSTNAME           | Replication 이 작동되는 Node 의 Hostname |
| ID                 | Sender 식별자                         |
| STATUS             | Sender Thread 의 작동상태               |
| PAYLOAD_RECV_COUNT | Sender 로부터 받은 페이로드 개수              |
| PAYLOAD_RECV_BYTES | Sender 로부터 받은 페이로드 크기 총합           |
| QUEUE_REMAIN_COUNT | Receive Queue 에 남은 버퍼의 개수          |
| NET_SEND_COUNT     | 전체 전송 횟수                           |
| NET_SEND_SIZE      | 전체 전송 크기 총합                        |
| NET_RECV_COUNT     | 전체 수신 횟수                           |
| NET_RECV_SIZE      | 전체 수신 크기 총합                        |

### V$REPL_SENDER_META
---

Replication 작동 시, Sender 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID  | Sender 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_RECEIVER
---

Replication 작동 시, Receiver 의 정보를 표시합니다.

| 컬럼 이름              | 설명                                 |
| ------------------ | ---------------------------------- |
| HOSTNAME           | Replication 이 작동되는 Node 의 Hostname |
| STATUS             | Receiver Thread 의 작동상태             |
| PAYLOAD_RECV_COUNT | Sender 로부터 받은 페이로드 개수              |
| PAYLOAD_RECV_BYTES | Sender 로부터 받은 페이로드 크기 총합           |
| QUEUE_REMAIN_COUNT | Receive Queue 에 남은 버퍼의 개수          |
| NET_SEND_COUNT     | 전체 전송 횟수                           |
| NET_SEND_SIZE      | 전체 전송 크기 총합                        |
| NET_RECV_COUNT     | 전체 수신 횟수                           |
| NET_RECV_SIZE      | 전체 수신 크기 총합                        |

### V$REPL_RECEIVER_META
---

Replication 작동 시, Receiver 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_READER
---

Replication 작동 시, Reader 의 정보를 표시합니다.

| 컬럼 이름       | 설명                                 |
| ----------- | ---------------------------------- |
| HOSTNAME    | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID   | Sender 식별자                         |
| ID          | Reader 식별자                         |
| STATUS      | Reader Thread의 작동상태                |
| FETCH_COUNT | FETCH 수행 횟수                        |

### V$REPL_READER_META
---

Replication 작동 시, Reader 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID  | Sender 식별자                         |
| ID         | Reader 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_WRITER
---

Replication 작동 시, Writer 의 정보를 표시합니다.

| 컬럼 이름        | 설명                                 |
| ------------ | ---------------------------------- |
| HOSTNAME     | Replication 이 작동되는 Node 의 Hostname |
| ID           | Writer 식별자                         |
| STATUS       | Writer Thread 의 작동상태               |
| APPEND_COUNT | APPEND 수행 횟수                       |

### V$REPL_WRITER_META
---

Replication 작동 시, Writer 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| ID         | Writer 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

## Others
### V$TABLES
---

V$로 시작하는 모든 Virtual Table 을 표시합니다.

| 컬럼 이름       | 설명           |
| ----------- | ------------ |
| NAME        | 테이블 이름       |
| TYPE        | 테이블 유형       |
| DATABASE_ID | 데이터베이스 식별자   |
| ID          | 테이블 식별자      |
| USER_ID     | 테이블을 생성한 사용자 |
| COLCOUNT    | 컬럼의 갯수       |

### V$COLUMNS
---

Virtual Table 의 컬럼 정보를 표시합니다.

| 컬럼 이름                | 설명         |
| -------------------- | ---------- |
| NAME                 | 컬럼명        |
| TYPE                 | 컬럼의 데이터 타입 |
| DATABASE_ID          | 데이터베이스 식별자 |
| ID                   | 컬럼의 식별자    |
| LENGTH               | 컬럼의 크기     |
| TABLE_ID             | 테이블 식별자    |
| FLAG                 | 비공개 데이터    |
| PART_PAGE_COUNT      | (사용되지 않음)  |
| PAGE_VALUE_COUNT     | (사용되지 않음)  |
| MINMAX_CACHE_SIZE    | (사용되지 않음)  |
| MAX_CACHE_PART_COUNT | (사용되지 않음)  |

### V$RETENTION_JOB
---

RETENTION POLICY가 적용된 테이블 정보를 표시합니다.

| 컬럼 이름         | 설명                                     |
|-------------------|------------------------------------------|
| USER_NAME         | 사용자 이름                              |
| TABLE_NAME        | 대상 TAG TABLE 이름                      |
| POLICY_NAME       | 적용되어 있는 POLICY 이름                |
| STATE             | RETENTION 상태 (RUNNING/WAITING/STOPPED) |
| LAST_DELETED_TIME | 마지막으로 삭제된 시간                   |

### V$USER_AUTH_KEYS
---

Challenge 인증에 등록된 공개 키 정보를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| KEY_ID | 키 식별자 |
| USER_ID | 사용자 식별자 |
| USER_NAME | 사용자 이름 |
| KEY_ALGO | 키 알고리즘 |
| KEY_PARAM | 키 파라미터 |
| PUBKEY | 공개 키 텍스트 |
| ACTIVATED | 키 활성화 여부 |
| VALID_AFTER | 키 유효 시작일 |
| VALID_BEFORE | 키 유효 종료일 |
| COMMENT | 키 설명 |
