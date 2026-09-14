# ROLLUP 생성과 삭제

## 생성 구문

```text
CREATE ROLLUP [IF NOT EXISTS] name
  ON source_tag [(column_or_json_path)]
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
  FROM source_rollup
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

EXTENSION 뒤에 별도 확장 이름은 쓰지 않습니다. CREATE의 단위는 SEC/MIN/HOUR이며,
조회 함수의 DAY/MONTH 등과 구분합니다. 간격은 양수이며 현행 검증 상한은 365일에
해당하는 간격입니다. 소스·계층·집계 모드의 조건도 함께 만족해야 합니다.

| 대상 | 조건 |
|---|---|
| 일반 숫자 컬럼 | 지원 숫자 타입을 지정; SUMMARIZED는 필수가 아님 |
| JSON 경로 | 해당 JSON 컬럼과 유효한 경로 지정 |
| JSON 문서 전체 | JSON SUMMARIZED 컬럼 필요 |
| WITH ROLLUP 자동 생성 | 세 번째 SUMMARIZED 컬럼 필요 |
| METADATA·거리축·비TAG | 일반 ROLLUP 대상이 아님 |

## 생성·중복 확인·조회 실습

```sql
CREATE TAG TABLE ch6_create (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_create);
ALTER ROLLUP ch6_create_ru FORCE;
SELECT DISTINCT ROLLUP_NAME, COLUMN_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CREATE_RU';
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_create WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

같은 이름의 재생성은 기존 정의를 유지합니다. IF NOT EXISTS는 정의 변경·동일성 확인 기능이
아니며, 잘못된 SQL이나 소스 검증을 모두 생략해 주는 옵션도 아닙니다.
두 간격 컬럼은 60000ms이고 조회 평균은 00:00에 15, 00:01에 30입니다.

IF NOT EXISTS 없이 같은 이름을 생성하면 오류입니다. 정상 실습과 분리해 확인합니다.

```sql
CREATE ROLLUP ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
```

## WITH ROLLUP 자동 생성

다음은 별도 테이블입니다. SEC부터 MIN·HOUR까지의 기본 계층을 자동 생성합니다.

```sql
CREATE TAG TABLE ch6_auto (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
SELECT DISTINCT ROLLUP_NAME, ROOT_TABLE, INTERVAL_TIME, EXT_TYPE
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_AUTO'
 ORDER BY INTERVAL_TIME;
```

INTERVAL_TIME이 1000·60000·3600000인 세 행이 조회됩니다.

EXTENSION 자동 생성은 `WITH ROLLUP (SEC) EXTENSION` 형태입니다. 실제 생성 이름은
V$ROLLUP에서 확인하고, 이름 충돌을 자동으로 해소한다고 가정하지 않습니다.

인자에 따라 만들어지는 계층이 달라집니다. `(SEC)`는 SEC·MIN·HOUR 세 개를, `(MIN)`은
MIN·HOUR 두 개를, `(HOUR)`는 HOUR 하나를 만들며, 인자를 생략하면 `(SEC)`와 같습니다.
이때 첫 단계만 원본 TAG를 소스로 삼고 다음 단계는 직전 ROLLUP을 소스로 삼는 계층으로
연결됩니다. 인자에는 SEC·MIN·HOUR만 사용할 수 있으며, 조회 함수가 받는 DAY 같은 단위를
지정하면 오류입니다.

## 삭제와 정의 변경

다른 ROLLUP이 참조하는 소스는 상위 의존 객체부터 제거합니다. Custom 대상 TAG는 작업을
삭제하기 전에 DROP할 수 없습니다. 정의를 바꾸려면 읽는 애플리케이션과 재집계 시간을
고려해 새 객체로 전환하거나 기존 정의를 제거한 뒤 다시 생성합니다.

```sql
DROP ROLLUP ch6_create_ru;
DROP TABLE ch6_create;
DROP TABLE ch6_auto CASCADE;
```

마지막 CASCADE는 이 실습의 자동 ROLLUP도 함께 제거합니다. 일반 운영 정리의 기본값으로
사용하지 않습니다. Custom 소스 CASCADE는 관련 작업을 제거하더라도 사용자 대상 TAG까지
자동 삭제하는 것으로 해석하지 마십시오.

조건·확장·JSON·Custom 실습은 각 절에서 독립적으로 제공합니다. 전체 구문은
SQL 레퍼런스를 참고합니다.
