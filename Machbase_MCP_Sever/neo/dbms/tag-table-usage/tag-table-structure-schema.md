# 테이블 구조와 스키마

## TAG 테이블 설계

TAG 테이블 설계는 컬럼을 몇 개 둘지 정하는 일이 아니라, 무엇을 하나의 태그로 볼지와
어떤 값을 어느 범위에 둘지 정하는 일입니다.

컬럼 위치에 따라 정해지는 역할, 축 컬럼의 타입, 지정할 수 없는 타입은
생성, 변경, 삭제를 참고합니다.
이 페이지는 그 규칙 안에서 결정할 항목을 다룹니다.

이 페이지의 DDL은 모델별 독립 예제입니다. 생성 순서가 필요한 실습은 해당 절 안에서
설명하며, 같은 이름의 기존 객체가 있으면 다른 이름으로 실행합니다.

스키마를 정할 때는 다음 항목을 함께 검토합니다.

- 활용 사례
- 태그 이름 컬럼
- 시간축과 거리축 선택
- 값 컬럼 설계
- METADATA 컬럼 설계
- JSON METADATA 컬럼 설계
- 이진 데이터 컬럼 설계
- VARCHAR 스토리지 최적화
- 스토리지 전략
- LSL·USL 설계
- 보정과 중복 정책
- 제약 및 지원 범위

### 활용 사례

TAG는 같은 구조의 관측값이 여러 대상에서 계속 쌓이는 업무에 적합합니다. 센서, 설비,
이동체, 검사 회차처럼 반복 관측 대상을 먼저 정하고, 그 대상별 이력을 시간 또는 거리 축으로
조회할 수 있는지 확인합니다. 이 항목에서는 대상을 TAG로 모델링할지, 다른 테이블 타입으로
나눌지를 확정합니다. 업무 모델 예시는 활용 사례를
참고합니다.

### 태그 이름 컬럼

센서별, 설비별, 검사 회차별 중 어떤 단위를 하나의 태그로 볼지 먼저 정합니다. 잘게
나누면 태그 수가 늘어 메타데이터와 인덱스 부담이 커지고, 크게 묶으면 한 태그 안에 서로
다른 대상의 이력이 섞입니다. 이름 규칙은
VARCHAR 스토리지 최적화에서 함께 다룹니다.

### 시간축과 거리축 선택

축은 조회 조건에서 무엇을 범위로 지정할지를 기준으로 고릅니다. 측정 시각으로 구간을
지정하면 시간축, 특정 경로의 누적 위치처럼 거리 구간으로 지정하면 거리축입니다. 한 TAG
테이블은 두 축을 동시에 가질 수 없으므로 나중에 바꾸려면 테이블을 다시 만들어야 합니다.

