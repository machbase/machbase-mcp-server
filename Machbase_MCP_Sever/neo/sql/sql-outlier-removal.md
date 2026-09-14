# Machbase Neo SQL Automatic Outlier Removal

## 소개

특히 산업·환경 현장의 물리 센서에서 나오는 시계열 데이터는 잡음, 순간 스파이크, 진동 간섭, 그 밖의 이상 측정값에 취약합니다. 이런 이상치는 수가 많을 수 있으며, 대개 기대되는 동작 범위를 벗어난 값이라 데이터 분석을 방해하고 저장 공간을 불필요하게 소모하며 처리 시간을 늘립니다.

이런 이상치를 수동으로 또는 애플리케이션 수준에서 걸러 내는 일은 복잡하고 계산 비용이 큽니다. Machbase는 TAG 테이블에 연결된 태그 메타데이터에 정의한 규격 한계(Specification Limits)를 활용해, 데이터 적재 중 이상치를 자동으로 제거하는 기능을 내장하고 있습니다. 센서별 유효 동작 범위를 선언적으로 정의하면 그 범위 안의 데이터만 저장됩니다.

## 핵심 개념: 규격 한계(LSL/USL)

자동 이상치 제거 기능은 주어진 Tag ID의 기대 값 범위를 정의해 동작합니다. 이 범위는 태그 메타데이터 테이블의 두 가지 특수 속성으로 지정합니다:

*   **LSL(하한 규격):** 특정 Tag ID의 센서 측정값에 허용되는 최솟값을 정의합니다.
*   **USL(상한 규격):** 특정 Tag ID의 센서 측정값에 허용되는 최댓값을 정의합니다.

새 데이터 행이 TAG 테이블에 입력될 때, Machbase는 해당 Tag ID의 메타데이터에 정의된 LSL·USL 값을 기준으로 다음 검증을 수행합니다:

1.  **메타데이터 조회:** 들어온 행의 `name`(Tag ID)에 해당하는 LSL·USL 값을 종속 태그 메타데이터 테이블(`_TableName_meta`)에서 가져옵니다.
2.  **값 비교:** 지정된 `value` 컬럼(`SUMMARIZED`로 표시된 컬럼)에 입력되는 값을 가져온 LSL·USL과 비교합니다.
3.  **검증 규칙:** 들어온 값이 `LSL <= 입력값 <= USL` 조건을 만족할 **때에만** 입력이 허용됩니다.
    *   LSL이 `NULL`이면 하한 검사를 건너뜁니다(`입력값 <= USL`).
    *   USL이 `NULL`이면 상한 검사를 건너뜁니다(`LSL <= 입력값`).
    *   LSL과 USL이 모두 `NULL`이면 검증하지 않고 값을 그대로 받아들입니다.
4.  **처리:** 검증에 성공하면 행이 TAG 테이블에 입력됩니다. 실패하면(값이 정의된 LSL/USL 범위를 벗어나면) 해당 행의 입력이 거부되고 그에 맞는 오류가 반환됩니다(예: 값 < LSL이면 `ERR-02342`, 값 > USL이면 `ERR-02341`).

이 메커니즘은 태그별로 미리 정의한 허용 범위를 기준으로 적재 시점에 곧바로 데이터를 걸러 냅니다.

## 설정

규격 한계(LSL/USL)는 `CREATE TAG TABLE` 문의 `METADATA` 절에서 특수 키워드로 컬럼을 정의하거나, 나중에 `ALTER TABLE`로 해당 컬럼을 추가해 설정합니다.

### 테이블 생성 시 한계 정의

LSL·USL 값을 담을 컬럼은 `METADATA` 절 안에서 각각 `LOWER LIMIT`, `UPPER LIMIT` 키워드로 정의합니다.

