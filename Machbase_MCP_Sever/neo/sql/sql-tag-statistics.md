# Machbase Neo SQL Tag Statistics

## 소개

Machbase TAG 테이블에 저장된 대용량 시계열 데이터를 조회할 때는 특정 Tag ID에 대한 통계 요약을 함께 얻는 경우가 많습니다. `NAME`(Tag ID)과 `time` 조건으로 TAG 테이블을 직접 조회하는 것이 기본이지만, 태그별로 방대한 데이터에서 최소·최대 값, 건수, 시간 경계 같은 집계 통계를 계산하면 상당한 계산 부담과 지연이 발생할 수 있습니다.

이 문제를 해결하고 태그별 핵심 통계에 빠르게 접근할 수 있도록, Machbase는 전용 시스템 뷰를 중심으로 한 자동 통계 집계 기능을 제공합니다. 이 기능은 Tag ID별 주요 통계 지표를 미리 계산해 유지하므로, 원본 TAG 테이블 데이터를 직접 계산하는 것보다 훨씬 빠르게 조회할 수 있습니다. 롤업 테이블과 비슷한 성능 이점을 주되, 시간 구간이 아니라 태그별 요약에 초점을 둡니다.

## The `v$tag_table_name_stat` View

TAG 테이블을 만들면 Machbase는 `v$tag_table_name_stat`라는 이름의 시스템 뷰를 자동으로 생성합니다(`tag_table_name`은 상위 TAG 테이블 이름). 이 뷰의 주된 역할은 Tag ID 단위로 집계한 통계 요약을 저장하고 손쉽게 제공하는 것입니다.

이 뷰는 Machbase 엔진이 내부적으로 채우고 관리하므로, 이런 일반적인 통계 지표를 위해 사용자가 복잡한 집계 과정을 직접 구성하거나 관리할 필요가 없습니다.

## 통계 수집 활성화

`v$tag_table_name_stat` 뷰가 채워지려면 TAG 테이블 정의 시 다음 설정이 필요합니다:

1.  **`TAG_STAT_ENABLE` 속성:** 태그별 통계 수집 기능의 전체 활성화 여부를 제어하는 테이블 속성입니다. 기본값은 `1`(활성)입니다. 테이블 생성 시 `0`으로 명시하면(`CREATE TAG TABLE ... TAG_STAT_ENABLE=0`) `v$tag_table_name_stat` 뷰가 채워지지 않고 태그별 통계도 유지되지 않습니다.
2.  **`SUMMARIZED` 키워드:** 값 기반 통계(최솟값, 최댓값과 그 시각)를 수집하려면 TAG 테이블 스키마의 값 컬럼(관례상 센서 측정값을 담는 세 번째 컬럼)을 `SUMMARIZED` 키워드로 정의해야 **합니다**. 값 컬럼 정의에서 `SUMMARIZED`를 빠뜨리면 값과 무관한 통계(행 수, 시간 경계, 최근 시각)만 수집·저장되고 값 관련 필드는 NULL로 남습니다.

**문법 예제(전체 통계 활성화):**

```sql
CREATE TAG TABLE device_metrics (
    name VARCHAR(80) PRIMARY KEY, -- Tag ID column
    time DATETIME BASETIME,        -- Timestamp column
    value DOUBLE SUMMARIZED        -- Value column with SUMMARIZED
)
TAG_STAT_ENABLE=1; -- Property (default, can be omitted)
```

## 제공되는 통계

`v$tag_table_name_stat` 뷰는 상위 TAG 테이블에 존재하는 Tag ID마다 다음의 사전 계산된 통계 컬럼을 제공합니다:

| 컬럼 이름         | 데이터 타입 | 설명                                                                     | `SUMMARIZED` 필요 |
| :---------------- | :-------- | :-------------------------------------------------------------------------- | :-------------------- |
| `NAME`            | VARCHAR   | 고유한 Tag ID입니다.                                                        | 아니오                |
| `ROW_COUNT`       | ULONG     | 이 Tag ID로 기록된 전체 데이터 포인트(행) 수입니다.                        | 아니오                |
| `MIN_TIME`        | DATETIME  | 이 Tag ID의 데이터 포인트 중 가장 이른 타임스탬프입니다.                   | 아니오                |
| `MAX_TIME`        | DATETIME  | 이 Tag ID의 데이터 포인트 중 가장 늦은 타임스탬프입니다.                   | 아니오                |
| `MIN_VALUE`       | *동일*    | 이 Tag ID의 `SUMMARIZED` 컬럼에 기록된 최솟값입니다.                       | **예**                |
| `MIN_VALUE_TIME`  | DATETIME  | `MIN_VALUE`가 처음 나타난 시각입니다.                                      | **예**                |
| `MAX_VALUE`       | *동일*    | 이 Tag ID의 `SUMMARIZED` 컬럼에 기록된 최댓값입니다.                       | **예**                |
| `MAX_VALUE_TIME`  | DATETIME  | `MAX_VALUE`가 처음 나타난 시각입니다.                                      | **예**                |
| `RECENT_ROW_TIME` | DATETIME  | 이 Tag ID로 가장 최근에 입력된 데이터 포인트의 시각입니다.                 | 아니오                |

