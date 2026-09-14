# 전체 함수 레퍼런스

## 오류 처리

|오류 유형|코드|발생 조건|
|---|---|---|
|인자 타입 오류|`ERR-02036`, `ERR-02037`|숫자 타입이 아닌 값을 넣었거나 `PI`에 인자를 전달한 경우|
|실행 오류|`ERR-02317`|`SQRT`의 음수 입력, `MOD`의 0 나누기, `LOG`의 잘못된 밑/값, `EXP`/`POWER`의 범위 초과 등|

입력이 `NULL`이면 결과도 `NULL`입니다.

## ABS

숫자형 컬럼의 절댓값을 실수로 반환합니다.

```sql
ABS(column_expr)
```

```sql
Mach> CREATE LOG TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO abs_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(2, 2.0, 'sqltest');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(3, 3.0, 'sqltest');
1 row(s) inserted.

Mach> SELECT ABS(c1), ABS(c2) FROM abs_table;
SELECT ABS(c1), ABS(c2) from abs_table;
ABS(c1)                     ABS(c2)
-----------------------------------------------------------
3                           3
2                           2
1                           1
[3] row(s) selected.
```

## ADD_TIME

DATETIME 컬럼에 년/월/일/시/분/초 단위의 증감 연산을 수행합니다. 밀리초, 마이크로초, 나노초 단위는 지원하지 않습니다. Diff 형식은 `"Year/Month/Day Hour:Minute:Second"`이며, 각 항목은 양수 또는 음수를 사용할 수 있습니다.

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE LOG TABLE add_time_table (id INTEGER, dt DATETIME);
Created successfully.

Mach> INSERT INTO  add_time_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(2, TO_DATE('2000-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(3, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(4, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(5, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(6, TO_DATE('2014-12-30 23:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/0/0 0:0:0')
----------------------------------
2015-12-30 23:22:33 444:555:666
2015-12-30 11:22:33 444:555:666
2014-11-11 01:02:03 004:005:006
2013-11-11 01:02:03 004:005:006
2001-11-11 01:02:03 004:005:006
2000-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 1:1:1')
----------------------------------
2014-12-31 00:23:34 444:555:666
2014-12-30 12:23:34 444:555:666
2013-11-11 02:03:04 004:005:006
2012-11-11 02:03:04 004:005:006
2000-11-11 02:03:04 004:005:006
1999-11-11 02:03:04 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '1/1/1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/1/1 0:0:0')
----------------------------------
2016-01-31 23:22:33 444:555:666
2016-01-31 11:22:33 444:555:666
2014-12-12 01:02:03 004:005:006
2013-12-12 01:02:03 004:005:006
2001-12-12 01:02:03 004:005:006
2000-12-12 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/0/0 0:0:0')
----------------------------------
2013-12-30 23:22:33 444:555:666
2013-12-30 11:22:33 444:555:666
2012-11-11 01:02:03 004:005:006
2011-11-11 01:02:03 004:005:006
1999-11-11 01:02:03 004:005:006
1998-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 -1:-1:-1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 -1:-1:-1')
----------------------------------
2014-12-30 22:21:32 444:555:666
2014-12-30 10:21:32 444:555:666
2013-11-11 00:01:02 004:005:006
2012-11-11 00:01:02 004:005:006
2000-11-11 00:01:02 004:005:006
1999-11-11 00:01:02 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/-1/-1 0:0:0')
----------------------------------
2013-11-29 23:22:33 444:555:666
2013-11-29 11:22:33 444:555:666
2012-10-10 01:02:03 004:005:006
2011-10-10 01:02:03 004:005:006
1999-10-10 01:02:03 004:005:006
1998-10-10 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-1/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
[2] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1') FROM add_time_table;
ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1')
------------------------------------------
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.
```

## APPROX_PERCENTILE

```
APPROX_PERCENTILE
APPROX_MEDIAN
APPROX_P05
APPROX_P10
APPROX_P90
APPROX_P95
```

이 함수들은 원시 값을 모두 정렬하지 않고 제한된 크기의 summary를 유지해 분위값을 근사합니다. 입력 데이터가 매우 크고, 작은 오차를 허용할 수 있을 때 유용합니다.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- 반환 타입은 `DOUBLE`입니다.
- `NULL` 값은 무시합니다.

`APPROX_MEDIAN(value)`는 근사 중앙값이며, `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, `APPROX_P95`는 자주 쓰는 분위값을 위한 축약형입니다.

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```

## ARRAY_LENGTH

`ARRAY_LENGTH(array_value)`는 non-NULL `ARRAY`의 선언 cardinality를 반환합니다.

```sql
SELECT ARRAY_LENGTH(ARRAY[10, NULL, 30]);
-- 3
```

모든 요소가 NULL이어도 cardinality를 반환합니다. whole NULL은 NULL을 반환하며, 타입
정보가 없는 `ARRAY_LENGTH(NULL)`은 오류입니다. 자세한 ARRAY 문법과 제약은
숫자 ARRAY 타입을 참고하십시오.

## ARRAY_SPARSE

`ARRAY_SPARSE`는 고정 길이 `ARRAY`에서 값이 있는 위치만 지정합니다. 위치는 0부터
시작하며, 생략한 위치는 element NULL입니다.

```sql
-- 대상 컬럼에서 타입과 cardinality를 결정합니다.
INSERT INTO sensor_array (id, channels)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));

-- 대상이 없는 표현식은 타입과 cardinality를 명시합니다.
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);

-- bracket 축약형은 가장 큰 position + 1로 cardinality를 추론합니다.
SELECT [1 => 12, 33 => 23];
```

bracket 축약형은 대상 ARRAY가 있으면 대상 타입과 cardinality를 사용합니다. standalone
표현식이면 dense ARRAY와 같은 숫자 공통 타입을 사용하고 가장 큰 position에 1을 더해
cardinality를 정합니다. target 없는 all-NULL sparse, 중복 또는 범위 밖 position은
오류입니다. 입력 방식과 SDK sparse 객체는
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

## AREA

`AREA(y, x)`는 숫자형 `(x, y)` 점들로 이루어진 곡선 아래 면적을 정확하게 계산하는 집계 함수입니다.

```sql
AREA(y, x)
```

- 두 인자는 모두 숫자형이어야 합니다.
- 둘 중 하나라도 `NULL`인 행은 무시합니다.
- 유효한 점이 2개 미만이면 결과는 `NULL`입니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```

## AVG

숫자형 컬럼의 평균값을 반환하는 집계 함수입니다.

```sql
AVG(column_name)
```

```sql
Mach> CREATE LOG TABLE avg_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO avg_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
-------------------------------------------
2                2
NULL             4
1                2
```

## BITAND / BITOR

두 정수 값을 64비트 부호 있는 정수로 변환한 뒤 비트 단위 AND/OR 연산 결과를 반환합니다. 입력은 정수형이어야 하며, 출력도 64비트 부호 있는 정수입니다.

0보다 작은 정수 값의 경우, 플랫폼에 따라 다른 결과가 나올 수 있으므로 uinteger 및 ushort 타입만 사용하는 것을 권장합니다.

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE LOG TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
Created successfully.

Mach> INSERT INTO bit_table VALUES (-1, 1, 1, 1, 2, 'aaa');
1 row(s) inserted.

Mach> INSERT INTO bit_table VALUES (-2, 2, 2, 2, 3, 'bbb');
1 row(s) inserted.

Mach> SELECT BITAND(i1, i2) FROM bit_table;
BITAND(i1, i2)
-----------------------
2
1
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT BITOR(i5, 1) FROM bit_table WHERE BITOR(i5, 1) = 3;
BITOR(i5, 1)
-----------------------
3
3
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i3, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i4, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITAND(i5, 1) FROM bit_table WHERE BITAND(i5, 1) = 1;
BITAND(i5, 1)
-----------------------
1
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i6, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i2) FROM bit_table;
BITOR(i1, i2)
-----------------------
-2
-1
[2] row(s) selected.

Mach> SELECT BITAND(i1, i3) FROM bit_table;
BITAND(i1, i3)
-----------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i6) FROM bit_table;
BITOR(i1, i6)
-----------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.
```

## CAST

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

`CAST`는 값, 컬럼 또는 표현식을 지정한 데이터 타입으로 명시적으로 변환합니다. `SELECT`,
조건식, `CASE`, `UNION ALL`, VIEW 정의와 prepared statement에서 사용할 수 있습니다.

### 문법

```sql
CAST(expression AS data_type)
CAST(expression AS data_type(length))
CAST(expression AS DECIMAL(precision[, scale]))
CAST(array_expression AS numeric_type[cardinality])
CAST(array_expression AS DECIMAL(precision[, scale])[cardinality])
```

- `expression`은 변환할 값, 컬럼 또는 SQL 표현식입니다.
- `array_expression`은 숫자 `ARRAY` 또는 SQL `NULL`입니다.
- `data_type`은 아래 표의 대상 타입 또는 별칭입니다.
- 타입 이름은 대소문자를 구분하지 않습니다.
- `length`, `precision`, `scale`은 대상 타입에서 허용할 때만 지정할 수 있습니다.
- ARRAY 입력과 대상의 `cardinality`는 정확히 같아야 합니다.

### 지원 타입과 별칭

| 분류 | 대상 타입 | 사용할 수 있는 이름 |
|------|-----------|---------------------|
| 부호 있는 정수 | 16비트 | `INT16`, `SHORT` |
|  | 32비트 | `INT32`, `INT`, `INTEGER` |
|  | 64비트 | `INT64`, `LONG` |
| 부호 없는 정수 | 16비트 | `UINT16`, `USHORT` |
|  | 32비트 | `UINT32`, `UINTEGER` |
|  | 64비트 | `UINT64`, `ULONG` |
| 실수 | 단정밀도·배정밀도 | `FLOAT`, `DOUBLE` |
| 고정소수 | DECIMAL | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| 문자 | 고정 길이·가변 길이 | `CHAR`, `VARCHAR` |
| 문자 LOB | 텍스트 | `TEXT`, `CLOB` |
| 날짜와 시간 | 나노초 정밀도 | `DATETIME` |
| 네트워크 주소 | IP 주소 | `IPV4`, `IPV6` |
| 바이너리 | 바이너리·바이너리 LOB | `BINARY`, `BLOB` |
| 문서 | JSON | `JSON` |

같은 행의 이름은 같은 타입으로 동작합니다. 예를 들어 `INTEGER`, `INT`, `INT32`는 모두
32비트 부호 있는 정수입니다. 결과 컬럼의 타입 메타데이터에는 표준 타입 이름이 표시될 수
있습니다.

### 길이와 정밀도

#### CHAR, VARCHAR, BINARY

| 타입 | 길이 생략 시 기본값 | 허용 길이 | 길이 초과 처리 |
|------|-------------------:|-----------|----------------|
| `CHAR(n)` | 1 byte | 1~32,767 byte | 앞에서부터 `n` byte 보존 |
| `VARCHAR(n)` | 32,767 byte | 1~32,767 byte | 앞에서부터 `n` byte 보존 |
| `BINARY(n)` | 1 byte | 1~67,108,864 byte | 앞에서부터 `n` byte 보존 |

길이는 문자 수가 아니라 byte 수입니다. UTF-8 문자열을 변환할 때는 다중 byte 문자가 중간에서
잘릴 수 있으므로 충분한 길이를 지정하십시오. `CHAR`는 남는 공간을 공백으로 채우지
않습니다. `CAST(... AS CHAR(n))`의 결과 메타데이터는 현재 `VARCHAR(n)`으로 표시됩니다.

```sql
SELECT '[' || CAST('abc' AS CHAR) || ']' AS char_default;
-- [a]

SELECT '[' || CAST('abc' AS CHAR(5)) || ']' AS char_value;
-- [abc] (공백을 추가하지 않음)

SELECT CAST('abcdef' AS VARCHAR(3)) AS varchar_value;
-- abc

SELECT CAST('414243' AS BINARY(2)) AS binary_value;
-- 4142
```

`TEXT`, `CLOB`, `BLOB`, `JSON`에는 `length`를 지정할 수 없습니다. 이 타입들의 CAST 결과는
현재 최대 32,767 byte를 지원하며, 허용된 길이 제한을 넘어 결과 의미가 손상되는 경우에는
자동으로 자르지 않고 오류를 반환합니다.

#### DECIMAL

| 구문 | 해석 |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(p)` | `DECIMAL(p,0)` |
| `DECIMAL(p,s)` | precision `p`, scale `s` |