**Syntax:**

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(...) PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype SUMMARIZED, -- Crucial: SUMMARIZED is required
    ...
)
METADATA (
    lsl_column_name numeric_datatype LOWER LIMIT, -- Column for LSL
    usl_column_name numeric_datatype UPPER LIMIT, -- Column for USL
    ... -- Other metadata columns
);
```

*   `value_column`: 숫자 타입이어야 하며 `SUMMARIZED` 키워드를 **반드시** 포함해야 합니다. 이상치 검증은 이 컬럼에 입력되는 값에만 적용됩니다.
*   `lsl_column_name`, `usl_column_name`: 한계 값을 저장할 메타데이터 컬럼의 이름으로, 사용자가 정합니다.
*   `numeric_datatype`: LSL/USL 컬럼의 데이터 타입은 `value_column`의 데이터 타입과 호환되어야 합니다.

**예제(LSL과 USL 모두):**

```sql
CREATE TAG TABLE sensor_readings (
    tag_id VARCHAR(50) PRIMARY KEY,
    ts DATETIME BASETIME,
    reading DOUBLE SUMMARIZED
)
METADATA (
    min_acceptable DOUBLE LOWER LIMIT,
    max_acceptable DOUBLE UPPER LIMIT,
    location VARCHAR(100) -- Regular metadata column
);
```

**예제(LSL만):**

최솟값 또는 최댓값 한쪽만 검증하면 되는 경우 한계를 하나만 정의해도 됩니다.

```sql
CREATE TAG TABLE pressure_monitor (
    tag_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure_kpa INTEGER SUMMARIZED
)
METADATA (
    min_pressure INTEGER LOWER LIMIT -- Only validate against a minimum pressure
);
```

### 기존 테이블에 한계 추가

기존 TAG 테이블의 메타데이터 정의에는 종속 메타데이터 테이블(`_TableName_meta`)에 `ALTER TABLE`을 실행해 LSL/USL 컬럼을 추가할 수 있습니다. 메타데이터 테이블에서 `DROP COLUMN`은 지원되지 **않습니다**.

**Syntax:**

LSL 컬럼 추가:

```sql
ALTER TABLE _table_name_meta ADD COLUMN ( lsl_column_name numeric_datatype LOWER LIMIT );
```

USL 컬럼 추가:

```sql
ALTER TABLE _table_name_meta ADD COLUMN ( usl_column_name numeric_datatype UPPER LIMIT );
```

**Example:**

처음에 LSL/USL 없이 'sensor_readings' 테이블이 있다고 가정합니다:

```sql
ALTER TABLE _sensor_readings_meta ADD COLUMN ( min_acceptable DOUBLE LOWER LIMIT );
```

```sql
ALTER TABLE _sensor_readings_meta ADD COLUMN ( max_acceptable DOUBLE UPPER LIMIT );
```

`ALTER TABLE`로 추가하면 기존 메타데이터 행들의 해당 컬럼 값은 처음에 모두 `NULL`입니다.

### 한계 값 설정

LSL/USL 컬럼을 정의한 뒤에는 종속 태그 메타데이터 테이블(`_TableName_meta`)의 행을 입력하거나 갱신해 Tag ID별 실제 한계 값을 설정합니다.

새 태그의 메타데이터를 입력하면서 한계를 설정합니다:

```sql
INSERT INTO sensor_readings metadata (tag_id, min_acceptable, max_acceptable, location)
VALUES ('TEMP_SENSOR_01', 10.0, 90.0, 'Boiler Room');
```

기존 태그의 한계를 갱신합니다:

```sql
UPDATE sensor_readings metadata
SET min_acceptable = 15.0, max_acceptable = 85.0
WHERE tag_id = 'TEMP_SENSOR_01';
```

## 동작과 제약

*   **`SUMMARIZED` 필수:** 자동 이상치 제거 기능은 TAG 테이블 정의의 대상 `value` 컬럼에 `SUMMARIZED` 키워드가 포함되어 있을 것을 **요구합니다**. 검증은 오직 이 컬럼에 입력되는 값에만 수행됩니다.
*   **데이터 타입 호환성:** `LOWER LIMIT`, `UPPER LIMIT`으로 지정한 메타데이터 컬럼의 데이터 타입은 TAG 테이블의 `SUMMARIZED` 값 컬럼 타입과 숫자적으로 호환되어야 합니다.
*   **LSL <= USL:** 특정 Tag ID에 LSL과 USL이 모두 정의되고 `NULL`이 아니면, LSL 값은 USL 값보다 작거나 같아야 합니다(`LSL <= USL`).
*   **검증 범위:** 검증은 TAG 테이블에 대한 `INSERT` 시에만 수행됩니다. 메타데이터에 LSL/USL을 정의하거나 갱신하기 전에 이미 들어 있던 데이터에는 소급 적용되지 않습니다.
*   **메타데이터 갱신:** 메타데이터의 LSL/USL 값을 갱신하면 *이후* 입력에 대한 검증 규칙이 바뀌지만, 새 한계를 벗어나게 된 기존 데이터를 다시 검증하거나 제거하지는 **않습니다**.
*   **NULL 처리:** 메타데이터에서 어떤 Tag ID의 LSL이 `NULL`이면 해당 태그로 들어오는 데이터의 하한 검사를 건너뜁니다. USL이 `NULL`이면 상한 검사를 건너뜁니다. 둘 다 `NULL`이면 그 Tag ID에는 이상치 검증을 수행하지 않습니다.
*   **한쪽 한계만 사용:** LSL 컬럼만 정의하면 최솟값 검사(`value >= LSL`)만 적용되고, USL 컬럼만 정의하면 최댓값 검사(`value <= USL`)만 적용됩니다.
*   **메타데이터 테이블 의존성:** 이 기능은 전적으로 종속 태그 메타데이터 테이블(`_TableName_meta`)의 구조와 내용에 의존합니다.

## 예제

이 절에서는 자동 이상치 제거 기능을 설정하고 활용하는 실전 예제를 다룹니다.

**1. LSL/USL을 포함한 스키마 정의:**

```sql
DROP TABLE IF EXISTS out_tag CASCADE;
```

LSL과 USL 메타데이터를 갖는 TAG 테이블을 만듭니다:

```sql
CREATE TAG TABLE out_tag (
    tag_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    lsl DOUBLE LOWER LIMIT,
    usl DOUBLE UPPER LIMIT
) TAG_PARTITION_COUNT=1;
```

**2. 메타데이터에 한계 정의:**

TAG_01의 동작 범위를 설정합니다(100.0 <= value <= 200.0):

```sql
INSERT INTO out_tag metadata (tag_id, lsl, usl) VALUES ('TAG_01', 100.0, 200.0);
```

메타데이터 항목을 확인합니다:

```sql
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
```

예상 출력:

```text
_ID | TAG_ID | LSL   | USL
--- | ------ | ----- | -----
1   | TAG_01 | 100.0 | 200.0
```

**3. 데이터 입력과 필터링 확인:**

LSL보다 작은 값(거부됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
```

