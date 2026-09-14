# 운영과 데이터 생명주기

TAG 데이터의 수명 주기는 수동 삭제, Retention Policy와 중복 입력 방지로 관리합니다. 이
페이지는 운영 선택 기준을 설명하며 전체 SQL 문법은 관련 레퍼런스로 연결합니다.

## TAG 데이터 삭제

TAG 데이터는 태그 식별자와 축 조건을 사용해 삭제 범위를 제한합니다. 시간축 TAG의 대표적인
선택은 다음과 같습니다.

| 목적 | 조건 |
| --- | --- |
| 한 태그의 전체 데이터 삭제 | 태그 `PRIMARY KEY` 일치 |
| 한 태그의 시간 범위 삭제 | 태그 일치 + BASETIME 범위 |
| 모든 태그의 과거 데이터 삭제 | BASETIME 조건 또는 `BEFORE` |
| 테이블의 전체 데이터 삭제 | 조건 없는 TAG `DELETE` |

다음 예제는 별도 검증 테이블을 만들고 삭제 범위를 확인한 뒤 정리합니다.

```sql
CREATE TAG TABLE ch5_lifecycle (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0002', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3.0);

DELETE FROM ch5_lifecycle
 WHERE name = 'TAG_0001'
   AND time < TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT name, time, value
  FROM ch5_lifecycle
 ORDER BY name, time;

DELETE FROM ch5_lifecycle;
SELECT COUNT(*) FROM ch5_lifecycle;
DROP TABLE ch5_lifecycle;
```

첫 삭제 후 TAG_0001의 2026-01-02 값 2.0과 TAG_0002의 값 3.0이 남습니다.
전체 삭제 후 COUNT는 0입니다. DATA 삭제와 METADATA 삭제는 별개입니다.
태그 등록 정보까지 제거하려면 METADATA 삭제 조건도 확인합니다.

삭제 조건의 연산자와 Edition별 지원 범위는
TAG DELETE 구문을
참고하십시오. 수동 삭제를 주기적으로 반복해야 한다면
Retention Policy를
사용하십시오.

### ROLLUP 데이터 처리

원시 TAG 데이터의 삭제와 이미 계산된 ROLLUP의 처리는 별개입니다. 원시 데이터를 정정하거나
삭제한 뒤 집계도 바뀌어야 한다면 대상 범위의 ROLLUP을 재구성합니다. ROLLUP 삭제 구문을
보관 정책처럼 반복 실행하지 마십시오.

- ROLLUP 부분 삭제와 재구성
- TAG 데이터 정정 후 ROLLUP 재구성

## 자동 중복 제거

`TAG_DUPLICATE_CHECK_DURATION`은 중복 검사 기간을 분 단위로 설정합니다.
Standard Edition에서는 0~43200분을 지정할 수 있으며 0은 비활성화입니다.
Cluster Edition에서는 0만 허용하므로 아래 활성화 실습은 Standard Edition 전용입니다.

서버 시각을 기준으로 검사 기간에 해당하는 데이터에서 태그·축·데이터 값이 같은 행을
중복으로 판정합니다. 인덱스 처리와 중복 행 정리 과정에서 수행되므로 Append 성공 응답을
“이미 중복 제거된 행 수”로 해석하지 않습니다. 늦게 도착한 데이터가 검사 기간 밖이면
기대한 중복 제거가 되지 않을 수 있으며 업무 키의 유일성 제약을 대신하지 않습니다.

```sql
CREATE TAG TABLE ch5_dedup (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
) TAG_DUPLICATE_CHECK_DURATION = 1440;

INSERT INTO ch5_dedup VALUES ('TAG_0001', NOW, 1.0);
INSERT INTO ch5_dedup SELECT name, time, value FROM ch5_dedup;

EXEC TABLE_FLUSH(ch5_dedup);
EXEC INDEX_FLUSH(ch5_dedup);

SELECT name, time, value
  FROM ch5_dedup
 WHERE name = 'TAG_0001';

ALTER TABLE ch5_dedup SET TAG_DUPLICATE_CHECK_DURATION = 60;
DROP TABLE ch5_dedup;
```

두 번째 입력은 첫 행을 복사하므로 축 시각도 정확히 같습니다. 이 실습은 운영 중 동시
입력이 없는 전제입니다. 저장 버퍼와 인덱스 처리를 기다린 뒤 한 행이 남는지 확인합니다.
일반 수집 루프에서 행마다 두 flush를 호출하는 패턴은 사용하지 않습니다.

전체 속성과 제약은 현재 버전의
CREATE TAG TABLE 구문을 기준으로
확인하십시오. 이미 보관 정책으로 삭제된 데이터는 중복 판정 대상에 남아 있지 않습니다.

## 운영 점검 순서

1. 원시 데이터와 ROLLUP의 보관 기간을 각각 정합니다.
2. 늦게 도착하는 데이터의 최대 지연을 측정해 중복 검사 기간을 정합니다.
3. 삭제·정정 전에 대상 태그와 시간 범위를 `SELECT`로 확인합니다.
4. 대량 변경 후 ROLLUP과 대표 조회 결과를 검증합니다.
5. 입력량, 디스크 사용량과 Retention 실행 상태를 함께 모니터링합니다.
