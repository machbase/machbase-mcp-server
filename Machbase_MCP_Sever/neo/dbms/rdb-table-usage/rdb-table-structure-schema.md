# 테이블 구조와 스키마

자동 번호가 있으니 중복 걱정은 끝났다고 생각하기 쉽습니다.
하지만 같은 외부 장비가 서로 다른 번호로 두 번 들어오는 일은 여전히 가능합니다.
행을 식별하는 키와 업무상 중복을 막는 키를 구분하는 것이 스키마 설계의 출발점입니다.

## 내부 식별자와 업무 키

다음 예제는 내부 번호와 외부 장비 코드를 따로 관리합니다.

```sql
CREATE TRANSACTION TABLE ch8_schema (
    id            LONG PRIMARY KEY AUTO_INCREMENT,
    external_code VARCHAR(64) NOT NULL,
    device_name   VARCHAR(128) NOT NULL,
    price         DECIMAL(18,2),
    state         JSON,
    updated_at    DATETIME
);
CREATE UNIQUE INDEX ch8_schema_code ON ch8_schema(external_code);

INSERT INTO ch8_schema(external_code, device_name, price, state, updated_at)
VALUES ('ERP-01', 'Pump A', 19900.25, '{"status":"NORMAL"}',
        TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));

SELECT external_code, device_name, price, state->'$.status' AS status
  FROM ch8_schema;
```

ERP-01 한 행, 가격 19900.25, 상태 NORMAL이 조회됩니다.
id는 서버가 부여합니다. 연속 번호나 빈 번호 없는 발급을 업무 조건으로 삼지는 마세요.
발급 번호를 받는 방법은 사용하는 SDK와
AUTO_INCREMENT를 확인하세요.

## PRIMARY KEY와 UNIQUE

TRANSACTION의 PRIMARY KEY는 테이블당 하나이며 단일 컬럼입니다.
컬럼 뒤에 PRIMARY KEY를 지정하거나, 기존 테이블에 CREATE PRIMARY KEY INDEX로 추가할 수
있습니다. NULL과 중복이 있는 데이터에는 만들 수 없습니다.

여러 컬럼의 조합을 고유하게 만들려면 복합 UNIQUE INDEX를 사용합니다.
CREATE TABLE 내부의 UNIQUE·FOREIGN KEY·테이블 수준 PRIMARY KEY 문법을 다른 DBMS에서
그대로 가져오지 마세요. 고유성은 테이블 생성 후 CREATE UNIQUE INDEX로 지정합니다.

UNIQUE INDEX의 키에 NULL이 포함되면 NULL 포함 키끼리는 중복으로 보지 않습니다.
“코드가 반드시 있고 고유해야 한다”면 예제처럼 NOT NULL도 함께 선언해야 합니다.
실수하기 쉬운 또 다른 값은 빈 문자열입니다. Machbase의 빈 문자열과 NULL 처리도 실제
입력 경로에서 확인하고, 필수 코드는 수집 단계에서 검증하세요.

다음 SQL은 UNIQUE 위반을 확인하는 선택 실습입니다. 정상 입력과 분리해서 실행하세요.

```sql
-- 의도적으로 실패: external_code 중복
INSERT INTO ch8_schema(external_code, device_name)
VALUES ('ERP-01', 'Duplicate Pump');
```

실패 후 ERP-01은 여전히 한 행이어야 합니다.
중복 시 갱신하려면 UPSERT의 별도 규칙을 사용합니다.

## 데이터 타입 선택

| 값 | 타입 선택 | 확인할 사항 |
|---|---|---|
| 식별자·수량 | SHORT·INTEGER·LONG 및 지원 unsigned 타입 | 범위와 NULL 예약값 |
| 측정값·근삿값 | FLOAT·DOUBLE | 부동소수점 반올림 |
| 금액·정확한 소수 | DECIMAL(M,D)와 NUMERIC 등 별칭 | precision·scale·입력 변환 |
| 코드·이름 | VARCHAR(n) | 문자 수가 아닌 바이트 길이 |
| 긴 문자열·바이너리 | TEXT/CLOB·BINARY/BLOB | 저장 지원과 정렬·함수·인덱스 지원을 구분 |
| 발생·변경 시각 | DATETIME | 원본 시간대와 변환 형식 |
| 네트워크 주소 | IPV4·IPV6 | 주소 형식과 비교 의미 |
| 부가 속성 | JSON | 자주 검색할 경로와 타입 |
| 고정 길이 수치 묶음 | 숫자 ARRAY | 요소 타입·길이·whole NULL과 요소 NULL |

전체 범위는 데이터 타입 사전을,
금액은 DECIMAL을
기준으로 확인하세요. 예제의 DOUBLE을 모든 금액 컬럼에 관성적으로 사용하지 않는 것이 좋습니다.

## 제약과 입력 검증

TRANSACTION에는 최소 하나의 사용자 컬럼이 필요합니다.
LOG의 자동 도착 시각이나 TAG의 METADATA·BASETIME·BASEDISTANCE를 사용할 수 없습니다.
외래 키가 자동으로 참조 무결성을 검사한다고 가정하지 말고, 필요한 관계 검증을
애플리케이션과 데이터 점검 절차에 포함하세요.

예제의 UNIQUE INDEX가 있다고 장비 이름·가격의 업무 유효성까지 검사되는 것은 아닙니다.
필수값, 허용 상태, 수량 범위는 별도로 정의해야 합니다.

```sql
SELECT COUNT(*) AS device_count FROM ch8_schema;
DROP TABLE ch8_schema;
```

정리 전 건수는 1입니다.
스키마 변경은 생성·변경·삭제, 조회 경로는
인덱스 설계에서 이어서 확인하세요.