- precision `p`는 `1~65`입니다.
- scale `s`는 `0~30`이며 precision보다 클 수 없습니다.
- 입력 값의 소수 자릿수가 scale보다 많으면 0에서 멀어지는 방향의 절반 올림을 적용합니다.
- DECIMAL 계열 이외의 타입에는 precision 또는 scale을 지정할 수 없습니다.

```sql
SELECT CAST('12.34' AS DECIMAL(5,2));
-- 12.34

SELECT CAST(123.456 AS NUMERIC(6,2));
-- 123.46
```

### NULL과 빈 문자열

- 입력이 `NULL`이면 대상 타입의 `NULL`을 반환합니다.
- Machbase에서는 길이가 0인 문자열 리터럴 `''`을 SQL `NULL`로 처리합니다.
- `''''`는 작은따옴표 한 글자를 나타내는 문자열이므로 빈 문자열이 아닙니다.

```sql
SELECT CAST(NULL AS INTEGER) AS null_integer;
SELECT CAST('' AS VARCHAR(10)) AS empty_value;
SELECT CAST('''' AS VARCHAR(10)) AS quote_value;
```

### 숫자 변환

숫자 타입끼리 변환하거나 숫자로 해석할 수 있는 문자열을 숫자 타입으로 변환할 수 있습니다.

```sql
SELECT CAST('123' AS INTEGER);
SELECT CAST('1.25' AS DOUBLE);
SELECT CAST(12.9 AS SHORT);       -- 12
SELECT CAST(-12.9 AS INTEGER);    -- -12
SELECT CAST('9223372036854775806e0' AS LONG);
```

- 실수를 정수로 변환할 때 소수부는 반올림하지 않고 0 방향으로 버립니다.
- 정수 문자열의 지수 표기도 정수 정밀도를 유지해 해석합니다.
- 대상 타입의 범위를 벗어나는 값은 오류입니다.
- 부호 없는 정수로 변환할 때 음수 결과는 허용하지 않습니다. 소수부를 버린 결과가 0인
  값은 0으로 변환할 수 있습니다.
- `NaN`, 양의 무한대, 음의 무한대는 정수 변환에 사용할 수 없습니다.

CAST로 만들 수 있는 정수 범위는 다음과 같습니다. 각 타입의 NULL 예약값은 유효한 결과
범위에 포함되지 않습니다.

| 대상 타입 | CAST 결과 범위 |
|-----------|----------------|
| `INT16`, `SHORT` | -32,767~32,767 |
| `UINT16`, `USHORT` | 0~65,534 |
| `INT32`, `INT`, `INTEGER` | -2,147,483,647~2,147,483,647 |
| `UINT32`, `UINTEGER` | 0~4,294,967,294 |
| `INT64`, `LONG` | -9,223,372,036,854,775,807~9,223,372,036,854,775,807 |
| `UINT64`, `ULONG` | 0~18,446,744,073,709,551,614 |

### 숫자 ARRAY 전체 변환

같은 cardinality의 숫자 `ARRAY`는 요소 타입을 전체 변환할 수 있습니다. 대상에는
`INT16`, `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `FLOAT`, `DOUBLE`, `DECIMAL`과
지원 타입 표의 숫자 별칭을 사용합니다.

```sql
SELECT CAST([1.9, NULL, -3.9] AS INT32[3]);
SELECT CAST([1.235, NULL, -2.345] AS DECIMAL(6,2)[3]);
```

- whole NULL은 변환 뒤에도 whole NULL입니다.
- element NULL은 같은 위치의 element NULL로 유지됩니다.
- 각 non-NULL 요소에는 대응하는 scalar 숫자 CAST의 절삭, 반올림과 범위 규칙을
  적용합니다.
- 한 요소라도 변환할 수 없으면 CAST와 이를 포함한 문장 전체가 실패합니다. 변환된 일부
  요소나 행을 결과로 남기지 않습니다.
- `DECIMAL[N]`은 `DECIMAL(10,0)[N]`, `DECIMAL(p)[N]`은 `DECIMAL(p,0)[N]`으로
  처리합니다.

prepared statement에서도 CAST 대상이 parameter의 요소 타입, cardinality와 DECIMAL
precision/scale을 결정합니다. 같은 statement에 dense ARRAY, sparse ARRAY와 whole NULL을
다시 bind할 수 있습니다.

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

scalar를 ARRAY로 확장하거나 ARRAY를 scalar로 축소할 수 없습니다. 서로 다른 cardinality
사이에 padding 또는 truncation하지 않으며 문자열, 날짜, IP, BINARY, JSON ARRAY를
대상으로 지정할 수 없습니다.

### 문자열 및 LOB 변환

숫자, 날짜와 시간, IP 주소, 바이너리, JSON을 문자 타입으로 변환할 수 있습니다.

- 정수와 DECIMAL은 값의 10진수 표현을 반환합니다.
- `FLOAT`는 최대 9자리, `DOUBLE`은 최대 17자리의 유효 숫자를 사용해 표현합니다.
- `DATETIME`은 세션의 날짜 형식과 시간대에 따라 문자열로 표시됩니다.
- `IPV4`와 `IPV6`은 표준화된 주소 문자열로 표시됩니다.
- `BINARY`와 `BLOB`은 접두사 없는 대문자 16진수 문자열로 표시됩니다.
- JSON은 원문의 JSON 표현을 유지합니다.

```sql
SELECT CAST(123456 AS VARCHAR(8));
-- 123456

SELECT CAST(CAST('2001:db8::1' AS IPV6) AS VARCHAR(64));

SELECT CAST(CAST('0x00ff10' AS BLOB) AS VARCHAR(8));
-- 00FF10
```

문자열을 `BINARY` 또는 `BLOB`으로 변환할 때는 접두사 없는 짝수 길이 16진수 또는
`0x`/`0X` 접두사가 있는 짝수 길이 16진수를 사용합니다.

```sql
SELECT CAST('414243' AS BINARY(3));
SELECT CAST('0x00ff10' AS BLOB);
SELECT CAST(X'414243' AS VARCHAR(6));
```

`BINARY(n)`은 앞에서부터 `n` byte만 보존합니다. 16진수가 아닌 문자나 홀수 길이
16진수는 오류입니다.

### DATETIME 변환

문자열 또는 숫자를 `DATETIME`으로 변환할 수 있습니다.

- 문자열은 session의 기본 날짜 형식과 시간대를 사용해 해석합니다.
- 숫자는 Unix epoch 기준 nanosecond로 해석합니다.
- 숫자 `-1`은 DATETIME의 NULL 표시용 예약값이므로 변환할 수 없습니다.
- `DATETIME`을 숫자로 변환하면 Unix epoch 기준 nanosecond 값을 반환합니다.

```sql
SELECT CAST('2026-08-15 12:34:56' AS DATETIME);
SELECT CAST(1000000000 AS DATETIME);
SELECT CAST(CAST(1000000000 AS DATETIME) AS VARCHAR(40));
```

같은 epoch 값도 session timezone이 다르면 문자열로 표시되는 날짜와 시간이 달라질 수
있습니다.

### IPV4와 IPV6 변환

문자열을 `IPV4` 또는 `IPV6`으로 변환할 수 있습니다. 주소 전체가 올바른 형식이어야 합니다.

```sql
SELECT CAST('127.0.0.1' AS IPV4);
SELECT CAST('2001:db8::1' AS IPV6);
```

잘못된 주소나 대상 타입과 맞지 않는 주소 형식은 오류입니다.

### JSON 변환

문자열을 `JSON`으로 변환할 때는 입력 전체가 유효한 JSON이어야 합니다. 객체와 배열뿐
아니라 JSON 문자열, 숫자, `true`, `false`, `null`도 사용할 수 있습니다.

```sql
SELECT CAST('{"ok":true}' AS JSON);
SELECT CAST('[1,2,3]' AS JSON);
SELECT CAST('"abc"' AS JSON);
SELECT CAST(CAST('"abc"' AS JSON) AS VARCHAR(16));
-- "abc"
```

일부만 유효한 JSON이거나 JSON이 아닌 문자가 뒤에 남아 있으면 변환할 수 없습니다.

### 표현식과 결과 메타데이터

CAST는 일반 SQL 표현식이므로 WHERE 조건, `CASE`, `UNION ALL`, VIEW 정의에서도 사용할 수
있습니다.

```sql
SELECT CASE
         WHEN reading >= 0 THEN CAST(reading AS VARCHAR(32))
         ELSE 'invalid'
       END AS reading_text
  FROM sensor_log;

CREATE VIEW sensor_cast_view AS
SELECT CAST(sensor_id AS VARCHAR(100)) AS sensor_id_text,
       CAST(value AS DECIMAL(12,3)) AS value_decimal
  FROM sensor_log;
```

prepared statement에서도 CAST 구문은 동일합니다. 입력값은 `?` 또는 SDK가 제공하는 named
marker로 전달하고, 대상 타입과 precision/scale은 SQL에 선언합니다.

```sql
SELECT CAST(? AS DECIMAL(12,2)) AS amount;
```

CAST 결과의 타입, byte 길이, DECIMAL precision과 scale은 결과 메타데이터와 VIEW 컬럼
정보에 반영됩니다. 결과의 NULL 가능 여부는 입력 표현식의 NULL 가능 여부를 따릅니다.

`CASE` 또는 `UNION ALL`에서 ARRAY 결과를 결합하려면 요소 타입, cardinality와 DECIMAL
precision/scale이 모두 같아야 합니다. 서로 다르면 각 결과를 명시적으로 같은 ARRAY
타입으로 CAST한 뒤 결합합니다.

각 SDK는 기존 결과 메타데이터 API로 CAST 결과를 확인합니다. CAST 전용 SDK API는 제공하지
않습니다.

| SDK | CAST 결과 metadata API |
|-----|------------------------|
| Machbase SQLCLI | `SQLDescribeCol()`, `SQLColAttribute()` |
| ODBC | `SQLDescribeCol()`, `SQLColAttribute()` |
| JDBC | `ResultSetMetaData` |
| Python | `cursor.description` |
| Node.js | `ColumnMeta` |
| .NET | `GetSchemaTable()` |
| Go (native) | native column metadata |
| Go (`database/sql`) | `ColumnTypeNullable()` 및 `ColumnType` API |

### 오류가 발생하는 경우

| 원인 | 예 |
|------|-----|
| 지원하지 않는 대상 타입 | `CAST('1' AS UNKNOWN_TYPE)` |
| 허용되지 않은 length 또는 precision/scale | `CAST('1' AS INTEGER(2))`, `CAST('1' AS DECIMAL(2,3))` |
| 숫자 범위 초과 또는 NULL 예약값 | `CAST('65535' AS USHORT)` |
| 부호 없는 정수로 변환되는 음수 | `CAST('-1' AS UINTEGER)` |
| 숫자로 변환할 수 없는 문자열 | `CAST('12x' AS INTEGER)` |
| scalar와 ARRAY 사이의 변환 | `CAST(1 AS INT32[1])`, `CAST([1] AS INT32)` |
| ARRAY cardinality 불일치 | `CAST([1, 2] AS INT32[3])` |
| 지원하지 않는 ARRAY 대상 타입 | `CAST([1] AS VARCHAR[1])` |
| 잘못된 IP 주소 | `CAST('999.1.1.1' AS IPV4)` |
| 홀수 길이 또는 비16진수 바이너리 문자열 | `CAST('123' AS BINARY(4))`, `CAST('GG' AS BLOB)` |
| 유효하지 않은 JSON | `CAST('{bad}' AS JSON)` |
| 허용 크기를 초과하는 LOB 또는 JSON 결과 | 32,767 byte를 초과하는 `TEXT`, `CLOB`, `BLOB`, `JSON` 결과 |

### 호환성

CAST 함수와 숫자 ARRAY 전체 CAST는 Machbase 8.7.0에서 지원됩니다. Standard Edition과
Cluster Edition에서 사용할 수 있으며, Cluster Edition에서는 모든 cluster node가 CAST를
지원하는 동일 버전이어야 합니다. CAST를 지원하지 않는 구버전 node와의 혼합 실행은
지원하지 않습니다.

### 관련 문서

- SQL 문법 사전
- 데이터 타입 사전
- 숫자 ARRAY 타입
- DECIMAL과 NUMERIC 고정소수점 타입

## COUNT

컬럼의 레코드 개수를 구하는 집계 함수입니다.

```sql
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO count_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
-----------------------
7
[1] row(s) selected.

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------------------
6
[1] row(s) selected.
```

## CUME_DIST

`CUME_DIST(value, threshold)`는 `value`가 `threshold` 이하인 행의 누적 비율을 반환합니다.

```sql
CUME_DIST(value, threshold)
```

- 윈도우 함수가 아닌 집계 함수입니다.
- 두 인자는 모두 숫자형이어야 합니다.
- `threshold`는 상수여야 합니다.
- 반환 값은 `0.0` 이상 `1.0` 이하의 `DOUBLE`입니다.

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```

