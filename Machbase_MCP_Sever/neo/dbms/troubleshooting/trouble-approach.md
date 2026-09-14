# 문제 해결 접근법

문제를 재현하기 전에 상태와 증거를 보존하고, 가장 작은 범위부터 원인을 좁힙니다.

## 5단계 문제 해결 절차

1. 실패 시각, 실행한 명령, 전체 오류 메시지와 `ERR-` 코드를 기록합니다.
2. `machadmin -e`와 연결 시험으로 서버·네트워크·인증 중 실패 단계를 구분합니다.
3. 같은 시각의 서버 로그와 세션·문장 상태를 확인합니다.
4. 한 번에 한 원인만 수정하고 같은 입력으로 재검증합니다.
5. 원인, 조치, 검증 결과와 재발 방지 항목을 남깁니다.

## 증상 확인

| 증상 | 첫 확인 |
|---|---|
| 서버 응답 없음 | `machadmin -e`, 프로세스와 포트, 서버 로그 |
| 연결 거부 | 서버 상태, 수신 주소, 방화벽, 포트 |
| 인증 실패 | 사용자, 인증 방식, 만료 상태, AUTH KEY 상태 |
| SQL 실패 | 전체 SQL, 대상 데이터베이스와 객체, 정확한 오류 코드 |
| 느린 쿼리 | 실행 계획, 시간 범위, 스캔 행 수, 동시 부하 |
| 적재 중단 | 성공·실패 행 수, bad/log 파일, 마지막 성공 위치 |

문제를 해결하기 전에 서버 재시작이나 설정 변경부터 수행하면 최초 원인의 증거를 잃을 수
있습니다.

## 진단 명령어 모음

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

```sql
SELECT * FROM V$VERSION;
SELECT ID, USER_NAME, CLOSED FROM V$SESSION ORDER BY ID;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
SELECT * FROM V$STORAGE_USAGE;
SELECT NAME, VALUE FROM V$PROPERTY ORDER BY NAME;
```

운영 환경에서는 결과에 SQL 본문, 사용자명, 경로 등 민감한 정보가 포함될 수 있으므로 공유
전에 검토하십시오.

## 로그 확인

기본 서버 로그 위치는 `$MACHBASE_HOME/trc/machbase.trc`입니다. 실제 경로와 순환 설정은
`V$PROPERTY`와 설치 설정을 기준으로 확인합니다.

```bash
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
rg -n 'ERR-|ERROR|WARN' "$MACHBASE_HOME/trc/machbase.trc"
```

로그 레벨이나 파일 수를 바꾸기 전에 현재 `TRACE_LOG_LEVEL`, `TRACE_LOGFILE_SIZE`,
`TRACE_LOGFILE_COUNT`, `TRACE_LOGFILE_PATH`를 조회하십시오. 장애 중 과도한 상세 로그는
디스크와 성능에 영향을 줄 수 있습니다.

## 오류 코드로 원인 찾기

정확한 오류 코드를 기록한 뒤
오류 코드 사전에서 현재 정의를 확인하십시오.
코드가 사전에 없으면 전체 메시지, 서버 빌드, 재현 SQL과 로그 시각을 함께 수집합니다.
