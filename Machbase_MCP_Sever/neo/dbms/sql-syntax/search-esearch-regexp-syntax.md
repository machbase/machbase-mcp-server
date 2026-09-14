# SEARCH / ESEARCH / REGEXP

검색 연산자는 비슷해 보여도 검사하는 대상이 다릅니다.
SEARCH·ESEARCH는 KEYWORD 인덱스의 토큰을 사용하고, LIKE·REGEXP는 원문에 조건을
평가합니다. 성능 때문에 연산자를 바꾸기 전에 결과 의미가 같은지 확인하세요.

## SEARCH

```text
column_name SEARCH 'search_term'
column_name NOT SEARCH 'search_term'
```

LOG의 VARCHAR·TEXT 컬럼에 KEYWORD 인덱스가 필요합니다.
다중 단어는 AND 의미로 찾으며, 어순·인접성을 보장하는 구문 검색은 아닙니다.
기본 모드에서 일반 ASCII 단어는 소문자로 정규화되고 한글 등은 2-gram으로 분리됩니다.
모든 언어의 형태소 분석이나 Unicode 대소문자 처리를 보장하는 기능은 아닙니다.

다음 테이블은 이 페이지 전체에서 사용하는 독립 실습입니다.

```sql
CREATE LOG TABLE ch7_ref_search (
    event_id INTEGER,
    message  VARCHAR(200),
    detail   VARCHAR(200)
);
CREATE INDEX ch7_ref_msg ON ch7_ref_search(message) INDEX_TYPE KEYWORD;
CREATE INDEX ch7_ref_detail ON ch7_ref_search(detail) INDEX_TYPE KEYWORD;
INSERT INTO ch7_ref_search VALUES (1, 'ERROR timeout occurred', 'connection reset');
INSERT INTO ch7_ref_search VALUES (2, 'pretimeout normal', 'port 8080');
INSERT INTO ch7_ref_search VALUES (3, NULL, NULL);
EXEC TABLE_FLUSH(ch7_ref_search);
EXEC INDEX_FLUSH(ch7_ref_search);

SELECT event_id FROM ch7_ref_search WHERE message SEARCH 'timeout' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search
 WHERE message SEARCH 'error' AND detail SEARCH 'reset'
 ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message NOT SEARCH 'timeout' ORDER BY event_id;
```

앞의 두 쿼리는 1번, 마지막 쿼리는 2번을 선택합니다.
NOT SEARCH는 NULL 메시지인 3번을 포함하지 않습니다.
여러 컬럼을 검색하려면 각 대상 컬럼에 필요한 인덱스를 준비하세요.

## ESEARCH

```text
column_name ESEARCH 'pattern%'
column_name ESEARCH '%pattern%'
```

색인된 단어에 패턴을 적용합니다. `pattern%`는 단어 접두사,
`%pattern%`는 단어 내부의 부분 패턴입니다.
`%`가 원문 전체의 단어 경계를 자유롭게 가로지르는 것으로 해석하지 마세요.
아래 예제는 ASCII 키워드 패턴을 기준으로 합니다.

```sql
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH '%time%' ORDER BY event_id;
```

결과는 각각 1번과 1·2번입니다.
현재 ESEARCH의 ASCII 패턴 비교는 대소문자를 구분하지 않습니다.
원문 LIKE의 완전한 대체 기능은 아니며, 패턴에 매칭되는 토큰·행 수에 따라 비용이 달라집니다.

`NOT ESEARCH` 구문은 지원하지 않습니다.
NOT SEARCH·NOT LIKE로 바꾸면 제외할 행도 달라질 수 있으므로 결과와 NULL 처리를 확인하세요.

## LIKE와 비교

```sql
SELECT event_id FROM ch7_ref_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

첫 쿼리는 1·2번, 두 번째는 0건입니다. NULL 행은 NOT LIKE에도 포함되지 않습니다.
LIKE는 현재 ASCII 비교에서 대소문자를 구분하지 않습니다.
`%`는 0개 이상의 문자, `_`는 한 문자를 나타냅니다.

LIKE 자체는 KEYWORD 인덱스를 사용하지 않습니다.
그렇다고 항상 테이블 전체 스캔이라고 단정할 수는 없습니다.
시간 조건이나 다른 인덱스 조건으로 먼저 대상 행이 제한될 수 있습니다.

## REGEXP

```text
column_name REGEXP 'pattern'
column_name NOT REGEXP 'pattern'
```

정규식 패턴에 맞는 부분을 검사합니다. 기본 비교는 대소문자를 구분합니다.
시작·끝을 제한하려면 `^`·`$`를 사용하세요.

```sql
SELECT event_id FROM ch7_ref_search
 WHERE message REGEXP '^ERROR.*timeout'
 ORDER BY event_id;
SELECT event_id FROM ch7_ref_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

첫 쿼리는 1번, 두 번째는 0건입니다.
REGEXP는 KEYWORD 인덱스를 직접 사용하지 않습니다.
SEARCH로 먼저 대상을 줄이려면 그 조건이 원하는 결과를 누락시키지 않는지 확인해야 합니다.

### 함수 형태 REGEXP

스칼라 표현식에서도 REGEXP 결과를 사용할 수 있습니다.

```sql
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' FROM dual;
```

결과는 1입니다. 함수 형태의 REGEXP_LIKE는 비교 옵션도 받을 수 있습니다.
현재 함수 입력은 VARCHAR여야 하며 패턴과 옵션은 상수 VARCHAR여야 합니다.
TEXT 컬럼을 받는 REGEXP 연산자와 입력 타입 제약이 같다고 가정하지 마세요.

```sql
SELECT event_id,
       REGEXP_LIKE(message, 'error') AS case_sensitive,
       REGEXP_LIKE(message, 'error', 'i') AS case_insensitive
  FROM ch7_ref_search
 WHERE event_id IN (1, 3)
 ORDER BY event_id;
```

1번의 결과는 0·1, 3번은 NULL·NULL입니다.
`i`는 대소문자 비구분, `c`는 구분이며 옵션을 생략하면 구분 비교입니다.

## 성능 권장사항

| 목적 | 선택 기준 |
|---|---|
| 단어 존재 확인 | SEARCH |
| 색인된 단어의 접두사·부분 패턴 | ESEARCH |
| 원문 문자열의 부분 패턴 | LIKE |
| 원문 형식·위치·복잡한 패턴 | REGEXP·REGEXP_LIKE |

인덱스 존재와 빌드 완료를 구분하고, 같은 데이터와 시간 범위에서 비교하세요.
실습을 마쳤으면 테이블을 정리합니다.

```sql
DROP TABLE ch7_ref_search;
```

## 관련 문서

- 텍스트 검색 실습 — 다중 단어·한글·NULL·TEXT 제약
- INDEX syntax — KEYWORD 인덱스 생성
