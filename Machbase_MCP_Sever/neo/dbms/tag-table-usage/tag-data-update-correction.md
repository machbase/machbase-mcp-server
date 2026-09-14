# TAG data UPDATE와 데이터 보정

TAG DATA 보정은 원본 값을 직접 바꾸는 방식과 원본을 보존하고 조회 시 보정값을 적용하는
방식으로 나눕니다. 두 방식은 ROLLUP에 미치는 영향도 다릅니다. 이 페이지의 UPDATE 실습은
Machbase DBMS 8.7.0 Standard Edition을 전제로 합니다.

## 직접 값 정정

태그명과 BASETIME 조건을 함께 지정합니다. SET 우변은 기존 행 컬럼을 참조할 수 없으므로
`SET value = value + 1` 같은 식 대신 계산한 값이나 바인딩 매개변수를 전달합니다.
이름이 겹치지 않는 다음 테이블을 준비합니다. ROLLUP 정정까지 확인하도록 기본 ROLLUP도
생성합니다.

```sql
CREATE TAG TABLE ch5_correction (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    status INTEGER
) WITH ROLLUP;
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-02', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
```

### 범위 확인, 수정, 재조회

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM ch5_correction
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
UPDATE ch5_correction SET value = 25.0, status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, time, value, status
  FROM ch5_correction ORDER BY name, time;
```

첫 조회는 2건, 최솟값 10.0, 최댓값 99.0입니다. UPDATE 후 TEMP-01의 두 행은
value=25.0, status=1이고 TEMP-02의 20.0은 유지됩니다. 사전 COUNT는 대상을 잠그지
않으므로 동시 입력이 있는 작업은 기준 시각과 범위를 별도로 통제합니다.

### 여러 태그와 오류 처리

태그 선택에는 `=`, `IN`, `LIKE`를 사용할 수 있습니다. 넓은 패턴이나 긴 시간 범위를
수정하기 전에 대상 이름과 건수를 확인하고 작은 범위로 나눕니다. 여러 태그는 순차
처리될 수 있으므로 실패했을 때 문장 전체가 원자적으로 취소됐다고 가정하지 않습니다.
수정된 값과 남은 대상을 다시 조회한 뒤 재시도합니다.

연속된 시간 구간은 `>= 시작 AND < 끝`으로 정의하면 경계 행을 중복 처리하지 않습니다.
하루 전체를 `23:59:59`까지로 지정하면 그 뒤의 소수 초 데이터를 놓칠 수 있습니다.
정확한 허용 조건과 바인딩은 TAG UPDATE를
참고합니다.

### ROLLUP 재구성

원본 수정은 이미 계산된 ROLLUP을 자동으로 바꾸지 않습니다. 위 실습의 수정 구간을
다음처럼 재구성하고 ROLLUP 재구성의 진행 상태와
조회 검증 절차를 따릅니다.

```sql
EXEC ROLLUP_REBUILD(ch5_correction, 'TEMP-01',
    TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

## 원본 보존과 NULL 보정

원본과 보정값을 별도 컬럼에 저장하면 최초 값을 유지할 수 있습니다. 보정값이 NULL일 수도
있으므로 `corrected_value IS NOT NULL`만으로 보정 여부를 판정하지 않고 플래그를 사용합니다.

```sql
CREATE TAG TABLE ch5_correction_overlay (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    raw_value DOUBLE,
    corrected_value DOUBLE,
    is_corrected SHORT
);
INSERT INTO ch5_correction_overlay VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, NULL, 0);
UPDATE ch5_correction_overlay
   SET corrected_value = NULL, is_corrected = 1
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, raw_value, is_corrected,
       CASE WHEN is_corrected = 1 THEN corrected_value ELSE raw_value END AS effective_value
  FROM ch5_correction_overlay;
```

raw_value는 99.0, is_corrected는 1, effective_value는 NULL입니다. 플래그가 0이면
원본을 사용합니다. 이 방식은 조회식으로 값을 선택하며 raw_value는 바꾸지 않습니다.
기본 ROLLUP이 이 CASE 식을 자동 집계하거나 raw_value의 재구성만으로 보정을 반영한다고
가정하지 말고, 유효값을 집계하는 별도 조회·집계 모델을 정합니다.

## 보정 이력과 검증

여러 번의 변경 사유와 담당자를 남기려면 별도 이력을 기록합니다.

```sql
CREATE LOG TABLE ch5_correction_log (
    sensor_name VARCHAR(64),
    target_time DATETIME,
    old_value DOUBLE,
    new_value DOUBLE,
    reason VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

TAG 수정과 LOG 이력 기록은 하나의 TRANSACTION 트랜잭션으로 묶이지 않습니다.
순서·부분 실패·재시도 시 같은 작업을 식별할 번호를 애플리케이션에서 설계합니다.
테이블 생성만으로 감사 이력이 자동 기록되지는 않습니다.

정정 뒤 원본/유효값, 영향 행 수, 구간 통계와 보고서를 확인합니다. 완료 후 이번 실습에서
만든 객체만 정리합니다. 아래 CASCADE는 ch5_correction의 ROLLUP도 함께 삭제합니다.

```sql
DROP TABLE ch5_correction CASCADE;
DROP TABLE ch5_correction_overlay;
DROP TABLE ch5_correction_log;
```
