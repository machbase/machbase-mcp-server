# 서버와 SDK 호환성

Machbase 서버와 SDK의 버전이 다르면 기본 연결은 가능하더라도 최신 인증, 메타데이터,
Named Bind Parameter 기능이 제한될 수 있습니다. 이 절에서는 서버와 SDK 버전 조합별 지원
범위와 업그레이드 순서를 설명합니다.

## 서버와 SDK 버전 호환 표

| 서버 버전 | 8.5 클라이언트 드라이버 | 8.7.0 클라이언트 드라이버 |
|-----------|:---------------------:|:---------------------:|
| **8.7.0 서버** | 제한적 호환 | 완전 호환 |
| **8.5 서버** | 완전 호환 | 하위 호환, 8.7.0 이름 API 미지원 |

- **완전 호환**: 같은 버전 조합입니다. 실제 사용 가능 기능은 Edition, 테이블 유형과
  SDK별 지원 범위에 따르며, 해당 기능이 포함된 빌드를 사용해야 합니다.
- **제한적 호환**: 기본 연결은 가능하나 8.7.0 신규 기능(AUTH KEY 확장 등)이 동작하지 않을 수 있습니다.
- **하위 호환**: 8.5 서버 범위의 기능만 사용 가능합니다.

## Machbase 8.7.0 SDK의 주요 변경 사항

### AUTH KEY 인증 확장

8.7.0에서 AUTH KEY challenge 인증 방식이 확장되었습니다.

- 지원 서명 방식: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`
- 8.5 이하 드라이버는 신규 서명 방식(`RSA_PSS`)을 지원하지 않을 수 있습니다.
- AUTH KEY 인증을 사용하는 경우 드라이버를 8.7.0으로 업데이트하십시오.

```text
-- AUTH KEY 등록 (서버)
ALTER USER app_user ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31'
);
```

### 연결 문자열 호환성

Machbase SQLCLI와 ODBC에서 AUTH KEY 관련 파라미터:

```ini
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./private_key.pem;
AUTH_SIG_SCHEME=ECDSA;
```

8.5 드라이버는 `AUTH_SIG_SCHEME` 파라미터를 무시할 수 있습니다.

### Nullable 메타데이터

결과 컬럼이 NULL을 허용하는지 확인하는 API와 서버·SDK 조합별 제약은
Nullable 메타데이터 지원 범위를
참고하십시오. 호환성을 점검할 때는 서버와 클라이언트 버전을 함께 기록합니다.

### Named Bind Parameter

이름이 있는 매개변수를 서버에 준비된 문장으로 전달하는지, 위치 순서로 바인딩하는지,
클라이언트에서 SQL 문자열로 변환하는지는 SDK마다 다릅니다.
SDK 기능 지원 범위에서
사용하는 클라이언트의 동작을 확인하십시오.

### ARRAY와 선택 컬럼 Append

고정 길이 숫자 ARRAY와 선택 컬럼 Append는 Machbase DBMS 8.7.0에서 지원합니다. DBMS
8.7.0 서버와 ARRAY 기능이 포함된 SDK 빌드를 함께 사용하십시오. 구버전 서버 또는 기능이
포함되지 않은 SDK는 ARRAY 메타데이터나 값을 기존 scalar 타입으로 대체하지 않으며 해당
요청을 오류로 처리합니다.

ARRAY의 SQL 요소 위치와 Machbase 전용 SDK position은 0-based입니다. 기존 1-based SQL,
sparse 객체와 indexed Append target은 위치를 1씩 낮춥니다. 저장 데이터와 dense ARRAY
요소 순서는 바뀌지 않습니다. JDBC parameter ordinal이나 `java.sql.Array` slice처럼
표준 API가 정의한 1-based 위치는 이 변경의 대상이 아닙니다.

Cluster Edition은 coordinator, broker와 warehouse를 모두 ARRAY를 지원하는 같은 DBMS
8.7.0 빌드로 구성합니다. 혼합 버전 상태에서는 ARRAY DDL이나 ARRAY 데이터를 사용하는
작업을 시작하지 마십시오.

SQL과 SDK별 요구사항은
숫자 ARRAY 타입과
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

## SDK 버전 확인

JDBC:

```java
Connection conn = DriverManager.getConnection(url, props);
DatabaseMetaData meta = conn.getMetaData();
System.out.println("Driver: " + meta.getDriverVersion());
```

Machbase SQLCLI:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

ODBC:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

## 업그레이드 권장 사항

1. 서버와 SDK를 같은 버전(8.7.0)으로 함께 업그레이드하십시오.
2. SDK를 순차적으로 업그레이드하는 경우, 업그레이드 기간 동안 8.5 SDK가 8.7.0 서버에 제한적으로 연결될 수 있음을 인지하십시오.
3. AUTH KEY 인증을 사용하는 경우 SDK를 가장 먼저 업그레이드하십시오.
4. Nullable 메타데이터를 애플리케이션 로직에 사용하는 경우 서버와 SDK를 모두 8.7.0으로
   업그레이드하십시오.
5. Named Bind Parameter의 이름 기반 SDK API를 사용하는 경우 서버와 SDK를 모두 8.7.0으로
   업그레이드하십시오.
6. ARRAY 또는 선택 컬럼 Append를 사용하는 경우 서버는 Machbase DBMS 8.7.0으로,
   클라이언트는 해당 기능이 포함된 SDK 빌드로 업그레이드하십시오. Cluster Edition은
   모든 노드를 함께 맞춥니다.
