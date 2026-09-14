# JSON 함수와 JSON dot 표기법

Machbase는 `JSON` 타입 컬럼에 저장된 데이터를 조작·조회하기 위한 함수와 JSON dot 표기법을 제공합니다.

## 빠른 참조

| 함수/표기법 | 문법 | 설명 |
|-------------|------|------|
| JSON dot 표기법 | `col.key` | JSON 객체에서 키 값 추출 |
| `JSON_EXTRACT` | `JSON_EXTRACT(doc, path)` | JSON 경로의 값을 JSON 문자열로 추출 |
| `JSON_EXTRACT_STRING` | `JSON_EXTRACT_STRING(doc, path)` | JSON 경로의 값을 문자열로 추출 |
| `JSON_EXTRACT_INTEGER` | `JSON_EXTRACT_INTEGER(doc, path)` | JSON 경로의 값을 정수로 추출 |
| `JSON_EXTRACT_DOUBLE` | `JSON_EXTRACT_DOUBLE(doc, path)` | JSON 경로의 값을 실수로 추출 |
| `JSON_TYPEOF` | `JSON_TYPEOF(doc, path)` | 지정한 JSON 경로에 있는 값의 타입 확인 |
| `JSON_IS_VALID` | `JSON_IS_VALID(json_text)` | JSON 문자열 유효성 확인 |
| `JSON_SET` | `JSON_SET(doc, path, scalar)` | JSON 경로에 스칼라 값 설정 |
| `JSON_SET_JSON` | `JSON_SET_JSON(doc, path, json_text)` | JSON 경로에 JSON 서브트리 설정 |
| `JSON_REMOVE` | `JSON_REMOVE(doc, path)` | JSON 경로의 멤버 제거 |

`JSON_TYPEOF`의 `path`는 필수 인자입니다. JSON 문서 전체의 타입은 `JSON_TYPEOF(doc, '$')`로 확인합니다.

---

## JSON dot 표기법

JSON 컬럼 뒤에 점(`.`)과 키 이름을 붙여 해당 키의 값을 조회합니다.
JSONPath 문자열을 작성하지 않고 JSON 컬럼의 멤버에 접근할 때 사용합니다.

```sql
json_column.key
```

```sql
-- JSON 컬럼에서 특정 키 값 추출
SELECT data.temperature AS temp FROM sensor_log;

-- WHERE 절에서 사용
SELECT * FROM sensor_log
 WHERE data.status = 'active';
```

JSONPath 문자열을 직접 지정할 때는 `data -> '$.temperature'`처럼 `->` 연산자를 사용합니다.
위의 JSON dot 표기법과 구분하여 작성합니다.

---

## JSON_SET

JSON 문서의 특정 경로에 SQL 스칼라 값을 JSON 스칼라로 저장합니다.

```sql
JSON_SET(json_doc, path, scalar)
```

- `path`는 full JSONPath(`$.key.subkey` 형식)를 사용해야 합니다.
- `JSON_SET(..., path, NULL)`은 JSON `null`을 저장합니다.
- JSON 문서 인자가 SQL `NULL`이면 결과는 SQL `NULL`입니다.
- 배열 요소 갱신(`$.items[0]`)은 지원하지 않습니다.

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
{"ship":{"status":"DONE"}}

Mach> SELECT JSON_SET('{"count":0}', '$.count', 42) FROM dual;
{"count":42}
```

---

## JSON_SET_JSON

세 번째 인자를 JSON 문자열로 해석하여 object 또는 array 서브트리를 저장합니다.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

- 세 번째 인자가 SQL `NULL`이면 결과는 SQL `NULL`입니다.
- 유효하지 않은 JSON 문자열은 오류가 발생합니다.
- 배열 요소 갱신은 지원하지 않습니다.

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
{"ship":{"owner":{"name":"machbase"}}}

Mach> SELECT JSON_SET_JSON('{"tags":{}}', '$.tags.sensors', '[1,2,3]') FROM dual;
{"tags":{"sensors":[1,2,3]}}
```

---

## JSON_REMOVE

JSON 문서에서 특정 멤버 또는 하위 경로를 제거합니다.

```sql
JSON_REMOVE(json_doc, path)
```

- `path`는 full JSONPath를 사용해야 합니다.
- 존재하지 않는 경로는 no-op으로 처리됩니다.
- `JSON_REMOVE(..., '$')`는 허용되지 않습니다.
- JSON 문서 인자가 SQL `NULL`이면 결과는 SQL `NULL`입니다.

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
{"owner":{"name":"machbase"}}

Mach> SELECT JSON_REMOVE('{"a":1,"b":2}', '$.a') FROM dual;
{"b":2}
```

---

## JSON 데이터 삽입 예시

```sql
-- JSON 타입 컬럼을 포함한 LOG 테이블
CREATE LOG TABLE device_log (
    ts    DATETIME,
    data  JSON
);

-- JSON 데이터 삽입
INSERT INTO device_log VALUES (NOW, '{"temperature":23.5,"humidity":60,"status":"active"}');

-- JSON dot 표기법으로 값 추출
SELECT ts, data.temperature AS temp
  FROM device_log
 WHERE data.status = 'active';
```

---

## 테이블 타입별 JSON 지원 현황

| 테이블 타입 | JSON 컬럼 | JSON path query | 비고 |
|------------|:---------:|:---------------:|------|
| TAG | O | O | JSON 컬럼과 JSON 함수 지원, JSON PK는 미지원 |
| LOG | O | O | 완전 지원 |
| LOOKUP | O | O | 일반 컬럼으로 지원, JSON path index는 미지원 |
| VOLATILE | X | X | JSON 컬럼 생성 불가 |
| TRANSACTION | O | O | 완전 지원 |

자세한 내용은 JSON 타입의 테이블 타입별 지원 범위를 참고하십시오.
