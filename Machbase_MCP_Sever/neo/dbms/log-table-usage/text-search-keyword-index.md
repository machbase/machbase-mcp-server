# 텍스트 검색과 KEYWORD 인덱스

메시지에 같은 글자가 들어 있어도 SEARCH와 LIKE의 결과는 다를 수 있습니다.
SEARCH는 색인된 단어를 찾고, LIKE는 원문 문자열에 패턴을 적용하기 때문입니다.
성능을 비교하기 전에 “어떤 행을 찾으려는가”를 먼저 맞춰 보겠습니다.

## 검색 데이터 준비

```sql
CREATE LOG TABLE ch7_search (
    event_id INTEGER,
    message  TEXT
);
CREATE INDEX ch7_search_msg ON ch7_search(message) INDEX_TYPE KEYWORD;

INSERT INTO ch7_search VALUES (1, 'ERROR connection timeout');
INSERT INTO ch7_search VALUES (2, 'connection slowly refused');
INSERT INTO ch7_search VALUES (3, 'pretimeout marker');
INSERT INTO ch7_search VALUES (4, 'normal service');
INSERT INTO ch7_search VALUES (5, NULL);
INSERT INTO ch7_search VALUES (6, '대한민국 연결 오류');
INSERT INTO ch7_search VALUES (7, 'ERR-1001 network');
INSERT INTO ch7_search VALUES (8, 'timeout refused connection');

EXEC TABLE_FLUSH(ch7_search);
EXEC INDEX_FLUSH(ch7_search);
```

표본의 `event_id`로 결과를 비교합니다. 메시지는 TEXT이므로 정렬 기준으로 사용하지
않습니다. LOG의 VARCHAR에도 같은 KEYWORD 검색을 사용할 수 있습니다.

## SEARCH와 NOT SEARCH

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH 'timeout' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH 'connection refused' ORDER BY event_id;
SELECT event_id FROM ch7_search
 WHERE message SEARCH 'connection' AND message SEARCH 'refused'
 ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT SEARCH 'timeout' ORDER BY event_id;
```

| 조건 | 선택되는 event_id | 이유 |
|---|---|---|
| SEARCH 'timeout' | 1, 8 | pretimeout은 별도 단어 |
| SEARCH 'connection refused' | 2, 8 | 두 단어가 모두 존재 |
| SEARCH 두 조건을 AND로 결합 | 2, 8 | 같은 메시지에서 두 단어 확인 |
| NOT SEARCH 'timeout' | 2, 3, 4, 6, 7 | 해당 단어가 없으며 NULL 행은 제외 |

다중 단어 SEARCH는 단어의 어순이나 인접성을 보장하는 구문 검색이 아닙니다.
2번에는 중간 단어가 있고 8번에는 순서가 뒤집혀 있지만 둘 다 선택됩니다.
다른 컬럼까지 SEARCH하려면 그 컬럼에도 해당 인덱스가 필요합니다.

기본 토큰화에서 일반 ASCII 단어는 소문자로 정규화됩니다.
예를 들어 1번의 `ERROR`는 `SEARCH 'error'`로도 검색됩니다.
이를 모든 Unicode 문자의 언어별 대소문자 처리로 확대해서 해석하지 마세요.

### 한글 토큰 분리

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH '대한' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH '연결' ORDER BY event_id;
```

둘 다 6번이 선택됩니다. 기본 모드에서 `대한민국`은 `대한`, `한민`, `민국`처럼
겹치는 2-gram으로 색인됩니다. 형태소나 문장 의미를 이해하는 검색은 아닙니다.
공백·구두점·한 글자·영문과 한글이 섞인 값은 토큰 경계가 달라질 수 있으므로 실제 표본으로
확인하세요. MODE 같은 인덱스 옵션을 바꾸면 토큰화도 달라질 수 있습니다.

## ESEARCH 확장 검색

```sql
SELECT event_id FROM ch7_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH '%time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH 'err%' ORDER BY event_id;
```

| 패턴 | 선택되는 event_id | 의미 |
|---|---|---|
| time% | 1, 8 | time으로 시작하는 단어 |
| %time% | 1, 3, 8 | time을 포함하는 단어 |
| err% | 1, 7 | error 또는 err처럼 err로 시작하는 단어 |

`time%`가 단어 중간의 time까지 찾는 것은 아닙니다.
또한 ESEARCH는 원문 전체에 LIKE를 적용하는 것과 같지 않습니다.
공백·구두점을 가로지르는 원문 패턴을 그대로 ESEARCH에 옮기지 마세요.
복잡한 다중 조건은 별도 SEARCH·ESEARCH 조건을 AND·OR로 결합해 의미를 명시하세요.

