# USER/AUTH

사용자 생성·삭제·비밀번호 변경, 권한 부여·회수, 공개키 기반 AUTH KEY 관리 구문입니다.

---

## CREATE USER

```sql
create_user_stmt ::=
    'CREATE USER' user_name 'IDENTIFIED BY' password
    [ 'PASSWORD POLICY' ( 'NONE' | 'LOW' | 'HIGH' ) ]
    [ 'WITH AUTH KEY' '(' auth_key_spec ')' ]

auth_key_spec ::=
    "key='" pem_public_key "',"
    "valid_before='" YYYY-MM-DD "',"
    "comment='" text "'"
```

사용자명은 저장 시 대문자로 변환됩니다.

```sql
-- 기본 사용자 생성
CREATE USER app_user IDENTIFIED BY 'App#1234';

-- 비밀번호 정책 지정
CREATE USER ops_user IDENTIFIED BY 'Ops@Strong1' PASSWORD POLICY HIGH;

-- AUTH KEY와 함께 생성 (공개키 기반 인증)
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(생략)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

### 비밀번호 정책

| 정책 | 설명 |
|------|------|
| `NONE` | 강도 제약 없음. 만료일 없음 |
| `LOW` | 최소 10자, 대/소문자/특수문자 포함, 연속 숫자·키보드 패턴 금지 |
| `HIGH` | LOW 규칙 + 최근 24개 비밀번호 재사용 금지 + 90일 자동 만료 |

---

## DROP USER

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

`SYS` 사용자는 삭제할 수 없습니다. 해당 사용자가 생성한 테이블이 남아 있으면 오류가 발생합니다.

다른 관리자 세션이 사용자를 삭제해도 기존 활성 세션은 즉시 종료되지 않습니다. 새 접속은
실패하며 기존 세션은 로그인 시점의 사용자명과 ID를 유지합니다. 운영 절차는
계정 관리를,
확인 함수는 사용자 컨텍스트 함수를
참고합니다.

```sql
DROP USER old_user;
```

---

## ALTER USER

```sql
-- 비밀번호 변경
alter_user_pwd_stmt ::=
    'ALTER USER' user_name 'IDENTIFIED BY' new_password
    [ 'PASSWORD POLICY' ( 'NONE' | 'LOW' | 'HIGH' ) ]
```

정책만 단독으로 변경하는 구문은 허용되지 않습니다. 정책을 변경할 때는 반드시 새 비밀번호를 함께 지정해야 합니다.

```sql
-- 비밀번호 변경
ALTER USER app_user IDENTIFIED BY 'NewPass#456';

-- 비밀번호와 정책 동시 변경
ALTER USER app_user IDENTIFIED BY 'NewPass#456' PASSWORD POLICY HIGH;
```

---

## CONNECT

```sql
user_connect_stmt ::= 'CONNECT' user_name '/' password
```

애플리케이션을 종료하지 않고 다른 사용자로 재연결합니다.

```sql
CONNECT app_user/App#1234;
```

---

## GRANT / REVOKE

```sql
grant_stmt  ::= 'GRANT'  priv_list 'ON' object_ref 'TO'   user_name
revoke_stmt ::= 'REVOKE' priv_list 'ON' object_ref 'FROM' user_name

priv_list  ::= priv_value ( ',' priv_value )*
object_ref ::= 'DATABASE' database_name
             | 'TABLE' ['database_name.'] owner_name '.' table_name
             | ['database_name.'] owner_name '.' table_name
```

### 테이블 권한

```sql
-- 테이블에 대한 DML 권한
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
GRANT ALL ON sys.sensor_log TO app_user;

-- 권한 회수
REVOKE INSERT ON sys.sensor_log FROM writer;
REVOKE ALL ON sys.sensor_log FROM app_user;
```

테이블 권한 종류: `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `ALL`

### 데이터베이스 권한 (Machbase 8.5 이상)

