# 조회와 분석

TAG 테이블에서 시계열 데이터를 조회하는 주요 패턴을 다룹니다. 시간축·거리축 범위 조회,
다중 태그 검색과 통계 뷰 활용을 포함합니다.

## Tag 데이터 조회

###  샘플 스키마 (시간축)

다음 예제는 TAG 테이블에 두 태그를 등록하고 태그마다 10개 행을 입력합니다.
`TAG_0001`은 2018년 1월 1일부터 10일까지, `TAG_0002`는 2월 1일부터 10일까지의 데이터를 사용합니다.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

insert into tag metadata values ('TAG_0001');
insert into tag metadata values ('TAG_0002');

insert into tag values('TAG_0001', '2018-01-01 01:00:00 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-02 02:00:00 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-03 03:00:00 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-04 04:00:00 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-05 05:00:00 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-06 06:00:00 000:000:000', 6);
insert into tag values('TAG_0001', '2018-01-07 07:00:00 000:000:000', 7);
insert into tag values('TAG_0001', '2018-01-08 08:00:00 000:000:000', 8);
insert into tag values('TAG_0001', '2018-01-09 09:00:00 000:000:000', 9);
insert into tag values('TAG_0001', '2018-01-10 10:00:00 000:000:000', 10);

insert into tag values('TAG_0002', '2018-02-01 01:00:00 000:000:000', 11);
insert into tag values('TAG_0002', '2018-02-02 02:00:00 000:000:000', 12);
insert into tag values('TAG_0002', '2018-02-03 03:00:00 000:000:000', 13);
insert into tag values('TAG_0002', '2018-02-04 04:00:00 000:000:000', 14);
insert into tag values('TAG_0002', '2018-02-05 05:00:00 000:000:000', 15);
insert into tag values('TAG_0002', '2018-02-06 06:00:00 000:000:000', 16);
insert into tag values('TAG_0002', '2018-02-07 07:00:00 000:000:000', 17);
insert into tag values('TAG_0002', '2018-02-08 08:00:00 000:000:000', 18);
insert into tag values('TAG_0002', '2018-02-09 09:00:00 000:000:000', 19);
insert into tag values('TAG_0002', '2018-02-10 10:00:00 000:000:000', 20);

exec table_flush(tag);
```

예제 마지막의 `TABLE_FLUSH`는 저장 버퍼를 명시적으로 처리하는 절차입니다. 트랜잭션 커밋이나
조회 가시성을 보장하는 명령으로 해석하지 않습니다. 자세한 동작은
TABLE_FLUSH를
참고하십시오.

### 모든 TAG 데이터 추출

```sql
select * from tag ORDER BY name, time;
```

```text
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
```

위 출력은 예제 실행 결과입니다. 결과 순서를 보장해야 하면 `ORDER BY name, time`을
명시합니다. 조건 없는 조회의 출력 순서는 실행 계획과 스캔 방향에 의존할 수 있습니다.

### 특정 tag 이름으로 데이터 추출

TAG 이름이 TAG_0002인 데이터를 조회하는 예제입니다.

```sql
select * from tag where name='TAG_0002' ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
TAG_0002              2018-02-05 05:00:00 000:000:000 15
TAG_0002              2018-02-06 06:00:00 000:000:000 16
TAG_0002              2018-02-07 07:00:00 000:000:000 17
TAG_0002              2018-02-08 08:00:00 000:000:000 18
TAG_0002              2018-02-09 09:00:00 000:000:000 19
TAG_0002              2018-02-10 10:00:00 000:000:000 20
[10] row(s) selected.
```

### 시간 범위 조회

TAG_0002에 대해 시간 범위를 지정해 데이터를 조회하는 예제입니다.

> `BETWEEN`은 양쪽 경계를 모두 포함하며 `>=`와 `<=`를 함께 쓴 조건과 같습니다.
> 아래 예제는 경계 시각에 데이터가 없어서 `>`·`<` 조건도 같은 결과를 반환합니다.
> 연속된 조회 구간이 경계 행을 중복해서 읽지 않도록 하려면 `time >= 시작 AND time < 종료`를
> 사용합니다.

```sql
select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

```sql
select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

### 거리축 샘플 스키마

거리축(`BASE DISTANCE`) Tag 테이블 기준의 예제입니다.

```sql
CREATE TAG TABLE trip_tag (
    name        VARCHAR(20) PRIMARY KEY,
    distance_m  DOUBLE BASE DISTANCE,
    value       DOUBLE,
    quality     INTEGER
);

