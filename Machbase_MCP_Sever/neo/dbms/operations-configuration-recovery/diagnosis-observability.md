# 관측과 진단

운영 진단은 재현 시각과 증상을 기록한 뒤 서버 상태, 세션·문장, 스토리지·메모리,
관련 로그를 같은 시간축에서 확인합니다. `M$` 메타데이터 테이블은 스키마를, `V$` virtual
테이블은 현재 상태를 제공합니다.

## 진단과 로그

1. 문제 시작·종료 시각과 클라이언트 정보를 기록합니다.
2. `machadmin -e`로 서버 응답을 확인합니다.
3. `V$SESSION`과 `V$STMT`에서 관련 작업을 찾습니다.
4. 스토리지·메모리·ROLLUP 등 증상에 맞는 가상 테이블을 확인합니다.
5. 같은 시각의 서버·클라이언트·loader 로그를 비교합니다.
6. 변경 전 현재 설정 속성과 기준값을 저장합니다.

## 트레이스 로그 설정

trace level과 파일 크기·보존 설정은 장애 분석에 필요한 범위만 조정합니다. 상세 설정 속성은
설정 레퍼런스에서 현재 릴리스의
이름, 허용값, 재시작 필요 여부를 확인합니다. 민감 SQL과 데이터가 기록될 수 있으므로 로그
접근 권한과 보존 기간을 설정합니다.

## 서버 로그

기본 trace 디렉터리는 `$MACHBASE_HOME/trc`입니다. 파일명이 고정돼 있다고 가정하지 말고
현재 디렉터리와 설정값을 확인합니다.

```bash
ls -lh "$MACHBASE_HOME/trc"
tail -n 200 "$MACHBASE_HOME/trc/machbase.trc"
```

오류 문자열만 세는 대신 최초 오류, 직전 경고, 서버 시작·종료, 체크포인트·스토리지 사건을
시간 순서로 봅니다. 로그 파일을 수동 명령으로 일괄 삭제하지 않습니다.

## machsql 로그

`machsql.history`에는 자격 증명이나 민감 SQL이 남을 수 있습니다. 운영 계정의 history
권한을 제한하고, 장애 공유 전에 내용을 검토합니다. 재현 SQL은 대상 데이터베이스와
실행 시각, 결과·오류를 함께 보존합니다.

## machloader 로그

대량 적재에서는 프로세스 종료 코드, 요약, 로그, 오류 행 파일을 함께 확인합니다.

- 스키마와 입력 컬럼 수·순서
- 구분자, 인용 문자, 인코딩
- NULL과 DATETIME 형식
- 최초 실패 행과 반복되는 오류 코드
- 최종 성공·실패 건수

오류 행 파일을 그대로 전체 재실행하지 말고 원인을 수정한 표본으로 검증한 뒤 실패 행만
재처리합니다.

## 메타데이터 테이블

`M$SYS_TABLES`, `M$SYS_COLUMNS`, `M$SYS_INDEXES` 등으로 현재 데이터베이스의 스키마를
확인합니다. 이름만으로 조인하지 말고 데이터베이스 ID, 소유자 ID, object ID를 포함합니다.
reserved object 이름과 내부 테이블 구조에 애플리케이션이 의존하지 않도록 합니다.

## 가상 테이블

먼저 현재 릴리스에서 실제 컬럼을 확인합니다.

```sql
SELECT * FROM V$SESSION LIMIT 1;
SELECT * FROM V$STMT LIMIT 1;
SELECT * FROM V$PROPERTY LIMIT 1;
SELECT * FROM V$STORAGE_USAGE LIMIT 1;
SELECT * FROM V$SYSMEM LIMIT 1;
SELECT * FROM V$ROLLUP LIMIT 1;
SELECT * FROM V$LICENSE_INFO LIMIT 1;
```

전체 목록과 컬럼 의미는
system 카탈로그을 참고합니다.

## 모니터링과 용량 관리

고정 임계값보다 정상 기준값, 증가율, 업무 최대 부하, 복구 여유를 기준으로 경보를
설정합니다. 파일 시스템 사용량과 데이터베이스 스토리지 사용량을 함께 보고 백업·내보내기가
사용하는 별도 공간도 포함합니다.

## 서버 상태

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

프로세스 존재만으로 정상이라고 판단하지 않습니다. 네이티브 연결과 가벼운 SQL,
최근 서버 로그까지 확인합니다.

## 세션과 실행 SQL

```sql
SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;

SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;
```

장시간 실행이 곧 오류는 아닙니다. 업무 종류, 처리 행, 클라이언트 시간 초과, I/O·CPU 상태를
함께 확인한 뒤 cancel·kill 여부를 결정합니다.

## 디스크 용량

```bash
df -h "$MACHBASE_HOME"
du -sh "$MACHBASE_HOME/dbs"
```

별도 `DBS_PATH`를 사용하면 실제 경로를 확인합니다. 내부 파티션 파일을 직접 수정하거나
삭제하지 않습니다.

## 메모리

OS available 메모리·swap과 `V$SYSMEM`, 캐시·쿼리 동시성을 함께 비교합니다. manager별
내부 이름을 자동화의 고정 기준으로 사용하지 않습니다.

## 백업 검증

백업 명령 성공만 확인하지 않습니다. 경로·크기·완료 상태를 기록하고 격리 환경에서
마운트 또는 복원 후 주요 테이블, 행 수, 시간 범위, 표본 쿼리를 검증합니다.

## 장애 자료 수집

- 릴리스와 에디션
- 문제 시각·시간대
- 재현 명령과 데이터베이스·사용자
- 서버·클라이언트·loader 로그
- 관련 가상 테이블 결과
- OS CPU·I/O·메모리·디스크
- 최근 스키마·설정 속성·배포 변경
- 이미 시도한 조치와 결과

자격 증명, AUTH KEY, 개인정보와 원문 민감 데이터는 지원 자료에서 제거합니다.
