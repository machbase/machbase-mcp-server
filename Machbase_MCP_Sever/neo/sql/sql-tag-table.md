# Machbase Neo SQL Tag Table

## 태그 테이블 데이터 모델 개요

이 문서는 Machbase 시계열 데이터베이스에서 센서 시계열 데이터를 저장·조회·관리하도록 최적화된 특수 테이블 구조인 Machbase 태그 테이블을 전반적으로 설명합니다.

### 개념적 데이터 모델

센서 데이터의 전통적인 데이터 모델링은 CSV처럼 넓은(wide) 형태를 띠는 경우가 많습니다. 한 행이 하나의 시각을 나타내고, 각 컬럼이 서로 다른 센서 측정값(태그)에 대응합니다.

**전통적 데이터 모델(넓은 형태):**

| timestamp           | temperature | humidity | pressure | vibration |
| :------------------ | :---------- | :------- | :------- | :-------- |
| 2023-04-15 09:34:12 | 23.5        | 78.9     | 11       | 55        |
| 2023-04-15 09:34:13 | 23.7        | 75.6     | 12       | 51        |
| ...                 | ...         | ...      | ...      | ...       |

*   **특징:**
    *   같은 시각에 측정된 값들을 하나의 레코드로 관리합니다.
    *   데이터를 원래의 넓은 형태 그대로 보기 좋습니다.
    *   스키마 변경(센서·태그 추가/제거)이 유연하지 않아 테이블 변경이 필요한 경우가 많습니다.

Machbase 태그 테이블은 다른 방식을 씁니다. 한 행이 특정 시각에 특정 센서(태그)에서 측정된 값 하나를 나타내는 길고 좁은(tall/narrow) 형태로 데이터를 구성합니다.

**Machbase 태그 테이블 데이터 모델(길고 좁은 형태):**

| TAGID         | timestamp           | value |
| :------------ | :------------------ | :---- |
| temperature   | 2023-04-15 09:34:12 | 23.5  |
| humidity      | 2023-04-15 09:34:12 | 78.9  |
| pressure      | 2023-04-15 09:34:12 | 11    |
| vibration     | 2023-04-15 09:34:12 | 55    |
| temperature   | 2023-04-15 09:34:13 | 23.7  |
| humidity      | 2023-04-15 09:34:13 | 75.6  |
| ...           | ...                 | ...   |

*   **특징:**
    *   각 측정값을 개별 레코드로 변환해 저장합니다.
    *   태그(센서) 관점의 스키마 변화에 최대한의 유연성을 제공합니다. 태그를 추가하거나 제거해도 테이블 구조를 바꿀 필요가 없습니다.
    *   태그 단위의 효율적인 집계와 통계 분석이 가능합니다.
    *   넓은 모델에 비해 행 수는 늘어나지만, 전용 구조 덕분에 조회와 적재 성능은 대체로 향상됩니다.

### 스키마 기준 데이터 모델 비교

데이터 모델링의 차이는 테이블 생성 문법에도 그대로 드러납니다.

**전통적 스키마(예):**

```sql
CREATE TABLE Vibration (
    time      DATETIME,
    temp      DOUBLE,
    humidity  DOUBLE,
    pressure  INTEGER,
    rms       LONG,
    tick      DOUBLE
    -- Additional columns for each new sensor type
);
```
*흔한 설계 방식이지만, 변화가 잦은 IoT 환경에서는 스키마가 경직되는 문제가 있습니다.*

**Machbase 태그 테이블 스키마:**

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- Identifier for the specific tag/sensor
    time  DATETIME    BASETIME,    -- Timestamp of the measurement
    value DOUBLE                   -- The actual measured value
);
```
*이 구조는 시계열 데이터의 본질적 요소인 식별자·시간·값에 집중해 핵심 스키마를 단순화합니다. 부가적인 맥락 정보는 메타데이터로 관리합니다.*

## 태그 테이블 기본

### Structure

태그 테이블은 정형화된 센서 데이터를 효율적으로 적재·조회·압축하도록 설계된 최적화 테이블 구조입니다. 기본 레코드 구조는 세 가지 핵심 요소로 이뤄집니다:

1.  **식별자(기본값은 `name` 컬럼):** 특정 센서나 데이터 소스를 식별하는 고유 문자열입니다(예: `"sensor-A"`, `"factory1-machine2-temp"`). 이 식별자는 연결된 메타데이터 구조에서 기본 키 역할을 합니다.
2.  **시간(기본값은 `time` 컬럼):** 데이터 포인트가 생성되거나 기록된 시각입니다. 64비트 정수로 저장되며 나노초 정밀도를 지원합니다.
3.  **값(기본값은 `value` 컬럼):** 해당 시각에 그 식별자와 연결된 실제 측정값 또는 이벤트 데이터입니다. 여러 데이터 타입을 지원하지만 `DOUBLE`(64비트 부동소수점)이 일반적이며 다양한 분석 함수를 사용할 수 있게 해 줍니다.

내부적으로 태그 테이블은 메타데이터(태그에 대한 설명 정보)와 실제 시계열 데이터 포인트를 분리해 관리합니다.

```
       Tag Table: Vibration