INSERT INTO trip_tag VALUES('ODO_A', 0, 10.1, 100);
INSERT INTO trip_tag VALUES('ODO_A', 500, 11.2, 101);
INSERT INTO trip_tag VALUES('ODO_A', 1000, 12.3, 102);

INSERT INTO trip_tag VALUES('ODO_B', 1000.1, 21.5, 100);
INSERT INTO trip_tag VALUES('ODO_B', 1500, 22.1, 101);
INSERT INTO trip_tag VALUES('ODO_B', 2000, 22.9, 102);

EXEC TABLE_FLUSH(trip_tag);
```

### 거리 구간 조회

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_A'
   AND distance_m BETWEEN 0 AND 1000
 ORDER BY distance_m;
```

시간축과 마찬가지로 거리축도 축 범위를 좁히는 것이 기본 조회 패턴입니다.

### DOUBLE 거리축의 소수 경계 조회

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

숫자값 그대로 비교하므로 `1000`은 제외되고 `1500`, `2000`은 포함됩니다.

### 거리축 실행 계획 확인

대용량 거리축 조회에서는 `EXPLAIN`으로 거리 조건이 key range로 들어가는지 확인합니다.

```sql
EXPLAIN
SELECT name, distance_m, value
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

확인할 포인트:

- `KEYVALUE INDEX SCAN` 또는 유사한 인덱스 스캔이 보이는지
- `KEY RANGE` 아래에 `distance_m between ...` 조건이 보이는지

### 거리 버킷 집계

아래 예제는 0 이상인 거리를 500 단위 구간으로 나눕니다. TRUNC는 0 방향으로 자르므로
음수 좌표의 구간이 필요하면 FLOOR 등 원하는 경계 규칙을 따로 선택합니다.

```sql
SELECT TRUNC(distance_m / 500, 0) * 500 AS dist_bucket,
       COUNT(*)                         AS sample_count,
       MIN(value)                       AS min_v,
       MAX(value)                       AS max_v,
       AVG(value)                       AS avg_v
  FROM trip_tag
 WHERE name = 'ODO_B'
 GROUP BY TRUNC(distance_m / 500, 0) * 500
 ORDER BY dist_bucket;
