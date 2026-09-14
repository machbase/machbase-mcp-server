# ROLLUP 대상 TAG 테이블 설계

## ON과 FROM

`ON source(column)`은 원본 시간축 TAG의 컬럼을 집계합니다. `FROM rollup_name`은
기존 일반/확장 ROLLUP의 통계를 더 큰 구간으로 합칩니다. Custom의 대상도 TAG이지만,
다음 Custom 단계는 대상 TAG를 SELECT하는 INTO...AS 구문으로 구성합니다.

## 계층 실습

```sql
CREATE TAG TABLE ch6_design (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_design_sec ON ch6_design(value) INTERVAL 1 SEC;
CREATE ROLLUP ch6_design_min FROM ch6_design_sec INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_hour FROM ch6_design_min INTERVAL 1 HOUR;
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_design);
ALTER ROLLUP ch6_design_sec FORCE;
ALTER ROLLUP ch6_design_min FORCE;
ALTER ROLLUP ch6_design_hour FORCE;

SELECT name, rollup('hour', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_design
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01은 합계 60, 건수 3, 평균 20이고 TEMP_02는 100, 1, 100입니다.
하위부터 FORCE해야 상위가 새로 생성된 하위 결과까지 처리할 수 있습니다.

### 계층 제약

- 상위 간격은 소스 간격보다 커야 하며 정수배여야 합니다. 같은 간격도 허용되지 않습니다.
- 일반 ROLLUP에서 FROM으로 확장 ROLLUP으로 바꾸거나 그 반대로 바꿀 수 없습니다.
  EXTENSION 속성을 계층에서 일치시킵니다.
- JSON 경로·문서 모드도 소스와 맞아야 합니다.
- 필요한 조회의 최소 구간보다 거친 통계로 더 세밀한 원본을 복원할 수 없습니다.

다음은 각각 의도적으로 실패하는 생성 예제입니다.

```sql
CREATE ROLLUP ch6_design_bad_same FROM ch6_design_min INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_bad_divisor FROM ch6_design_min INTERVAL 90 SEC;
CREATE ROLLUP ch6_design_bad_ext FROM ch6_design_sec INTERVAL 1 MIN EXTENSION;
```

## 간격과 저장량 결정

모든 태그가 모든 구간에 값을 갖는다고 가정하면 논리 버킷 수는 대략
`(보관 시간 / 버킷 간격) × 태그 수`입니다. 태그 1만 개의 1초 버킷을 365일 보관하면
약 3,154억 버킷입니다. 실제 저장 행 수는 부분 집계·빈 구간·컬럼 수의 영향을 받고
디스크 크기는 압축과 저장 부가 비용까지 측정해야 합니다.

초 단위 관측을 분 단위로만 조회한다면 처음부터 모든 초 계층이 필요한지 검토합니다.
생성 간격은 SEC/MIN/HOUR로 표현하지만 DAY/WEEK/MONTH/YEAR는 조회 버킷 단위입니다.
특히 일 조회에 24 HOUR 저장 간격을 그대로 적용할 수 있다고 가정하지 말고
후보 선택 규칙을 확인합니다.

새 ROLLUP은 소스에 남아 있는 기존 데이터도 초기 집계하므로 초기 처리량과 gap을 확인합니다.
원본 보정은 FORCE로 되감기지 않습니다. REBUILD 지원 범위를 따릅니다.

## 정리

```sql
DROP ROLLUP ch6_design_hour;
DROP ROLLUP ch6_design_min;
DROP ROLLUP ch6_design_sec;
DROP TABLE ch6_design;
```