+--------------------------------------+------------------------------------------+
|        Meta (Sensor Attributes)      |            Data (Sensor Readings)        |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | NAME    | Attribute1| Attribute2 | | | ID | TIME (nanoseconds)        |VALUE| |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | Sensor-A| LocationX | TypeY      | | | 0  | 1719292147529850600       |-1.3 | |
| | Sensor-B| LocationZ | TypeW      | | | 1  | 1719292148529850600       |-2.3 | |
| | Sensor-C| LocationX | TypeY      | | | 2  | 1719292149529850600       |-3.3 | |
| | ...     | ...       | ...        | | | 0  | 1719292150000000000       |-4.3 | |
| +---------+-----------+------------+ | | 0  | 1719292167529850600       |-5.3 | |
|                                      | | 2  | 1719292177529850600       |-6.3 | |
| (Managed in _Vibration_META table)   | | 1  | 1719292187529850600       |-7.3 | |
|                                      | | .. | ...                       | ... | |
|                                      | +----+---------------------------+-----+ |
|                                      | (Managed in _Vibration_DATA_N partitions)|
+--------------------------------------+------------------------------------------+
```

기본 `CREATE` 문에 이 구조가 반영되어 있습니다:

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- Links to Meta table, unique identifier
    time  DATETIME    BASETIME,    -- Core time column for indexing
    value DOUBLE                   -- Core value column
    -- Optional additional data columns can be defined here
);
-- Metadata columns are defined separately in the METADATA clause
```

### 지원하는 데이터 타입

Machbase 태그 테이블은 `value` 컬럼과 추가 데이터 컬럼에 다음 데이터 타입을 지원합니다:

| 타입     | 설명                             | 범위 / 표현                                                     | NULL 표현                     |
| :------- | :------------------------------- | :-------------------------------------------------------------- | :---------------------------- |
| `SHORT`    | 16비트 부호 있는 정수            | -32767 ~ 32767                                                  | -32768                        |
| `USHORT`   | 16비트 부호 없는 정수            | 0 ~ 65534                                                       | 65535                         |
| `INTEGER`  | 32비트 부호 있는 정수            | -2147483647 ~ 2147483647                                        | -2147483648                   |
| `UINTEGER` | 32비트 부호 없는 정수            | 0 ~ 4294967294                                                  | 4294967295                    |
| `LONG`     | 64비트 부호 있는 정수            | -9223372036854775807 ~ 9223372036854775807                      | -9223372036854775808          |
| `ULONG`    | 64비트 부호 없는 정수            | 0 ~ 18446744073709551614                                       | 18446744073709551615          |
| `FLOAT`    | 32비트 부동소수점                | ±1.175494e-38 ~ ±3.402823e+38                                   | 3.402823466e+38               |
| `DOUBLE`   | 64비트 부동소수점                | ±2.225074e-308 ~ ±1.797693e+308                                 | 1.7976931348623158e+308       |
| `DATETIME` | 날짜와 시간(나노초 정밀도)       | 1970-01-01 00:00:00 000:000:000 UTC 부터                        | 해당 없음                     |
| `VARCHAR`  | 가변 길이 문자열(UTF-8)        | 1바이트 ~ 32KB(32767바이트)                                     | NULL                          |
| `IPV4`     | IPv4 주소                        | "0.0.0.0" ~ "255.255.255.255"                                   | NULL                          |
| `IPV6`     | IPv6 주소                        | "::" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"                | NULL                          |
| `JSON`     | JSON 데이터 타입                 | 데이터 길이: 1바이트 ~ 32KB, 경로 길이: 1 ~ 512자             | NULL                          |

**참고:** 태그 테이블에서 `TEXT`와 `BINARY` 데이터 타입은 **지원되지 않습니다**.

## 태그 테이블 생성과 내부 구조

### 태그 테이블 생성

