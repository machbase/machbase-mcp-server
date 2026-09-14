# 계정 관리

애플리케이션과 운영 작업에는 서로 다른 사용자 계정을 사용합니다. `SYS`는 사용자와 권한을
관리하는 계정으로 제한하고, 일상적인 조회·적재에는 필요한 권한만 가진 계정을 사용하십시오.

## 사용자 생성과 삭제

```sql
CREATE USER app_user IDENTIFIED BY 'App#Strong123' PASSWORD POLICY HIGH;

SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 WHERE NAME = 'APP_USER';
```

사용자명은 대문자로 저장됩니다. 논리 데이터베이스에 연결하려면 계정 생성 후 대상 데이터베이스의
`CONNECT` 권한을 별도로 부여합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

비밀번호를 바꿀 때는 새 비밀번호와 정책을 함께 지정할 수 있습니다.

```sql
ALTER USER app_user IDENTIFIED BY 'App#Changed456' PASSWORD POLICY HIGH;
```

사용자 삭제 전에는 실행 중인 세션, 부여한 권한, 사용자가 소유한 객체를 확인합니다. 소유
객체가 있으면 계정을 삭제할 수 없습니다.

```sql
DROP USER app_user;
```

`SYS` 계정과 현재 연결 중인 자기 계정은 삭제할 수 없습니다. `machsql`에서 다른 계정으로
작업을 계속하려면 `CONNECT user/password;`로 새 세션 인증을 수행하거나 클라이언트를 다시
연결합니다.

### 활성 세션이 있는 사용자 삭제

다른 관리자 세션이 사용자를 삭제해도 해당 사용자로 이미 인증한 세션은 즉시 종료되지
않습니다. 기존 세션은 로그인할 때 보존한 사용자명과 내부 ID를 유지하지만, 삭제된 사용자는
새로 접속할 수 없고 `M$SYS_USERS`에서도 조회되지 않습니다. 삭제 전 활성 세션을 확인하고
애플리케이션 연결을 먼저 종료합니다.

Machbase 8.7.0부터 기존 세션의 사용자 컨텍스트는
CURRENT_USER와 SESSION_USER 함수로
확인할 수 있습니다.

## 비밀번호 정책

| 정책 | 주요 동작 |
|---|---|
| `NONE` | 호환성을 위한 기본 정책. 강도·만료 제약 없음 |
| `LOW` | 길이와 문자 조합을 검사 |
| `HIGH` | LOW 검사, 최근 비밀번호 재사용 제한, 유효기간 적용 |

LOW와 HIGH는 10자 이상의 비밀번호를 요구합니다. 대소문자 검사 방식은
`ENABLE_CASE_SENSITIVE_PASSWORD` 설정의 영향을 받습니다. HIGH는 설정 시점에서 90일 뒤를
`VALID_BEFORE`로 기록합니다.

```sql
CREATE USER reader_user
  IDENTIFIED BY 'Reader#Strong123'
  PASSWORD POLICY HIGH;

ALTER USER reader_user
  IDENTIFIED BY 'Reader#Changed456'
  PASSWORD POLICY LOW;
```

정책만 단독으로 바꾸는 대신 새 비밀번호를 함께 지정합니다. 현재 정책과 만료일은 다음처럼
확인합니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;
```

`PWD_POLICY_LEVEL`은 `0=NONE`, `1=LOW`, `2=HIGH`입니다. 애플리케이션에 비밀번호를 직접
기록하지 말고 운영 환경의 비밀 관리 수단을 사용하십시오. 전체 문법은
USER/AUTH 문법을
참고하십시오.
