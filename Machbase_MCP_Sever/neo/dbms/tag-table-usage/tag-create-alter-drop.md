# 생성, 변경, 삭제

TAG 테이블은 태그 식별자와 하나의 축 컬럼을 필수로 가집니다. 이 페이지에서는 실행 가능한
기본 예제를 제공하고, 전체 옵션은 SQL 레퍼런스로 연결합니다.

## TAG 테이블 생성

TAG 테이블은 앞의 두 컬럼이 고정된 역할을 가집니다. 이름 컬럼과 축 컬럼은 생략할 수
없고, 순서를 바꾸거나 다른 위치에 지정하면 생성에 실패합니다.

| 컬럼 위치 | 용도와 특성 |
| --- | --- |
| 첫 번째 | 태그 이름입니다. `VARCHAR` 컬럼에 `PRIMARY KEY`를 지정하며 다른 타입은 사용할 수 없습니다. 센서·설비·검사 회차처럼 반복해서 관측할 대상을 식별하고, 같은 태그 이름으로 여러 DATA 행을 입력할 수 있으므로 관계형 테이블의 행별 고유 키와 다르게 이해합니다. |
| 두 번째 | 관측값을 시간 또는 거리·위치 기준으로 정렬·조회합니다. 시간축은 `DATETIME BASETIME`, 거리축은 `DOUBLE`, `LONG`, `ULONG` 중 하나에 `BASEDISTANCE`를 지정합니다. 한 TAG 테이블에는 시간축 또는 거리축 중 하나만 정의할 수 있습니다. |
| 세 번째 이후 | 온도, 압력, 상태, 품질 코드처럼 관측마다 달라지는 DATA 컬럼입니다. 숫자형, `VARCHAR`, `DATETIME`, JSON, 숫자 ARRAY, BINARY를 사용할 수 있습니다. 여러 DATA 컬럼 중 그 태그를 대표하는 값 하나를 정해 두면 태그별 값 통계와 자동 ROLLUP의 기준으로 쓸 수 있고, 이때 `SUMMARIZED`를 지정합니다. 선택 사항이며 세 번째 컬럼에만 지정할 수 있습니다. |

ARRAY는 이름 컬럼, 축 컬럼과 `SUMMARIZED` 컬럼에는 사용할 수 없고 그 밖의 DATA
컬럼에만 사용합니다. `TEXT`, `CLOB`, `BLOB`은 LOG 테이블과 달리 TAG 테이블의 DATA 컬럼에 사용할
수 없으므로, 긴 문자열은 `VARCHAR`로, 이진 데이터는 `BINARY`로 저장합니다. 타입별 표기와
값 범위는 데이터 타입 사전을 참고합니다.

태그마다 한 번만 저장하는 속성은 위 컬럼 위치가 아니라 `METADATA` 절에 따로 선언합니다.
아래 시간축 예제의 `location`이 여기에 해당합니다.

다음 두 테이블은 이 페이지의 독립 실습용입니다. 기존 객체가 없는지 확인한 뒤 순서대로
실행합니다. 시간축과 거리축 중 데이터의 실제 의미에 맞는 축을 선택합니다. 거리축 TAG에는
ROLLUP을 사용할 수 없습니다.

### 시간축 TAG

```sql
CREATE TAG TABLE ch5_tag_ddl (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```

`SUMMARIZED`를 지정하면 두 가지가 따라옵니다. 첫째, 태그별 STAT 뷰에 `MIN_VALUE`,
`MAX_VALUE`처럼 값 자체의 통계가 이 컬럼을 기준으로 쌓입니다. `SUMMARIZED` 컬럼이 없으면
STAT에는 행 수와 축 범위만 남고 값 통계는 저장되지 않습니다. 둘째, `WITH ROLLUP` 자동
생성과 JSON 문서 전체 ROLLUP이 이 컬럼을 대상으로 삼습니다.

반대로 일반 숫자 ROLLUP은 `CREATE ROLLUP ... ON table(column)`에서 컬럼을 직접 지정하므로
`SUMMARIZED`가 없어도 만들 수 있습니다. 값 통계가 필요 없고 ROLLUP도 직접 만들 계획이면
지정하지 않아도 됩니다. 지정할 수 있는 타입은 지원 숫자 타입과 JSON이며, ROLLUP 생성
조건은 6장을 참고합니다.

위치·단위처럼 태그마다 한 번 저장하는 속성은 `METADATA`, 매 측정마다 달라지는 값은 일반
데이터 컬럼에 정의합니다.

### 거리축 TAG

```sql
CREATE TAG TABLE ch5_distance_ddl (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

소수 거리값에는 `DOUBLE`, 정수 축에는 값 범위에 맞는 `LONG` 또는 `ULONG`을 사용합니다.

## TAG 테이블 변경

이 절의 METADATA ADD/DROP 실습은 Standard Edition을 전제로 합니다.
TAG 데이터 컬럼의 임의 변경은 제한됩니다. 스키마를 확장해야 한다면 새 테이블로 전환하는
방법을 먼저 검토하십시오. 메타데이터 컬럼은 지원 구문으로 추가하거나 삭제할 수 있습니다.

```sql
ALTER TABLE ch5_tag_ddl
    METADATA ADD COLUMN (team VARCHAR(32));

ALTER TABLE ch5_tag_ddl METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch5_tag_ddl
    METADATA DROP COLUMN (team);

ALTER TABLE ch5_tag_ddl METADATA
    DROP COLUMN (limits);
```

Standard Edition에서는 TAG METADATA에 고정 길이 숫자 ARRAY 컬럼을 추가할 수 있습니다.
ALTER 전에 존재한 metadata row에는 명시한 ARRAY DEFAULT를 적용합니다. ALTER 뒤 TAG DATA
입력으로 자동 등록되는 metadata row에는 DEFAULT를 다시 적용하지 않으며 새 ARRAY 컬럼은
whole NULL입니다.

TAG DATA의 일반 ARRAY 컬럼은 `CREATE TABLE`에서 선언할 수 있지만 ALTER로 추가할 수
없습니다. TAG METADATA ARRAY에는 자동 index를 만들지 않으며 명시적 index도 지원하지
않습니다. 자세한 규칙은 TAG 메타데이터와
숫자 ARRAY 타입을 참고하십시오.

데이터가 있는 운영 테이블에서는 변경 전에 의존 쿼리, SDK 컬럼 순서와 재입력 경로를
확인합니다. ALTER 후 `DESC ch5_tag_ddl;`과 METADATA 조회로 변경 결과를 확인합니다.

## TAG 테이블 삭제

`DROP TABLE`은 원시 데이터와 메타데이터를 함께 제거합니다. ROLLUP 등 의존 객체가 있으면
먼저 의존 순서에 따라 정리해야 합니다. TAG의 `DROP TABLE ... CASCADE`는 연결된
ROLLUP도 제거할 수 있으므로 단순 정리의 기본 명령으로 사용하지 않습니다.
Custom ROLLUP의 대상 테이블은 별도 의존 제약도 확인합니다.

```sql
DROP TABLE ch5_distance_ddl;
DROP TABLE ch5_tag_ddl;
```

정확한 속성, 허용 범위와 DDL은
DDL 구문 사전을 참고하십시오.

다음으로 읽을 내용:

- TAG 테이블 구조와 스키마
- TAG 데이터 입력과 변경
- TAG 메타데이터