```sql
-- 측정 시각으로 구간을 지정하는 시간축 TAG입니다.
CREATE TAG TABLE time_sensor (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

```sql
-- 거리·위치로 구간을 지정하는 거리축 TAG입니다.
CREATE TAG TABLE rail_sensor (
    name     VARCHAR(40) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

`DURATION`, ROLLUP과 시간 함수는 BASETIME에만 적용됩니다. 거리 범위 조회는 일반 비교와
`BETWEEN`을 사용하며, 실행 예제는 조회와 분석을 참고합니다.

### 값 컬럼 설계

TAG 테이블의 값 컬럼은 태그 이름과 축 컬럼을 제외한 일반 데이터 컬럼입니다. 계측값,
상태, 품질 코드처럼 측정 행마다 달라지는 값을 저장합니다.

#### 지원 타입

아래는 자주 사용하는 타입의 예입니다. JSON, BINARY, DECIMAL과 숫자 ARRAY를 포함한 전체
지원 범위는 데이터 타입 사전을 참고하십시오.

| 타입 | 설명 | 저장 크기 |
|------|------|---------|
| `DOUBLE` | 64비트 부동소수점 | 8바이트 |
| `FLOAT` | 32비트 부동소수점 | 4바이트 |
| `LONG` | 64비트 정수 | 8바이트 |
| `INTEGER` (`INT`) | 32비트 정수 | 4바이트 |
| `SHORT` | 16비트 정수 | 2바이트 |
| `VARCHAR(n)` | 가변 문자열 | 최대 n바이트 |

#### 권장 타입 선택

| 데이터 | 권장 타입 |
|--------|---------|
| 온도, 습도, 압력 등 아날로그 값 | `DOUBLE` |
| 카운터, 상태 코드 | `INTEGER` |
| 플래그, 이진 상태 | `SHORT` |
| 에너지, 유량 누적값 | `DOUBLE` 또는 `LONG` |
| 태그 문자열 값 | `VARCHAR(n)` |

#### 다중 값 컬럼 설계

한 테이블에 여러 계측항목을 함께 저장할 때는 NULL 값이 발생할 수 있습니다. 계측항목이 서로 동시에 수집되는 경우에 적합합니다.

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- 항상 수집
    humidity    DOUBLE,     -- 항상 수집
    wind_speed  DOUBLE,     -- 옵션
    rainfall    DOUBLE      -- 옵션
);
```

#### NULL 허용 설계

TAG 테이블 값 컬럼은 기본적으로 NULL을 허용합니다. 특정 태그가 일부 항목만 수집하는 경우 나머지 컬럼에 NULL을 삽입합니다.

```sql
-- wind_speed와 rainfall이 없는 경우
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```

### METADATA 컬럼 설계

METADATA 컬럼은 DATA 행마다 반복 저장할 값이 아니라 태그별 현재 속성을 저장할 때 사용합니다.
설치 위치, 단위, 장비 설정, 관리 상태처럼 태그 이름에 붙는 속성이 여기에 해당합니다. DATA와
METADATA를 분리하면 관측 이력은 유지하면서 태그의 현재 속성만 따로 조회하거나 변경할 수
있습니다. 이 항목에서는 각 속성을 METADATA로 올릴지 DATA 컬럼으로 남길지 확정합니다.
관측마다 값이 달라지면 DATA, 태그 수명 동안 대체로 고정이면 METADATA입니다. 입력, 조회,
수정 예제는 METADATA 사용을 참고합니다.

### JSON METADATA 컬럼 설계

태그별 속성이 계층 구조를 갖거나 속성 집합이 자주 바뀌면 JSON METADATA 컬럼을 검토합니다.
예를 들어 설비 위치, 제조사 정보, 설치 옵션을 하나의 JSON 문서로 저장하고 필요한 path만
조회할 수 있습니다. 이 항목에서는 METADATA를 개별 컬럼으로 둘지 JSON 문서 하나로 둘지
확정합니다. 속성 집합이 고정이고 조건 조회가 잦으면 개별 컬럼이, 태그마다 속성 구성이
다르면 JSON이 유리합니다. 자주 조건으로 사용하는 path는 인덱스 설계도 함께 검토합니다.
자세한 문법과 예제는 JSON METADATA를 참고합니다.

### 이진 데이터 컬럼 설계

TAG 테이블의 `BINARY(n)`은 1~32767바이트의 센서 프레임을 저장할 때 사용합니다. 입력
literal, 길이 제약과 드라이버 동작은 Binary 컬럼을
참고하십시오. 큰 이미지나 파형은 외부 스토리지에 두고 참조 키만 저장하는 설계도
검토하십시오.

### VARCHAR 스토리지 최적화

`VARCHAR`는 실제 최대 길이에 맞춰 선언합니다. 저장 option의 정확한 문법은
DDL 사전을 참고하십시오. 태그 이름에는 사이트,
설비, 센서 식별자를 일관된 구분자로 조합해 범위 조회가 가능하도록 설계합니다.

### 스토리지 전략

데이터는 태그별로 분리된 컬럼 스토리지에 저장됩니다. 데이터 양과 조회 패턴에 따라 적절한 전략을 선택합니다.

#### 단일 테이블 vs 다중 테이블

##### 단일 TAG 테이블 (권장)

같은 종류의 센서는 하나의 TAG 테이블에 모아서 관리합니다.

```sql
-- 권장: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

