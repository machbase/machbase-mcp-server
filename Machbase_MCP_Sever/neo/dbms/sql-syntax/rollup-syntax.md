# ROLLUP

ROLLUP은 시간축 TAG의 반복 집계를 위한 저장·조회 기능입니다. 일반·조건·확장 ROLLUP은
공개 `rollup()` 조회로, Custom은 사용자 대상 TAG의 재집계로 읽습니다.

## 생성

다음은 문법 형식이며 대괄호·중괄호를 그대로 실행하지 않습니다.

```text
CREATE ROLLUP [IF NOT EXISTS] name
    ON source_tag [(column_name | json_path_expression)]
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    FROM source_rollup
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    INTO (destination_tag)
    AS (SELECT ...)
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }];
```

- EXTENSION은 키워드만 쓰며 별도 extension_name을 붙이지 않습니다.
- CREATE의 시간 단위는 SEC/MIN/HOUR입니다. DAY 등은 조회 단위와 구분합니다.
- 일반 숫자 컬럼은 SUMMARIZED 없이 명시할 수 있습니다. JSON 경로 집계와 JSON
  문서 전체 집계를 구분하며, 문서 전체와 WITH ROLLUP 자동 생성에는 SUMMARIZED 조건이 있습니다.
- FROM 간격은 소스보다 큰 정수배이며 확장 속성·집계 모드가 맞아야 합니다.
- WAKEUP은 양수, 집계 간격 이하이며 그 간격을 나누어떨어지게 해야 합니다.
- Custom은 Standard 전용이고 소스 TAG 하나와 미리 만든 대상 TAG가 필요합니다.
  WHERE는 SELECT 내부에 쓰고 BASETIME 직접 조건·JOIN·FROM 서브쿼리는 허용하지 않습니다.
- IF NOT EXISTS는 기존 이름에 대해 생성하지 않는 동작이지 정의를 수정하거나 비교해
  일치시키는 기능이 아닙니다. 문법과 소스 검증을 모두 무시하는 옵션도 아닙니다.

## 삭제

```sql
DROP ROLLUP rollup_name;
```

참조하는 상위 ROLLUP부터 삭제합니다. Custom 대상 TAG는 관련 작업이 남아 있으면 DROP이
거부됩니다. 원본 TAG의 CASCADE는 관련 ROLLUP 제거 범위까지 확인한 뒤 사용하며,
사용자 Custom 대상 테이블은 별도 수명주기로 관리합니다.

## 제어

```sql
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name WAKEUP;
ALTER ROLLUP rollup_name FORCE;
ALTER ROLLUP rollup_name SET WAKEUP INTERVAL 10 SEC;
```

이 명령은 이미 존재하는 작업과 간격 조건을 전제로 합니다.
생성 시 자동 시작되며 이미 시작·중지된 상태를 반복 지정하면 오류가 날 수 있습니다.
WAKEUP은 완료를 기다리지 않고 FORCE는 대상의 소스 처리 범위를 따라잡도록 기다립니다.
과거 원본 보정에는 REBUILD의 별도 지원 범위를 확인합니다.

## 조회와 후보 선택

```text
rollup(time_unit, period, basetime_column [, origin])
```

반환 타입은 DATETIME입니다. period는 양의 정수 리터럴입니다. 일반 DATE_TRUNC +
GROUP BY 쿼리가 ROLLUP의 존재만으로 자동 전환된다고 안내하지 않습니다. ROLLUP 조회에는
`rollup()`을 명시하고, 적용 가능한 후보가 없으면 별도의 원본 쿼리를 사용합니다.

자동 선택은 같은 컬럼·경로·모드에서 조건 없는 후보를 먼저 찾고, 가능한 가장 큰 간격을
선택합니다. 같은 간격은 등록 순서의 영향을 받습니다. 일반/확장만으로 우선순위를
단정하지 않습니다. 특정 데이터 집합을 고정하려면 ROLLUP_TABLE 힌트를 사용합니다.

SEC/MIN의 후보 간격은 period초/분을 기준으로 하며 HOUR·DAY·WEEK·MONTH·YEAR는
후보 선택 단계에서 period시간을 기준으로 검사합니다. 결과 버킷의 달력 계산과 별개의
규칙입니다. 월·년 origin은 월의 1일 조건을 확인합니다.

SELECT에 name을 반환하는 태그별 집계는 GROUP BY에도 name을 포함합니다.
시간 범위·origin·NULL 처리와 후보 조건을 맞춘 뒤 원본 결과와 비교합니다.
일반 숫자 ROLLUP은 MIN/MAX/SUM/COUNT/AVG/SUMSQ, 확장은 FIRST/LAST를 추가로 지원합니다.
원본 FIRST/LAST 사용과 저장 ROLLUP의 확장 필요조건을 구분합니다.
JSON의 문서 전체 COUNT와 경로별 건수는 별도 계약입니다.

실행 가능한 생성·조회·오류 예제는 6장 ROLLUP 활용과
조회 문법을 참고하십시오.
