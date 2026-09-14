# 데이터 입력과 변경

TAG 데이터는 SQL `INSERT`, Append API 또는 파일 적재 도구로 입력합니다. SQL 예제는 기능
확인과 소량 입력에 사용하고, 지속적인 수집은 Append API를 우선 검토합니다.

## SQL INSERT

다음 예제는 시간축과 거리축 TAG를 각각 만들고 데이터를 확인한 뒤 정리합니다.
실습 이름이 기존 테이블과 겹치지 않는지 먼저 확인합니다. 시간축 이름은 센서,
거리축 이름은 한 검사 대상·회차를 식별합니다.

```sql
CREATE TAG TABLE ch5_input_time (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.7);

CREATE TAG TABLE ch5_input_distance (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE,
    quality  INTEGER
);

INSERT INTO ch5_input_distance VALUES ('PIPE_A', 0.0, 10.1, 100);
INSERT INTO ch5_input_distance VALUES ('PIPE_A', 500.5, 11.2, 100);

EXEC TABLE_FLUSH(ch5_input_time);
EXEC TABLE_FLUSH(ch5_input_distance);

SELECT name, time, value FROM ch5_input_time ORDER BY time;
SELECT name, distance, value, quality
  FROM ch5_input_distance
 ORDER BY distance;

SELECT COUNT(*) FROM ch5_input_time;
SELECT COUNT(*) FROM ch5_input_distance;

DROP TABLE ch5_input_distance;
DROP TABLE ch5_input_time;
```

두 테이블은 각각 두 행을 반환합니다. 시간축 값은 25.5, 25.7이고 거리축은
0.0, 500.5입니다. 태그를 미리 등록하지 않았으므로 첫 DATA 입력에서 해당 이름이 자동
등록됩니다. 실제 발생 시각과 재전송 여부는 애플리케이션에서 관리합니다.

`TABLE_FLUSH`는 pending storage/input buffer를 명시적으로 flush해야 하는 검증·운영 절차에
사용합니다. transaction commit이나 조회 가시성 보장 수단은 아니며, 일반 수집 루프에서 행마다
실행하지 마십시오. 인자와 오류 계약은
EXEC procedure 정본을
참고합니다.

## 메타데이터와 함께 입력

사용자 메타데이터가 있는 TAG도 DATA만 입력해 새 태그를 자동 등록할 수 있습니다.
위치·단위 같은 값을 먼저 정해야 하면 `INSERT ... METADATA`로 등록한 뒤 DATA를
입력합니다. 데이터와 메타데이터를 함께 전달하는 지원 구문도 있습니다.
이미 등록된 속성을 일반 DATA 입력마다 갱신하는 것으로 가정하지 마십시오. 시스템 관리 컬럼은 입력
목록에 포함하지 않습니다.

메타데이터 값의 등록·갱신·삭제는 TAG 메타데이터를 참고하십시오.

## 입력 경로 선택

| 경로 | 적합한 경우 | 확인할 사항 |
| --- | --- | --- |
| SQL `INSERT` | 기능 확인, 저빈도 입력 | 문장별 파싱·왕복 비용 |
| SDK Append | 지속적인 고처리량 입력 | 배치 크기, flush와 오류 처리 |
| `csvimport` / `machloader` | 클라이언트 파일 일괄 적재 | 컬럼 순서, 날짜 형식, bad 파일 |
| `LOAD DATA INFILE` | 서버가 접근할 수 있는 파일 | 서버 경로·권한, 오류 정책 |

SDK별 연결과 Append 예제는 개발 도구 연동을,
파일 형식과 명령은
데이터 입력·적재·반출을
참고하십시오.

## 데이터 정정

TAG data UPDATE는 Standard Edition에서 태그 선택 조건과 BASETIME 범위를 함께 지정해
실행합니다. 태그명, 축과 메타데이터 컬럼은 일반 data UPDATE 대상으로 사용하지 않습니다.
정정 후 이미 계산된 ROLLUP은 자동으로 바뀌지 않으므로, ROLLUP이 있다면 대상 범위를
명시적으로 재구성합니다. 재구성 절차는 ROLLUP_REBUILD를
참고합니다.

성공 응답·실패 행 수와 재시도 정책을 선택한 입력 API에서 확인합니다. SQL의 NULL,
SDK의 NULL 표현과 숫자 0을 구분하고, 같은 관측을 재전송할 때의 중복 정책도 정합니다.
숫자 ARRAY·희소 입력은 ARRAY Append 예제를
사용합니다.

자세한 절차는 TAG 데이터 정정을 참고하십시오.