**장점**
- 관리 포인트 최소화
- 크로스-태그 집계 용이
- 운영 간소화

##### 다중 TAG 테이블

컬럼 구성이 다르거나 보존 기간·접근 권한·운영 주기를 따로 관리해야 하면 테이블 분리를
검토합니다. 센서 수가 늘었다는 이유만으로 센서별 테이블을 만들지는 않습니다.

```sql
-- 온도·습도 센서 (DOUBLE 값)
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- 진동 센서 (DOUBLE + BINARY 파형)
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY(4096)
);
```

#### 태그 수 관리

- 태그 수 증가에 따른 태그 인덱스와 메타데이터 메모리 사용량을 운영 규모의 데이터로
  측정합니다.
- 센서 계층 구조를 태그 이름에 인코딩하여 관리합니다.
- 태그 이름이 매 레코드마다 고유한 값이 되는 설계는 피합니다 (안티패턴).

#### 파티션 전략

시간축 TAG는 `BASETIME`을 기준으로 범위를 제한해 조회합니다. 시스템 저장 객체나 파티션
이름에 의존하지 말고, 보존 기간은 데이터 보존 정책으로
관리하십시오.

### LSL·USL 설계

LSL(Lower Specification Limit)은 하한 규격값, USL(Upper Specification Limit)은 상한
규격값입니다. TAG 테이블의 METADATA 컬럼에 태그별 허용 범위를 설정하면 범위 밖 DATA
입력을 차단할 수 있으므로, 태그마다 다른 입력 품질 기준을 적용할 수 있습니다.

값을 보정하는 기능이 아니라 입력을 거부하는 기능입니다. 범위를 벗어난 입력은 수집 오류
정책에 따라 기록·재처리해야 합니다.

#### 제약 조건

다음 제약 조건이 적용됩니다.

* LSL/USL을 Cluster 전체에서 미지원으로 묶지 않습니다. 테이블 생성 시 한계 정의와
  메타데이터 값 설정, DATA INSERT·Append의 한계 검사는 공통 경로입니다.
  기존 METADATA에 한계 컬럼을 ALTER로 추가하는 아래 실습은 Standard Edition에서 수행합니다.
* LSL/USL을 설정하려면 Tag 테이블의 세 번째 컬럼인 __Value__가 __SUMMARIZED__로 설정되어야 합니다.
* LSL은 USL보다 작거나 같아야 하며, __Value__ 컬럼의 입력 값은 LSL과 USL 사이에 있어야 합니다 (포함). __(LSL <= Value <= USL)__
* LSL/USL 설정을 부여하기 전에 입력된 데이터는 검증되지 않습니다.
* LSL/USL 컬럼을 NULL로 설정하면 입력 데이터를 검증하지 않습니다.
* LSL/USL 기능은 개별적으로 사용할 수 있습니다. 상한 사양만 일치시키려면 USL만 설정할 수 있습니다.
* USL만 설정하면 상한 초과만 검사하고, LSL만 설정하면 하한 미달만 검사합니다.

#### 지원되는 데이터 타입

한계 컬럼은 대상 __Value__ 컬럼과 타입이 같아야 합니다. 아래는 기본 숫자 타입의
규격 범위 설정을 설명합니다. SUMMARIZED 자체의 전체 지원 타입에는 JSON도 있으므로
SUMMARIZED 선언 가능 여부와 숫자 한계 설정을 같은 조건으로 해석하지 않습니다.

