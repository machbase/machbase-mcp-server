# SYSTEM/SESSION/ALTER SYSTEM

`ALTER SYSTEM`은 서버 전역 자원을 관리하는 구문입니다. `ALTER SESSION`은 현재 세션에만 적용되는 파라미터를 설정합니다.

> **권한**: `ALTER SYSTEM` 명령은 `SYS` 계정 또는 `GRANT ALTER ON DATABASE database_name TO user_name;`으로 권한을 부여받은 사용자만 실행할 수 있습니다.

---

## ALTER SYSTEM

### 명령어 목록

| 명령어 | 설명 |
|--------|------|
| `KILL SESSION n` | 지정한 세션 강제 종료 |
| `CANCEL SESSION n` | 세션은 유지하고 실행 중인 쿼리만 취소 |
| `CHECKPOINT` | 메모리 버퍼를 디스크에 즉시 동기화 |
| `FREEZE` | 모든 DML 일시 중단 (백업 준비용) |
| `UNFREEZE` | FREEZE로 중단된 DML 재개 |
| `FLUSH AGER` | Ager 스레드를 즉시 실행하여 만료 데이터 정리 |
| `FLUSH SYS_STAT` | 쿼리 최적화기용 시스템 통계 정보 갱신 |
| `FLUSH PVO_CACHE` | PVO Statement 캐시 초기화 |
| `FLUSH PAGE_CACHE` | OS 페이지 캐시 강제 해제 |
| `FLUSH TAG_CACHE` | TAG 테이블 메타데이터 캐시 초기화 |
| `INSTALL LICENSE` | 기본 경로에 라이선스 파일 설치 |
| `INSTALL LICENSE = 'path'` | 지정 경로에 라이선스 파일 설치 |
| `CHECK DISK_USAGE` | 로그 테이블 디스크 사용량 재계산 |
| `SET property = value` | 시스템 속성 동적 변경 |

---

### KILL SESSION / CANCEL SESSION

```sql
alter_system_kill_session_stmt   ::= 'ALTER SYSTEM KILL SESSION'   session_id
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' session_id
```

```sql
-- 현재 세션 목록 확인
SELECT id, user_id, client_type FROM v$session;

-- 세션 강제 종료 (접속 해제, 트랜잭션 롤백)
ALTER SYSTEM KILL SESSION 12;

-- 실행 중인 쿼리만 취소 (접속 유지)
ALTER SYSTEM CANCEL SESSION 6;
```

- `KILL SESSION`: SYS 사용자만 실행 가능. 대상 세션 즉시 종료.
- `CANCEL SESSION`: 같은 사용자 또는 SYS만 실행 가능. 세션은 유지되고 현재 실행 중인 SQL만 중단.

---

### CHECKPOINT

```sql
alter_system_checkpoint_stmt ::= 'ALTER SYSTEM CHECKPOINT'
```

메모리에 버퍼링된 데이터를 디스크에 즉시 동기화합니다.

```sql
ALTER SYSTEM CHECKPOINT;
```

---

### FREEZE / UNFREEZE

```sql
alter_system_freeze_stmt   ::= 'ALTER SYSTEM FREEZE'
alter_system_unfreeze_stmt ::= 'ALTER SYSTEM UNFREEZE'
```

백업 준비 등 일관성이 필요할 때 모든 DML을 일시 중단합니다.

```sql
ALTER SYSTEM FREEZE;
-- (백업 또는 점검 수행)
ALTER SYSTEM UNFREEZE;
```

---

### FLUSH

```sql
alter_system_flush_stmt ::=
    'ALTER SYSTEM FLUSH'
    ( 'AGER'
    | 'SYS_STAT'
    | 'PVO_CACHE'
    | 'PAGE_CACHE'
    | 'TAG_CACHE' )
```

```sql
-- Ager 즉시 실행 (만료 데이터 정리)
ALTER SYSTEM FLUSH AGER;

-- 쿼리 최적화기 통계 갱신
ALTER SYSTEM FLUSH SYS_STAT;

-- PVO Statement 캐시 초기화
ALTER SYSTEM FLUSH PVO_CACHE;

-- OS 페이지 캐시 강제 해제
ALTER SYSTEM FLUSH PAGE_CACHE;

-- TAG 메타데이터 캐시 초기화
ALTER SYSTEM FLUSH TAG_CACHE;
```

---

### INSTALL LICENSE

```sql
-- 기본 경로 ($MACHBASE_HOME/conf/license.dat)
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'

-- 지정 경로
alter_system_install_license_path_stmt ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

```sql
-- 기본 경로에서 설치
ALTER SYSTEM INSTALL LICENSE;

-- 지정 경로에서 설치
ALTER SYSTEM INSTALL LICENSE = '/tmp/new_license.dat';
```

---

### CHECK DISK_USAGE

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

`V$STORAGE`의 `DC_TABLE_FILE_SIZE` 값을 파일 시스템에서 재계산합니다. 프로세스 장애나 정전 후 사용량이 부정확할 때 사용합니다.

```sql
ALTER SYSTEM CHECK DISK_USAGE;
```

---

### SET (시스템 속성 동적 변경)

```sql
alter_system_set_stmt ::=
    'ALTER SYSTEM SET' property_name '=' value_expr