```

예를 들어 `1750`은 `1500` 버킷에 집계됩니다.

### 다중 tag에 대한 시간 범위 검색

두 개 이상의 태그에 같은 시간 범위를 적용하는 예제입니다. 대상 이름 목록이 정해져 있으면
`IN`으로 표현합니다. 대상 태그가 많을 때의 성능은 목록 크기와 시간 범위를 함께 측정합니다.

```sql
select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-01-05 05:00:00 000:000:000 5
TAG_0001              2018-01-06 06:00:00 000:000:000 6
TAG_0001              2018-01-07 07:00:00 000:000:000 7
TAG_0001              2018-01-08 08:00:00 000:000:000 8
TAG_0001              2018-01-09 09:00:00 000:000:000 9
TAG_0001              2018-01-10 10:00:00 000:000:000 10
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[10] row(s) selected.
```

### 특정 값 이상의 데이터 검색

tag 값에 대한 조건도 지정할 수 있습니다. TAG_0002의 값 중 12보다 크고 15보다 작은 값에 대해 필터링한 결과입니다.

```sql
select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[2] row(s) selected.
```

### TAG별 통계 뷰 `V$<TABLE>_STAT`

tag 테이블을 생성하면, tag ID별 통계 정보를 집계하는 가상 테이블이 자동으로 만들어집니다. 이 가상 테이블의 이름은 v${tag 테이블 이름}_stat입니다.

태그명·축 관련 통계와 세 번째 SUMMARIZED 컬럼의 값 통계를 구분합니다.
STAT는 백그라운드 인덱스·통계 처리 상태를 반영하므로 직전 입력의 검증은 원본 SELECT와
함께 수행합니다. 즉시 통계 확인이 필요한 실습에서는 TABLE_FLUSH 후 INDEX_FLUSH로
처리를 기다립니다.

<span class="badge-since">BASE DISTANCE 축별 STAT 스키마는 Machbase 8.7.0부터 지원</span>

축 관련 컬럼 이름과 타입은 TAG 테이블의 축에 따라 달라집니다.

| TAG 축 | 최소/최대 축 | 최소/최대값 발생 축 | 최근 입력 row 축 | 축 통계 타입 |
|--------|--------------|----------------------|------------------|--------------|
| `DATETIME BASE TIME` | `MIN_TIME`, `MAX_TIME` | `MIN_VALUE_TIME`, `MAX_VALUE_TIME` | `RECENT_ROW_TIME` | `DATETIME` |
| `DOUBLE/LONG/ULONG BASE DISTANCE` | `MIN_DISTANCE`, `MAX_DISTANCE` | `MIN_VALUE_DISTANCE`, `MAX_VALUE_DISTANCE` | `RECENT_ROW_DISTANCE` | 원본 BASE DISTANCE 타입 |

두 Edition의 공통 컬럼은 `NAME`, `ROW_COUNT`, `MIN_VALUE`, `MAX_VALUE`입니다. Cluster
Edition에서는 스키마 맨 앞에 `HOSTNAME VARCHAR(64)`가 추가됩니다.

#### BASE TIME STAT 스키마

```sql
DESC v$tag_stat;
```

```text
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_TIME                                                             datetime            31
MAX_TIME                                                             datetime            31
MIN_VALUE                                                            double              17
MIN_VALUE_TIME                                                       datetime            31
MAX_VALUE                                                            double              17
MAX_VALUE_TIME                                                       datetime            31
RECENT_ROW_TIME                                                      datetime            31
```

세 번째 컬럼에 SUMMARIZED 키워드가 없으면 VALUE 관련 정보(MIN_VALUE, MAX_VALUE, MIN_VALUE_TIME, MAX_VALUE_TIME)는 저장되지 않습니다.

수집되는 통계 정보는 다음과 같습니다.

|컬럼 이름|정보|
|--|--|
|NAME|Tag ID의 이름|
|ROW_COUNT|행 수|
|MIN_TIME|해당 tag ID 행 중 가장 작은 basetime 컬럼 값|
|MAX_TIME|해당 tag ID 행 중 가장 큰 basetime 컬럼 값|
|MIN_VALUE|해당 tag ID 행 중 가장 작은 summarized 컬럼 값|
|MIN_VALUE_TIME|MIN_VALUE와 함께 삽입된 basetime 컬럼 값|
|MAX_VALUE|해당 tag ID 행 중 가장 큰 summarized 컬럼 값|
|MAX_VALUE_TIME|MAX_VALUE와 함께 삽입된 basetime 컬럼 값|
|RECENT_ROW_TIME|가장 최근에 삽입된 basetime 컬럼 값|

다음 통계 실습은 앞의 20행 조회 예제와 분리한 테이블을 사용합니다. 따라서 아래 두 태그만
조회되며, 앞의 TAG_0001·TAG_0002가 통계 예상 결과에 섞이지 않습니다.

1. SUMMARIZED 컬럼이 존재하는 경우

```sql
CREATE TAG TABLE ch5_stat_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
```

```sql
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(ch5_stat_time);
EXEC INDEX_FLUSH(ch5_stat_time);
SELECT * FROM v$ch5_stat_time_stat ORDER BY name;
```

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 5
2021-08-11 00:00:00 000:000:000 20                          2021-08-14 00:00:00 000:000:000 2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 50
2022-08-10 00:00:00 000:000:000 200                         2022-08-11 00:00:00 000:000:000 2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

2. SUMMARIZED 컬럼이 존재하지 않는 경우

```sql
CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
```

```text
Executed successfully.
```

```sql
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(other_tag);
EXEC INDEX_FLUSH(other_tag);
SELECT * FROM v$other_tag_stat ORDER BY name;
```

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

#### BASE DISTANCE STAT 스키마

거리축 TAG 테이블의 통계 뷰는 거리값을 숫자 타입으로 제공합니다.

```sql
CREATE TAG TABLE distance_sensor (
    name       VARCHAR(32) PRIMARY KEY,
    odometer_m DOUBLE BASE DISTANCE,
    value      DOUBLE SUMMARIZED
);

INSERT INTO distance_sensor VALUES('sensor', 20.5, 8);
INSERT INTO distance_sensor VALUES('sensor', 10.25, 3);
INSERT INTO distance_sensor VALUES('sensor', 30.75, 5);