|타입|설명|범위|유효 자릿수|
|----|------|-----|----|
|short|16비트 부호 있는 정수 데이터 타입|-32767 ~ 32767|-|
|ushort|16비트 부호 없는 정수 데이터 타입|0 ~ 65534|-|
|integer|32비트 부호 있는 정수 데이터 타입|-2147483647 ~ 2147483647|-|
|uinteger|32비트 부호 없는 정수 데이터 타입|0 ~ 4294967294|-|
|long|64비트 부호 있는 정수 데이터 타입|-9223372036854775807 ~ 9223372036854775807|-|
|ulong|64비트 부호 없는 정수 데이터 타입|0~18446744073709551614|-|
|float|32비트 부동 소수점 데이터|-|6[^1]|
|double|64비트 부동 소수점 데이터|-|15[^1]|

#### LSL/USL 설정 및 사용

다음 CREATE 예제들은 서로 다른 선택을 보여 줍니다. 기본 `example`만 이후
INSERT·UPDATE 실습에서 사용하고, 대안 테이블은 별도로 생성합니다.

태그 메타데이터 테이블의 컬럼에 `LOWER LIMIT`(LSL) 또는 `UPPER LIMIT`(USL) 키워드를 지정합니다. Tag 테이블 생성 시 또는 메타데이터 컬럼 추가 시 설정할 수 있습니다.