태그 테이블 생성의 기본 문법은 다음과 같습니다:

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(size) PRIMARY KEY, -- Tag identifier column
    time_column DATETIME BASETIME,         -- Time column with BASETIME property
    value_column datatype [SUMMARIZED]     -- Value column(s)
    [, additional_data_column datatype ...] -- Optional extra data columns
)
METADATA (
    meta_column1 datatype,                 -- Metadata columns
    meta_column2 datatype
    [, ...]
)
[ table_property = value [, ...] ];        -- Optional table properties
```

**주요 구성 요소:**

| 요소                         | 설명                                                                                                                                        | 영역       |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :--------- |
| `name_column` (`PRIMARY KEY`)  | 고유한 태그 식별자(예: 센서 이름)를 담는 컬럼입니다. 최대 길이를 지정한 `VARCHAR` 타입이어야 하며 `PRIMARY KEY`로 선언합니다. | 데이터/메타 |
| `time_column` (`BASETIME`)   | 각 데이터 포인트의 시각을 저장하는 컬럼으로 보통 `DATETIME`입니다. 기본 시간 인덱스임을 뜻하는 `BASETIME` 속성이 있어야 합니다. | 데이터     |
| `value_column` [`SUMMARIZED`] | 측정값을 담는 컬럼입니다. 보통 `DOUBLE`, `LONG`을 사용합니다. 선택적 `SUMMARIZED` 키워드를 붙이면 이 컬럼에 내장 통계 집계가 활성화됩니다. | 데이터     |
| `additional_data_column`   | 같은 시각의 주 값과 함께 보조 데이터를 저장하는 선택 컬럼입니다(예: 품질 플래그, 배치 번호).                                    | 데이터     |
| `METADATA` 절                | `name_column`에 지정된 각 고유 태그의 설명 속성(메타데이터)을 저장할 컬럼을 정의합니다. 이 속성들은 `name_column`으로 연결됩니다. | 메타       |
| `table_property`             | 테이블 동작과 자원 할당을 설정하는 선택적 키-값 쌍입니다(예: 파티셔닝, 통계).                                               | 테이블     |

### 태그 테이블 속성

태그 테이블 생성 시 성능과 자원 사용을 최적화하는 여러 속성을 설정할 수 있습니다:

| 속성                             | 설명                                                                                                                                      | 기본값  | 비고                                                                                          |
| :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :------ | :-------------------------------------------------------------------------------------------- |
| `TAG_PARTITION_COUNT`            | 생성되는 내부 데이터 파티션(하위 테이블) 수입니다. 적재와 조회의 병렬성에 영향을 줍니다.                                   | 4       | 값이 클수록 동시성이 좋아지지만 메모리 사용이 늘어납니다. 자원이 제한된 엣지 장비에서는 낮은 값(1 또는 2)을 사용하세요. |
| `TAG_DATA_PART_SIZE`             | 파티션 내 데이터 저장 단위의 목표 크기(바이트)입니다.                                                                     | 16MB    | 데이터 버퍼링과 인덱싱 관련 메모리 할당에 영향을 줍니다.                                      |
| `TAG_STAT_ENABLE`                | 태그별 통계 메타데이터(min, max, count, sum) 수집을 켜고 끕니다. `V$tableName_STAT` 뷰에 필요합니다.                       | 1 (켬)  | 통계가 필요 없으면 0으로 설정해 약간의 부담을 줄일 수 있습니다.                               |
| `TAG_DUPLICATE_CHECK_DURATION`   | 적재 중 중복 레코드(같은 name, time, value)를 무시할 수 있는 시간 창(나노초)입니다.                                       | 0       | 데이터를 간혹 재전송하는 소스의 중복 데이터를 다루는 데 도움이 됩니다.                        |
| `VARCHAR_FIXED_LENGTH_MAX`       | 주 데이터 저장 영역에 인라인으로 저장할 `VARCHAR` 데이터의 최대 길이(바이트)입니다. 더 긴 문자열은 외부에 저장될 수 있습니다. | 15      | 가변 길이 문자열의 저장 효율과 조회 성능에 영향을 줍니다.                                     |

**속성을 지정한 예제:**

```sql
CREATE TAG TABLE basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT=2,
TAG_STAT_ENABLE=0,
TAG_DUPLICATE_CHECK_DURATION=3;
```

### 내부 테이블 구조

태그 테이블(예: `MYTAG`)을 만들면 내부적으로 다음의 관련 객체들이 함께 생성·관리됩니다:

1.  **`MYTAG`(가상 테이블):** 데이터를 조회하는 기본 인터페이스입니다. 메타데이터와 시계열 데이터를 결합한 통합 뷰를 제공합니다.
2.  **`_MYTAG_META`(메타데이터 테이블):** `METADATA` 절에 정의한 메타데이터 속성을 저장합니다. 여기서는 `name` 컬럼이 기본 키 역할을 해 태그별 메타데이터 항목의 고유성을 보장합니다. 빠른 조회를 위해 보통 메모리에 상주합니다.
3.  **`_MYTAG_DATA_N`(데이터 파티션 테이블):** 실제 시계열 데이터(`time`, `value`, 추가 데이터 컬럼)를 저장하는 내부 테이블입니다(`N`은 0부터 `TAG_PARTITION_COUNT - 1`까지). 데이터는 태그 `name`을 기준으로 이 파티션들에 분산됩니다.
4.  **`V$MYTAG_STAT`(통계 뷰):** `TAG_STAT_ENABLE=1`일 때 제공되는 시스템 뷰로, 데이터 파티션에서 도출한 태그별 요약 통계(최소/최대 시각, 최소/최대 값, 건수, 합)를 제공합니다.

```
      << Internal Structure of MYTAG >>

+---------------------------------------------------+
|                  MYTAG (Virtual Table)            |
|  (Query Interface)                                |
+---------------------+-----------------------------+
                      |                             |
+---------------------v-----------------------------+ +-----------------------+
|            _MYTAG_META (Metadata Table)           | |   V$MYTAG_STAT        |
| +-------+-----------+-----------+-----+           | | (Statistics View)     |
| | _ID   | NAME      | factory   | equip |         | +-----------------------+
| +-------+-----------+-----------+-----+           |           ^
| | 1     | sensor-A  | fac1      | eq1   | <------lookup-----+
| | 2     | sensor-B  | fac1      | eq2   |         |           |
| | ...   | ...       | ...       | ...   |         |           | (Aggregated From)
+---------+-----------+-----------+-------+         |           |
       (Memory Resident Lookup)                     |           |
                                                    |           |
                      +-----------------------------+-----------+
                      | (Data distributed by hash(NAME))
                      |
        +-------------+-------------+ ... +-------------+
        |             |             |     |             |
+-------v-------+ +---v-----------+ +-----+-------------v---+
| _MYTAG_DATA_0 | | _MYTAG_DATA_1 | | ... | | _MYTAG_DATA_3 |
| +---+ T | V + | | +---+ T | V + | |     | | +---+ T | V + |
| | 0 |...|...| | | | 1 |...|...| | |     | | | 3 |...|...| |
| | 0 |...|...| | | | 1 |...|...| | |     | | |.. |...|...| |
| +---+---+---+ | | +---+---+---+ | |     | | +---+---+---+ |
+---------------+ +---------------+ +-----+ +---------------+
   (Data Partition) (Data Partition)         (Data Partition)
```

## 태그 테이블의 메타데이터 관리

### 메타데이터의 역할

메타데이터는 원본 시계열 데이터 포인트에 필수적인 맥락을 제공합니다. 각 태그(`name`)에 설명 속성(예: 위치, 설비 종류, 제조사, 측정 단위)을 연결하면 다음이 가능해집니다:

*   **구조적 검색:** 알아보기 어려운 태그 이름 대신 특성을 기준으로 데이터를 필터링하고 조회할 수 있습니다.
*   **계층적 구성:** 센서, 설비, 위치 등의 관계를 표현할 수 있습니다.
*   **분석 강화:** 메타데이터로 정의한 의미 있는 범주로 데이터를 묶어 집계할 수 있습니다.

**개념적 계층 예시:**

```
Company
├── city1 Plant
│   ├── Air Conditioner
│   │   ├── Tag (Current Sensor)
│   │   ├── Tag (Voltage Sensor)
│   │   └── ...
│   ├── Refrigerator
│   ├── Compressor
│   └── Crane
├── city2 Plant
│   ├── ... (similar structure)
└── city3 Plant
    └── ... (similar structure)
