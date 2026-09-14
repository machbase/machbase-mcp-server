# 운영과 데이터 생명주기

오래된 업무 데이터를 지울 때는 날짜만 보는 것으로 충분하지 않습니다.
취소된 주문과 아직 처리 중인 주문은 보관 기준이 다르고, 정리 작업 자체도 다른 쓰기와
충돌할 수 있습니다. 업무 조건과 작업 단위를 먼저 정한 뒤 삭제를 실행하세요.

## 데이터 보관 기준

TAG·LOG에는 원본 시계열을, TRANSACTION에는 변경 가능한 상태나 요약 결과를 둘 수 있습니다.
두 종류의 보관 기간이 반드시 같을 필요는 없습니다.
TRANSACTION에는 TAG·LOG의 Retention Policy를 그대로 적용하지 않습니다.
업무 조건에 맞는 DELETE와 외부 작업 스케줄을 설계하세요.

## 삭제와 롤백

```sql
CREATE TRANSACTION TABLE ch8_cleanup (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME
);
INSERT INTO ch8_cleanup VALUES (1, 'CANCELLED', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (2, 'PENDING', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (3, 'CANCELLED', TO_DATE('2026-02-01', 'YYYY-MM-DD'));

BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
DELETE FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
SELECT id, status FROM ch8_cleanup ORDER BY id;
ROLLBACK;

SELECT COUNT(*) AS after_rollback FROM ch8_cleanup;
```

대상은 1건, 삭제 중에는 2·3번, 롤백 후에는 3건입니다.
확인용 실습에서는 롤백했지만 운영에서 확정할 때는 업무 승인과 결과 확인 후 COMMIT을
선택합니다. 결과 커서는 종료 전에 닫아야 합니다.

실수하기 쉬운 부분은 사전 조회 건수와 실제 영향 행 수를 같은 것으로 보는 것입니다.
동시 변경과 스냅샷 충돌을 고려하고, 실행 시 받은 영향 행 수와 최종 상태까지 기록하세요.
잠금과 재시도에서 관련 상황을 확인할 수 있습니다.

## 배치 처리와 재개

전체 삭제를 하나의 긴 트랜잭션으로 처리하기보다 날짜 구간이나 고유 키 범위로 나눕니다.
각 구간의 경계, 처리 건수와 커밋 결과를 기록하세요.
중간 장애 뒤 어디부터 다시 처리해야 하는지 알 수 있어야 합니다.

기준 정보 이동을 위해 다른 테이블에 복사한 뒤 원본을 삭제할 때도 주의가 필요합니다.
현재 여러 TRANSACTION 테이블의 장애 시 원자적 커밋을 보장한다고 가정하지 마세요.
트랜잭션의 보장 범위에 맞춰 복사 결과 확인과 재개 절차를 설계합니다.
외부 API 호출과 긴 파일 작업을 BEGIN 안에서 기다리지 않는 것도 중요합니다.

## 백업 검증

백업 명령의 성공만 확인하지 말고, 마운트한 백업에서 업무 키·행 수·합계·인덱스를 점검하세요.
마운트 조회에는 `마운트명.소유자.테이블명`의 세 부분 이름을 사용합니다.
두 부분 이름을 사용해 운영 데이터와 혼동하지 마세요.

TRANSACTION은 증분 백업에서도 해당 백업 시점의 전체 테이블 저장소 스냅샷이 포함됩니다.
변경한 행 수만큼만 공간이 늘어날 것이라고 계산하지 마세요.
구체적인 실습은 백업·복원·마운트에 있습니다.

## 정리 후 운영 점검

행이 줄었다고 운영체제의 파일 크기가 곧바로 같은 비율로 줄어드는 것은 아닙니다.
업무 데이터 건수, 실제 파일 사용량, 백업 보관량을 각각 살펴보세요.
파일 크기를 줄이려고 내부 SQLite 파일에 직접 접속하거나 임의로 파일을 삭제하지 마세요.

```sql
DROP TABLE ch8_cleanup;
```

정리 작업이 실패하면 추가 삭제부터 시도하지 말고 마지막 성공 구간과 커밋 결과부터
확인하세요. 이런 기록이 있어야 데이터 누락과 중복 처리를 줄일 수 있습니다.
