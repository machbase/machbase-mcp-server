# 서버와 연결 문제

연결 문제는 서버 시작, TCP 연결, 사용자 인증 순서로 분리해 확인합니다.

## 서버가 시작되지 않을 때

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

다음을 차례로 확인합니다.

1. 설정한 포트를 다른 프로세스가 사용 중인지
2. Machbase 서버 OS 계정이 설치·데이터·로그 경로를 읽고 쓸 수 있는지
3. 파일 시스템의 공간과 inode가 충분한지
4. 라이선스가 설치되어 있고 유효한지 (`machadmin -f`)
5. 이전 프로세스와 lock 파일이 남은 원인이 무엇인지

원인을 확인하지 않은 강제 종료나 lock 파일 삭제는 피하십시오. 정상 종료가 불가능하면 로그와
프로세스 상태를 보존한 뒤 승인된 복구 절차를 사용합니다.

## 연결할 수 없을 때

서버 호스트에서는 먼저 로컬 연결을 시험합니다.

```bash
machadmin -e
machsql -s 127.0.0.1 -P 5656 -u app_user
```

로컬은 성공하고 원격만 실패하면 다음을 확인합니다.

- 클라이언트가 사용하는 주소와 포트
- `GRANT_REMOTE_ACCESS`, `BIND_IP_ADDRESS`의 현재 값
- 운영체제·클라우드 방화벽과 중간 네트워크 경로
- `MAX_SESSION_COUNT` 도달 여부와 닫히지 않은 세션

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS', 'MAX_SESSION_COUNT');

SELECT ID, USER_NAME, CLOSED
  FROM V$SESSION
 ORDER BY ID;
```

리스너 관련 설정은 서버 시작 시 적용되므로 설정 파일을 바꾼 뒤 유지보수 재시작과 원격·로컬
접속 검증을 함께 수행합니다. 방화벽 명령은 배포 운영체제의 공식 문서을 따릅니다.

## 인증이 실패할 때

먼저 연결에서 선택한 인증 방식을 확인합니다. `AUTH_MODE`는 서버 `V$PROPERTY`가 아니라
클라이언트 연결 옵션입니다.

비밀번호 인증은 사용자명, 비밀번호 정책과 만료일을 확인합니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

AUTH KEY 인증은 등록 키와 클라이언트 옵션을 확인합니다.

```sql
SELECT KEY_ID, USER_NAME, KEY_ALGO, KEY_PARAM, ACTIVATED, VALID_BEFORE
  FROM V$USER_AUTH_KEYS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY KEY_ID;
```

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user.key
```

개인키 파일이 존재하고 클라이언트 프로세스가 읽을 수 있는지, 서버의 공개키와 짝이 맞는지,
키가 활성·유효 상태인지 확인합니다. 계정 잠금 해제나 `CREATE AUTH KEY` 같은 현행 문법에 없는
구문을 사용하지 마십시오. 등록과 교체는 AUTH KEY 인증을
따릅니다.