> 예상 오류: `[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]`

LSL과 같은 값(허용됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 100.0);
```

범위 안의 값(허용됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
```

USL과 같은 값(허용됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 200.0);
```

USL보다 큰 값(거부됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 205.5);
```

> 예상 오류: `[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]`

허용된 데이터를 확인합니다:

```sql
SELECT * FROM out_tag WHERE tag_id = 'TAG_01';
```

예상 출력(타임스탬프는 다를 수 있음):

```text
TAG_ID | TIME                              | VALUE | LSL   | USL
------ | --------------------------------- | ----- | ----- | -----
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 100.0 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 150.5 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 200.0 | 100.0 | 200.0
```

**4. 메타데이터의 한계 갱신:**

TAG_01의 한계를 10.0 <= value <= 100.0으로 변경합니다:

```sql
UPDATE out_tag metadata SET lsl = 10.0, usl = 100.0 WHERE tag_id = 'TAG_01';
```

메타데이터의 변경을 확인합니다:

```sql
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
```

예상 출력:

```text
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | -----
1   | TAG_01 | 10.0 | 100.0
```

이전에 허용되던 150.5는 이제 새 USL을 넘습니다(거부됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
```

> 예상 오류: `[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]`

이전에 거부되던 95.2는 이제 새 범위 안에 들어옵니다(허용됨):

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
```

> 참고: 앞서 입력된 값(100.0, 150.5, 200.0)은 'out_tag' 테이블에 그대로 남아 있습니다. 메타데이터 한계 갱신은 기존 데이터에 영향을 주지 않습니다.

**5. NULL로 필터링 비활성화하기:**

한계를 NULL로 설정해 TAG_01의 이상치 필터링을 끕니다:

```sql
UPDATE out_tag metadata SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
```

메타데이터를 확인합니다:

```sql
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
```

예상 출력:

```text
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | ----
1   | TAG_01 | NULL | NULL
```

이전에 거부되던 값을 입력합니다(이제 성공해야 합니다). 이전 LSL보다 작은 값:

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 9.0);
```

이전 USL보다 큰 값:

```sql
INSERT INTO out_tag VALUES ('TAG_01', NOW, 250.0);
```
