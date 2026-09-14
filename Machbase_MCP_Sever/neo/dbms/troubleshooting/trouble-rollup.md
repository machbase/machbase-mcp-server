# ROLLUP 문제

ROLLUP 결과가 늦거나 원본과 다르면 처리 지연과 집계 의미의 차이를 먼저 구분합니다.
예제의 이름은 실제 진단할 테이블·작업으로 바꾸고 삭제·재생성을 첫 조치로 실행하지 않습니다.

## 1. 상태와 범위 확인

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL, ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP은 machsql 명령이며 SDK SQL API에는 보내지 않습니다.
gap은 RID 처리 차이이며 시간 지연이나 원본 보정 완료를 직접 나타내지 않습니다.
여러 계층·Cluster 노드의 상태, 서버 빌드와 데이터베이스·소유자를 함께 기록합니다.

## 2. 같은 데이터 집합인지 비교

| 증상 | 확인 |
|---|---|
| 일부 표본이 없음 | 조건 ROLLUP 후보가 선택됐는지, 원본 필터와 같은지 |
| FIRST/LAST 오류 | 실제 선택 후보가 EXTENSION인지 |
| 월·일 조회에 후보 없음 | 저장 간격 선택 규칙과 조회 버킷을 혼동했는지 |
| 평균 불일치 | NULL·유효 건수·부분 평균 재집계·태그 단위가 같은지 |
| 원본 정정 후에도 값이 같음 | FORCE로 과거를 되감으려 하지 않았는지, REBUILD 대상인지 |
| JSON 건수 불일치 | 원본 문서·SQL NULL·경로별 건수·문서 집계 건수를 구분했는지 |

원본은 DATE_TRUNC/DATE_BIN과 GROUP BY로, 저장 집계는 rollup()으로 조회해 비교합니다.
태그·시각·origin·종료 경계·집계 함수를 고정합니다. 적용 가능한 ROLLUP이 없으면
rollup()이 원본 스캔으로 자동 전환된다고 가정하지 않습니다.

## 3. 새 입력을 따라잡기

대상 작업이 활성화된 상태인지 확인하고 필요한 작업을 이름으로 지정합니다.

```sql
ALTER ROLLUP rollup_name FORCE;
SHOW ROLLUPGAP;
```

WAKEUP은 깨우기만 하고 FORCE는 처리 범위를 따라잡도록 기다립니다.
중지된 작업은 상태를 확인한 뒤 START하고, 여러 계층은 하위부터 처리합니다.
`ALTER SYSTEM FLUSH ROLLUP`은 지원되는 명령이 아니므로 진단 예제로 사용하지 않습니다.

## 4. 과거 보정과 재구성

Standard Edition에서도 모든 생성 구성이 REBUILD 대상인 것은 아닙니다.
완전한 자동 계층인지, Custom 간격·버킷이 지원되는지, 원본이 남아 있는지 먼저 확인합니다.
시간 인수는 지원되는 상수 문자열/TO_DATE를 쓰며 해당 시각의 버킷 전체가 재계산됩니다.

관련 작업의 중지·재시작과 부분 실패 가능성을 고려합니다. 성공·실패 뒤에도 결과와 실제
활성 상태를 확인합니다. REBUILD 실습과
인수 계약을 따릅니다.

## 5. 지원 요청 자료

- 서버 빌드·Edition·클라이언트와 접속 대상
- TAG 스키마, ROLLUP 정의, 조건과 의존 관계
- 상태·gap과 관측 시각
- 비교한 원본/ROLLUP SQL, 시간대·origin과 예상/실제 결과
- 최초 오류와 최근 원본 보정·삭제·대량 입력·설정 변경 이력
