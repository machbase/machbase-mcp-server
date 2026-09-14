# _arrival_time 시간 모델

원본 로그에는 어제 시각이 적혀 있는데 조회에서는 오늘 수집한 데이터로 보일 수 있습니다.
발생 시각과 수집 시각을 섞어서 사용하면 정상 입력도 누락처럼 보입니다.
LOG에서는 두 시간을 구분하는 것이 조회와 보존 정책의 출발점입니다.

## 발생 시각과 도착 시각

`event_time` 같은 사용자 DATETIME 컬럼은 “사건이 언제 발생했는가?”에 답합니다.
자동 생성되는 `_arrival_time`은 LOG의 시간 범위 접근과 보존형 삭제 기준입니다.
값을 생략하면 서버 시각을 사용하지만, 명시 입력과 역전 보정도 있으므로
항상 실제 네트워크 수신 시각이라고 단정해서는 안 됩니다.

DATETIME은 나노초 단위 값을 표현합니다. 이는 서버 시계가 매번 나노초 정밀도로 시간을
측정한다는 뜻이 아닙니다. 저장 후 LOG의 UPDATE로 시각을 고칠 수도 없습니다.

## 지연 이벤트 조회

아래는 빈 실습 테이블에 도착 시각을 오름차순으로 지정한 예제입니다.

```sql
CREATE LOG TABLE ch7_time (
    event_id   INTEGER,
    event_time DATETIME,
    message    VARCHAR(64)
);

INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1,
        TO_DATE('2026-01-02 09:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'normal arrival');
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 2,
        TO_DATE('2026-01-01 23:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'delayed arrival');

SELECT event_id
  FROM ch7_time
 WHERE event_time >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND event_time <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
 ORDER BY event_id;

SELECT event_id
  FROM ch7_time
 DURATION FROM TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS');
```

발생 시각 조회는 2번만, 도착 시각 조회는 1·2번 모두를 선택합니다.
늦게 들어온 이벤트의 발생 시각을 억지로 바꿀 필요는 없습니다.

## 시각 역전과 보정

`DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE`는 직전 도착 시각보다 작은 값이 들어올 때의
처리를 정합니다. 현재 Standard 코드 기준 동작은 다음과 같습니다.

| 값 | 역전 입력 처리 |
|---|---|
| 1, 기본값 | 직전 저장 `_arrival_time`보다 1ns 큰 값으로 보정 |
| 0 | 시각 역전 오류로 입력 거부 |

같은 시각은 역전이 아니므로 이 규칙만으로 행마다 고유한 시간이 보장되지는 않습니다.
시간이 같을 때도 순서를 고정해야 하면 이벤트 번호 등 추가 기준을 ORDER BY에 넣으세요.

다음은 앞의 실습 테이블을 그대로 사용하는 선택 실습입니다.
먼저 설정을 조회하고, 값이 1인 검증 환경에서만 실행하세요.
이 예제를 위해 운영 서버 설정을 변경하지는 마세요.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE';
```

```sql
-- 설정값 1에서 실행합니다. 값이 0이면 입력 오류가 예상됩니다.
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3,
        TO_DATE('2026-01-02 08:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'inverted arrival');

SELECT event_id,
       TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') AS stored_time
  FROM ch7_time
 ORDER BY event_id;
```

설정값 1에서는 3번의 저장 시각이 입력한 09:00이 아니라
`2026-01-02 10:01:00 000:000:001`이 됩니다. 발생 시각은 입력한 값 그대로입니다.
따라서 시각 역전 “허용”을 과거 시각의 무조건 보존으로 해석하면 안 됩니다.

## 데이터 이관 주의사항

원본 `_arrival_time`을 보존하려면 빈 대상에 오름차순으로 입력하는 것이 기본입니다.
정렬했더라도 대상에 더 최신 시각의 행이 있거나 다른 입력이 끼어들면 보정·오류가
발생할 수 있습니다. 이관과 일반 실시간 수집을 같은 테이블에서 섞지 마세요.

`DURATION`은 `event_time`이 아닌 `_arrival_time`을 사용합니다.
시간대와 날짜 형식까지 맞췄는데 범위가 다르다면 어떤 시간 컬럼을 조회하고 있는지
다시 확인해 보세요. 경계와 출력 방향은 조회 실습에서 이어집니다.

```sql
DROP TABLE ch7_time;
```

시간 문제를 문의할 때는 원본 시각, 저장된 시각, 해당 설정값을 함께 준비하면 좋습니다.
세 값을 나란히 놓으면 변환과 보정 중 어느 단계인지 구분하기 쉬워집니다.