value_expr ::=
    value
  | property_name '|'  number   -- 비트 OR (플래그 추가)
  | property_name '&' '~' number -- 비트 AND NOT (플래그 제거)
```

변경 가능한 속성 목록:

| 속성 | 설명 |
|------|------|
| `QUERY_PARALLEL_FACTOR` | 쿼리 병렬 처리 스레드 수 |
| `DEFAULT_DATE_FORMAT` | 기본 날짜 형식 (예: `'YYYY-MM-DD HH24:MI:SS'`) |
| `TRACE_LOG_LEVEL` | 트레이스 로그 레벨 (비트 플래그) |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | 디스크 컬럼형 페이지 캐시 최대 크기 |
| `MAX_SESSION_COUNT` | 최대 세션 수 |
| `SESSION_IDLE_TIMEOUT_SEC` | 세션 유휴 타임아웃 (초) |
| `PROCESS_MAX_SIZE` | 프로세스 최대 메모리 크기 |
| `TAG_CACHE_MAX_MEMORY_SIZE` | TAG 캐시 최대 메모리 크기 |
| `PVO_CACHE_ENABLE` | PVO 캐시 활성화 (0/1) |
| `PVO_CACHE_MAX_MEMORY_SIZE` | PVO 캐시 최대 메모리 크기 |

```sql
-- 직접 값 설정
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
-- 변경 전 현재값 확인
SELECT NAME, VALUE, MIN, MAX
  FROM V$PROPERTY
 WHERE NAME = 'MAX_SESSION_COUNT';

-- 비트 플래그 추가 (OR)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;

-- 비트 플래그 제거 (AND NOT)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;

-- 16진수로 설정
ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000003;
```

---

## ALTER SESSION

세션 단위 파라미터를 변경합니다.

```sql
alter_session_stmt ::=
    'ALTER SESSION SET' session_property_name '=' value
```

### SET SQL_LOGGING

```sql
ALTER SESSION SET SQL_LOGGING = flag
-- flag: 비트 OR 조합
-- 0x1: 파싱·검증·최적화 단계 로그
-- 0x2: DDL 수행 결과 로그
```

```sql
ALTER SESSION SET SQL_LOGGING = 3;  -- 파싱 로그 + DDL 로그
ALTER SESSION SET SQL_LOGGING = 0;  -- 로깅 비활성화
```

### SET DEFAULT_DATE_FORMAT

```sql
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYYMMDD';
```

### SET SHOW_HIDDEN_COLS

`SELECT *` 시 숨김 컬럼(`_arrival_time`)을 함께 출력할지 설정합니다.

```sql
ALTER SESSION SET SHOW_HIDDEN_COLS = 1;  -- 숨김 컬럼 표시
ALTER SESSION SET SHOW_HIDDEN_COLS = 0;  -- 숨김 컬럼 숨김 (기본값)
```

### SET FEEDBACK_APPEND_ERROR

Append API에서 발생한 에러 메시지를 클라이언트로 전달할지 설정합니다.

```sql
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 1;  -- 에러 메시지 전송
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 0;  -- 에러 메시지 미전송 (기본값)
```

### SET MAX_QPX_MEM

단일 SQL이 GROUP BY, DISTINCT, ORDER BY 연산 시 사용할 수 있는 최대 메모리 (바이트 단위)입니다.

```sql
ALTER SESSION SET MAX_QPX_MEM = 1073741824;  -- 1GB
```

### SET DDL_LOCK_TIMEOUT

Standard Edition에서 충돌한 DDL 잠금을 기다릴 시간을 초 단위로 지정합니다. 기본값은 `0`,
설정 범위는 `0`~`1000000`입니다. `0`이면 기다리지 않고 즉시
`ERR-02031: Resource busy (<object>)`를 반환합니다.

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;  -- 최대 10초 대기
```

실행 중인 DDL의 대기 시간은 변경되지 않으며 새 값은 다음 DDL부터 적용됩니다. 현재 세션별
설정값은 `V$SESSION.DDL_LOCK_TIMEOUT`에서 확인합니다.

```sql
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

충돌 범위와 오류 처리 방법은 DDL 동시성과 잠금을 참고하십시오.

### SET SESSION_IDLE_TIMEOUT_SEC

세션 유휴 상태 연결 유지 최대 시간 (초 단위)입니다.

```sql
ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC = 300;  -- 5분
```

### SET QUERY_TIMEOUT

쿼리 실행 대기 최대 시간 (초 단위)입니다. 초과 시 쿼리가 자동 중단됩니다.

```sql
ALTER SESSION SET QUERY_TIMEOUT = 60;  -- 60초
```

---

## 관련 뷰

| 뷰 | 설명 |
|----|------|
| `v$session` | 현재 접속 세션 목록 및 세션별 파라미터 |
| `v$storage` | 디스크 사용량 정보 (`DC_TABLE_FILE_SIZE` 등) |
| `v$license_info` | 설치된 라이선스 정보 |
| `v$property` | 시스템 속성 및 현재 값 |

```sql
-- 세션 목록 조회
SELECT id, user_id, client_type, login_time FROM v$session;

-- 시스템 속성 확인
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';
```

---

## 관련 문서

- ALTER SYSTEM 운영 가이드 - 상세 운영 절차 및 각 명령별 동작 설명
- GRANT/REVOKE - ALTER SYSTEM 권한 부여
