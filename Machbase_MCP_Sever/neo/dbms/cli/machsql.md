# machsql 명령/옵션 사전

`machsql`은 터미널에서 SQL 쿼리를 대화형으로 실행하는 클라이언트 도구입니다. SQL 스크립트 파일 실행, 결과 파일 저장, 공개키 인증도 지원합니다.

## 옵션 목록

```bash
machsql -h
```

| 짧은 옵션 | 긴 옵션 | 기본값 | 설명 |
|----------|---------|--------|------|
| `-s` | `--server` | 127.0.0.1 | 접속할 서버 IP 주소 |
| `-P` | `--port` | 5656 | 서버 포트 번호 |
| `-u` | `--user` | SYS | 사용자 이름 |
| `-p` | `--password` | MANAGER | 사용자 비밀번호 |
| `-K` | `--auth-key-file` | - | 공개키 인증용 개인키 파일 경로 (8.5 이상) |
| | `--auth-sig-scheme` | - | 인증 서명 스킴. `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` (8.5 이상) |
| `-f` | `--script` | - | 실행할 SQL 스크립트 파일 |
| `-o` | `--output` | - | 쿼리 결과를 저장할 파일 이름 |
| `-r` | `--format` | csv | 출력 파일 포맷 (`csv`, `json` 등) |
| `-z` | `--timezone` | - | 타임존 설정. 예: `+0900`, `-1230` |
| `-n` | `--nls` | - | NLS 설정 |
| `-c` | `--connstr` | - | 추가 연결 매개변수 문자열 (6.1 이상) |
| `-D` | `--database` | `MACHBASEDB` | 연결 직후 사용할 논리 데이터베이스 (8.7.0 Standard) |
| `-i` | `--silent` | - | 저작권 배너 없이 실행 |
| `-v` | `--verbose` | - | 상세 출력 |
| `-x` | `--testing` | - | 테스트 모드로 실행 |
| `-h` | `--help` | - | 옵션 목록 출력 |

## 접속 예시

기본 접속:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
machsql --server=localhost --user=SYS --password=MANAGER
```

포트 지정:

```bash
machsql -s 192.168.1.10 -P 5656 -u SYS -p MANAGER
```

SQL 스크립트 실행:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -f create_tables.sql
```

타임존 지정:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
machsql -s 127.0.0.1 -u SYS -p MANAGER -z -1230
```

결과를 파일로 저장:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -o result.csv -f query.sql
```

## 공개키 인증 (Machbase 8.5 이상)

비밀번호 대신 공개키 기반 challenge 인증을 사용할 수 있습니다.

ECDSA 키로 접속:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA
```

RSA-PSS 키로 접속:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS
```

지원 키 알고리즘:

| 알고리즘 | 키 파라미터 | 기본 서명 스킴 |
|---------|-----------|--------------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` |

## 추가 연결 매개변수 (6.1 이상)

`-c` 옵션으로 추가 연결 파라미터를 지정합니다.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -P 5656 \
    -c 'ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10'
```

환경변수로도 설정할 수 있습니다.

```bash
export MACHBASE_CONNECTION_STRING="ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3"
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

`-c` 옵션이 환경변수보다 우선 적용됩니다.

## 논리 데이터베이스 선택

Machbase 8.7.0 Standard Edition에서는 `-D` 또는 `--database`로 연결 직후 사용할
논리 데이터베이스를 지정할 수 있습니다.

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' -D factory_a
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' --database=factory_a
```

`-c` 연결 문자열을 사용할 때는 `DATABASE=factory_a` 또는 호환 별칭인
`DBNAME=factory_a`를 지정할 수 있습니다. `-D`와 연결 문자열의 database 값이 다르면
연결을 거부하므로 하나만 지정하거나 같은 값을 사용하십시오. 연결 후 다음 SQL로 실제
server catalog를 확인합니다.

```sql
SELECT CURRENT_DATABASE();
SHOW CURRENT DATABASE;
```

## machsql 내장 명령

machsql 프롬프트(`Mach>`)에서 사용할 수 있는 내장 명령입니다.