```

각 태그는 자신의 맥락 정보(예: 공장, 설비)를 본질적으로 가지고 있습니다.

**활용 사례 예시:**

*   "'울산 공장'의 '크레인'에 연결된 모든 '전류 센서'의 최근 1분 데이터를 조회한다."
*   "'냉장고'에 속하고 이름이 'Current'로 시작하는 센서의 2022년 1월 31일 11:00~12:00 데이터를 모두 가져온다."
*   "모든 공장에서 'Air Conditioner'로 시작하는 설비의 'Current-3' 태그에 대해 지난달 최댓값을 찾는다."

### 메타데이터 컬럼 정의와 활용

메타데이터 컬럼은 `CREATE TAG TABLE` 문의 `METADATA` 절에서 정의합니다.

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA ( -- Define metadata columns here
    factory VARCHAR(32),
    equipment VARCHAR(64)
);
```

기존 태그 테이블의 메타데이터 구조에는 내부 메타데이터 테이블(`_tableName_META`)에 `ALTER TABLE`을 실행해 컬럼을 추가할 수도 있습니다.

```sql
ALTER TABLE _mytag_meta ADD COLUMN (line VARCHAR(16) DEFAULT 'op01');
```

메타데이터는 `_tableName_META` 테이블에 저장되며, 가상 태그 테이블에 대한 질의에서 효율적으로 조인하기 위해 보통 메모리에 유지됩니다. `name` 컬럼이 메타데이터 속성과 시계열 데이터를 잇는 고유 키 역할을 합니다.

```
       Metadata Area (_mytag_meta)             Data Area (_mytag_data_N)
+---------+----------+------------+----------+   +----+---------------------+-------+
| NAME    | factory  | equipment  | line     |   | ID | TIME                | VALUE |
+---------+----------+------------+----------+   +----+---------------------+-------+
| Sensor-A| Seoul    | drill      | op01     |   | 0  | ...                 | -1.3  | <= Data for Sensor-A
| Sensor-B| Seoul    | punch      | op01     |   | 1  | ...                 | -2.3  | <= Data for Sensor-B
| Sensor-C| Ulsan    | rolling    | op01     |   | 2  | ...                 | -3.3  | <= Data for Sensor-C
+---------+----------+------------+----------+   | ...| ...                 | ...   |
       (Unique entries per NAME)                      (Time-series measurements)
```

### 메타데이터 적재

새 태그의 메타데이터는 보통 그 태그의 첫 데이터 적재 시에 함께 제공됩니다. 데이터를 append할 때 태그 `name`이 `_tableName_META` 테이블에 아직 없으면, 해당 append 작업에서 제공된 값으로 새 메타데이터 레코드가 생성됩니다.

**중요:** 태그 `name`이 메타데이터 테이블에 이미 있으면, 그 태그에 대한 이후 append 작업은 기존 메타데이터 속성을 갱신하지 **않습니다**. 메타데이터 갱신은 `UPDATE ... METADATA` 명령으로 명시적으로 해야 합니다.

### 메타데이터 조건으로 데이터 조회

가상 태그 테이블에 대한 질의에는 데이터 컬럼(`time`, `value` 등)과 메타데이터 컬럼(`factory`, `equipment` 등) 양쪽의 조건을 함께 넣을 수 있습니다. 데이터베이스 엔진이 태그 `name`을 기준으로 데이터 파티션과 메타데이터 테이블을 자동으로 조인합니다.

```sql
-- Retrieve data for a specific tag in a specific factory and equipment
-- within a given time range.
SELECT name, time, value, factory, equipment
FROM mytag
WHERE factory = 'Seoul'            -- Metadata filter
  AND equipment LIKE '%chill%'     -- Metadata filter (LIKE supported)
  AND name = 'tag-1'               -- Data/Tag identifier filter
  AND time BETWEEN TO_DATE('2022-01-01 00:00:00')
               AND TO_DATE('2022-12-31 23:59:59'); -- Time filter
```

### 메타데이터 항목 수정

특정 태그의 기존 메타데이터 속성은 `UPDATE ... METADATA SET` 문법으로 수정할 수 있습니다.

```sql
UPDATE mytag METADATA SET equipment = 'chiller_unit_01', factory = 'Busan'
WHERE name = 'tag-existing'; -- MUST specify the target tag via 'name = ...'
```

**제약 사항:**

*   `WHERE` 절에는 `name` 컬럼에 대한 등호 조건이 반드시 있어야 **합니다**(`WHERE name = 'specific_tag_name'`).
*   메타데이터 저장 구조가 키-값 형태이므로 메타데이터 갱신에서는 `WHERE` 절의 다른 조건을 허용하지 않습니다.
*   메타데이터 속성 값을 기준으로 한 일괄 갱신은 이 명령으로 직접 지원되지 않습니다(향후 개선될 수 있습니다).

### 메타데이터 항목 삭제

메타데이터 항목은 `DELETE FROM ... METADATA` 문법으로 삭제할 수 있습니다.

```sql
DELETE FROM mytag METADATA WHERE name = 'tag_to_remove';
```

**Constraint:**

*   데이터 파티션에 해당 태그의 시계열 데이터가 남아 있으면 메타데이터 항목을 삭제할 수 **없습니다**.
*   메타데이터 항목을 지우려면 먼저 표준 `DELETE FROM table_name WHERE name = '...'` 명령으로 연결된 시계열 데이터를 삭제해야 합니다.

### 활용 사례: 메타데이터를 이용한 동적 태그 분류