##### CREATE

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,
    usl     INTEGER UPPER LIMIT
);
```

두 컬럼을 함께 사용하거나 하나만 사용할 수 있습니다.
LSL만 설정하면 `Value >= LSL`을 검사하고 상한은 제한하지 않습니다. USL 값을 `NULL`로
둔 것과 같은 의미입니다.

```sql
CREATE TAG TABLE example_lower_only (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT
);
```

##### ADD COLUMN

데이터가 이미 입력된 후 `ADD COLUMN`을 사용하여 추가하는 경우 기본값은 __NULL__입니다.

```sql
CREATE TAG TABLE example_alter_limits (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_limits METADATA ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE example_alter_limits METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

CREATE와 마찬가지로 하나의 속성만 추가할 수도 있습니다.

```sql
CREATE TAG TABLE example_alter_upper (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_upper METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

##### INSERT

특정 TAG ID에 대한 LSL/USL 값을 설정합니다.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

설정 후 태그 데이터를 입력하면 다음과 같이 동작합니다.

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- Failure
```

```text
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 100); -- Success (Inclusive)
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 150); -- Success
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 200); -- Success (Inclusive)
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 205); -- Failure
```

```text
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

Tag 테이블을 조회하면 규격 범위 내 데이터만 입력된 것을 확인할 수 있습니다.

```sql
SELECT * FROM example;
```

```text
TAG_ID                                              TIME                            VALUE       LSL         USL
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200
[3] row(s) selected.
Elapsed time: 0.001
```

##### UPDATE

LSL/USL 컬럼의 값을 수정합니다. 이미 입력된 데이터에는 소급 적용되지 않으므로 주의가 필요합니다.

```sql
UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              10          100
[1] row(s) selected.
Elapsed time: 0.001
```

##### DELETE

LSL/USL 컬럼은 `DROP COLUMN`으로 제거하지 않고 값을 NULL로 설정해 제약을 해제합니다.

```sql
UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              NULL        NULL
[1] row(s) selected.
Elapsed time: 0.001
```

#### TRACE 로그로 LSL/USL 위반 확인
- 위치: `$MACHBASE_HOME/trc/machbase.trc`
- 빠른 필터:
  ```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
  ```
- 로그 포맷: `LIMIT_DROP (TYPE=<UPPER|LOWER>) TABLE=<테이블명> TAG=<tag name> <컬럼명=값 ...>`
  - TYPE=LOWER/UPPER로 어떤 한계가 위반됐는지 구분.
  - DATETIME은 `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` 형태.
- 실제 예시:
  ```
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:00 000:000:000 VALUE=5.55
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:04 000:000:000 VALUE=30.55
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:000 VALUE=0
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:008 VALUE=45
  ```
- 활용 포인트
  - TAG별로 LOWER/UPPER 위반 시각과 값을 한눈에 파악.
  - grep으로 TAG/테이블명을 추가 필터하면 특정 대상만 추적 가능.
- 주의: 한 줄 최대 약 4KB라 컬럼이 많을 때 뒤가 잘릴 수 있으며, 기동 직후 메타 캐시 준비 전에는 테이블명이 ID로 보일 수 있습니다.

[^1]: IEEE 754 (https://en.wikipedia.org/wiki/IEEE_754)

### 보정과 중복 정책

값 보정과 중복 제거는 컬럼 정의만으로 끝나는 항목은 아니지만, 스키마 설계 단계에서 미리
정해야 합니다. 보정이 필요하면 어떤 값 컬럼을 수정할 수 있는지, 원본을 별도 컬럼이나 별도
테이블에 보존할지, 보정 후 ROLLUP을 어떻게 재구성할지 결정합니다. DATA의 UPDATE는
Standard Edition 전용이므로, Cluster Edition에서는 보정 대신 재입력과 재집계
절차를 설계합니다. 자세한 내용은
데이터 보정을 참고합니다.

같은 태그와 같은 축 값이 반복 입력될 수 있으면 중복을 허용할지, 수집 단계에서 제거할지,
Machbase의 자동 중복 제거 기능을 사용할지 정합니다. 설정 변경과 운영 검증 절차는
자동 중복 제거를 참고합니다.

### 제약 및 지원 범위

TAG 테이블은 반복 관측 이력에 맞춘 구조이므로 모든 SQL 기능을 일반 관계형 테이블처럼
지원하지 않습니다. 축 컬럼, METADATA, 값 보정, ROLLUP, Edition별 지원 범위는 설계 전에
확인해야 합니다. 이 항목에서는 앞에서 정한 설계안이 지원 범위 안에 있는지 점검하고,
벗어나면 해당 항목으로 돌아가 스키마를 조정합니다. 지원하지 않는 기능과 대표 오류는
제약 및 주의사항을 참고합니다.

## Binary 컬럼

`BINARY(n)`은 Tag 테이블에서 센서 프레임용 고정 길이 바이너리 값을 저장합니다.
TAG의 길이 생략형 `BINARY`는 32767바이트로 처리됩니다. 필요한 프레임 크기를 명시하면
저장·전송 크기를 이해하기 쉽습니다. TAG 외 테이블에는 `BINARY(n)` 길이 지정형을
선언할 수 없습니다. 길이는 1~32K-1
(1~32767)바이트만 유효하며, 인덱스를 생성할 수 없습니다.

명시적 binary literal로 `BINARY` 값을 입력합니다.

### DDL 규칙

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- 유효 길이: `1 <= n <= 32767` (32K-1).
- 범위를 벗어나면 생성 시 오류가 발생합니다(`BINARY(0)` 등).
- `DESC`와 테이블 메타데이터는 선언된 바이트 길이(헥스 폭 아님)를 표시합니다.
  SQL `LENGTH(binary_col)`는 짧은 입력값에 붙은 뒤쪽 0 패딩을 제외한 표시
  값 길이를 반환합니다.

### 지원 입력 형식

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| 형식 | 의미 | 단위 |
| --- | --- | --- |
| `X'...'`, `x'...'` | 16진수 literal | 16진수 2자리 = 1바이트 |
| `B'...'`, `b'...'` | 2진수 literal | bit 8자리 = 1바이트 |
| `O'...'`, `o'...'` | 8진수 literal | 8진수 3자리 = 1바이트 |

prefix는 대소문자 모두 허용됩니다.

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`, `B'00001010'`, `O'012'`는 모두 1바이트 값 `0x0A`를 의미합니다.

### Binary literal 규칙

#### 16진수 literal

`X'...'`와 `x'...'`에는 `0-9`, `A-F`, `a-f`를 사용할 수 있습니다.

```sql
X'00'
X'0AFF'
x'abcdef'
```

16진수 문자는 반드시 짝수 개여야 합니다. 두 자리가 1바이트에 해당합니다.

#### 2진수 literal

`B'...'`와 `b'...'`에는 `0`과 `1`만 사용할 수 있습니다.

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

bit 수는 반드시 8의 배수여야 합니다. 8자리가 1바이트에 해당합니다.

#### 8진수 literal

`O'...'`와 `o'...'`에는 `0-7`만 사용할 수 있습니다.

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

8진수 문자는 반드시 3자리 단위여야 합니다. 각 3자리 값은 `000`부터
`377`까지의 1바이트 범위여야 합니다.

#### 빈 값

작은따옴표 안을 비워 길이 0인 binary 값을 표현합니다.

```sql
X''
B''
O''
```

### 길이 제한

`BINARY(n)` 컬럼에는 최대 `n`바이트까지만 입력 가능합니다.

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- 실패: 3바이트
```

source 종류와 무관하게 최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면
입력은 실패합니다. 이 규칙은 binary literal뿐 아니라 일반 문자열, 기존
`'0x...'` 문자열 입력, 다른 `BINARY` 컬럼 값을 `INSERT ... SELECT`로
복사하는 경우에도 동일하게 적용됩니다.

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- 실패: 8바이트 값을 BINARY(4)에 입력
```

`CASE`, `INSERT ... SELECT`, view 등 SQL expression 안에서 사용하더라도
최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면 입력은 실패합니다.

### 올바르지 않은 입력

다음 입력은 유효하지 않습니다.

```sql
X'0'        -- 16진수 문자가 홀수 개
X'0G'       -- G는 16진수 문자가 아님
B'0101'     -- bit 수가 8의 배수가 아님
B'00000002' -- 2는 2진수 문자가 아님
O'12'       -- 8진수 문자가 3자리 단위가 아님
O'400'      -- 1바이트 범위 초과
X'0102      -- 닫는 작은따옴표가 없음
```

잘못된 값이나 길이 초과 입력은 다음 오류로 실패합니다.

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

### 기존 문자열 입력과의 차이

기존 호환성을 위해 문자열 형태의 `'0x...'` 입력도 사용할 수 있습니다.
`'0x...'`는 문자열에서 `BINARY` 컬럼으로 변환되는 방식이고,
`X'...'`, `B'...'`, `O'...'`는 SQL에서 binary 값임을 명확히 표시하는
binary literal입니다.

일반 문자열을 `BINARY(n)` 컬럼에 입력하는 것도 가능하지만, 문자열 byte 길이가 `n`을
초과하면 실패합니다. 새 SQL 작성 시에는 의미가 명확한 binary literal 형식을
권장합니다.

`'0b...'`, `'0o...'`, 따옴표 없는 `0x...`, `0b...`, `0o...` 형식은
binary literal로 지원하지 않습니다.

### 출력 및 도구 메모

- machsql은 `0x` 없는 대문자 헥스로 출력합니다. 짧은 입력값에 붙은 뒤쪽
  0 패딩은 텍스트 출력에 표시되지 않습니다.
- machloader: 스키마에 `BINARY(n)`을 선언하고, 잘못된 값이나 길이 초과는
  실패합니다.
- Machbase SQLCLI, ODBC, Java, C#, Node.js 드라이버는 고정 길이 버퍼로 송수신하며 메타데이터
  `LENGTH`는 바이트 길이입니다.

## 예제 정리

이 페이지에서 실제로 만든 테이블만 정리합니다. 대안 DDL을 실행하지 않았다면 그 테이블의
DROP 문도 실행하지 않습니다.

```sql
DROP TABLE time_sensor;
DROP TABLE rail_sensor;
DROP TABLE weather_station;
DROP TABLE temperature_sensor;
DROP TABLE thermo_sensor;
DROP TABLE vibration_sensor;
DROP TABLE example;
DROP TABLE example_lower_only;
DROP TABLE example_alter_limits;
DROP TABLE example_alter_upper;
DROP TABLE t1;
DROP TABLE t_bin;
DROP TABLE t_limit;
DROP TABLE t_dst;
DROP TABLE t_src;
```