현재 비교 경로에서 ESEARCH는 ASCII 대소문자를 구분하지 않습니다.
대상 키워드가 넓게 매칭될수록 검색 비용도 커지므로 항상 LIKE보다 빠르다고 단정할 수는
없습니다. 이 예제는 ASCII 키워드 패턴을 기준으로 합니다.

`NOT ESEARCH` 구문은 지원하지 않습니다. `NOT SEARCH`나 `NOT LIKE`로 바꾸면
검색 의미도 바뀝니다. 어떤 행을 제외할지 다시 정의하고 NULL 처리까지 확인하세요.

## LIKE와 NOT LIKE

```sql
SELECT event_id FROM ch7_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message LIKE 'ERR-____' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

첫 쿼리는 1·3·8번, 두 번째는 0건, 세 번째는 2·4·6·7번입니다.
7번 메시지는 `ERR-1001` 뒤에도 문자열이 있으므로 `ERR-____` 전체 패턴과 맞지 않습니다.
`%`는 0개 이상의 문자, `_`는 한 문자를 나타냅니다.
리터럴 `%`·`_`·역슬래시를 찾을 때는 역슬래시 이스케이프 규칙도 확인하세요.

LIKE도 현재 ASCII 비교에서는 대소문자를 구분하지 않습니다.
KEYWORD 인덱스는 사용하지 않으며, WHERE의 다른 조건이나 시간 범위로 검사할 행을
줄일 수 있습니다. 따라서 LIKE가 있다는 이유만으로 항상 테이블 전체를 읽는다고
설명하는 것도 정확하지 않습니다.

## REGEXP와 REGEXP_LIKE

```sql
SELECT event_id FROM ch7_search
 WHERE message REGEXP '^ERR-[0-9]+'
 ORDER BY event_id;

SELECT event_id FROM ch7_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

첫 쿼리는 7번, 두 번째는 2·4·6·7번입니다.
REGEXP는 정규식 패턴에 맞는 부분이 있는지 검사합니다.
문자열 시작이나 끝을 제한하려면 `^`·`$`를 명시하세요.

함수로 사용할 때는 `REGEXP_LIKE`를 사용합니다.
현재 이 함수의 입력은 VARCHAR여야 하고, 패턴과 옵션도 상수 VARCHAR여야 합니다.
앞의 TEXT 컬럼을 그대로 전달하면 타입 오류가 나므로 별도 표본을 준비합니다.

```sql
CREATE LOG TABLE ch7_regexp_fn (event_id INTEGER, message VARCHAR(200));
INSERT INTO ch7_regexp_fn VALUES (1, 'ERROR connection timeout');
INSERT INTO ch7_regexp_fn VALUES (5, NULL);

SELECT event_id,
       REGEXP_LIKE(message, 'error') AS case_sensitive,
       REGEXP_LIKE(message, 'error', 'i') AS case_insensitive
  FROM ch7_regexp_fn
 WHERE event_id IN (1, 5)
 ORDER BY event_id;
```

1번은 각각 0·1, NULL 메시지인 5번은 두 결과 모두 NULL입니다.
기본 정규식 비교는 대소문자를 구분하며, `i` 옵션은 비구분 비교입니다.
명시적인 구분 비교에는 `c`를 사용할 수 있습니다.

정규식은 KEYWORD 인덱스로 직접 처리되지 않습니다.
시간 조건이나 SEARCH로 대상을 줄일 수 있지만, 선행 조건이 원하는 행을 놓치면
뒤의 정규식이 그 행을 되살려 주지는 못합니다.

## TEXT 제약과 검색 성능

TEXT는 최대 64MiB 원문을 담을 수 있지만, TEXT 자체의 ORDER BY·GROUP BY는 지원하지
않습니다. 정렬·집계할 장치·오류 코드·등급은 별도 컬럼에 두세요.
같은 데이터에서 인덱스 존재 여부, 빌드 상태, 조회 범위를 확인한 뒤 성능을 비교합니다.

```sql
DROP TABLE ch7_regexp_fn;
DROP TABLE ch7_search;
```

검색 결과가 다르면 원문 한 행과 사용한 패턴을 함께 확인해 보세요.
“단어를 찾는지, 원문 일부를 찾는지”를 구분하는 것만으로 해결되는 경우가 많습니다.
