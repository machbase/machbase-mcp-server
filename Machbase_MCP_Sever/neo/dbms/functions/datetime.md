# 날짜/시간 함수

Machbase의 `DATETIME` 타입은 1970-01-01 00:00:00 UTC 이후 경과한 나노초 값을 내부적으로 저장합니다. 날짜/시간 함수는 이 값을 인간이 읽을 수 있는 형식으로 변환하거나 산술 연산을 수행합니다.

## 빠른 참조

| 함수 | 문법 | 설명 |
|------|------|------|
| SYSDATE / NOW | `SYSDATE`, `NOW` | 현재 시스템 시간 반환 |
| TO_DATE | `TO_DATE(str [, fmt])` | 문자열을 DATETIME으로 변환 |
| TO_DATE_SAFE | `TO_DATE_SAFE(str [, fmt])` | 변환 실패 시 NULL 반환 |
| TO_CHAR | `TO_CHAR(col [, fmt])` | DATETIME을 문자열로 변환 |
| ADD_TIME | `ADD_TIME(col, diff)` | 날짜/시간 증감 |
| DATE_TRUNC | `DATE_TRUNC(unit, col [, count])` | 지정 단위로 시간 절사 |
| DATE_BIN | `DATE_BIN(unit, count, col [, origin])` | 지정 기준으로 시간 버킷 처리 |
| DAYOFWEEK | `DAYOFWEEK(col)` | 요일 번호 반환 (0=일요일) |
| YEAR / MONTH / DAY | `YEAR(col)`, `MONTH(col)`, `DAY(col)` | 연, 월, 일 추출 |
| FROM_UNIXTIME | `FROM_UNIXTIME(unix_ts)` | Unix 타임스탬프(32비트)를 DATETIME으로 변환 |
| UNIX_TIMESTAMP | `UNIX_TIMESTAMP(col)` | DATETIME을 Unix 타임스탬프(32비트)로 변환 |
| FROM_TIMESTAMP | `FROM_TIMESTAMP(ns)` | 나노초 정수를 DATETIME으로 변환 |
| TO_TIMESTAMP | `TO_TIMESTAMP(col)` | DATETIME을 나노초 정수로 변환 |

---

## SYSDATE / NOW

현재 시스템 시간을 반환하는 의사 컬럼입니다. `SYSDATE`와 `NOW`는 동일한 값을 반환합니다.

```sql
SYSDATE
NOW
```

```sql
Mach> SELECT SYSDATE, NOW FROM t1;
SYSDATE                         NOW
-------------------------------------------------------------------
2017-01-16 14:14:53 310:973:000 2017-01-16 14:14:53 310:973:000
```

---

## TO_DATE

지정한 포맷 문자열에 따라 문자열을 `DATETIME` 타입으로 변환합니다. 포맷을 생략하면 기본값 `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`을 사용합니다.

```sql
TO_DATE(date_string [, format_string])
```

```sql
Mach> SELECT TO_DATE('2014-12-30 11:22:33 444:555:666');
2014-12-30 11:22:33 444:555:666

Mach> SELECT TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS');
1999-12-31 13:12:32 000:000:000

Mach> SELECT TO_DATE('1999', 'YYYY');
1999-01-01 00:00:00 000:000:000
```

변환 실패 시 오류 없이 NULL을 반환하는 `TO_DATE_SAFE()`도 제공합니다.

```sql
Mach> SELECT TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD');
NULL
```

---

## TO_CHAR (DATETIME)

`DATETIME` 컬럼 값을 임의의 문자열로 변환합니다. 포맷을 생략하면 기본값 `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`을 사용합니다.

```sql
TO_CHAR(datetime_col [, format_string])
```

### 포맷 문자열

| 포맷 표현식 | 설명 |
|------------|------|
| `YYYY` | 연도 4자리 |
| `YY` | 연도 2자리 |
| `MM` | 월 2자리 (`01~12`) |
| `MON` | 월 3자리 영문 약어 (JAN, FEB, ...) |
| `DD` | 일 2자리 |
| `DAY` | 요일 3자리 영문 약어 (SUN, MON, ...) |
| `IW` | ISO 8601 주차 (`1~53`, 월요일 기준) |
| `WW` | 연간 주차 (`1~53`, 요일 무관) |
| `W` | 월간 주차 (`1~5`, 요일 무관) |
| `HH` | 시간 2자리 |
| `HH12` | 시간 12시간제 (`1~12`) |
| `HH24` | 시간 24시간제 (`0~23`) |
| `HH2`, `HH3`, `HH6` | 지정 단위로 시간 절사 |
| `MI` | 분 2자리 |
| `MI2`, `MI5`, `MI10`, `MI20`, `MI30` | 지정 단위로 분 절사 |
| `SS` | 초 2자리 |
| `SS2`, `SS5`, `SS10`, `SS20`, `SS30` | 지정 단위로 초 절사 |
| `AM` | AM/PM |
| `mmm` | 밀리초 3자리 (`0~999`) |
| `uuu` | 마이크로초 3자리 (`0~999`) |
| `nnn` | 나노초 3자리 (`0~999`) |