메타데이터 컬럼을 사용하면 핵심 데이터 구조를 바꾸지 않고도 태그를 동적으로 분류하거나 표시할 수 있습니다.

**시나리오:** 오류가 자주 발생하거나 특정 리포트에 쓰이는 태그를 추적합니다.

1.  **`alias` 메타데이터 컬럼을 추가합니다:**
    ```sql
    ALTER TABLE _basic_meta ADD COLUMN (alias VARCHAR(128) DEFAULT 'normal');
    ```

2.  **특정 태그의 메타데이터를 갱신합니다:**
    ```sql
    UPDATE basic METADATA SET alias = 'error' WHERE name = 'tag-2';
    UPDATE basic METADATA SET alias = 'report' WHERE name = 'tag-4';
    ```

3.  **동적 분류를 기준으로 데이터를 조회합니다:**
    ```sql
    -- 특정 시간 범위에서 'error'로 표시된 태그의 데이터를 찾습니다
    SELECT * FROM basic
    WHERE alias = 'error'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';

    -- 'report'로 표시된 태그의 데이터를 찾습니다
    SELECT * FROM basic
    WHERE alias = 'report'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';
    ```

### `name` 컬럼의 고유성과 사용법

`name` 컬럼(태그 테이블 정의에서 `PRIMARY KEY`로 지정한 컬럼)은 다음과 같은 핵심 역할을 합니다:

*   **메타데이터의 기본 키:** `_tableName_META` 테이블에서 각 태그를 고유하게 식별해 메타데이터 속성의 생성·조회·갱신·삭제를 가능하게 합니다. 태그 이름은 고유해야 합니다.
*   **데이터 조회의 연결 고리:** 질의 시 메타데이터 속성과 해당 시계열 데이터 포인트를 연결합니다.
*   **직접 필터링:** 특정 태그의 원본 데이터와 집계 데이터를 직접 선택하거나 필터링할 수 있습니다.

**`name` 값 구성 팁:**

*   **태그 수가 적고(100개 미만) 메타데이터가 없는 경우:** 사람이 읽기 쉬운 간단한 고유 문자열을 사용하세요(예: `'tag_001'`, `'temp_sensor_main'`). `name`으로 직접 조회하는 경우가 많습니다.
*   **태그 수가 많고(1000개 이상) 메타데이터가 풍부한 경우:** 전체 `name`으로 직접 조회하는 일은 드뭅니다. 주요 메타데이터 필드를 이어 붙여 `name`을 구성하면(예: `'factoryA-equipmentX-sensorTypeZ-instance01'`) 고유성을 보장하고 맥락도 담을 수 있지만, 주된 조회는 전용 메타데이터 컬럼으로 필터링해야 합니다(예: `WHERE factory = 'factoryA' AND equipment = 'equipmentX'`). 이 방식이 크고 복잡한 시스템에서 탐색과 필터링에 더 잘 확장됩니다.

## 태그 테이블 활용

### 태그 테이블 설계 예제

특정 생산 로트와 연결된 여러 센서 측정값을 추적하는 제조 현장 시나리오를 생각해 봅시다.

태그 테이블 정의:

```sql
CREATE TAG TABLE tag (
    name                   VARCHAR(100) PRIMARY KEY,
    time                   DATETIME BASETIME,
    value                  DOUBLE SUMMARIZED,
    lot_no                 VARCHAR(32)
)
METADATA (
    factory_id             VARCHAR(16),
    equipment_id           VARCHAR(16),
    tag_id                 VARCHAR(32)
);
```

선택: lot_no로 빠르게 조회하도록 추가 데이터 컬럼에 인덱스를 만듭니다:

```sql
CREATE INDEX idx_tag_lot_no ON tag (lot_no) INDEX_TYPE TAG;
```

**질의 예제:**

특정 공장의 모든 태그 데이터를 조회합니다:

```sql
SELECT * FROM tag WHERE factory_id = 'fac01';
```

특정 공장의 특정 설비 데이터를 조회합니다:

```sql
SELECT * FROM tag WHERE factory_id = 'fac01' AND equipment_id = 'equip01';
```

특정 생산 로트와 연결된 데이터에서 원하는 컬럼만 조회합니다(효과가 있으면 idx_tag_lot_no를 사용):

```sql
SELECT name, time, value FROM tag WHERE lot_no = 'lot2001';
```

특정 공장·설비의 특정 태그 데이터를 시간 범위로 조회합니다:

```sql
SELECT * FROM tag
WHERE factory_id = 'fac01'
  AND equipment_id = 'equip01'
  AND tag_id IN ('tag01', 'tag02', 'tag03')
  AND time BETWEEN TO_DATE('2023-08-15 00:00:00') AND TO_DATE('2023-08-15 23:59:59');
```

### 기본 데이터 조회

`name`과 `time`에 대한 암묵적 인덱스를 활용해 표준 SQL `SELECT` 문을 사용합니다.

전체 레코드 수를 구합니다:

```sql
SELECT count(*) FROM tag;
```

데이터의 전체 시간 범위를 구합니다:

```sql
SELECT min(time), max(time) FROM tag;
```

특정 태그의 원본 데이터를 시간 범위로 조회합니다(시간순 정렬):

```sql
SELECT time, value FROM tag
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');
```

여러 특정 태그의 원본 데이터를 최신순으로 조회합니다:

```sql
SELECT /*+ SCAN_BACKWARD(tag) */ time, value FROM tag
WHERE name IN ('TAG1', 'TAG2')
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');
```

**참고:** `name` 컬럼의 조건은 일반적으로 등호(`=`)와 `IN` 목록 비교를 효율적으로 지원합니다.

### 복합 분석 시나리오

태그 테이블은 메타데이터와 선택적 롤업 기능을 함께 쓰면 정교한 분석을 가능하게 합니다.