*참고: `MIN_VALUE`와 `MAX_VALUE`의 데이터 타입은 상위 TAG 테이블에서 `SUMMARIZED`로 선언한 `value` 컬럼의 타입을 따릅니다.*

## 통계 조회

`v$tag_table_name_stat` 뷰의 가장 큰 장점은 방대할 수 있는 원본 TAG 테이블 데이터를 훑지 않고도 핵심 통계를 빠르게 얻을 수 있다는 점입니다.

**기본 질의 패턴:**

특정 태그의 최소/최대 시간 경계를 조회합니다('your_tag_table'을 실제 테이블 이름으로 바꾸세요):

```sql
SELECT min_time, max_time
FROM v$your_tag_table_stat
WHERE name = 'specific_tag_id';
```

여러 태그의 최소/최대 시간 경계를 조회합니다:

```sql
SELECT name, min_time, max_time
FROM v$your_tag_table_stat
WHERE name IN ('tag_id_1', 'tag_id_2', 'tag_id_3');
```

특정 태그의 행 수와 최소/최대 값을 조회합니다(SUMMARIZED 필요):

```sql
SELECT row_count, min_value, max_value
FROM v$your_tag_table_stat
WHERE name = 'specific_tag_id';
```

모든 태그의 전체 통계를 조회합니다:

```sql
SELECT *
FROM v$your_tag_table_stat;
```

특정 태그의 가장 최근 항목에 해당하는 실제 데이터 레코드를 조회합니다:

```sql
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT recent_row_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');
```

특정 태그의 최솟값이 나타난 시점의 실제 데이터 레코드를 조회합니다:

```sql
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT min_value_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');
```

## 제약 사항

태그별 통계 기능은 성능 면에서 매우 유용하지만 다음과 같은 본질적 제약이 있습니다:

*   **고정된 통계 범위:** 이 뷰는 미리 정해진 8가지 통계 지표만 제공합니다. 다른 통계나 더 복잡한 통계 함수(예: 표준편차, 백분위수)가 필요하면 원본 TAG 테이블에서 직접 계산하거나 롤업 테이블 같은 다른 기능을 사용해야 합니다.
*   **원본 데이터 품질 의존:** `v$tag_table_name_stat` 뷰에 저장되는 통계의 정확도는 원본 TAG 테이블에 적재된 데이터의 품질에 직접 좌우됩니다. 잘못된 데이터 포인트나 잡음은 집계 결과(MIN_VALUE, MAX_VALUE 등)에 그대로 반영됩니다. 입력 데이터 검증과 정제를 권장합니다.
*   **설정 요구 사항:** 앞서 설명했듯 통계 수집 기능이 온전히 동작하려면 `TAG_STAT_ENABLE=1` 속성과 대상 값 컬럼의 `SUMMARIZED` 키워드가 필요합니다. 설정이 잘못되면 뷰의 통계 데이터가 불완전하거나 아예 없게 됩니다.

## 예제

이 절에서는 태그별 통계 기능의 설정과 사용법을 보여 주는 실전 예제를 다룹니다.

### 사전 준비: 스키마 생성과 데이터 적재

이 예제들은 `tag`라는 TAG 테이블을 만들고 데이터를 채운 상태를 가정합니다.

**1. 스키마 정의(통계 활성화 확인):**

필요하면 기존 테이블을 삭제합니다: `DROP TABLE tag;`

통계를 활성화하고 'value'를 요약 대상으로 지정해 TAG 테이블을 만듭니다:

```sql
CREATE TAG TABLE tag (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
tag_partition_count=1,
TAG_STAT_ENABLE=1;
```

**2. 데이터 적재(`machbase-neo` import 사용 예):**

`tag_name,unix_timestamp,value` 형식의 데이터가 담긴 `homes.csv` 파일이 있다고 가정합니다.