| 명령 | 설명 |
|------|------|
| `SHOW TABLES` | 전체 테이블 목록 출력 |
| `SHOW TABLE table_name` | 특정 테이블의 컬럼 및 인덱스 정보 출력 |
| `SHOW INDEXES` | 전체 인덱스 목록 출력 |
| `SHOW INDEX index_name` | 특정 인덱스 정보 출력 |
| `SHOW INDEXGAP` | 인덱스 생성 GAP 정보 출력 |
| `SHOW LSM` | LSM 인덱스 생성 정보 출력 |
| `SHOW TABLESPACES` | 전체 테이블스페이스 목록 출력 |
| `SHOW TABLESPACE name` | 특정 테이블스페이스 정보 출력 |
| `SHOW STORAGE` | 테이블별 디스크 사용량 출력 |
| `SHOW STATEMENTS` | 서버에 등록된 쿼리 목록 출력 |
| `SHOW USERS` | 사용자 목록 출력 |
| `SHOW LICENSE` | 라이선스 정보 출력 |
| `SHOW DATABASES` | active/mounted 데이터베이스 목록 출력 |
| `SHOW CURRENT DATABASE` | 현재 session의 데이터베이스 출력 |
| `SHOW LAST ROWID` | 가장 최근에 성공한 단일 INSERT의 ROWID 출력 |
| `SHOW LASTID` | `SHOW LAST ROWID`와 같은 명령 |

### 마지막 INSERT의 ROWID 확인

Machbase 8.7.0 Standard Edition에서는 단일 `INSERT ... VALUES`를 실행한 직후 입력된 행의
ROWID를 확인할 수 있습니다.

```sql
INSERT INTO orders(item) VALUES('pump');
SHOW LAST ROWID;
```

```text
Last ROWID : 2048
```

`SHOW LASTID`도 같은 값을 출력합니다. 반환할 ROWID가 없으면 `0`이 아니라 `NULL`을
출력합니다. INSERT 실패, batch·Append·loader, `INSERT ... SELECT`, UPSERT 또는 재접속
뒤에는 이전 값을 사용하지 않습니다. SELECT와 COMMIT 같은 비 INSERT 명령은 마지막 값을
유지합니다.

테이블별 ROWID 조건과 SDK에서 확인하는 방법은
ROWID와 INSERT 결과 ID를 참고하십시오.

## DESC와 PRIMARY KEY 메타데이터

`DESC table_name`은 컬럼과 인덱스 정보에 이어 `[ PRIMARY KEY ]` 섹션을 표시합니다. 이
섹션에서 PRIMARY KEY 이름, 컬럼 이름, key sequence를 확인할 수 있습니다. TRANSACTION·
LOOKUP·VOLATILE 테이블의 선언된 PK와 TAG 테이블의 `NAME`이 대상이며, 일반 LOG 테이블에는
PK 행이 표시되지 않습니다.

```sql
DESC ACCOUNT;
```

이 출력은 SELECT 결과 컬럼 메타데이터와 별개입니다. SDK에서 SELECT 결과의 PK 여부를
확인하려면 PRIMARY KEY 메타데이터 지원 범위를
참고하십시오.

## ARRAY 표시와 DESC

Machbase DBMS 8.7.0의 `DESC`는 ARRAY 컬럼을 `INT32[3]`,
`DECIMAL(12,4)[2]`와 같은 canonical 선언으로 표시합니다. 조회 결과는
`[value,null,value]` 형식이며 소문자 `null`은 element NULL입니다. 컬럼 전체가 NULL이면
일반 SQL `NULL`로 표시합니다.

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

ARRAY 선언, NULL 구분과 표현식은
숫자 ARRAY 타입을 참고하십시오.

## Named Bind Parameter

`machsql`의 `PREPARE` SQL에는 `:name` marker를 사용할 수 있습니다. 값은 이름이 아니라
SQL에 나타난 순서대로 `$1`, `$2`, ... 변수에 지정합니다.

```sql
PREPARE INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
        VALUES (:id, :name, :value);
$1 := 900;
$2 := 'machsql-client';
$3 := 72.125000;
EXECUTE;
PREPARE CLEAN;
```

같은 이름이 반복되어도 각 발생 위치에 값을 지정합니다.

```sql
PREPARE SELECT ID, NAME
        FROM SENSOR_DATA
        WHERE ID = :id OR PARENT_ID = :id;
$1 := 900;
$2 := 900;
EXECUTE;
PREPARE CLEAN;
```

이름 문법과 발생 순서 규칙은
Named Bind Parameter syntax를
참고하십시오.

## 사용 예시

```bash
# 대화형 모드로 접속
machsql -s 127.0.0.1 -u SYS -p MANAGER

# 접속 후 테이블 확인
Mach> SHOW TABLES;

# 테이블 구조 확인
Mach> SHOW TABLE sensor_data;

# SQL 스크립트를 실행하고 결과를 CSV로 저장
machsql -s 127.0.0.1 -u SYS -p MANAGER \
    -f report.sql -o report_output.csv -i
```
