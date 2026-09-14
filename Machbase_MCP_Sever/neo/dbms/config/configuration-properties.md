# 설정 프로퍼티 사전

`$MACHBASE_HOME/conf/machbase.conf` 파일에서 설정하는 Standard Edition 주요 프로퍼티
사전입니다. 별도 표시가 없는 한 서버 재시작이 필요합니다.

## 서버 기본 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `PORT_NO` | 5656 | 1024~65535 | 클라이언트 TCP/IP 연결 포트 |
| `BIND_IP_ADDRESS` | 0.0.0.0 | - | 클라이언트 리스너 바인드 IP. `0.0.0.0`은 모든 인터페이스 |
| `GRANT_REMOTE_ACCESS` | 1 | 0~1 | 원격 접속 허용 여부. 0이면 로컬만 허용 |
| `MAX_SESSION_COUNT` | 4096 | 64~2^64-1 | 동시 세션 최대 개수 |
| `MAX_STMT_COUNT_PER_SESSION` | 1024 | 512~2^32-1 | 세션당 최대 statement 수 |
| `SESSION_IDLE_TIMEOUT_SEC` | 0 | 0~2^64-1 | 세션 유휴 타임아웃(초). 0이면 비활성 |
| `SESSION_QUERY_TIMEOUT_SEC` | 0 | 0~2^64-1 | 쿼리 실행 타임아웃(초). 0이면 비활성 |
| `UNIX_PATH` | machbase-unix | - | Unix domain socket 파일 이름 |
| `DBS_PATH` | ?/dbs | - | 데이터베이스 파일 저장 경로(`?`는 `$MACHBASE_HOME`) |
| `PID_PATH` | ?/conf | - | PID 파일 저장 경로 |

## CPU / 스레드 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `CPU_COUNT` | 1 | 0~2^32-1 | 사용할 CPU 수. 0이면 전체 사용 |
| `CPU_PARALLEL` | 1 | 1~2^32-1 | CPU당 병렬 스레드 수 |
| `CPU_AFFINITY_BEGIN_ID` | 0 | 0~2^32-1 | CPU 친화도 시작 번호 |
| `CPU_AFFINITY_COUNT` | 0 | 0~2^32-1 | CPU 친화도 사용 수. 0이면 전체 |
| `DISK_IO_THREAD_COUNT` | 3 | 1~2^32-1 | 디스크 I/O 스레드 수 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 0~2^32-1 | 인덱스 빌드 스레드 수. 0이면 인덱스 생성 안 함 |
| `INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT` | 3 | 1~1024 | LSM 인덱스 병합 스레드 수 |
| `INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT` | 1 | 1~1024 | LSM 인덱스 불필요 파일 삭제 스레드 수 |
| `QUERY_PARALLEL_FACTOR` | 0 | 0~100 | 병렬 질의 실행 스레드 수. Standard 기본값 0, Cluster 기본값 4 |

## 메모리 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `PROCESS_MAX_SIZE` | 8GB | 1GB~2^64-1 | 서버 프로세스 최대 메모리(바이트). 배포 샘플은 `16GB`로 설정되어 있을 수 있음 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 256MB~2^64-1 | 로그 테이블 입력 버퍼 상한. 전체 메모리 예산 안에서 조정 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE` | 100MB | 1MB~2^64-1 | 서버 시작 시 사전 확보 메모리 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE` | 2MB | 1MB~2^64-1 | 컬럼 파티션 메모리 블록 크기 |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE` | 2MB | 1MB~2^32-1 | 데이터 일관성/복구용 double write 파일 초기 크기 |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE` | 1MB | 1MB~2^32-1 | double write 파일 확장 크기 |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | 2GB | 0~2^64-1 | 페이지 캐시 최대 크기(바이트) |
| `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` | 2GB | 0~2^64-1 | Volatile/Lookup 테이블 전체 메모리 한도 |
| `MAX_QPX_MEM` | 1GB | 1MB~2^64-1 | GROUP BY/ORDER BY 등 쿼리 처리기 최대 메모리 |
| `MEMORY_ROW_TEMP_TABLE_PAGESIZE` | 32768 | 8KB~2^32-1 | Volatile/Lookup 임시 테이블 페이지 크기(바이트) |