EXEC TABLE_FLUSH(distance_sensor);
EXEC INDEX_FLUSH(distance_sensor);
```

Standard Edition에서 `DOUBLE BASE DISTANCE` 테이블의 스키마는 다음과 같습니다.

```sql
DESC V$DISTANCE_SENSOR_STAT;
```

```text
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_DISTANCE                                                         double              17
MAX_DISTANCE                                                         double              17
MIN_VALUE                                                            double              17
MIN_VALUE_DISTANCE                                                   double              17
MAX_VALUE                                                            double              17
MAX_VALUE_DISTANCE                                                   double              17
RECENT_ROW_DISTANCE                                                  double              17
```

거리축 통계 컬럼 다섯 개의 타입은 원본 BASE DISTANCE 컬럼 타입을 따릅니다.

| BASE DISTANCE 타입 | STAT 컬럼 타입 | `DESC` 길이 |
|--------------------|----------------|-------------|
| `DOUBLE` | `double` | 17 |
| `LONG` | `long` | 20 |
| `ULONG` | `ulong` | 20 |

```sql
SELECT name,
       row_count,
       min_distance,
       max_distance,
       min_value,
       min_value_distance,
       max_value,
       max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 WHERE name = 'sensor';
```

- `MIN_DISTANCE`와 `MAX_DISTANCE`는 해당 통계 row의 최소·최대 거리입니다.
- `MIN_VALUE_DISTANCE`와 `MAX_VALUE_DISTANCE`는 각각 최소·최대 summarized value가
  발생한 거리입니다.
- `RECENT_ROW_DISTANCE`는 가장 큰 거리가 아니라 가장 최근에 입력된 row의 거리입니다.
- `SUMMARIZED` 컬럼이 없으면 `MIN_VALUE_DISTANCE`와 `MAX_VALUE_DISTANCE`는 `NULL`입니다.

##### Cluster Edition에서 조회

Cluster Edition의 통계 뷰에는 `HOSTNAME`이 추가되고 warehouse별 통계 row가 반환될 수
있습니다. 먼저 warehouse별 값을 확인합니다.

```sql
SELECT hostname, name, row_count,
       min_distance, max_distance,
       min_value, min_value_distance,
       max_value, max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 ORDER BY hostname, name;
```

row 수와 거리 경계는 tag 이름으로 안전하게 집계할 수 있습니다.

```sql
SELECT name,
       SUM(row_count)     AS row_count,
       MIN(min_distance)  AS min_distance,
       MAX(max_distance)  AS max_distance
  FROM V$DISTANCE_SENSOR_STAT
 GROUP BY name;
```

> **주의**
> `MIN_VALUE`와 `MIN_VALUE_DISTANCE`, `MAX_VALUE`와 `MAX_VALUE_DISTANCE`는 같은 warehouse
> row의 짝을 유지해야 합니다. 두 컬럼을 각각 독립적으로 `MIN` 또는 `MAX`하면 서로 다른
> warehouse의 값이 결합될 수 있습니다. `RECENT_ROW_DISTANCE`도 warehouse별 최근 입력
> 거리이므로 `MAX(RECENT_ROW_DISTANCE)`를 전체 cluster의 최근 입력 row로 해석하지 않습니다.

##### 8.7.0 호환성

BASE DISTANCE 통계 뷰의 기존 이름은 alias로 제공되지 않습니다. 기존 테이블도 8.7.0
서버가 재시작되면 새 스키마로 구성됩니다.

| 8.7.0 이전 이름 | 8.7.0 이름 |
|-----------------|------------|
| `MIN_TIME` | `MIN_DISTANCE` |
| `MAX_TIME` | `MAX_DISTANCE` |
| `MIN_VALUE_TIME` | `MIN_VALUE_DISTANCE` |
| `MAX_VALUE_TIME` | `MAX_VALUE_DISTANCE` |
| `RECENT_ROW_TIME` | `RECENT_ROW_DISTANCE` |

BASE TIME TAG 테이블은 기존 `*_TIME DATETIME` 스키마를 유지합니다.

### scan 방향 hint

축 방향의 순회와 결과 정렬을 구분합니다. 역방향 축 조회에서의 최신값은 가장 큰 축 값이며
마지막에 입력한 행을 나타내는 STAT의 RECENT_ROW 값과 다를 수 있습니다.
같은 축 값의 여러 행까지 순서를 구분해야 하면 애플리케이션의 추가 기준이 필요합니다.

```sql
SELECT *
  FROM tag
 WHERE name = 'TAG_0001'
 ORDER BY time
 LIMIT 10;

SELECT /*+ SCAN_FORWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;

SELECT /*+ SCAN_BACKWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;
```

hint가 없을 때의 기본 방향은
TABLE_SCAN_DIRECTION을 참고합니다.

## 정리

```sql
DROP TABLE ch5_stat_time;
DROP TABLE distance_sensor;
DROP TABLE trip_tag;
DROP TABLE other_tag;
DROP TABLE tag;
```