## CURRENT_USER / SESSION_USER / CURRENT_USER_ID / SESSION_USER_ID

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

현재 SQL 실행의 유효 권한 사용자와 접속 세션 사용자를 이름 또는 내부 ID로 조회합니다.
Standard Edition과 Cluster Edition에서 모두 지원합니다.

| 함수 | 반환형 | 설명 |
|---|---|---|
| `CURRENT_USER()` | `VARCHAR` | 현재 SQL 실행에 적용되는 유효 권한 사용자명 |
| `SESSION_USER()` | `VARCHAR` | 현재 접속 세션의 인증 사용자명 |
| `CURRENT_USER_ID()` | `INTEGER` | 유효 권한 사용자의 내부 ID |
| `SESSION_USER_ID()` | `INTEGER` | 인증 세션 사용자의 내부 ID |

네 함수는 인자를 받지 않으며 괄호를 포함해 호출합니다. 괄호 없는 `CURRENT_USER` keyword나
`USER`, `SYSTEM_USER`, `CURRENT_SCHEMA` alias는 지원하지 않습니다.

```sql
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id;
```

일반 SQL에서는 current user와 session user가 같습니다.

```text
CURRENT_NAME  SESSION_NAME  CURRENT_ID  SESSION_ID
SYS           SYS           1           1
```

### VIEW에서의 사용자 컨텍스트

다른 사용자가 소유한 definer VIEW를 조회하면 VIEW 내부 SQL은 소유자 권한으로 실행됩니다.

- `CURRENT_USER()`와 `CURRENT_USER_ID()`는 VIEW owner를 반환합니다.
- `SESSION_USER()`와 `SESSION_USER_ID()`는 VIEW를 호출한 접속 세션 사용자를 반환합니다.

재현 가능한 owner/caller 예제는 VIEW 문법을
참고합니다.

### 사용자가 삭제된 활성 세션

다른 관리자 세션이 현재 접속 중인 사용자를 `DROP USER`해도 기존 접속은 즉시 종료되지
않습니다. 기존 세션의 네 함수는 로그인할 때 보존한 사용자명과 ID를 계속 반환합니다. 삭제된
사용자는 새로 접속할 수 없으며 `M$SYS_USERS`에서도 조회되지 않습니다.

사용자 ID는 Machbase metadata의 내부 식별자입니다. 장기간 보존하는 업무용 사용자 key로
사용하지 말고 현재 metadata를 비교하거나 join할 때만 사용합니다.

```sql
SELECT COUNT(*)
  FROM M$SYS_USERS
 WHERE NAME = SESSION_USER()
   AND USER_ID = SESSION_USER_ID();
```

### 오류

함수에 인자를 전달하면 `ERR-02036`을 반환합니다. 나머지 세 함수도 같은 규칙을 적용합니다.

```sql
SELECT CURRENT_USER(1);
-- ERR-02036: Function [CURRENT_USER] has an invalid argument.
```

관련 계정 lifecycle은 계정 관리를 참고합니다.

## DATE_TRUNC