## 디스크 I/O 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `DISK_BUFFER_COUNT` | 16 | 1~2^32-1 | 디스크 I/O 버퍼 수 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 0~1 | 쓰기 Direct I/O 사용 여부. ZFS 등 미지원 파일시스템은 0으로 설정 |
| `DISK_TABLESPACE_DIRECT_IO_READ` | 0 | 0~1 | 읽기 Direct I/O 사용 여부 |
| `DISK_TABLESPACE_DIRECT_IO_FSYNC` | 0 | 0~1 | Direct I/O 시 fsync 사용 여부 |
| `DISK_TABLESPACE_SYNCHRONOUS` | 1 | 0~3 | 동기화 정책. 0=OFF, 1=NORMAL, 2=FULL, 3=EXTRA |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | 0~2^32-1 | 파티션 파일 디스크 반영 주기(초) |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE` | 0 | 0~1 | 컬럼 파티션이 가득 찼을 때만 flush할지 여부 |
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | 테이블 체크포인트 주기(초) |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | 인덱스 체크포인트 주기(초) |
| `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE` | 1 | 0~1 | LOG 시각 역전 시 1=직전 시각+1ns로 보정, 0=입력 거부 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT` | 80 | 0~100 | 메모리 사용량 임계값(%). 초과 시 입력 속도 저하 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC` | 1 | 0~2^32-1 | 임계값 초과 시 레코드당 대기 시간(ms) |

LOG의 `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1`은 명시한 과거 시각을 그대로
저장한다는 뜻이 아닙니다.
직전 `_ARRIVAL_TIME`보다 작은 값은 보정됩니다. 같은 시각은 이 역전 조건에 해당하지
않으므로 모든 행의 시각이 고유해지는 것도 아닙니다.
이관 시에는 시간 모델의 정렬·대상 상태를
함께 확인하세요.

## 인덱스 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `DEFAULT_LSM_MAX_LEVEL` | 2 | 0~3 | LSM 인덱스 기본 최대 레벨 |
| `INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD` | 100000 | 1~2^32-1 | 인덱스 빌드 시작 기준 미인덱싱 레코드 수 |
| `INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX` | 3 | 1~2^32-1 | 인덱스당 최대 flush 요청 수 |
| `INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT` | 70 | 0~100 | LSM 인덱스 생성 최대 메모리 사용 비율(%) |
| `DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH` | 0 | 0~1 | 종료 시 인덱스를 디스크에 모두 반영할지 여부 |
| `DISK_COLUMNAR_INDEX_FDCACHE_COUNT` | 0 | 0~2^32-1 | 오픈 인덱스 파티션 파일 디스크립터 수 |
| `DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT` | 0 | 0~2^32-1 | 오픈 컬럼 파일 디스크립터 수 |
| `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` | 100MB | 0~2^64-1 | `_ARRIVAL_TIME` 컬럼 MINMAX 캐시 크기(바이트) |

## TAG 테이블 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `TAG_CACHE_ENABLE` | 31 | 0~31 | TAG 캐시 사용 범위(비트 OR). 0=사용 안 함, 1=map, 2=row, 4=data file, 8=varchar file, 16=delete vector |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | 32KB~2^64-1 | TAG 캐시 풀 1개당 최대 메모리(바이트) |
| `TAG_CACHE_POOL_COUNT` | 1 | 1~128 | TAG 캐시 풀 개수. 전체 한도 = `TAG_CACHE_MAX_MEMORY_SIZE × TAG_CACHE_POOL_COUNT` |
| `TAG_MEMORY_INDEX_TYPE` | 1 | 0~1 | 메모리 인덱스 유형. 0=RBTree, 1=BTree |
| `TAG_MEMORY_INDEX_PANOUT` | 255 | 127~65536 | B-Tree 인덱스 차수. `TAG_MEMORY_INDEX_TYPE=1`일 때 적용 |
| `TAGDATA_AUTO_META_INSERT` | 2 | 0~2 | TAG_NAME 없을 때 처리. 0=실패, 1=이름만 삽입, 2=메타데이터 포함 삽입 |
| `TAG_TABLE_META_MAX_SIZE` | 524288000 | 1MB~2^32-1 | TAGDATA 테이블 메타데이터 최대 메모리(바이트) |
| `TAG_PARTITION_COUNT` | 4 | 1~1024 | Tag 테이블 Key Value 파티션 수 |
| `TAG_DATA_PART_SIZE` | 16MB | 1MB~1GB | Tag 데이터 파티션 크기(바이트) |
| `ROLLUP_FETCH_COUNT_LIMIT` | 3000000 | 0~2^32-1 | 롤업 스레드 1회 패치 데이터 수. 0이면 무제한 |

## 보안 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `ENABLE_CASE_SENSITIVE_PASSWORD` | 0 | 0~1 | 비밀번호 대소문자 구분 여부. 0이면 대문자로 변환 |

## 세션 / 쿼리 설정

`TABLE_SCAN_DIRECTION`은 TAG 전용 설정이 아닙니다. LOG 등 스캔 방향을 사용하는
쿼리에도 영향을 줄 수 있으며, 최종 출력 정렬을 보장하는 설정도 아닙니다.
출력 순서는 ORDER BY로 지정하고 실제 접근 경로는 EXPLAIN으로 확인하세요.

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `TABLE_SCAN_DIRECTION` | 0 | -1~1 | -1=역방향, 0=테이블 유형 기본값, 1=정방향 |
| `DDL_LOCK_TIMEOUT` | 0 | 0~1000000 | Standard Edition DDL 잠금 대기 시간(초). 0이면 즉시 오류 반환 |
| `SHOW_HIDDEN_COLS` | 0 | 0~1 | `SELECT *`에서 `_ARRIVAL_TIME` 컬럼 표시 여부 |
| `DURATION_BEGIN` | 0 | 0~2^32-1 | `DURATION` 미지정 SELECT의 기본 시작 오프셋(초) |
| `DURATION_GAP` | 0 | 0~2^31-1 | `DURATION` 미지정 SELECT의 기본 기간(초) |
| `LOOKUP_APPEND_UPDATE_ON_DUPKEY` | 0 | 0~1 | Lookup 테이블 Append 시 중복 키 처리. 0=실패, 1=UPDATE |
| `LIN_HASH_BIT_SIZE` | 7 | 1~31 | 내부 선형 해시 초기 버킷 비트 수 |

`machbase.conf`의 `DDL_LOCK_TIMEOUT`은 서버를 재시작한 뒤 새 세션에 복사됩니다. 현재 세션의
값은 `ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds`로 변경하고 `V$SESSION`에서 확인합니다.
Cluster Edition은 이 프로퍼티를 제공하지 않습니다.

## TRANSACTION 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `TRANSACTION_BUSY_TIMEOUT_MS` | 30000 | -1~2147483647 | 재시도 가능한 TRANSACTION 잠금 충돌의 대기 시간(ms). -1은 취소·해제까지 대기, 0은 즉시 반환 |
| `TRANSACTION_SYNCHRONOUS` | 2 | 1~2 | TRANSACTION 테이블 트랜잭션 내구성 수준. 1=NORMAL, 2=FULL |
| `TRANSACTION_JOURNAL_MODE` | 4 | 0~4 | TRANSACTION 저널 모드. 0=DELETE, 4=WAL |

새 세션은 서버의 TRANSACTION_BUSY_TIMEOUT_MS를 복사하며 현재 연결은 ALTER SESSION으로
변경할 수 있습니다. 이 값은 모든 busy 오류에 대한 최소 대기 시간을 보장하지 않습니다.
WAL에서 오래된 읽기 스냅샷을 쓰기로 전환할 때의 충돌은 -1이어도 즉시 반환될 수 있습니다.
이 경우 같은 문장을 반복하지 말고 ROLLBACK 후 새 트랜잭션에서 읽기와 판단부터
다시 수행하세요. 두 연결 실습에서
일시적인 쓰기 잠금과 스냅샷 충돌을 비교할 수 있습니다.

## 로그 / 진단 설정

| 프로퍼티 | 기본값 | 범위 | 설명 |
|----------|--------|------|------|
| `TRACE_LOG_LEVEL` | 277 | 0~2^32-1 | 트레이스 로그 상세 수준. 값이 높을수록 상세 |
| `TRACE_LOGFILE_PATH` | ?/trc | - | 트레이스 로그 파일 저장 경로 |
| `TRACE_LOGFILE_SIZE` | 10MB | 1MB~2^32-1 | 트레이스 로그 파일 최대 크기(바이트) |
| `TRACE_LOGFILE_COUNT` | 1000 | 1~2^32-1 | 트레이스 로그 파일 최대 개수 |
| `DUMP_TRACE_INFO` | 300 | 0~2^32-1 | DBMS 상태를 trc에 기록하는 주기(초). 0이면 비활성 |
| `DUMP_APPEND_ERROR` | 0 | 0~1 | Append API 오류 시 trc에 기록 여부. 테스트 목적으로만 사용 권장 |
| `FEEDBACK_APPEND_ERROR` | 1 | 0~1 | Append 오류 데이터를 클라이언트에 전송할지 여부 |
| `GEN_CORE_FILE` | 1 | 0~1 | 비정상 종료 시 core 파일 생성 여부 |
| `GEN_CALLSTACK_FOR_ABORT_ERROR` | 0 | 0~1 | 비정상 종료 시 call stack 기록 여부 |

## 프로퍼티 조회 예시

```sql
-- 현재 적용된 프로퍼티 값 전체 조회
SELECT name, value, type FROM v$property ORDER BY name;

-- 특정 프로퍼티 상세 조회
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'MAX_SESSION_COUNT';
```

동적 변경 가능한 프로퍼티는 서버 재시작 없이 `ALTER SYSTEM SET`으로 변경할 수 있습니다.

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET SESSION_QUERY_TIMEOUT_SEC = 30;
```