```sql
Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
2014-12-30 11:22:33
2013-11-11 01:02:03

Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
2014-12-30 11:22:33 444.555.666
```

---

## ADD_TIME

`DATETIME` 컬럼에 년/월/일/시/분/초 단위의 증감 연산을 수행합니다. 밀리초·마이크로초·나노초 단위는 지원하지 않습니다.

```sql
ADD_TIME(column, time_diff_format)
```

`time_diff_format` 형식: `"Year/Month/Day Hour:Minute:Second"` (각 항목은 양수 또는 음수)

```sql
-- 1년 후
Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM t;

-- 1시간 1분 1초 후
Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM t;

-- 1년 1개월 1일 전
Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM t;
```

---

## DATE_TRUNC

주어진 `DATETIME` 값을 지정 시간 단위로 절사하여 반환합니다. `count`를 지정하면 해당 배수 단위로 절사합니다.

```sql
DATE_TRUNC(field, date_val [, count])
```

### 지원 시간 단위 및 최대 범위

| 시간 단위 | 최대 범위 |
|-----------|----------|
| `nanosecond` (`nsec`) | 1,000,000,000 (1초) |
| `microsecond` (`usec`) | 60,000,000 (60초) |
| `millisecond` (`msec`) | 60,000 (60초) |
| `second` (`sec`) | 86,400 (1일) |
| `minute` (`min`) | 1,440 (1일) |
| `hour` | 24 (1일) |
| `day` | 1 |
| `week` | 1 (일요일 시작) |
| `month` | 1 |
| `year` | 1 |

```sql
-- 초 단위 절사
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM t GROUP BY tm ORDER BY 2;

-- 2초 단위 절사
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM t GROUP BY tm ORDER BY 2;

-- 2분 단위 절사 (DATE_TRUNC('second', time, 120)과 동일)
Mach> SELECT COUNT(*), DATE_TRUNC('minute', ts, 2) tm FROM t GROUP BY tm;
```

---

## DATE_BIN

지정한 기준 시각(`origin`)을 기준으로 `DATETIME` 값을 시간 단위와 범위로 버킷 처리합니다. `origin`을 생략하면 로컬 타임존 기준 `1970-01-01 00:00:00`을 사용합니다.

```sql
DATE_BIN(field, count, source [, origin])
```

```sql
-- 2시간 버킷 (특정 origin 기준)
SELECT DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;

-- 3시간 버킷 (로컬 타임존 경계 기준)
SELECT DATE_BIN('hour', 3, ts) FROM t ORDER BY ts;
```

---

## DAYOFWEEK

`DATETIME` 값의 요일을 정수로 반환합니다.

```sql
DAYOFWEEK(date_val)
```

| 반환값 | 요일 |
|--------|------|
| 0 | 일요일 |
| 1 | 월요일 |
| 2 | 화요일 |
| 3 | 수요일 |
| 4 | 목요일 |
| 5 | 금요일 |
| 6 | 토요일 |

```sql
SELECT DAYOFWEEK(dt) FROM log_table;
```

---

## YEAR / MONTH / DAY

입력 `DATETIME` 값에서 연, 월, 일을 추출해 정수로 반환합니다.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
---------------------------------
2001        1           1
```

---

## FROM_UNIXTIME / UNIX_TIMESTAMP

`FROM_UNIXTIME`은 32비트 Unix 타임스탬프 정수를 `DATETIME`으로 변환합니다. `UNIX_TIMESTAMP`는 반대로 `DATETIME`을 32비트 Unix 타임스탬프로 변환합니다.

```sql
FROM_UNIXTIME(unix_timestamp_value)
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671);
1980-01-01 11:11:11 000:000:000

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
Mach> SELECT * FROM unix_table;
C1
-----------
978274800
```

---

## FROM_TIMESTAMP / TO_TIMESTAMP

`FROM_TIMESTAMP`는 UTC 기준 1970-01-01 00:00:00부터 경과한 나노초 정수를 `DATETIME`으로 변환합니다.
`TO_TIMESTAMP`는 반대로 `DATETIME`을 같은 기준 시점부터 경과한 나노초 정수로 변환합니다.

기준 시점은 UTC+09:00에서 1970-01-01 09:00:00으로 표시됩니다.
아래 예제의 날짜와 시각은 UTC+09:00 기준입니다.

```sql
FROM_TIMESTAMP(nanosecond_time_value)
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869);
2019-07-05 13:56:00 007:248:869

Mach> SELECT TO_TIMESTAMP(c1) FROM datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
```

나노초 단위 산술 연산 예시:

```sql
-- 현재 시각에서 1ms (1,000,000 ns) 전
SELECT FROM_TIMESTAMP(SYSDATE - 1000000) FROM t;
```