**예제 시나리오 구성:**

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64),
    alias VARCHAR(64) -- For dynamic tagging
)
WITH ROLLUP; -- Enable automatic time-based aggregation (details in Rollup documentation)
```

**질의 유형:**

1.  **원본 데이터 추출:**
    *   2024년 2월 12일 '서울' 공장의 모든 태그 데이터.
    *   2024년 7월 12일 12:00~13:00, '서울' 공장 '압축기'의 데이터.
    *   2024년 9월 13일 13:20~13:30, 모든 공장의 '냉각 장치'에 연결되고 이름이 'Current'로 시작하는 태그의 데이터.
    *   2024년 12월 23일부터 29일까지, alias가 'CriticalSensor'로 표시된 모든 태그의 데이터.

2.  **통계 데이터 추출(롤업 사용):**
    *   2024년 한 해 동안 '서울' 공장 '크레인'의 모든 태그에 대한 월별 평균 `value`.
    *   2024년 6월 '청주' 공장에서 이름에 'Current'가 포함된 태그의 일별 최대 `value`.
    *   2020년부터 2024년까지 모든 공장에서 alias가 'CriticalSensor'인 모든 태그의 월별 평균 `value`.

3.  **통계 데이터 기반 분석(롤업 사용):**
    *   최근 5년간 이름에 'Power'가 포함된 모든 센서에 대해, 주별 최댓값과 그 주를 찾습니다.
    *   최근 1년간 '청주' 공장에서 이름에 'Temperature'가 포함된 모든 센서에 대해, 일별 최고 온도가 가장 높았던 날과 그날의 평균 온도를 찾습니다.
    *   최근 3개월간 모든 공장에서 이름에 'Pressure'가 포함된 센서에 대해, 일별 평균 압력이 가장 높았던 날과 그 평균값을 찾습니다.

**질의 예제(시간별 평균과 마지막 값):**

```sql
-- Get hourly average and last value for all tags in 'factory1' for a 12-hour period
SELECT
    name,
    ROLLUP('hour', 1, time) AS rollup_time, -- Aggregate time to the hour
    AVG(value) AS avg_value,
    LAST(time, value) AS last_value -- Get the last value within the hour
FROM mytag
WHERE name IN (SELECT name FROM _mytag_meta WHERE factory_id = 'factory1') -- Filter tags by metadata
  AND time BETWEEN TO_DATE('2000-01-01 00:00:00') AND TO_DATE('2000-01-01 11:59:59') -- Time range