```bash
# Example import command (adjust path and options as needed)
machbase-neo>> import --input C:\path\to\homes.csv --timeformat s --table tag --method append TAG;
```

### 통계 확인과 기본 질의

**1. 통계 뷰 구조 살펴보기:**

```sql
-- Display the columns and types of the auto-generated statistics view
DESC v$tag_stat;
```

**2. 태그별 행 수 확인:**

통계 뷰를 사용해 행 수를 효율적으로 얻습니다:

```sql
SELECT name, row_count
FROM v$tag_stat
ORDER BY name;
```

원본 테이블에서 직접 세는 방식과 비교합니다(테이블이 크면 더 느립니다):

```sql
SELECT name, COUNT(*) AS direct_count
FROM tag
GROUP BY name
ORDER BY name;
```

**3. 시간 경계 조회:**

```sql
-- Get the earliest and latest timestamps for specific tags
SELECT name, min_time, max_time
FROM v$tag_stat
WHERE name IN ('use', 'gen', 'temperature');
```

**4. 특정 통계 시점의 데이터 조회:**

가장 최근에 추가된 'use' 태그 데이터의 전체 레코드를 가져옵니다:

```sql
SELECT *
FROM tag
WHERE name = 'use'
  AND time = (SELECT recent_row_time FROM v$tag_stat WHERE name = 'use');
```

'temperature'의 최솟값이 기록된 시점의 전체 레코드를 가져옵니다:

```sql
SELECT *
FROM tag
WHERE name = 'temperature'
  AND time = (SELECT min_value_time FROM v$tag_stat WHERE name = 'temperature');
```

'gen' 태그의 최대 시각에 기록된 값을 가져옵니다:

```sql
SELECT value
FROM tag
WHERE name = 'gen'
  AND time = (SELECT max_time FROM v$tag_stat WHERE name = 'gen');
```

### 설정에 따른 차이 확인(제약)

다음 예제는 설정 선택이 통계 수집에 어떤 영향을 주는지 보여 줍니다.

**시나리오 구성:** 설정이 서로 다른 테이블 세 개를 만들고 *같은* 샘플 데이터를 적재합니다.

**테이블 1: 전체 통계 활성화(표준)**

```sql
DROP TABLE IF EXISTS stat1;
```

```sql
CREATE TAG TABLE stat1 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=1;
```

**테이블 2: SUMMARIZED 키워드 누락**

```sql
DROP TABLE IF EXISTS stat2;
```

```sql
CREATE TAG TABLE stat2 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_STAT_ENABLE=1;
```

**테이블 3: 속성으로 통계 비활성화**

```sql
DROP TABLE IF EXISTS stat3;
```

```sql
CREATE TAG TABLE stat3 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=0;
```

stat1에 동일한 샘플 데이터를 입력합니다:

```sql
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
```

```sql
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
```

```sql
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
```

```sql
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
```

```sql
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
```

```sql
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-15'), 120);
```

stat2에 동일한 샘플 데이터를 입력합니다:

```sql
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
```

```sql
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
```

```sql
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
```

```sql
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
```

```sql
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
```

```sql
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-15'), 120);
```

stat3에 동일한 샘플 데이터를 입력합니다:

```sql
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
```

```sql
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
```

```sql
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
```

```sql
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
```

```sql
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
```

```sql
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-15'), 120);
```


**결과 확인:**

테이블 1의 통계를 조회합니다(전체 통계 — MIN/MAX_VALUE와 그 시각까지 모든 컬럼이 채워짐):

```sql
SELECT * FROM v$stat1_stat;
```

테이블 2의 통계를 조회합니다(SUMMARIZED 없음 — MIN_VALUE, MIN_VALUE_TIME, MAX_VALUE, MAX_VALUE_TIME은 NULL이고 ROW_COUNT, MIN_TIME, MAX_TIME, RECENT_ROW_TIME은 채워짐):

```sql
SELECT * FROM v$stat2_stat;
```

테이블 3의 통계를 조회합니다(TAG_STAT_ENABLE=0 — 행이 반환되지 않으며 통계 수집이 완전히 꺼져 있음):

```sql
SELECT * FROM v$stat3_stat;
```

이 예제들은 태그별 통계 기능을 온전히 활용하려면 올바른 테이블 정의(특히 `SUMMARIZED` 키워드)와 `TAG_STAT_ENABLED` 속성이 필요하다는 점을 분명히 보여 줍니다.
