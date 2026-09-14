# AUTH KEY 인증

AUTH KEY 인증은 서버에 공개키를 등록하고 클라이언트가 보관한 개인키로 서버의 인증 요청값
(challenge)에 서명하는 방식입니다. 비밀번호 대신 개인키를 사용할 수 있지만, 개인키
보호와 교체 절차는 별도로 운영해야 합니다. 연결마다 `AUTH_MODE=PASSWORD` 또는
`AUTH_MODE=CHALLENGE`를 선택합니다.

## 준비 사항

1. 애플리케이션 전용 사용자를 만듭니다.
2. 클라이언트 호스트에서 키 쌍을 생성합니다.
3. 공개키만 서버에 등록합니다.
4. 개인키 파일을 클라이언트의 비밀 저장소에 보관합니다.
5. CHALLENGE 연결을 확인한 뒤 키 만료와 교체 일정을 기록합니다.

지원되는 키와 AUTH KEY SQL의 전체 문법은
USER/AUTH 문법을
참고하십시오.

## 사용자 AUTH KEY 관리

등록 상태는 `V$USER_AUTH_KEYS`에서 확인합니다.

```sql
SELECT KEY_ID, USER_NAME, KEY_ALGO, KEY_PARAM,
       ACTIVATED, VALID_AFTER, VALID_BEFORE, COMMENT
  FROM V$USER_AUTH_KEYS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY KEY_ID;
```

`PUBKEY`에는 공개키 본문이 있으므로 일반 운영 보고서에는 포함하지 않는 것이 좋습니다.

### CREATE USER ... WITH AUTH KEY

사용자를 만들면서 공개키를 등록할 수 있습니다. 아래 공개키 문자열은 실제 PEM의 줄바꿈을
`\n`으로 바꾼 값으로 교체합니다.

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial application key'
);
```

비밀번호도 비상 복구 경로로 관리될 수 있으므로 별도의 강한 값과 정책을 사용합니다.

### ALTER USER ... ADD AUTH KEY

기존 사용자에는 다음처럼 새 공개키를 추가합니다.

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='replacement key'
);
```

등록 후 새 `KEY_ID`, 알고리즘, 활성 상태, 만료일을 조회합니다.

### AUTH KEY 활성화와 비활성화

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

비활성화는 키 메타데이터를 보존하면서 인증을 차단합니다. 운영 키를 비활성화하기 전에는 다른
인증 경로가 실제로 동작하는지 확인하십시오.

### AUTH KEY 만료 변경

```sql
ALTER USER app_user
  ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

만료일을 연장하기 전에 키 사용 주체와 보관 상태를 다시 확인합니다. 유효기간을 연장해도
키 자체가 바뀌지는 않으므로 교체 주기는 별도로 관리합니다.

### AUTH KEY 삭제

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

삭제는 되돌릴 수 없습니다. 새 키 접속 성공과 이전 키 비활성화 상태를 확인한 뒤 삭제합니다.
사용자를 삭제하면 그 사용자의 AUTH KEY도 함께 정리됩니다.

## 키 롤오버

1. 새 키 쌍을 생성합니다.
2. 새 공개키를 `ADD AUTH KEY`로 등록합니다.
3. 새 개인키로 CHALLENGE 연결을 검증합니다.
4. 이전 키를 비활성화하고 이전 키의 접속 실패를 검증합니다.
5. 관찰 기간이 끝나면 이전 키를 삭제합니다.

한 번에 기존 키를 덮어쓰지 않으면 서비스 중단 없이 교체 결과를 검증할 수 있습니다.

## AUTH KEY challenge 인증

클라이언트는 서버에 등록된 공개키와 짝을 이루는 개인키 파일을 읽을 수 있어야 합니다. 개인키
자체는 서버에 등록하지 않습니다. 키 파일이 없거나, 등록된 키와 일치하지 않거나, 비활성 또는
만료 상태이면 CHALLENGE 인증이 실패합니다. 자동으로 PASSWORD 인증으로 전환되지 않으므로
필요한 경우 별도의 PASSWORD 연결을 명시합니다.

## SYS AS USER 인증 제약

`SYS`도 CHALLENGE 인증을 사용하려면 `SYS` 사용자에 AUTH KEY가 등록되어 있어야 합니다.
그러나 애플리케이션 접속에는 `SYS`를 사용하지 말고, 전용 계정에 최소 권한과 키를 부여하십시오.
`SYS` 키 변경은 다른 관리 경로가 검증된 유지보수 시간에 수행합니다.

## AUTH_MODE=CHALLENGE

`machsql`에서는 연결 문자열과 개인키 옵션을 함께 지정합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user.key
```

JDBC 연결 속성 예시는 다음과 같습니다.

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/secure/path/app_user.key
```

로그나 오류 보고서에 개인키 경로의 내용, 비밀번호, 연결 문자열의 비밀값을 남기지 마십시오.

## AUTH_KEY_FILE

개인키는 클라이언트 호스트에서 생성하고 공개키만 SQL 등록에 사용합니다. 예를 들어 ECDSA
P-256 키 쌍은 다음처럼 만들 수 있습니다.

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key
```

`chmod 600`은 개인키 노출을 줄이기 위한 운영 권장사항입니다. 실제 프로세스 계정이 파일과
상위 디렉터리를 읽을 수 있는지도 확인합니다. 공개키를 SQL 인라인 문자열로 만들 때는 다음과
같이 줄바꿈을 `\n`으로 표현합니다.

```bash
awk '{printf "%s\\n", $0}' app_user.pub
```

PKCS#8을 포함한 실제 지원 개인키 형식은 사용 중인 클라이언트와 배포 버전에서 검증하십시오.

## AUTH_SIG_SCHEME

| 공개키 | 사용 가능한 서명 스킴 |
|---|---|
| ECDSA P-256, P-384, P-521 | `ECDSA` |
| RSA 2048, 3072, 4096 | `RSA_PKCS1_V15`, `RSA_PSS` |

키에 맞는 기본 스킴을 사용할 수 있습니다. RSA-PSS를 명시하려면 클라이언트 옵션을 함께
지정합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /secure/path/app_user_rsa.key \
  --auth-sig-scheme=RSA_PSS
```

등록된 공개키 타입과 서명 스킴이 맞지 않으면 인증에 실패합니다.

## RSA / ECDSA / RSA_PSS 지원 범위

알고리즘은 보안 정책, 사용 중인 클라이언트 지원, 키 관리 시스템과의 호환성을 기준으로
선택합니다. 특정 알고리즘의 속도나 보안성을 모든 환경에 동일하게 단정하지 마십시오. 키를
등록하기 전에 실제 클라이언트로 생성·연결·롤오버·폐기 전 과정을 검증합니다.