```sql
-- DDL 권한 (CREATE + DROP)
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- 개별 DDL 권한
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO create_user;
GRANT DROP   ON DATABASE factory_a TO drop_user;
GRANT ALTER  ON DATABASE factory_a TO ops_user;

-- 운영 권한
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT MOUNT  ON DATABASE MACHBASEDB TO mount_user;
GRANT USAGE  ON DATABASE factory_a_backup TO report_user;

-- 모든 데이터베이스 권한
GRANT ALL ON DATABASE factory_a TO admin_user;

-- 권한 회수
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

데이터베이스 권한 종류: `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP`, `MOUNT`, `USAGE`,
`DDL`(`CREATE+DROP`), `ALL`(`CONNECT+CREATE+DROP+ALTER+BACKUP`)

### 데이터베이스 권한이 필요한 작업

| 작업 | 필요한 권한 |
|------|------------|
| CREATE/DROP TABLE, VIEW, INDEX, ROLLUP, TABLESPACE, RETENTION | `CREATE`, `DROP`, 또는 `DDL` |
| ALTER SYSTEM | `ALTER` |
| BACKUP DATABASE | `BACKUP` |
| MOUNT/UMOUNT DATABASE | `MOUNT` |

### 사용자 생성 시 기본 권한

신규 생성 사용자는 `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `CREATE`, `DROP` 권한을 기본 보유합니다.
`ALTER`, `MOUNT`, `BACKUP`은 명시적으로 부여해야 합니다.

---

## AUTH KEY 관리

AUTH KEY는 비밀번호 대신 공개키 기반 challenge 인증을 사용할 때 Machbase에 등록하는 공개키입니다.

### 지원 알고리즘

| 알고리즘 | 지원 파라미터 | 서명 스킴 |
|---------|-------------|----------|
| ECDSA | P-256, P-384, P-521 | ECDSA |
| RSA | 2048, 3072, 4096 bits | RSA_PKCS1_V15, RSA_PSS |

### 키 파일 생성 (openssl)

```bash
# ECDSA P-256 키 생성
openssl ecparam -name prime256v1 -genkey -noout -out app_user.key
openssl ec -in app_user.key -pubout -out app_user.pub
chmod 600 app_user.key

# RSA 2048-bit 키 생성
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key

# PEM을 SQL 인라인 형식으로 변환 (줄바꿈을 \n으로)
awk '{printf "%s\\n", $0}' app_user.pub
```

### AUTH KEY 추가

```sql
alter_user_add_auth_key_stmt ::=
    'ALTER USER' user_name 'ADD AUTH KEY' '(' auth_key_spec ')'

auth_key_spec ::=
    "key='" pem_public_key "',"
    "valid_before='" YYYY-MM-DD "',"
    "comment='" text "'"
```

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkw...(생략)...==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='primary key'
);
```

추가된 키는 즉시 활성 상태(`ACTIVATED=1`)로 등록됩니다.

### AUTH KEY 활성화 / 비활성화

```sql
alter_user_activate_key_stmt   ::= 'ALTER USER' user_name 'ACTIVATE AUTH KEY ID'   key_id
alter_user_deactivate_key_stmt ::= 'ALTER USER' user_name 'DEACTIVATE AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

### AUTH KEY 유효기간 변경

```sql
alter_user_alter_key_stmt ::=
    'ALTER USER' user_name 'ALTER AUTH KEY ID' key_id
    "VALID_BEFORE='" YYYY-MM-DD "'"
```

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

### AUTH KEY 삭제

```sql
alter_user_drop_key_stmt ::=
    'ALTER USER' user_name 'DROP AUTH KEY ID' key_id
```

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

### AUTH KEY 조회

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

`V$USER_AUTH_KEYS` 주요 컬럼: `KEY_ID`, `USER_NAME`, `KEY_ALGO`, `KEY_PARAM`, `ACTIVATED`, `VALID_AFTER`, `VALID_BEFORE`, `COMMENT`, `PUBKEY`

---

## 관련 문서

- 사용자 관리 가이드 - 사용자 운영 절차 및 예시
- 시스템/세션 관리 문법 - ALTER SYSTEM, ALTER SESSION