GROUP BY name, rollup_time -- Group by tag and aggregated time interval
ORDER BY name, rollup_time;
```

### PIVOT을 이용한 데이터 모델 변환

`PIVOT` 절을 사용하면 길고 좁은 태그 테이블 형태를 전통적 모델과 비슷한 넓은 형태로 되돌릴 수 있어 특정 분석이나 리포팅에 활용할 수 있습니다.

```sql
-- Pivot selected tag values into columns based on time
SELECT *
FROM (
    -- Subquery selecting relevant data
    SELECT time, name, value -- Assuming name corresponds to tagid, value to dvalue
    FROM mytag
    WHERE time BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
      AND name IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
PIVOT (
    SUM(value) -- Aggregation function applied if multiple values exist for the same time/tag
    FOR name -- The column whose unique values become the new column headers
    IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE') -- List of tag names to pivot into columns
)
WHERE "FRONT_AXIS_TORQUE" >= 40 AND "REAR_AXIS_TORQUE" >= 20; -- Optional filtering on pivoted columns
```

**출력 예시(개념):**

```
time                          'FRONT_AXIS_TORQUE' 'REAR_AXIS_TORQUE' 'HOIST_AXIS_TORQUE' 'SLIDE_AXIS_TORQUE'
----------------------------- ------------------- ------------------ ------------------- -------------------
2018-12-07 16:42:29 840:000:000 12158               7244               NULL                NULL
2018-12-07 14:56:26 220:000:000 3308                663                NULL                NULL
...                           ...                 ...                ...                 ...
```
*(참고: 피벗된 컬럼 이름이 키워드와 겹치거나 특수 문자를 포함하면 따옴표로 감싸야 할 수 있습니다.)*

### 데이터 삭제

태그 테이블의 데이터 삭제는 주로 시간 기준 또는 태그 기준입니다. append에 최적화된 구조이므로 개별 레코드의 수정이나 삭제는 일반적으로 지원되지 않습니다.

**삭제 문법 예제:**

모든 태그에서 특정 시각 이전의 데이터를 모두 삭제합니다:

```sql
DELETE FROM table_name BEFORE TO_DATE('2023-01-15 00:00:00');
```

테이블의 모든 데이터를 삭제합니다(각별히 주의해서 사용):

```sql
DELETE FROM table_name;
```

특정 태그의 모든 데이터를 삭제합니다:

```sql
DELETE FROM table_name WHERE name = 'TAG01';
```

특정 태그의 특정 시각 이전 데이터를 삭제합니다:

```sql
DELETE FROM table_name WHERE name = 'TAG01' AND time < TO_DATE('2023-02-01 00:00:00');
```

## 태그 테이블의 인덱스

### 내부 인덱스와 외부 인덱스

태그 테이블은 (`name`, `time`) 컬럼에 자동으로 생성되는 고도로 최적화된 **내부 인덱스**를 갖추고 있습니다. 이 인덱스는 일반적인 시계열 질의 성능의 근간입니다.

*   **`WHERE name = '...'` 질의:** 내부 인덱스로 해당 태그의 모든 데이터를 효율적으로 찾아 시간순으로 반환합니다.
*   **`WHERE time BETWEEN ... AND ...` 질의:** 내부 인덱스로 지정한 시간 범위 안의 모든 태그 데이터를 훑어 시간순으로 반환합니다.
*   **`WHERE name = '...' AND time BETWEEN ... AND ...` 질의:** 내부 인덱스로 특정 태그의 특정 시간 범위 데이터를 매우 효율적으로 조회합니다.
*   **`WHERE name = '...' AND time BETWEEN ... AND ... AND value > ...` 질의:** 내부 인덱스로 해당 (`name`, `time`) 데이터 블록을 찾은 뒤, 가져온 데이터에 `value` 조건을 적용합니다.

**한계:** `name`이나 `time` 조건 없이 `value` 컬럼(또는 추가 데이터 컬럼)*만*으로 필터링하는 질의는 기본 내부 인덱스를 제대로 활용하지 못합니다.

*   **`WHERE name = '...' AND value > ...` 질의(시간 조건 없음):** `value` 조건을 적용하려면 `'tag-1'`에 속한 *모든* 데이터 블록을 훑어야 합니다. 그 태그의 전체 데이터량에 비례해 성능이 떨어집니다.

이런 경우에는 **외부 인덱스**를 만들 수 있습니다.

### 외부 인덱스 생성과 사용

이 컬럼들을 주로 필터링하는 질의를 빠르게 하려면 `value` 컬럼이나 다른 추가 데이터 컬럼에 외부 인덱스를 명시적으로 만들 수 있습니다.

**Syntax:**

```sql
CREATE INDEX index_name ON table_name (column_name) [INDEX_TYPE TAG];
-- INDEX_TYPE TAG is specific for optimizing indexes on Tag Table data columns.
```

**Example:**

```sql
CREATE TAG TABLE mytag (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    lot_no VARCHAR(32)
);
```

'value'와 'lot_no' 컬럼에 외부 인덱스를 만듭니다:

```sql
CREATE INDEX idx_mytag_value ON mytag(value) INDEX_TYPE TAG;
```

```sql
CREATE INDEX idx_mytag_lotno ON mytag(lot_no) INDEX_TYPE TAG;
```

이제 이 질의는 외부 인덱스 idx_mytag_value를 사용할 수 있습니다:

```sql
SELECT * FROM mytag WHERE name = 'TAG-2' AND value > 33;
```

이 질의는 외부 인덱스 idx_mytag_lotno를 사용할 수 있습니다:

```sql
SELECT * FROM mytag WHERE lot_no = 'LOTXYZ' AND time > TO_DATE('2024-01-01');
```

**외부 인덱스의 특성:**

*   **비동기:** 인덱스 갱신이 데이터 적재보다 약간 늦을 수 있습니다. 새로 적재된 데이터가 외부 인덱스에 아직 반영되지 않은 짧은 시간 차가 있을 수 있습니다.
*   **지역성:** 이 인덱스들은 보통 데이터 파티션과 함께 지역적으로 분할됩니다. 전체 데이터량이 늘어나면 외부 인덱스를 쓰는 질의도 다소 느려질 수 있지만, 인덱스 없이 전체를 훑는 것보다는 훨씬 낫습니다.
*   **자원 소모:** 외부 인덱스는 추가 저장 공간을 사용하며 데이터 적재 시 약간의 부담을 더합니다.

## 태그 테이블 데이터 적재

### 적재 방법 개요

Machbase Neo는 성능 요구와 클라이언트 환경에 따라 태그 테이블에 데이터를 적재하는 여러 경로를 제공합니다.

```
+-------------------+      +-------------------+      +-------------------+
|    ODBC/JDBC/     |      |       MQTT/       |      |    Machbase       |
|   .NET Clients    | ---> |   HTTP Clients    | ---> |     Native        | ---> Machbase Neo
+-------------------+      +-------------------+      |  CLI/SDK (C/Py)   |      (Tag Table)
                                                     +-------------------+
 (Standard SQL INSERT,      (REST API /append,       (High-Throughput
  or Append Protocol)        MQTT Subscription)        Append Protocol)
```

### 적재 방식 상세

1.  **SQL `INSERT` 문:**
    *   표준 `INSERT INTO table_name VALUES (...)` 문법을 사용합니다.
    *   요청/응답 방식으로 동작합니다.
    *   적은 양이거나 드문 입력에 적합합니다.
    *   성능 한계 때문에 고처리량·대용량 시계열 데이터에는 **권장하지 않습니다**.

2.  **Append 프로토콜:**
    *   대량 데이터 적재에 최적화된 Machbase 전용 고성능 프로토콜입니다.
    *   레코드당 네트워크 부담과 서버 측 처리를 최소화합니다.
    *   다음을 통해 사용할 수 있습니다:
        *   **Machbase CLI(명령행 인터페이스):** 파일에서 대량 적재하는 유틸리티입니다.
        *   **ODBC/JDBC/.NET:** Machbase 드라이버가 제공하는 확장 API로 Append 작업을 수행합니다.
        *   **C/C++/Go SDK:** 네이티브 라이브러리로 Append API에 직접 접근해 최고 성능을 냅니다.
        *   **Python(`machbaseAPI`):** Append 기능에 접근하는 래퍼 라이브러리입니다.
    *   높은 처리량이 필요한 대부분의 시계열 적재 시나리오에 **권장합니다**.

3.  **REST API:**
    *   Machbase Neo는 데이터 처리를 위한 HTTP 엔드포인트를 제공합니다.
    *   데이터 적재 엔드포인트는 `append` 메서드 파라미터를 지원하며, 내부적으로 효율적인 Append 프로토콜을 사용합니다.
    *   웹 기반 클라이언트나 HTTP로 연동하는 시스템에 적합합니다.

4.  **기타 언어(Python, Go, R):**
    *   보통 CLI나 ODBC/네이티브 SDK를 감싼 래퍼를 통해 효율적인 Append 프로토콜을 사용합니다.

**성능 참고:** 고주파 진동 데이터처럼 초당 수십만~수백만 건의 입력이 필요한 까다로운 사례에서는 최고 적재 속도를 내기 위해 네이티브 C/C++ SDK와 Append API를 사용해야 하는 경우가 많습니다.

## 운영 시 고려 사항

### 주요 사용 주의점

*   **메모리 사용:** 각 태그 테이블은 파티션 수(`TAG_PARTITION_COUNT`)와 데이터 버퍼(`TAG_DATA_PART_SIZE`)에 따른 기본 메모리를 사용합니다. 태그 테이블을 많이 만들면 서버 전체 메모리 사용량에 큰 영향을 줍니다. 가용 자원을 고려해 테이블 생성을 계획하세요.
*   **조회 성능:** 인덱스가 있는 컬럼(`name`, `time`, 또는 외부 인덱스가 있는 컬럼)에 조건이 없는 `SELECT` 질의는 전체 스캔이나 큰 범위의 부분 스캔을 유발해 데이터량에 비례해 성능이 떨어집니다. 가능하면 항상 `name`이나 `time` 범위 조건을 넣으세요.
*   **외부 인덱스:** 시간 조건 없이 해당 컬럼*만*으로 자주 필터링하는 경우에만 데이터/값 컬럼에 외부 인덱스를 만드세요. 저장 공간과 적재 부담이 늘어납니다.
*   **데이터 불변성:** 태그 테이블은 append 전용 데이터를 위해 설계되었습니다. 기존 데이터 레코드의 수정은 지원되지 않습니다. 삭제는 주로 시간 기준 또는 태그 전체 기준입니다.
*   **적재 방식:** 성능 요구에 맞는 적재 방식을 선택하세요. 대용량 데이터에는 Append 프로토콜(SDK, CLI, 드라이버, REST API `append` 메서드)을 사용합니다.

### 메모리 사용 고려 사항

태그 테이블의 메모리 사용량은 다음 요인들의 영향을 받습니다:

*   **적재 버퍼:** `TAG_DATA_PART_SIZE`(기본 16MB)에 비례합니다. 내부적으로 여러 버퍼를 사용합니다.
*   **파티션 수:** `TAG_PARTITION_COUNT`(기본 4)입니다. 파티션마다 자체 버퍼와 인덱스 구조를 유지합니다.
*   **인덱스 공간:** 파티션별 데이터량과 카디널리티에 따라 동적으로 할당됩니다. 대략 `TAG_DATA_PART_SIZE`와 평균 행 크기에 관련됩니다.

**테이블당 대략적인 메모리 계산식:**

`Memory ≈ (TAG_DATA_PART_SIZE * BufferFactor) + ((IndexSizeFactor * TAG_DATA_PART_SIZE / AvgRowSize) * IndexOverheadFactor) * TAG_PARTITION_COUNT`

*(내부 요인과 동적 할당 때문에 정확한 계산은 복잡하지만, 주요 결정 요인을 보여 줍니다.)*

기본 설정(`TAG_PARTITION_COUNT=4`, `TAG_DATA_PART_SIZE=16MB`)에서 태그 테이블은 부하 상황에서 주로 인덱싱과 버퍼링을 위해 대략 **최대 4GB**(파티션당 약 1GB)의 메모리를 동적으로 사용할 수 있습니다.

**메모리 사용 관리:**

*   **`TAG_PARTITION_COUNT` 축소:** 파티션 수를 낮추면(예: 1 또는 2) 병렬 계수와 그에 따른 메모리가 직접 줄어듭니다. `ALTER TABLE` 속성으로 동적으로 조정할 수 있습니다. 자원이 제한된 환경에 적합하지만 최대 동시 성능에는 영향이 있을 수 있습니다.
*   **`TAG_DATA_PART_SIZE` 조정:** 서버 설정에서 이 값을 줄이면(예: 4MB나 8MB, 1MB 이상이어야 함) 내부 버퍼와 인덱스 세그먼트 크기가 줄어 메모리 압박이 완화됩니다. 적용하려면 서버를 재시작해야 합니다.

## 요약

Machbase 태그 테이블은 센서 시계열 데이터를 효율적으로 관리하도록 설계된 특수 데이터베이스 객체입니다. 주요 특징은 다음과 같습니다:

*   **최적화된 구조:** 센서 측정값에 적합한 길고 좁은 데이터 모델([식별자, 시간, 값])을 사용합니다.
*   **메타데이터와 데이터 분리:** 설명 속성(메타데이터)과 원본 시계열 측정값(데이터)을 분리해 메타데이터를 유연하게 관리하고 데이터를 효율적으로 저장합니다.
*   **메타데이터 관리:** 메타데이터는 고유한 태그 `name`(기본 키)으로 연결되며 유연한 조회·추가·수정·삭제를 지원합니다(삭제는 데이터 삭제가 선행되어야 함).
*   **데이터 작업:** 고속 append 작업에 최적화되어 있습니다. 태그 `name`이나 `time`으로 필터링할 때 조회가 매우 효율적입니다. 데이터 수정은 지원되지 않으며 삭제는 주로 시간 범위 또는 태그 기준입니다.
*   **확장성:** 메타데이터 영역과 데이터 영역 모두 컬럼을 추가해 더 풍부한 맥락 정보나 측정 정보를 저장할 수 있습니다.
*   **성능:** 내부 파티셔닝과 전용 인덱싱으로 높은 적재 처리량과 빠른 시간 기준 질의 성능을 제공합니다.

태그 테이블은 Machbase 생태계에서 확장 가능한 시계열 애플리케이션을 구축하기 위한 견고하고 성능 좋은 기반을 제공합니다.
