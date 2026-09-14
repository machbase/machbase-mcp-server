# 정규식 함수

Machbase는 PCRE(Perl Compatible Regular Expressions) 기반의 정규식 함수를 제공합니다. 모든 정규식 함수는 `VARCHAR` 타입 컬럼에서만 동작합니다.

## 빠른 참조

| 함수 | 문법 | 설명 |
|------|------|------|
| REGEXP_LIKE | `REGEXP_LIKE(src, pat [, flag])` | 패턴 일치 여부 확인 |
| REGEXP_INSTR | `REGEXP_INSTR(src, pat [, pos [, occ [, ret [, flag]]]])` | 패턴 일치 위치 반환 |
| REGEXP_SUBSTR | `REGEXP_SUBSTR(src, pat [, pos [, occ [, flag]]])` | 패턴 일치 부분 문자열 추출 |
| REGEXP_REPLACE | `REGEXP_REPLACE(src, pat [, repl [, pos [, occ [, flag]]]])` | 패턴 일치 문자열 치환 |

### match_param (공통 파라미터)

| 값 | 설명 |
|----|------|
| `'c'` | 대소문자 구분 (기본값) |
| `'i'` | 대소문자 무시 |

---

## REGEXP_LIKE

문자열이 정규식 패턴과 일치하는지 검사합니다. `WHERE` 절에서 주로 사용하며 Boolean(1/0)을 반환합니다.

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`: 검사할 `VARCHAR` 컬럼 또는 식
- `pattern`: 상수 `VARCHAR` 정규식
- `match_param`: `'c'`(대소문자 구분, 기본) 또는 `'i'`(대소문자 무시)

```sql
-- 'error' 또는 'warn'을 포함하는 메시지 조회 (대소문자 무시)
SELECT *
  FROM sensor_text
 WHERE REGEXP_LIKE(message, 'error|warn', 'i');

-- 숫자로 시작하는 코드 조회
SELECT *
  FROM event_log
 WHERE REGEXP_LIKE(code, '^[0-9]+');

-- 이메일 형식 검증
SELECT name
  FROM users
 WHERE REGEXP_LIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
```

---

## REGEXP_INSTR

정규식과 일치하는 위치를 반환합니다. 일치하는 값이 없으면 `0`을 반환합니다. 위치는 1부터 시작합니다.

```sql
REGEXP_INSTR(source, pattern)
REGEXP_INSTR(source, pattern, position)
REGEXP_INSTR(source, pattern, position, occurrence)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos, match_param)
```

| 파라미터 | 설명 |
|---------|------|
| `source` | 검사할 `VARCHAR` |
| `pattern` | 상수 `VARCHAR` 정규식 |
| `position` | 검색 시작 위치 (1 이상, 기본값: 1) |
| `occurrence` | 찾을 몇 번째 일치 (1 이상, 기본값: 1) |
| `return_pos` | `0`: 시작 위치, `1`: 일치 문자열 다음 위치 |
| `match_param` | `'c'` 또는 `'i'` |

```sql
-- 'The' 패턴의 위치 반환 (대소문자 무시, 첫 번째 발견, 다음 위치)
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
-- 결과: 10 (일치 문자열 'The' 다음 위치)
```

---

## REGEXP_SUBSTR

정규식과 일치하는 부분 문자열을 반환합니다. 일치하는 값이 없으면 NULL을 반환합니다.

```sql
REGEXP_SUBSTR(source, pattern)
REGEXP_SUBSTR(source, pattern, position)
REGEXP_SUBSTR(source, pattern, position, occurrence)
REGEXP_SUBSTR(source, pattern, position, occurrence, match_param)
```

| 파라미터 | 설명 |
|---------|------|
| `source` | 검사할 `VARCHAR` |
| `pattern` | 상수 `VARCHAR` 정규식 |
| `position` | 검색 시작 위치 (1 이상, 기본값: 1) |
| `occurrence` | 찾을 몇 번째 일치 (1 이상, 기본값: 1) |
| `match_param` | `'c'` 또는 `'i'` |

```sql
-- 두 번째 모음 추출 (대소문자 무시)
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
-- 결과: 'O'

-- IP 주소에서 첫 번째 옥텟 추출
SELECT REGEXP_SUBSTR(ip_str, '[0-9]+', 1, 1) FROM log_table;

-- 로그에서 오류 코드 추출
SELECT REGEXP_SUBSTR(message, 'ERR-[0-9]+') FROM event_log;
```

---

## REGEXP_REPLACE

정규식과 일치하는 문자열을 지정한 문자열로 치환합니다.

```sql
REGEXP_REPLACE(source, pattern)
REGEXP_REPLACE(source, pattern, replacement)
REGEXP_REPLACE(source, pattern, replacement, position)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence, match_param)
```

| 파라미터 | 설명 |
|---------|------|
| `source` | 대상 `VARCHAR` |
| `pattern` | 상수 `VARCHAR` 정규식 |
| `replacement` | 치환 문자열 (생략 시 일치 문자열 제거) |
| `position` | 검색 시작 위치 (1 이상, 기본값: 1) |
| `occurrence` | `0`: 모든 일치 치환, 양수 n: n번째 일치만 치환 (기본값: 0) |
| `match_param` | `'c'` 또는 `'i'` |

```sql
-- 두 번째 모음을 'Z'로 치환 (대소문자 무시)
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
-- 결과: 'TechZnTheNet'

-- 모든 숫자 제거
SELECT REGEXP_REPLACE(code, '[0-9]', '') FROM log_table;

-- 공백 정규화 (연속 공백을 단일 공백으로)
SELECT REGEXP_REPLACE(message, '\s+', ' ') FROM event_log;
```

---

## PCRE 정규식 기초

| 패턴 | 설명 | 예시 |
|------|------|------|
| `.` | 임의의 문자 1개 | `a.c` → abc, aXc |
| `*` | 0회 이상 반복 | `ab*c` → ac, abc, abbc |
| `+` | 1회 이상 반복 | `ab+c` → abc, abbc |
| `?` | 0 또는 1회 | `colou?r` → color, colour |
| `^` | 문자열 시작 | `^error` |
| `$` | 문자열 끝 | `\.log$` |
| `[abc]` | 문자 클래스 | `[aeiou]` |
| `[^abc]` | 부정 문자 클래스 | `[^0-9]` |
| `\d` | 숫자 (`[0-9]`) | `\d+` |
| `\w` | 단어 문자 | `\w+` |
| `\s` | 공백 문자 | `\s+` |
| `a\|b` | a 또는 b | `error\|warn` |
| `(abc)` | 그룹 | `(foo)+` |
| `{n,m}` | n~m회 반복 | `\d{3,5}` |

---

## SEARCH / ESEARCH와의 차이

| 기능 | REGEXP_LIKE | SEARCH / ESEARCH |
|------|:-----------:|:----------------:|
| 적용 타입 | `VARCHAR` | `TEXT` (전문 검색 인덱스) |
| 정규식 지원 | O (PCRE) | X (키워드 검색) |
| 인덱스 활용 | X | O |
| 대용량 텍스트 | 제한적 | 권장 |

대용량 텍스트에서 키워드 검색이 필요하면 `TEXT` 타입과 `SEARCH` 절을 사용하는 것이 성능 면에서 유리합니다. 정규식 패턴 매칭이 필요한 경우 `VARCHAR` 컬럼과 `REGEXP_LIKE`를 사용합니다.