DATETIME 값을 지정한 시간 단위로 절사하여 반환합니다.

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 INTEGER, i2 DATETIME);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (1, TO_DATE('1999-11-11 1:2:0 4:5:1'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (2, TO_DATE('1999-11-11 1:2:0 5:5:2'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (3, TO_DATE('1999-11-11 1:2:1 6:5:3'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (4, TO_DATE('1999-11-11 1:2:1 7:5:4'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (5, TO_DATE('1999-11-11 1:2:2 8:5:5'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (6, TO_DATE('1999-11-11 1:2:2 9:5:6'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (7, TO_DATE('1999-11-11 1:2:3 10:5:7'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (8, TO_DATE('1999-11-11 1:2:3 11:5:8'));
1 row(s) inserted.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
4                    1999-11-11 01:02:00 000:000:000
4                    1999-11-11 01:02:02 000:000:000
[2] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nanosecond', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
1                    1999-11-11 01:02:00 004:005:000
1                    1999-11-11 01:02:00 005:005:002
1                    1999-11-11 01:02:01 006:005:002
1                    1999-11-11 01:02:01 007:005:004
1                    1999-11-11 01:02:02 008:005:004
1                    1999-11-11 01:02:02 009:005:006
1                    1999-11-11 01:02:03 010:005:006
1                    1999-11-11 01:02:03 011:005:008
[8] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //Same as DATE_TRUNC('sec', i2, 1)
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

시간 단위별로 허용되는 시간 범위는 다음과 같습니다.

* nanosecond, microsecond, millisecond 단위 및 약어는 5.5.6부터 사용 가능합니다.
* week는 일요일부터 시작합니다.

|시간 단위|시간 범위|
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|millisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

예를 들어, DATE_TRUNC('second', time, 120)을 입력하면 반환되는 값은 **2분마다** 표시되며, 이는 DATE_TRUNC('minute', time, 2)와 동일합니다.

## DATE_BIN
지정한 기준 시각(`origin`)을 기준으로 DATETIME 값을 `time unit`과 `time range`로 구간(bin) 처리합니다.

```sql
DATE_BIN(field, count, source [, origin])
```

- `origin`을 지정하면 해당 시각을 기준으로 버킷을 계산합니다.
- `origin`을 생략하면 서버 로컬 타임존의 `1970-01-01 00:00:00`을 기준으로 버킷을 계산합니다.
- `count`는 1 이상의 정수여야 합니다.

`DATE_TRUNC()` 또는 `ROLLUP()`과 같은 로컬 타임존 경계로 버킷을 맞추고 싶으면
`origin`을 생략한 3-인자 형식을 사용하면 됩니다. 반대로 서버 타임존과 무관하게 항상
동일한 경계를 사용해야 하면 4-인자 형식으로 `origin`을 명시해야 합니다.

예를 들어, 서버 타임존이 `UTC+09:00`일 때 과거에는 `DATE_BIN(..., 0)` 대신
타임존 보정이 적용된 `origin` 값을 직접 넣어야 로컬 시간 경계에 맞출 수 있었지만,
이제는 `DATE_BIN(field, count, source)`만으로 같은 효과를 얻을 수 있습니다.

```sql
Mach> CREATE LOG TABLE log (time DATETIME);
Created successfully.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 00:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 01:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 02:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 04:00:00'));
1 row(s) inserted.

Mach> SELECT TIME, DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00'))
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 01:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000
[5] row(s) selected.
```

로컬 타임존 경계를 기준으로 버킷을 계산하는 예는 다음과 같습니다.

```sql
Mach> CREATE LOG TABLE t3521 (ts DATETIME);
Created successfully.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 00:30:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 02:59:59'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 08:00:00'));
1 row(s) inserted.

Mach> SELECT ts,
             DATE_BIN('hour', 3, ts) AS date_bin_3arg,
             DATE_TRUNC('hour', ts, 3) AS date_trunc_3arg
        FROM t3521
    ORDER BY ts;
ts                              date_bin_3arg                   date_trunc_3arg
----------------------------------------------------------------------------------------------------
2000-01-01 00:30:00 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:59:59 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000
2000-01-01 08:00:00 000:000:000 2000-01-01 06:00:00 000:000:000 2000-01-01 06:00:00 000:000:000
[4] row(s) selected.
```

시간 단위별 허용 범위는 다음과 같습니다.

* nanosecond, microsecond, millisecond 단위 및 약어는 5.5.6부터 사용할 수 있습니다.
* week는 7일과 같습니다.

|시간 단위|
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|millisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|

## DAYOFWEEK

DATETIME 값의 요일을 정수로 반환합니다.

TO_CHAR (time, 'DAY')와 의미적으로 동일하지만, 여기서는 정수를 반환합니다.

```sql
DAYOFWEEK(date_val)
```

반환되는 자연수는 아래 표와 같이 요일을 나타냅니다.

|반환값|요일|
|--|--|
|0|일요일|
|1|월요일|
|2|화요일|
|3|수요일|
|4|목요일|
|5|금요일|
|6|토요일|

## DECODE

컬럼 값을 search 값들과 비교하여 일치하면 대응하는 return 값을 반환합니다. 일치하는 search 값이 없으면 default 값을, default를 생략하면 NULL을 반환합니다.

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE LOG TABLE decode_table (id1 VARCHAR(11));
Created successfully.

Mach> INSERT INTO decode_table VALUES('decodetest1');
1 row(s) inserted.

Mach> INSERT INTO decode_table VALUES('decodetest2');
1 row(s) inserted.

Mach> SELECT id1, DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT') FROM decode_table;
id1          DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT')
---------------------------------------------------------
decodetest2  result2
decodetest1  result1
[2] row(s) selected.

Mach> SELECT id1, DECODE(id1, 'codetest', 2, 99) FROM decode_table;
id1          DECODE(id1, 'codetest', 2, 99)
-----------------------------------------------
decodetest2  99
decodetest1  99
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'decodetest1', 2) FROM decode_table;
DECODE(id1, 'decodetest1', 2)
--------------------------------
NULL
2
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'codetest', 2) FROM decode_table;
DECODE(id1, 'codetest', 2)
-----------------------------
NULL
NULL
[2] row(s) selected.
```

## EXTRACT_*

바이너리 프레임에서 비트를 추출하는 함수 모음입니다.
`EXTRACT_*`는 빅엔디안, `EXTRACT_LE_*`는 리틀엔디안 모델을 사용합니다.
모든 함수는 `BINARY/VARBINARY`를 입력으로 받으며 frame이 NULL이면 결과도 NULL입니다.

**엔디안 모델**

- `EXTRACT_*`: MSB 우선 (`bit 0`은 `byte[0]`의 MSB)
- `EXTRACT_LE_*`: LSB 우선 (`bit 0`은 `byte[0]`의 LSB)
- 비트 인덱스는 프레임 전체 기준으로 0부터 시작합니다.

**공통 규칙**

- 단일 비트: `0 <= bit_pos < frame_bits`
- 범위 추출: `start_bit >= 0`, `1 <= bit_count <= 64`,
  `start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*`는 32비트, `EXTRACT_DOUBLE*`는 64비트를 읽습니다.
- signed 추출은 2의 보수(two's complement)로 해석하고 64비트로 부호 확장합니다.
- 범위 오류: `ERR_QP_INVALID_ARG_VALUE` (`ERR-02229` 계열)
- 인자 타입 오류: `ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

단일 비트를 0 또는 1로 반환합니다.

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

1~64비트를 부호 없는/2의 보수 정수로 읽습니다.

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

32/64비트를 IEEE754 float/double로 재해석하며, 지정한 비트 구간이 frame 안에
들어와야 합니다.

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

1~64비트를 `signed=0`이면 부호 없는 값, `signed=1`이면 2의 보수 signed 값으로
읽고 `raw * scale + offset`을 반환합니다.

```sql
-- 20비트 센서값, scale 0.01, offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```

## FIRST / LAST

각 그룹에서 '기준 값'으로 정렬한 순서 기준으로 가장 앞(또는 마지막) 레코드의 특정 값을 반환하는 집계 함수입니다.

* FIRST: 정렬 순서에서 가장 앞 레코드의 값을 반환합니다.
* LAST: 정렬 순서에서 마지막 레코드의 값을 반환합니다.

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> create table firstlast_table (id integer, name varchar(20), group_no integer);
Created successfully.
Mach> insert into firstlast_table values (1, 'John', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (2, 'Grey', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (5, 'Ryan', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (4, 'Andrew', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (7, 'Kyle', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (6, 'Ross', 1);
1 row(s) inserted.

Mach> select group_no, first(id, name) from firstlast_table group by group_no;
group_no    first(id, name)
-------------------------------------
1           Grey
0           John
[2] row(s) selected.

Mach> select group_no, last(id, name) from firstlast_table group by group_no;
group_no    last(id, name)
-------------------------------------
1           Kyle
0           Ryan
```

## FROM_TIMESTAMP

UTC 기준 1970-01-01 00:00:00부터 경과한 나노초 값을 datetime 타입으로 변환합니다.

(TO_TIMESTAMP()는 datetime 타입을 같은 기준 시점부터 경과한 나노초 값으로 변환합니다.)

기준 시점은 UTC+09:00에서 1970-01-01 09:00:00으로 표시됩니다.
아래 예제의 날짜와 시각은 UTC+09:00 기준입니다.

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869);
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

`SYSDATE`와 `NOW`는 현재 시각을 나타내는 DATETIME 값입니다.
아래 예제는 현재 시각을 그대로 변환하는 경우와 1밀리초(1,000,000나노초)를 빼는 경우를 보여줍니다.

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.

Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms (1,000,000 ns) 차이가 발생함
[1] row(s) selected.
```

## FROM_UNIXTIME

정수로 입력된 32비트 UNIXTIME 값을 datetime 타입으로 변환합니다. (UNIX_TIMESTAMP는 datetime 데이터를 32비트 UNIXTIME 정수로 변환합니다.)

아래 예제의 날짜와 시각은 UTC+09:00 기준입니다.

```sql
FROM_UNIXTIME(unix_timestamp_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671) FROM TEST;
FROM_UNIXTIME(315540671)
----------------------------------
1980-01-01 11:11:11 000:000:000

Mach> SELECT FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01')) FROM unix_table;
FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01'))
------------------------------------------
2001-01-01 00:00:00 000:000:000
```

## GROUP_CONCAT

그룹 내 컬럼 값들을 문자열로 이어 붙여 반환하는 집계 함수입니다.

> **주의**
> Cluster Edition에서는 사용할 수 없습니다.

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: 중복 값은 한 번만 연결합니다.
* ORDER BY: 지정한 컬럼 값을 기준으로 연결 순서를 정렬합니다.
* SEPARATOR: 컬럼 값을 연결할 때 사용할 구분자 문자열입니다. 기본값은 쉼표(,)입니다.

구문 관련 주의사항은 다음과 같습니다.

* 하나의 컬럼만 지정할 수 있으며, 여러 컬럼을 붙이려면 TO_CHAR()와 CONCAT 연산자(||)로 하나의 표현식으로 만들어야 합니다.
* ORDER BY에는 연결 대상 컬럼 외의 컬럼도 지정할 수 있으며, 여러 컬럼을 지정할 수 있습니다.
* SEPARATOR에는 문자열 상수만 지정할 수 있으며, 문자열 컬럼은 지정할 수 없습니다.

```sql
Mach> CREATE LOG TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
Created successfully.

Mach> INSERT INTO concat_table VALUES (1, 2, 'John');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (2, 1, 'Ram');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (3, 2, 'Zara');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (4, 2, 'Jill');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (5, 1, 'Jack');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (6, 1, 'Jack');
1 row(s) inserted.

Mach> SELECT GROUP_CONCAT(name) AS G_NAMES FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(DISTINCT name) AS G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name SEPARATOR '.') G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack.Jack.Ram
Jill.Zara.John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name ORDER BY id1) G_NAMES, GROUP_CONCAT(id1 ORDER BY id1) G_SORTID FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
G_SORTID
------------------------------------------------------------------------------------
Ram,Jack,Jack
2,5,6
John,Zara,Jill
1,3,4
[2] row(s) selected.
```

## INSTR

대상 문자열에서 패턴 문자열이 시작하는 위치를 반환합니다. 위치는 1부터 시작합니다.

* 패턴이 없으면 0을 반환합니다.
* 찾을 패턴의 길이가 0이거나 NULL이면 NULL을 반환합니다.

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE LOG TABLE string_table(c1 VARCHAR(20));
Created successfully.

Mach> INSERT INTO string_table VALUES ('abstract');
1 row(s) inserted.

Mach> INSERT INTO string_table VALUES ('override');
1 row(s) inserted.

Mach> SELECT c1, INSTR(c1, 'act') FROM string_table;
c1                    INSTR(c1, 'act')
------------------------------------------
override              0
abstract              6
[2] row(s) selected.
```

## LEAST / GREATEST

여러 컬럼/값을 입력하면 LEAST는 최소값, GREATEST는 최대값을 반환합니다.

입력 값이 1개이거나 없으면 오류로 처리됩니다. 입력 값이 NULL이면 NULL을 반환합니다. 따라서 입력이 컬럼인 경우 함수로 미리 변환해야 합니다.
비교할 수 없는 컬럼(BLOB, TEXT 등)이 포함되거나 비교를 위한 타입 변환이 불가능하면 오류로 처리됩니다.

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE LOG TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
Created successfully.

Mach> INSERT INTO lgtest_table VALUES (1, 2, 'abstract', 'ace');
1 row(s) inserted.

Mach> INSERT INTO lgtest_table VALUES (null, 100, null, 'bag');
1 row(s) inserted.

Mach> SELECT LEAST (c1, c2) FROM lgtest_table;
LEAST (c1, c2)
-----------------------
NULL
1
[2] row(s) selected.

Mach> SELECT LEAST (c1, c2, -1) FROM lgtest_table;
LEAST (c1, c2, -1)
-----------------------
NULL
-1
[2] row(s) selected.

Mach> SELECT GREATEST(c3, c4) FROM lgtest_table;
GREATEST(c3, c4)
--------------------
NULL
ace
[2] row(s) selected.

Mach> SELECT LEAST(c3, c4) FROM lgtest_table;
LEAST(c3, c4)
-----------------
NULL
abstract
[2] row(s) selected.

Mach> SELECT LEAST(NVL(c3, 'aa'), c4) FROM lgtest_table;
LEAST(NVL(c3, 'aa'), c4)
----------------------------
aa
abstract
[2] row(s) selected.
```

## LENGTH

문자열 컬럼의 길이를 반환합니다. 반환 값은 영문(ASCII) 기준 바이트 수입니다.

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE LOG TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
Created successfully.

Mach> INSERT INTO length_table VALUES(1, 10, 'Around the Horn');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(NULL, 20, 'Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(3, NULL, 'Antonio Moreno');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(4, 40, NULL);
1 row(s) inserted.

Mach> select * FROM length_table;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
3           NULL                        Antonio Moreno
NULL        20                          Alfreds Futterk
1           10                          Around the Horn
[4] row(s) selected.

Mach> select id1 * 10 FROM length_table;
id1 * 10
-----------------------
40
30
NULL
10
[4] row(s) selected.

Mach> select * FROM length_table Where id1 > 1 and id2 < 50;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
[1] row(s) selected.

Mach> select name || ' with null concat' FROM length_table;
name || ' with null concat'
------------------------------------
NULL
Antonio Moreno with null concat
Alfreds Futterk with null concat
Around the Horn with null concat
[4] row(s) selected.

Mach> select LENGTH(name) FROM length_table;
LENGTH(name)
---------------
NULL
14
15
15
[4] row(s) selected.
```

## LOWER

영문 문자열을 소문자로 변환합니다.

```sql
LOWER(column_name)
```

```sql
Mach> CREATE LOG TABLE lower_table (name VARCHAR(20));
Created successfully.

Mach> INSERT INTO lower_table VALUES('');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('James Backley');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Antonio MORENO');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT LOWER(name) FROM lower_table;
LOWER(name)
------------------------
NULL
antonio moreno
alfreds futterkiste
james backley
NULL
[5] row(s) selected.
```

## LPAD / RPAD

입력 문자열이 지정 길이가 될 때까지 왼쪽(LPAD) 또는 오른쪽(RPAD)에 문자를 채웁니다.

마지막 파라미터 char는 생략할 수 있으며, 생략 시 공백(' ')으로 채웁니다.
입력 값이 지정 길이보다 길면 문자를 덧붙이지 않고 앞에서부터 지정 길이만큼만 반환합니다.

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE LOG TABLE pad_table (c1 integer, c2 varchar(15));
Created successfully.

Mach> INSERT INTO pad_table VALUES (1, 'Antonio');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (25, 'Johnathan');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (30, 'M');
1 row(s) inserted.

Mach> SELECT LPAD(to_char(c1), 5, '0') FROM pad_table;
LPAD(to_char(c1), 5, '0')
-----------------------------
00030
00025
00001
[3] row(s) selected.

Mach> SELECT RPAD(to_char(c1), 5, '0') FROM pad_table;
RPAD(to_char(c1), 5, '0')
-----------------------------
30000
25000
10000
[3] row(s) selected.

Mach> SELECT LPAD(c2, 5) FROM pad_table;
LPAD(c2, 5)
---------------
    M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 5) FROM pad_table;
RPAD(c2, 5)
---------------
M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 10, '***') FROM pad_table;
RPAD(c2, 10, '***')
-----------------------
M*********
Johnathan*
Antonio***
[3] row(s) selected.
```

## LTRIM / RTRIM

첫 번째 인자에서 패턴 문자열에 포함된 문자를 제거합니다. LTRIM은 왼쪽부터, RTRIM은 오른쪽부터 패턴에 포함된 문자를 검사하며, 패턴에 없는 문자를 만나면 멈춥니다. 모든 문자가 패턴에 포함되어 있으면 NULL을 반환합니다.

패턴을 지정하지 않으면 공백(' ')을 기준으로 공백을 제거합니다.

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE LOG TABLE trim_table1(name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table1 VALUES ('   smith   ');
1 row(s) inserted.

Mach> SELECT ltrim(name) FROM trim_table1;
ltrim(name)
---------------
smith
[1] row(s) selected.

Mach> SELECT rtrim(name) FROM trim_table1;
rtrim(name)
---------------
   smith
[1] row(s) selected.

Mach> SELECT ltrim(name, ' s') FROM trim_table1;
ltrim(name, ' s')
---------------------
mith
[1] row(s) selected.

Mach> SELECT rtrim(name, 'h ') FROM trim_table1;
rtrim(name, 'h ')
---------------------
   smit
[1] row(s) selected.

Mach> CREATE LOG TABLE trim_table2 (name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table2 VALUES ('ddckaaadkk');
1 row(s) inserted.

Mach> SELECT ltrim(name, 'dc') FROM trim_table2;
ltrim(name, 'dc')
---------------------
kaaadkk
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dk') FROM trim_table2;
rtrim(name, 'dk')
---------------------
ddckaaa
[1] row(s) selected.

Mach> SELECT ltrim(name, 'dckak') FROM trim_table2;
ltrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dckak') FROM trim_table2;
rtrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.
```

## MAX

지정한 숫자 컬럼의 최대값을 반환하는 집계 함수입니다.

```sql
MAX(column_name)
```

```sql
Mach> CREATE LOG TABLE max_table (c INTEGER);
Created successfully.

Mach> INSERT INTO max_table VALUES(10);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(20);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(30);
1 row(s) inserted.

Mach> SELECT MAX(c) FROM max_table;
MAX(c)
--------------
30
[1] row(s) selected.
```

## MEDIAN

`MEDIAN(value)`는 숫자식의 정확한 중앙값을 반환하며 `PERCENTILE_CONT(value, 0.5)`와 같은
방식으로 동작합니다.

```sql
MEDIAN(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```

## MIN

지정한 숫자 컬럼의 최소값을 반환하는 집계 함수입니다.

```sql
MIN(column_name)
```

```sql
Mach> CREATE LOG TABLE min_table(c1 INTEGER);
Created successfully.

Mach> INSERT INTO min_table VALUES(1);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(22);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(33);
1 row(s) inserted.

Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------------
1
[1] row(s) selected.
```

## NVL

컬럼 값이 NULL이면 지정한 값으로 대체하고, NULL이 아니면 원래 값을 반환합니다.

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE LOG TABLE nvl_table (c1 varchar(10));
Created successfully.

Mach> INSERT INTO nvl_table VALUES ('Johnathan');
1 row(s) inserted.

Mach> INSERT INTO nvl_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT NVL(c1, 'Thomas') FROM nvl_table;
NVL(c1, 'Thomas')
---------------------
Thomas
Johnathan
```

## NEXTVAL

`NEXTVAL(sequence_column)`은 Lookup 테이블의 Sequence 컬럼에 대해 다음 값을 반환합니다.

```sql
NEXTVAL(sequence_column)
```

- `NEXTVAL`은 `INSERT` 문에서만 사용할 수 있습니다.
- 인자는 `PROPERTY(SEQUENCE=...)`로 설정된 컬럼이어야 합니다.
- Sequence 컬럼 생성과 예제는 Sequence Column을 참고하십시오.

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```

## ROUND

입력 값의 지정한 자릿수(입력 자릿수 + 1)를 반올림한 결과를 반환합니다. 자릿수를 생략하면 소수점 0자리에서 반올림합니다. 음수를 지정해 정수부 자리에서 반올림할 수 있습니다.

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE LOG TABLE round_table (c1 DOUBLE);
Created successfully.

Mach> INSERT INTO round_table VALUES (1.994);
1 row(s) inserted.

Mach> INSERT INTO round_table VALUES (1.995);
1 row(s) inserted.

Mach> SELECT c1, ROUND(c1, 2) FROM round_table;
c1                          ROUND(c1, 2)
-----------------------------------------------------------
1.995                       2
1.994                       1.99
```

## ROWNUM

SELECT 결과 행에 번호를 부여합니다.

SELECT에서 사용하는 서브쿼리나 인라인 뷰 내부에서 사용할 수 있습니다. 인라인 뷰의 Target List에서 ROWNUM()을 사용한 경우 외부에서 참조할 수 있도록 Alias를 지정해야 합니다.

```sql
ROWNUM()
```

**사용 가능한 절**

SELECT Target List, GROUP BY, ORDER BY 절에서 사용할 수 있습니다. WHERE와 HAVING 절에서는 사용할 수 없습니다. 결과 번호로 WHERE/HAVING을 제어하려면 인라인 뷰에서 ROWNUM()을 계산한 뒤 외부 쿼리에서 참조합니다.

|사용 가능 절|사용 불가 절|
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'Second Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Third Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Fourth Row');
1 row(s) inserted.

Mach> SELECT INNER_RANK, c3 AS NAME
    2 FROM   (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
    3 WHERE  INNER_RANK < 3;
INNER_RANK           NAME
------------------------------------
1                    Fourth Row
2                    Third Row
[2] row(s) selected.
```

**정렬로 인한 결과 번호 변화**

SELECT에 ORDER BY 절이 있으면 Target List의 ROWNUM() 결과가 순차적으로 부여되지 않을 수 있습니다. 이는 ROWNUM()이 ORDER BY보다 먼저 처리되기 때문입니다. 순차 번호가 필요하면 ORDER BY를 포함한 쿼리를 인라인 뷰로 만든 뒤, 외부 SELECT에서 ROWNUM()을 호출하십시오.

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'John');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Sarah');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Micheal');
1 row(s) inserted.

Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
    2 FROM   ( SELECT * FROM rownum_table ORDER BY c3 );
ROWNUM()             SORT                        NAME
-----------------------------------------------------------------
1                    1                           NULL
2                    2                           John
3                    4.3                         Micheal
4                    3.3                         Sarah
[4] row(s) selected.
```

## SERIESNUM

`SERIES BY`로 구분한 연속 구간 중 각 행이 속한 구간의 번호를 반환합니다. 같은 구간의
행에는 같은 번호를 부여하므로 구간 안의 행 순번과는 다릅니다. 반환 타입은 BIGINT이며,
`SERIES BY` 절을 사용하지 않으면 항상 1을 반환합니다.

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Created successfully.

Mach> INSERT INTO T1 VALUES (0, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (2, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (4, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (5, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (6, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (7, 1);
1 row(s) inserted.

Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM() C1 C2
-------------------------------------------------
1 1 2
1 2 3
1 3 2
2 5 2
2 6 3
[5] row(s) selected.
```

## STDDEV / STDDEV_POP

입력 컬럼의 표본 표준편차(STDDEV)와 모표준편차(STDDEV_POP)를 반환하는 집계 함수입니다. 각각 VARIANCE, VAR_POP의 제곱근입니다.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE LOG TABLE stddev_table(c1 INTEGER, C2 DOUBLE);

Mach> INSERT INTO stddev_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (4, 2);
1 row(s) inserted.

Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV(c1)
-----------------------------------------------------------
1                           0.707107
2                           0.707107
[2] row(s) selected.

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV_POP(c1)
-----------------------------------------------------------
1                           0.5
2                           0.5
[2] row(s) selected.
```

## SUBSTR

문자열 컬럼에서 START 위치부터 SIZE 길이만큼 잘라 반환합니다.

* START는 1부터 시작하며 0이면 NULL을 반환합니다.
* SIZE가 START 위치부터 남은 문자열 길이보다 크면 START 위치부터 문자열 끝까지 반환합니다.
SIZE는 선택 사항이며 생략하면 문자열 길이가 사용됩니다.

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> INSERT INTO substr_table values('abstract');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
a
A
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
str
CDE
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
bstract
BCDEFG
[2] row(s) selected.

Mach> drop table substr_table;
Dropped successfully.

Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
A
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
CDE
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
BCDEFG
[1] row(s) selected.
```

## SUBSTRING_INDEX

입력된 count만큼 구분자(delim)를 찾을 때까지의 부분 문자열을 반환합니다. count가 음수이면 문자열 끝에서부터 구분자를 찾고, 구분자를 찾은 위치부터 문자열 끝까지 반환합니다.

count가 0이면 NULL을 반환합니다. count가 0이 아니고 문자열에 구분자가 없으면 입력 문자열 전체를 반환합니다.

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE LOG TABLE substring_table (url VARCHAR(30));
Created successfully.

Mach> INSERT INTO substring_table VALUES('www.machbase.com');
1 row(s) inserted.

Mach> SELECT SUBSTRING_INDEX(url, '.', 1) FROM substring_table;
SUBSTRING_INDEX(url, '.', 1)
----------------------------------
www
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 2) FROM substring_table;
SUBSTRING_INDEX(url, '.', 2)
----------------------------------
www.machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', -1) FROM substring_table;
SUBSTRING_INDEX(url, '.', -1)
----------------------------------
com
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1) FROM substring_table;
SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1)
-------------------------------------------
machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 0) FROM substring_table;
SUBSTRING_INDEX(url, '.', 0)
----------------------------------
NULL
[1] row(s) selected.
```

## SUM

숫자 컬럼의 합계를 반환하는 집계 함수입니다.

```sql
SUM(column_name)
```

```sql
Mach> CREATE LOG TABLE sum_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sum_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(3, 4);
1 row(s) inserted.

Mach> SELECT c1, SUM(c1) from sum_table group by c1;
c1          SUM(c1)
------------------------------------
2           6
3           3
1           3
[3] row(s) selected.

Mach> SELECT c1, SUM(c2) from sum_table group by c1;
c1          SUM(c2)
------------------------------------
2           6
3           4
1           6
[3] row(s) selected.
```

## SUMSQ

SUMSQ는 숫자 값들의 제곱합을 반환합니다.

```sql
SUMSQ(value)
```

```sql
Mach> CREATE LOG TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sumsq_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 3);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 4);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 5);
1 row(s) inserted.

Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
------------------------------------
2           41
1           14
[2] row(s) selected.
```

## SYSDATE / NOW

SYSDATE는 함수가 아닌 의사 컬럼으로, 시스템 현재 시간을 반환합니다.

NOW는 SYSDATE와 동일한 기능이며, 사용자 편의를 위해 제공합니다.

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

## TO_CHAR

주어진 데이터 타입을 문자열 타입으로 변환합니다. 타입에 따라 format_string을 지정할 수 있지만, 바이너리 타입에는 사용할 수 없습니다.

```sql
TO_CHAR(column)
```

**TO_CHAR: 기본 데이터 타입**

기본 데이터 타입은 아래와 같이 문자열 형태로 변환됩니다.

```sql
Mach> CREATE LOG TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
Created successfully.

Mach> INSERT INTO fixed_table values(200, 19234, 1234123412, 3.14, 7.8338, '192.168.0.1', '::127.0.0.1', 'log varchar');
1 row(s) inserted.

Mach> SELECT '[ ' || TO_CHAR(id1) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id1) || ' ]'
------------------------------------------------------------------------------------
[ 200 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id2) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id2) || ' ]'
------------------------------------------------------------------------------------
[ 19234 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id3) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id3) || ' ]'
------------------------------------------------------------------------------------
[ 1234123412 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id4) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id4) || ' ]'
------------------------------------------------------------------------------------
[ 3.140000 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id5) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id5) || ' ]'
------------------------------------------------------------------------------------
[ 7.833800 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id6) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id6) || ' ]'
------------------------------------------------------------------------------------
[ 192.168.0.1 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id7) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id7) || ' ]'
------------------------------------------------------------------------------------
[ 0000:0000:0000:0000:0000:0000:7F00:0001 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id8) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id8) || ' ]'
------------------------------------------------------------------------------------
[ log varchar ]
[1] row(s) selected.
```

**TO_CHAR: 부동소수점 숫자**

* 5.5.6 버전부터 지원

float와 double 값을 문자열로 변환합니다.
포맷 표현식은 반복해서 사용할 수 없으며 '[letter][number]' 형태로 입력해야 합니다.

|포맷 표현식|설명|
|--|--|
|F / f|컬럼 값의 소수점 자릿수를 지정합니다. 입력 가능한 최대 값은 30입니다.|
|N / n|소수점 자릿수를 지정하고 정수부 3자리마다 콤마(,)를 삽입합니다. 입력 가능한 최대 값은 30입니다.|

```sql
Mach> create table float_table (i1 float, i2 double);
Created successfully.

Mach> insert into float_table values (1.23456789, 1234.5678901234567890);
1 row(s) inserted.

Mach> select TO_CHAR(i1, 'f8'), TO_CHAR(i2, 'N9') from float_table;
TO_CHAR(i1, 'f8')       TO_CHAR(i2, 'N9')
--------------------------------------------------------------
1.23456788              1,234.567890123
[1] row(s) selected.
```

**TO_CHAR: DATETIME 타입**

datetime 컬럼 값을 임의의 문자열로 변환하는 함수입니다. 이를 이용해 다양한 문자열을 생성하고 조합할 수 있습니다.

format_string을 생략하면 기본값은 "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"입니다.

|포맷 표현식|설명|
|--|--|
|YYYY|연도를 4자리 숫자로 변환합니다.|
|YY|연도를 2자리 숫자로 변환합니다.|
|MM|월을 2자리 숫자로 변환합니다.|
|MON|월을 3자리 영문 약어로 변환합니다. (예: JAN, FEB, MAY, ...)|
|DD|일을 2자리 숫자로 변환합니다.|
|DAY|요일을 3자리 영문 약어로 변환합니다. (예: SUN, MON, ...)|
|IW|ISO 8601 규칙에 따라 특정 연도의 주차를 `1~53`으로 변환합니다(요일 고려).<br> - 한 주의 시작은 월요일입니다.<br> - 첫 주는 전년도 마지막 주로 간주될 수 있습니다. 마찬가지로 마지막 주는 다음 해의 첫 주로 간주될 수 있습니다.<br>    자세한 내용은 ISO 8601을 참고하십시오.|
|WW|요일을 고려하지 않고 특정 연도의 주차를 `1~53`으로 변환합니다.<br>즉, `1월 1일~1월 7일`은 1로 변환됩니다.|
|W|요일을 고려하지 않고 특정 월의 주차를 `1~5`로 변환합니다.<br>즉, `3월 1일~3월 7일`은 1로 변환됩니다.|
|HH|시간을 2자리 숫자로 변환합니다.|
|HH12|시간을 `1~12` 범위의 2자리 숫자로 변환합니다.|
|HH24|시간을 `00~23` 범위의 2자리 숫자로 변환합니다.|
|HH2, HH3, HH6|HH 뒤 숫자 단위로 시간을 절단합니다.<br><br>예를 들어 HH6을 사용하면 `0~5`는 0, `6~11`은 6으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.<br>이 값은 24시간 기준으로 표시됩니다.|
|MI|분을 2자리 숫자로 표시합니다.|
|MI2, MI5, MI10, MI20, MI30|MI 뒤 숫자 단위로 분을 절단합니다.<br><br>예를 들어 MI30은 `0~29`분은 0, `30~59`분은 30으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.|
|SS|초를 2자리 숫자로 표시합니다.|
|SS2, SS5, SS10, SS20, SS30|SS 뒤 숫자 단위로 초를 절단합니다.<br><br>예를 들어 SS30은 `0~29`초는 0, `30~59`초는 30으로 표시합니다.<br>이 표현은 시간열 통계 계산에 유용합니다.|
|AM|시간을 AM/PM으로 표시합니다.|
|mmm|밀리초를 3자리 숫자로 표시합니다.<br><br>값 범위는 `0~999`입니다.|
|uuu|마이크로초를 3자리 숫자로 표시합니다.<br><br>값 범위는 `0~999`입니다.|
|nnn|나노초를 3자리 숫자로 표시합니다.<br><br>값 범위는 `0~999`입니다.|

```sql
Mach> CREATE LOG TABLE datetime_table (id integer, dt datetime);
Created successfully.

Mach> INSERT INTO  datetime_table values(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(3, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(4, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2013-11-11 1:2:3') and dt < TO_DATE('2014-11-11 1:2:3');
id          dt
-----------------------------------------------
3           2013-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_CHAR(dt) FROM datetime_table;
id          TO_CHAR(dt)
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY')
-------------------------------------------------------------------------------------------------
4           2014
3           2013
2           2012
1           1999
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM')
-------------------------------------------------------------------------------------------------
4           2014-12
3           2013-11
2           2012-11
1           1999-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD')
-------------------------------------------------------------------------------------------------
4           2014-12-30
3           2013-11-11
2           2012-11-11
1           1999-11-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR')
-------------------------------------------------------------------------------------------------
4           2014-12-30 TO_CHAR
3           2013-11-11 TO_CHAR
2           2012-11-11 TO_CHAR
1           1999-11-11 TO_CHAR
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33
3           2013-11-11 01:02:03
2           2012-11-11 01:02:03
1           1999-11-11 01:02:03
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444.555.666
3           2013-11-11 01:02:03 004.005.006
2           2012-11-11 01:02:03 004.005.006
1           1999-11-11 01:02:03 004.005.006
[4] row(s) selected.
```

**TO_CHAR: 지원하지 않는 타입**

현재 TO_CHAR는 바이너리 타입을 지원하지 않습니다.

일반 문자열로 변환할 수 없기 때문입니다. 화면에 출력하려면 TO_HEX() 함수로 16진 값을 출력해 확인할 수 있습니다.

## TO_DATE

지정한 포맷 문자열에 따라 문자열을 datetime 타입으로 변환합니다.

format_string을 생략하면 기본값은 "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"입니다.

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE to_date_table (id INTEGER, dt datetime);
Created successfully.

Mach> INSERT INTO  to_date_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(3, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(4, TO_DATE('2014-12-30 23:22:34 777:888:999', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn'));
1 row(s) inserted.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('1999-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2012-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS') and dt < TO_DATE('2014-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS');
id          dt
-----------------------------------------------
2           2012-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999.12.01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999-12-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI')
-------------------------------------------------------
4           1999-12-31 13:12:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------
4           1999-12-31 13:12:32 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') FROM to_date_table LIMIT 1;
id           TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:789
[1] row(s) selected.
```

## TO_DATE_SAFE

TO_DATE()와 유사하지만 변환에 실패하면 오류 없이 NULL을 반환합니다.

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE date_table (ts DATETIME);
Created successfully.

Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-01', 'YYYY-MM-DD'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-02', 'YYYY'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD'));
1 row(s) inserted.

Mach> SELECT ts FROM date_table;
ts
----------------------------------
NULL
NULL
2016-01-01 00:00:00 000:000:000
[3] row(s) selected.
```

## TO_HEX

컬럼 값이 NULL이면 NULL을 반환하고, NULL이 아니면 원래 값을 16진 문자열로 반환합니다. 출력 일관성을 위해 short, int, long 타입은 BIG ENDIAN으로 변환합니다.

```sql
TO_HEX(column)
```

```sql
Mach> CREATE LOG TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
id11 DATETIME);
Created successfully.

Mach> INSERT INTO hex_table VALUES(256, 65535, '0123456789', 3.141592, 1024 * 1024 * 1024 * 3.14, 13513135446, '192.168.0.1', '::192.168.0.1', 'textext',
'binary', TO_DATE('1999', 'YYYY'));
1 row(s) inserted.

Mach> SELECT TO_HEX(id1), TO_HEX(id2), TO_HEX(id3), TO_HEX(id4), TO_HEX(id5), TO_HEX(id6), TO_HEX(id7), TO_HEX(id8), TO_HEX(id9), TO_HEX(id10), TO_HEX(id11)
FROM hex_table;
TO_HEX(id1)  TO_HEX(id2)  TO_HEX(id3)            TO_HEX(id4)  TO_HEX(id5)        TO_HEX(id6)        TO_HEX(id7)
-------------------------------------------------------------------------------------------------------------------------
TO_HEX(id8)                          TO_HEX(id9)
--------------------------------------------------------------------------------------------------------------------------
TO_HEX(id10)                                                                      TO_HEX(id11)
--------------------------------------------------------------------------------------------------------
0100   0000FFFF   30313233343536373839   D80F4940   1F85EB51B81EE941   0000000325721556   04C0A80001
06000000000000000000000000C0A80001   74657874657874
62696E617279                                                                      0CB325846E226000
[1] row(s) selected.
```

## TO_INET_STR

`TO_INET_STR(ipv4_value)`는 `IPV4` 값을 점으로 구분된 십진 문자열로 변환합니다.

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```

## TO_IPV4 / TO_IPV4_SAFE

주어진 문자열을 IPv4 타입으로 변환합니다. 문자열을 숫자 값으로 변환할 수 없으면 TO_IPV4()는 오류를 반환하고 작업을 중단합니다.

반면 TO_IPV4_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv4_table (c1 varchar(100));
Created successfully.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES('     192.168.0.2    ');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES(NULL);
1 row(s) inserted.

Mach> SELECT c1 FROM ipv4_table;
c1
------------------------------------------------------------------------------------
NULL
     192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table;
TO_IPV4(c1)
------------------
NULL
192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1.1');
1 row(s) inserted.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table limit 1;
TO_IPV4(c1)
------------------
[ERR-02068 : Invalid IPv4 address format (192.168.0.1.1).]
[0] row(s) selected.

Mach> SELECT TO_IPV4_SAFE(c1) FROM ipv4_table;
TO_IPV4_SAFE(c1)
-------------------
NULL
NULL
192.168.0.2
192.168.0.1
[4] row(s) selected.
```

## TO_IPV6 / TO_IPV6_SAFE

주어진 문자열을 IPv6 타입으로 변환합니다. 문자열을 숫자 타입으로 변환할 수 없으면 TO_IPV6()는 오류를 반환하고 작업을 중단합니다.

반면 TO_IPV6_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv6_table (id varchar(100));
Created successfully.

Mach> INSERT INTO ipv6_table VALUES('::0.0.0.0');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0' || '.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::127.0.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.4  ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::FFFF:255.255.255.255   ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table;
TO_IPV6(id)
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[7] row(s) selected.

Mach> INSERT INTO ipv6_table VALUES('127.0.0.10.10');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table limit 1;
TO_IPV6(id)
---------------------------------------------------------------
[ERR-02148 : Invalid IPv6 address format.(127.0.0.10.10)]
[0] row(s) selected.

Mach> SELECT TO_IPV6_SAFE(id) FROM ipv6_table;
TO_IPV6_SAFE(id)
---------------------------------------------------------------
NULL
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[8] row(s) selected.
```

## TO_NUMBER / TO_NUMBER_SAFE

주어진 문자열을 숫자(double)로 변환합니다. 문자열을 숫자 값으로 변환할 수 없으면 TO_NUMBER()는 오류를 반환하고 작업을 중단합니다.

반면 TO_NUMBER_SAFE()는 오류 발생 시 NULL을 반환하므로 작업을 계속할 수 있습니다.

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE number_table (id varchar(100));
Created successfully.

Mach> INSERT INTO number_table VALUES('10');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('20');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('30');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from number_table;
TO_NUMBER(id)
------------------------------
30
20
10
[3] row(s) selected.

Mach> CREATE LOG TABLE safe_table (id varchar(100));
Created successfully.

Mach> INSERT INTO safe_table VALUES('invalidnumber');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from safe_table;
TO_NUMBER(id)
------------------------------
[ERR-02145 : The string cannot be converted to number value.(invalidnumber)]
[0] row(s) selected.

Mach> SELECT TO_NUMBER_SAFE(id) from safe_table;
TO_NUMBER_SAFE(id)
------------------------------
NULL
[1] row(s) selected.
```

## TOP_K

`TOP_K(value, k)`는 가장 자주 등장한 `k`개의 숫자 값을 `value:count` 형식의 문자열로 반환합니다.

```sql
TOP_K(value, k)
```

- `value`는 숫자형이어야 합니다.
- `k`는 양의 정수 상수여야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `VARCHAR`입니다.
- 정렬 기준은 빈도 내림차순이며, 빈도가 같으면 값 오름차순입니다.

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

예시 결과:

```text
101:532,205:317,301:90
```

## TO_TIMESTAMP

datetime 타입을 UTC 기준 1970-01-01 00:00:00부터 경과한 나노초 값으로 변환합니다.

아래 예제의 날짜와 시각은 UTC+09:00 기준입니다.

```sql
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> create table datetime_tbl (c1 datetime);
Created successfully.

Mach> insert into datetime_tbl values ('2010-01-01 10:10:10');
1 row(s) inserted.

Mach> select to_timestamp(c1) from datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
[1] row(s) selected.
```

## TRUNC

TRUNC 함수는 소수점 이하 n자리에서 잘라낸 값을 반환합니다.

n을 생략하면 0으로 간주하여 소수점을 모두 제거합니다. n이 음수이면 소수점 앞 n자리에서 잘라낸 값을 반환합니다.

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 DOUBLE);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (158.799);
1 row(s) inserted.

Mach> SELECT TRUNC(i1, 1), TRUNC(i1, -1) FROM trunc_table;
TRUNC(i1, 1)                TRUNC(i1, -1)
-----------------------------------------------------------
158.7                       150
[1] row(s) selected.

Mach> SELECT TRUNC(i1, 2), TRUNC(i1, -2) FROM trunc_table;
TRUNC(i1, 2)                TRUNC(i1, -2)
-----------------------------------------------------------
158.79                      100
[1] row(s) selected.
```

## TS_CHANGE_COUNT

특정 컬럼 값의 변경 횟수를 구하는 집계 함수입니다.

입력 데이터가 시간순으로 입력된다는 것을 보장할 수 없으므로 1) Join 또는 2) Inline view와 함께 사용할 수 없습니다.
VARCHAR 타입은 지원하지 않습니다.

* **Cluster Edition에서는 사용할 수 없습니다.**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE LOG TABLE ipcount_table (id INTEGER, ip IPV4);
Created successfully.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> SELECT id, TS_CHANGE_COUNT(ip) from ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
------------------------------------
2           2
1           4
[2] row(s) selected.
```

## UNIX_TIMESTAMP

UNIX_TIMESTAMP는 유닉스 time() 시스템 콜 기준으로 date 타입 값을 32비트 정수로 변환하는 함수입니다. (FROM_UNIXTIME은 반대로 정수 값을 date 타입으로 변환합니다.)

```sql
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> CREATE table unix_table (c1 int);
Created successfully.

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
1 row(s) inserted.

Mach> SELECT * FROM unix_table;
C1
--------------
978274800
[1] row(s) selected.
```

## UPPER

영문 문자열을 대문자로 변환합니다.

```sql
UPPER(string_value)
```

```sql
Mach> CREATE LOG TABLE upper_table(id INTEGER,name VARCHAR(10));
Created successfully.

Mach> INSERT INTO upper_table VALUES(1, '');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(2, 'James');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(3, 'sarah');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(4, 'THOMAS');
1 row(s) inserted.

Mach> SELECT id, UPPER(name) FROM upper_table;
id          UPPER(name)
----------------------------
4           THOMAS
3           SARAH
2           JAMES
1           NULL
[4] row(s) selected.
```

## VARIANCE / VAR_POP

지정한 숫자 컬럼의 분산을 반환하는 집계 함수입니다. VARIANCE는 표본 분산, VAR_POP은 모분산을 반환합니다.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE LOG TABLE var_table(c1 INTEGER, c2 DOUBLE);
Created successfully.

Mach> INSERT INTO var_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 2);
1 row(s) inserted.

Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
------------------------------
0.333333
[1] row(s) selected.

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
------------------------------
0.25
[1] row(s) selected.
```

## YEAR / MONTH / DAY

입력 datetime 컬럼 값에서 각각 연, 월, 일을 추출해 정수로 반환합니다.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE LOG TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.

Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.

Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```

## ISNAN / ISINF

인자로 받은 숫자 값이 NaN 또는 Inf인지 판별합니다. NaN 또는 Inf이면 1, 그렇지 않으면 0을 반환합니다.

```sql
ISNAN(number)
ISINF(number)
```

다음 예제는 테이블에 이미 `NaN` 및 `Inf` 값이 들어 있는 경우를 가정합니다.
SQL `INSERT` 문에서 `nan` 또는 `inf` 토큰을 값으로 직접 입력할 수는 없습니다.

```sql
Mach> SELECT * FROM test;
I1                          I2                          I3
------------------------------------------------------------------------
1                           1                           1
nan                         inf                         0
NULL                        NULL                        NULL
[3] row(s) selected.

Mach> SELECT ISNAN(i1), ISNAN(i2), ISNAN(i3), i3 FROM test ;
ISNAN(i1)   ISNAN(i2)   ISNAN(i3)   i3
-----------------------------------------------------
0           0           0           1
1           0           0           0
NULL        NULL        NULL        NULL
[3] row(s) selected.

Mach> SELECT * FROM test WHERE ISNAN(i1) = 1;
I1                          I2                          I3
------------------------------------------------------------------------
nan                         inf                         0
[1] row(s) selected.
```

## JSON_SET

JSON 문서의 특정 경로에 SQL scalar 값을 JSON scalar로 저장합니다.

```sql
JSON_SET(json_doc, path, scalar)
```

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE')
--------------------------------------------------------------------------------
{"ship":{"status":"DONE"}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- `JSON_SET(..., path, NULL)` 은 JSON `null` 을 저장합니다.
- JSON 문서 인자가 `NULL` 이면 결과는 SQL `NULL` 입니다.
- `path` 가 `NULL` 이거나 빈 문자열이면 오류가 발생합니다.
- object 경로 중심으로 지원합니다.
- array element 갱신 예: `$.items[0]` 는 지원하지 않습니다.

## JSON_SET_JSON

세 번째 인자를 JSON 문자열로 해석하여 object 또는 array subtree를 저장합니다.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}')
----------------------------------------------------------------------------
{"ship":{"owner":{"name":"machbase"}}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- 세 번째 인자가 SQL `NULL` 이면 결과는 SQL `NULL` 입니다.
- 유효하지 않은 JSON 문자열은 오류가 발생합니다.
- object 경로 중심으로 지원합니다.
- array element 갱신은 지원하지 않습니다.

## JSON_REMOVE

JSON 문서에서 특정 멤버 또는 하위 경로를 제거합니다.

```sql
JSON_REMOVE(json_doc, path)
```

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team')
--------------------------------------------------------------------------
{"owner":{"name":"machbase"}}
[1] row(s) selected.
```

주의사항:

- `path` 는 full JSONPath를 사용해야 합니다.
- 존재하지 않는 경로는 no-op 으로 처리됩니다.
- `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.
- JSON 문서 인자가 `NULL` 이면 결과는 SQL `NULL` 입니다.

## PI()

`DOUBLE` 타입의 π 상수를 반환합니다.

```sql
SELECT PI();
```

```sql
Mach> SELECT PI();
PI()
------------------------------
3.141592653589793
[1] row(s) selected.
```

## SQRT()

제곱근을 반환합니다.

```sql
SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
```

```sql
Mach> SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
SQRT(9)   SQRT(2.25)         SQRT(16.0)
-----------------------------------------------
3         1.5000000000000000  4
[1] row(s) selected.
```

## POWER()

`base`의 `exponent` 거듭제곱을 반환합니다.

```sql
SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
```

```sql
Mach> SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
POWER(2, 3)   POWER(9, 0.5)   POWER(4, -1)
------------------------------------------------
8             3.0000000000000000 0.2500000000000000
[1] row(s) selected.
```

## POW()

`POWER()`의 별칭입니다.

```sql
SELECT POW(2, 3), POW(2, -1), POW(10, 0);
```

```sql
Mach> SELECT POW(2, 3), POW(2, -1), POW(10, 0);
POW(2, 3)   POW(2, -1)   POW(10, 0)
-----------------------------------------
8           0.5           1
[1] row(s) selected.
```

## LOG()

`LOG(n)`은 자연로그, `LOG(base, n)`은 지정한 밑의 로그를 계산합니다.

```sql
SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
```

```sql
Mach> SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
LOG(2, 8)   LOG(100)             LOG(10, 1000)
------------------------------------------------
3           4.605170185988092     3
[1] row(s) selected.
```

## LN()

자연로그 `ln(n)`을 반환합니다.

```sql
SELECT LN(1), LN(10), LN(1000);
```

```sql
Mach> SELECT LN(1), LN(10), LN(1000);
LN(1)      LN(10)         LN(1000)
-----------------------------------
0          2.302585092994046 6.907755278982137
[1] row(s) selected.
```

## EXP()

`e^n`을 반환합니다.

```sql
SELECT EXP(0), EXP(1), EXP(-1);
```

```sql
Mach> SELECT EXP(0), EXP(1), EXP(-1);
EXP(0)      EXP(1)         EXP(-1)
-----------------------------------
1           2.718281828459045 0.36787944117144233
[1] row(s) selected.
```

## FLOOR()

음의 무한대 방향으로 내림합니다.

```sql
SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
```

```sql
Mach> SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
FLOOR(-1.2)  FLOOR(3.9)  FLOOR(-3.0)
-----------------------------------------
-2            3           -3
[1] row(s) selected.
```

## CEIL()

양의 무한대 방향으로 올림합니다.

```sql
SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
```

```sql
Mach> SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
CEIL(-1.2)  CEIL(3.2)  CEIL(-3.0)
-------------------------------------
-1           4          -3
[1] row(s) selected.
```

## SIN()

라디안 입력, 사인값 반환.

```sql
SELECT SIN(0), SIN(PI()/2), SIN(PI());
```

```sql
Mach> SELECT SIN(0), SIN(PI()/2), SIN(PI());
SIN(0)      SIN(PI()/2)   SIN(PI())
------------------------------------
0           1             0
[1] row(s) selected.
```

## SLOPE

`SLOPE(y, x)`는 숫자형 `(x, y)` 점들에 대한 선형 회귀 직선의 기울기를 계산합니다.

```sql
SLOPE(y, x)
```

- 두 인자는 모두 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 유효한 데이터가 부족하거나 `x` 분산이 0이면 결과는 `NULL`입니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS()

라디안 입력, 코사인값 반환.

```sql
SELECT COS(0), COS(PI()), COS(PI()/2);
```

```sql
Mach> SELECT COS(0), COS(PI()), COS(PI()/2);
COS(0)      COS(PI())   COS(PI()/2)
-------------------------------------
1           -1          0
[1] row(s) selected.
```

## TAN()

라디안 입력, 탄젠트값 반환.

```sql
SELECT TAN(0), TAN(PI()/4), TAN(PI());
```

```sql
Mach> SELECT TAN(0), TAN(PI()/4), TAN(PI());
TAN(0)      TAN(PI()/4)  TAN(PI())
-----------------------------------
0           1            0
[1] row(s) selected.
```

## MOD()

몫을 0으로 절사한 기준으로 나머지를 계산합니다.

```sql
SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
```

```sql
Mach> SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
MOD(10, 3)  MOD(11, 4)  MOD(-10, 3)  MOD(3.5, 0.5)
-------------------------------------------------------
1           3           -1           0
[1] row(s) selected.
```

## MODE

`MODE(value)`는 입력 집합에서 가장 자주 나타나는 숫자 값을 반환합니다.

```sql
MODE(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 최빈값이 여러 개면 더 작은 값을 반환합니다.
- 반환 타입은 `DOUBLE`입니다.

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95

자주 쓰는 분위값을 빠르게 표현할 수 있도록 준비된 정확 분위수 축약 함수입니다.

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value`는 숫자형이어야 합니다.
- `NULL` 값은 무시합니다.
- 반환 타입은 `DOUBLE`입니다.

`P05`, `P10`, `P90`, `P95`는 각각 `PERCENTILE_CONT(value, 0.05)`, `0.10`, `0.90`, `0.95`와 같은 의미입니다.

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC

이 함수들은 숫자형 입력에 대해 정확한 분위값을 계산하는 집계 함수입니다.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- `PERCENTILE_CONT`는 필요하면 인접한 정렬 값 사이를 보간합니다.
- `PERCENTILE_DISC`는 목표 순위에 해당하는 실제 관측값 중 하나를 선택합니다.
- 두 함수 모두 반환 타입은 `DOUBLE`입니다.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE

`QUANTILE(value, ratio)`는 숫자형 입력에 대해 정확한 연속 분위값을 계산합니다.

```sql
QUANTILE(value, ratio)
```

- `value`는 숫자형이어야 합니다.
- `ratio`는 `0.0` 이상 `1.0` 이하의 상수여야 합니다.
- 반환 타입은 `DOUBLE`입니다.
- `PERCENTILE_CONT`와 같은 연속 분위수 의미를 사용합니다.

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND()

난수 값을 생성합니다.

```sql
SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default;
```

```sql
Mach> SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default FROM m$sys_users WHERE name = 'SYS';
same_seed   diff_seed   diff_default
------------------------------------
1           0           0
[1] row(s) selected.
```

`RAND(seed)`는 같은 시드면 동일한 값이 나오며, `RAND()`는 세션 내부 상태를 기반으로 `[0,1)` 범위의 값을 생성합니다.

## REGEXP_LIKE

`REGEXP_LIKE`는 문자열이 정규식 패턴과 일치하는지 검사합니다. Boolean 값을 반환하며
주로 `WHERE` 절에서 사용합니다.

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `match_param`은 선택 항목이며 상수 `VARCHAR`여야 합니다. `c`는 대소문자를
  구분하고, `i`는 대소문자를 구분하지 않습니다. 기본값은 `c`입니다.

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## REGEXP_INSTR

`REGEXP_INSTR`는 정규식과 일치하는 위치를 1부터 시작하는 값으로 반환합니다. 일치하는
값이 없으면 `0`을 반환합니다.

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `position`과 `occurrence`는 `1` 이상의 상수 정수입니다.
- `return_pos`는 상수 정수입니다. `0`은 시작 위치를 반환하고, `1`은 일치한 문자열
  다음 위치를 반환합니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## REGEXP_SUBSTR

`REGEXP_SUBSTR`는 정규식과 일치하는 부분 문자열을 반환합니다.

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`은 상수 `VARCHAR` 정규식이어야 합니다.
- `position`과 `occurrence`는 `1` 이상의 상수 정수입니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## REGEXP_REPLACE

`REGEXP_REPLACE`는 정규식과 일치하는 문자열을 치환합니다.

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- `source`는 `VARCHAR`여야 합니다.
- `pattern`과 `replacement`는 상수 `VARCHAR` 값이어야 합니다.
- `replacement`를 생략하면 일치하는 문자열을 제거합니다.
- `position`은 `1` 이상의 상수 정수입니다.
- `occurrence`는 상수 정수입니다. `0`은 모든 일치 항목을 치환하고, `0`보다 큰 값은
  해당 번째 일치 항목만 치환합니다.
- `match_param`은 `c` 또는 `i`를 사용할 수 있습니다. 기본값은 `c`입니다.

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

## 내장 함수 지원 타입

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|x|x|x|x|x|x|
|ADD_TIME|x|x|x|x|x|x|x|x|x|o|x|
|APPROX_PERCENTILE / APPROX_MEDIAN / APPROX_P05 / APPROX_P10 / APPROX_P90 / APPROX_P95|o|o|o|o|o|x|x|x|x|x|x|
|AREA|o|o|o|o|o|x|x|x|x|x|x|
|AVG|o|o|o|o|o|x|x|x|x|x|x|
|BITAND / BITOR|o|o|o|x|x|x|x|x|x|x|x|
|COUNT|o|o|o|o|o|o|x|o|o|o|x|
|CUME_DIST|o|o|o|o|o|x|x|x|x|x|x|
|DATE_TRUNC|x|x|x|x|x|x|x|x|x|o|x|
|DECODE|o|o|o|o|o|o|x|o|x|o|x|
|FIRST / LAST|o|o|o|o|o|o|x|o|o|o|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIN|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
|REGEXP_LIKE|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_INSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_REPLACE|x|x|x|x|x|o|x|x|x|x|x|
|SLOPE|o|o|o|o|o|x|x|x|x|x|x|
|TOP_K|o|o|o|o|o|x|x|x|x|x|x|
|ROUND|o|o|o|o|o|x|x|x|x|x|x|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|x|x|x|x|x|x|
|SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|SUBSTRING_INDEX|x|x|x|x|x|o|o|x|x|x|x|
|SUM|o|o|o|o|o|x|x|x|x|x|x|
|SYSDATE / NOW|x|x|x|x|x|x|x|x|x|x|x|
|TO_CHAR|o|o|o|o|o|o|x|o|o|o|x|
|TO_DATE / TO_DATE_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|x|x|x|x|x|x|x|o|x|x|x|
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|

## JSON 관련 함수

이 함수들은 JSON 데이터 타입을 인자로 사용합니다.

|함수명|설명|비고|
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|값을 문자열 타입으로 반환합니다.<br>(값이 없으면 ERROR를 반환합니다.)| - JSON object or array : 모든 객체를 문자열로 변환해 반환합니다.<br> - String type : 그대로 반환합니다.<br> - Numeric type : 문자열로 변환해 반환합니다.<br> - boolean type : \"True\" 또는 \"False\"를 반환합니다.|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')|값을 64비트 double 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)| - JSON object or array : NULL을 반환합니다.<br> - String type : 변환 가능하면 변환해 반환하고, 불가능하면 NULL을 반환합니다.<br> - Numeric type : 64비트 실수로 반환합니다.<br> - boolean type : \"True\"는 1.0, \"False\"는 0.0으로 반환합니다.|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|값을 64비트 정수 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)| - JSON object or array : NULL을 반환합니다.<br> - String type : 변환 가능하면 변환해 반환하고, 불가능하면 NULL을 반환합니다.<br> - Numeric type : 64비트 정수로 반환합니다.<br> - boolean type : \"True\"는 1, \"False\"는 0으로 반환합니다.|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|값을 문자열 타입으로 반환합니다.<br>(값이 없으면 NULL을 반환합니다.)<br>연산자(→)와 동일한 결과를 반환합니다.| - JSON object or array : 모든 객체를 문자열로 변환해 반환합니다.<br> - String type : 그대로 반환합니다. <br> - Numeric type : 문자열로 변환해 반환합니다. <br> - boolean type : \"True\" 또는 \"False\"를 반환합니다.|
|JSON_SET(json_doc, path, scalar)|지정한 경로에 SQL scalar 값을 JSON scalar로 저장한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - `NULL` 값은 JSON `null` 로 저장됩니다.<br> - object 경로만 지원합니다.|
|JSON_SET_JSON(json_doc, path, json_text)|지정한 경로에 JSON 문자열을 object 또는 array subtree로 저장한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - 세 번째 인자가 SQL `NULL` 이면 결과는 SQL `NULL` 입니다.<br> - 유효하지 않은 JSON 문자열은 오류가 발생합니다.|
|JSON_REMOVE(json_doc, path)|지정한 경로의 멤버 또는 subtree를 제거한 새 JSON 문서를 반환합니다.| - `path` 는 full JSONPath를 사용합니다.<br> - 존재하지 않는 경로는 no-op 입니다.<br> - `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.|
|JSON_IS_VALID('json string')|json 문자열이 형식에 맞는지 확인합니다.| - 0 : False<br> - 1 : True|
|JSON_TYPEOF(JSON column name, 'json path')|값의 타입을 반환합니다.| - None : 키가 존재하지 않음<br> - Object : Object 타입<br> - Integer : 정수 타입<br> - Real : 실수 타입<br> - String : 문자열 타입<br> - True/False : Boolean<br> - Array : Array 타입<br> - Null : NULL|

```sql
Mach> CREATE LOG TABLE jsontbl (name VARCHAR(20), jval JSON);
Created successfully.

Mach> INSERT INTO jsontbl VALUES("name1", '{"name":"test1"}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name2", '{"name":"test2", "value":123}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name3", '{"name":{"class1": "test3"}}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name4", '{"myarray": [1, 2, 3, 4]}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name5", '{"name":"error"');
[ERR-02233: Error occurred at column (2): (Error in json load.)]

Mach> SELECT name, JSON_EXTRACT_STRING(jval, '$.name') FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, JSON_EXTRACT_INTEGER(jval, '$.myarray[1]') FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, JSON_TYPEOF(jval, '$.name') FROM jsontbl;
name                  JSON_TYPEOF(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 None
name3                 Object
name2                 String
name1                 String
[4] row(s) selected.
```

## JSON 연산자

`->` 연산자는 JSON 데이터의 객체에 접근할 때 사용합니다.

JSON_EXTRACT_STRING 함수와 동일한 결과를 반환합니다.

```sql
json_col -> 'json path'
```

JSON 컬럼의 멤버 값은 JSONPath를 사용하는 `->` 연산자와 dot 축약 문법으로 접근할 수 있습니다.

```sql
-- JSONPath arrow 문법
jval->'$.sensor.temperature'

-- JSON dot 축약 문법
jval.sensor.temperature
```

두 표현식은 같은 JSON 값을 조회합니다. 기존 `->` 연산자는 계속 사용할 수 있으며, dot 문법은 같은 값을 더 짧게 표현하기 위한 추가 문법입니다.

```sql
Mach> SELECT name, jval->'$.name' FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, jval->'$.myarray[1]' FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, jval->'$.name.class1' FROM jsontbl;
name                  jval->'$.name.class1'
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 test3
name2                 NULL
name1                 NULL
[4] row(s) selected
```

### JSONPath arrow 문법

arrow 문법은 JSONPath 문자열을 사용합니다.

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

대괄호를 사용해 JSON key를 직접 지정할 수도 있습니다. key 이름에 점(`.`)이 포함된 경우에는 대괄호 문법을 사용합니다.

```sql
-- key 이름이 a.b인 경우
jval->'$["a.b"]'
jval->'$[a.b]'

-- 여러 단계 key를 대괄호로 지정
jval->'$[Plant1][Line1][Temperature]'

-- 점이 포함된 하나의 key 이름
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]`는 `Plant1.Line1.Temperature`라는 하나의 key를 찾습니다. `Plant1`, `Line1`, `Temperature`를 단계별 key로 찾으려면 `$[Plant1][Line1][Temperature]` 또는 `$.Plant1.Line1.Temperature`를 사용합니다.

key 이름에 특수 문자나 점이 포함된 경우에는 다음처럼 따옴표가 있는 bracket 문법을 권장합니다.

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

다음 문법은 지원하지 않습니다.

```sql
jval->'$."a.b"'
```

### JSON dot 축약 문법

JSON 컬럼 뒤에 멤버 이름을 붙여 JSON 값을 조회할 수 있습니다.

```sql
-- 단일 멤버
jval.name

-- 중첩 멤버
jval.sensor.temperature

-- 배열 index
jval.items[0].name

-- 특수 문자가 포함된 key
jval.items[0]."product-id"
```

dot 문법에서 double quote로 감싼 key는 대소문자와 특수 문자를 그대로 사용합니다.

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### WHERE 절 타입 비교

JSON 멤버 접근 결과는 조회할 때 문자열처럼 표시됩니다. 그러나 `WHERE` 절에서 숫자 타입 값과 비교하면 JSON 값을 숫자로 파싱해 숫자 비교를 수행합니다.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.value' > 100
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value BETWEEN 10 AND 30
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value IN (10, 20, 30)
 ORDER BY name;
```

지원되는 비교는 다음과 같습니다.

- JSON integer 값과 SQL integer 값 비교
- JSON real/double 값과 SQL numeric 값 비교
- JSON 숫자 문자열과 SQL numeric 값 비교
- JSON boolean 값과 문자열 `'true'`, `'false'` 비교
- `=`, `<>`, `<`, `<=`, `>`, `>=`, `BETWEEN`, literal `IN (...)`

SQL integer 값과 비교하는 경우 JSON integer는 정수로 비교하므로 `9007199254740992`와 `9007199254740993`처럼 double 정밀도 범위를 넘는 값도 서로 다른 값으로 비교할 수 있습니다.

문자 타입 값과 비교하면 기존처럼 문자열 비교를 수행합니다.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

숫자 비교에서 JSON 값이 숫자로 해석될 수 없으면 조건에 매칭되지 않습니다. 오류로 처리하지 않습니다. 일반 `VARCHAR` 컬럼과 숫자 값의 비교 정책은 변경되지 않으며, 숫자 자동 비교는 JSON 멤버 접근식에만 적용됩니다.

### 이름 해석 규칙

일반 SQL의 컬럼 이름 해석이 JSON dot 해석보다 우선합니다.

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

위 표현식은 먼저 일반 컬럼 이름으로 해석을 시도합니다. 일반 컬럼으로 해석되지 않고 `jval`이 JSON 컬럼이면 `jval.name`을 JSON 멤버 접근으로 처리합니다.

JSON dot 접근은 JSON 컬럼을 기준으로만 사용할 수 있습니다.

```sql
-- 지원하지 않음
(jval->'$.sensor').temperature
name.member
```

### 제한 사항

다음 문법은 지원하지 않습니다.

- wildcard: `jval.items[*].name`
- recursive descent: `jval..name`
- filter expression: `jval.items[?(@.price > 10)]`
- negative array index: `jval.items[-1]`
- single quoted key: `jval.'product-id'`
- dot 문법과 arrow 문법 혼합: `jval.items->'$.name'`
- JSON 컬럼이 아닌 컬럼의 dot 접근: `name.member`
- 임의 expression 뒤의 dot 접근: `(jval->'$.sensor').temperature`
- quoted member arrow path: `jval->'$."a.b"'`

`IN (SELECT ...)` 형태의 subquery `IN`에서는 JSON 멤버 값의 숫자 자동 비교를 지원하지 않습니다. literal `IN (...)`을 사용합니다.

## 윈도우 함수

윈도우 함수는 행 간 비교, 연산, 정의를 위한 함수이며 분석 함수 또는 랭킹 함수라고도 합니다.

SELECT 문에서만 사용할 수 있습니다.

### 윈도우 함수 구문

윈도우 함수는 반드시 OVER 절을 포함합니다.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: 윈도우 함수 이름
* ARGUMENTS: 함수에 따라 0~N개의 인자를 지정할 수 있습니다.
* PARTITION BY clause: 전체 집합을 기준에 따라 작은 그룹으로 나눕니다. (생략 가능)
* ORDER BY clause: 정렬 기준이 되는 ORDER BY 절을 지정합니다. (생략 가능)

### 윈도우 함수 목록

#### LAG

파티션별 윈도우에서 이전 N번째 행의 값을 가져옵니다.

가져올 행이 없으면 NULL을 반환합니다.

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first previous value.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1)
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL
name1       2024-01-02 00:00:00 000:000:000 2           1
name1       2024-01-03 00:00:00 000:000:000 3           2
[3] row(s) selected.
```

#### LEAD

파티션별 윈도우에서 N번째 다음 행의 값을 가져옵니다.

가져올 행이 없으면 NULL을 반환합니다.

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first and subsequent values.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1)
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2
name1       2024-01-02 00:00:00 000:000:000 2           3
name1       2024-01-03 00:00:00 000:000:000 3           NULL
[3] row(s) selected.
```

#### NTILE

`NTILE(n)`은 정렬된 행을 가능한 균등하게 `n`개의 버킷으로 나누고, 각 행이 속한 버킷 번호를 반환합니다.

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n`은 양의 상수여야 합니다.
- `OVER (...)` 안의 `ORDER BY`는 필수입니다.
- 행 수가 균등하게 나누어지지 않으면 앞쪽 버킷이 한 행씩 더 가집니다.

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
