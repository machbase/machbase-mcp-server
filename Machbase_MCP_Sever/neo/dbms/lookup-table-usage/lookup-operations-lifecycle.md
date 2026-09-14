# 운영과 데이터 생명주기

LOOKUP 테이블의 백업·복구와 데이터 영속성을 다룹니다.

LOOKUP 테이블은 디스크에 영속 저장되는 참조 데이터 테이블입니다. 운영 중 값이 바뀔 수 있으므로 변경 절차, 백업, 복구, 조회 반영 시점을 함께 관리합니다.

영속 저장과 조회 시 데이터 위치는 구분해야 합니다. 서버가 기동되면 영속 저장본의 모든
LOOKUP 행을 메모리 테이블에 복원하고 `PRIMARY KEY`와 보조 인덱스를 구성합니다. 서비스 중
SQL 조회는 이 메모리 구조를 사용합니다.

## 데이터 생명주기

LOOKUP 데이터는 생성, 입력, 갱신, 참조, 백업, 복구의 흐름으로 관리합니다.

```
테이블 생성
  └── 기준 데이터 입력
        └── TAG/LOG/TRANSACTION 조회에서 JOIN 또는 참조
              └── 운영 중 UPDATE/DELETE
                    └── 백업 / 복구 / 마운트
```

기준 데이터는 원본 이벤트보다 작지만, 조회 결과 해석에 직접 영향을 줍니다. 따라서 변경 전후의 값과 적용 시점을 기록하는 운영 절차를 둡니다.

## 기준 데이터 변경 절차

운영 중 LOOKUP 데이터를 변경할 때는 다음 순서로 진행합니다.

1. 변경 대상 행을 조회합니다.
2. 영향 범위를 확인합니다.
3. UPDATE 또는 DELETE를 실행합니다.
4. 필요한 경우 `EXEC TABLE_REFRESH(table_name)`을 실행합니다.
5. 대표 조회 쿼리로 반영 여부를 확인합니다.

`TABLE_REFRESH`는 일반 SQL DML 직후마다 실행하는 명령이 아닙니다. 영속 LOOKUP 내용을 runtime
memory table에 다시 반영해야 할 때 사용하며, 이름 범위·권한·오류 계약은
EXEC procedure 정본을
참고합니다.

다음은 이 절차를 그대로 따라가는 실습입니다.

```sql
CREATE LOOKUP TABLE ch9_ops_sensor (
    sensor_id  VARCHAR(32) PRIMARY KEY,
    site       VARCHAR(16),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_ops_sensor VALUES ('TEMP-01', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-02', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-03', 'BUSAN', 'READY', NOW);

-- 변경 대상을 조회합니다.
SELECT sensor_id, site, status FROM ch9_ops_sensor WHERE sensor_id = 'TEMP-01';

-- 변경합니다.
UPDATE ch9_ops_sensor
   SET status = 'INACTIVE', updated_at = NOW
 WHERE sensor_id = 'TEMP-01';

-- 필요하면 memory table에 다시 반영합니다.
EXEC TABLE_REFRESH(ch9_ops_sensor);

-- 대표 조회로 확인합니다.
SELECT sensor_id, status FROM ch9_ops_sensor ORDER BY sensor_id;
```

TEMP-01만 `INACTIVE`가 되고 나머지 두 행은 `READY`로 남습니다.

일괄 변경은 반드시 대상 건수를 먼저 확인합니다.

```sql
SELECT COUNT(*) FROM ch9_ops_sensor
 WHERE site = 'SEOUL' AND status = 'READY';
```

TEMP-01이 이미 바뀌었으므로 COUNT는 1입니다. 변경 전에 세지 않으면 대상이 달라집니다.

```sql
DROP TABLE ch9_ops_sensor;
```

## 백업·복구 지원 범위

LOOKUP은 disk에 영속 저장되고 database backup에 포함되며, restore 뒤 row를 memory table과
index로 다시 구성합니다.
공통 BACKUP·RESTORE·MOUNT 명령과 Edition 범위는
백업·복원·마운트를 정본으로
사용합니다. 복구 뒤 대표 key와 JOIN 결과를 검증합니다.

## 운영 점검 항목

- 기준 데이터 변경 이력을 별도 로그나 운영 절차로 남깁니다.
- 대량 UPDATE/DELETE 전에는 대상 건수를 확인합니다.
- 자주 JOIN하는 컬럼에는 인덱스를 검토합니다.
- 서버 기동 시간과 LOOKUP 행·인덱스의 메모리 사용량을 실제 데이터 규모로 점검합니다.
- Append 중복 키 처리를 사용하는 경우 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정을 확인합니다.
- 백업 복구 후 대표 JOIN 쿼리로 참조 결과를 확인합니다.
