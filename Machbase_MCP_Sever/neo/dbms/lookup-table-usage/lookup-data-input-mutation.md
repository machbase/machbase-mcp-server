# 데이터 입력과 변경

LOOKUP 테이블의 데이터 입력, 갱신, 삭제 방법을 하나의 실행 가능한 예제로 설명합니다.

## 예제 테이블 준비

다음 예제는 마지막의 정리 구문까지 순서대로 실행할 수 있습니다.

```sql
CREATE LOOKUP TABLE ch9_mutation (
    code       VARCHAR(32) PRIMARY KEY,
    label      VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_mutation VALUES ('TEMP', 'Temperature', 'ACTIVE', NOW);
INSERT INTO ch9_mutation VALUES ('PRESS', 'Pressure', 'ACTIVE', NOW);
```

SEQUENCE 키가 필요하면 SEQUENCE를 참고합니다.

## UPDATE

단건 변경은 PRIMARY KEY 조건으로 처리합니다.

```sql
UPDATE ch9_mutation
SET status = 'INACTIVE',
    updated_at = NOW
WHERE code = 'TEMP';
```

여러 행을 변경할 때는 먼저 같은 `WHERE` 절로 대상을 조회합니다. 단건 변경은 대상이 명확하고
인덱스를 사용할 수 있는 `PRIMARY KEY` 조건을 권장합니다.

PRIMARY KEY 컬럼 자체는 UPDATE할 수 없습니다. 키를 바꿔야 하면 기존 행을 삭제하고 새 키로
다시 입력합니다. 두 문장을 하나의 TRANSACTION 트랜잭션으로 묶을 수 없으므로 중간 실패와
참조 데이터의 변경 절차도 함께 설계합니다.

## 중복 키 처리

SQL INSERT에서 키 중복 시 갱신이 필요하면 `ON DUPLICATE KEY UPDATE`를 사용합니다.

```sql
INSERT INTO ch9_mutation
VALUES ('TEMP', 'Temperature sensor', 'ACTIVE', NOW)
ON DUPLICATE KEY UPDATE SET label = 'Temperature sensor', status = 'ACTIVE', updated_at = NOW;
```

Append로 데이터를 삽입할 때 primary key가 중복되면 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정에 따라 해당 행을 업데이트할 수 있습니다. 이 설정은 LOOKUP 테이블 append 경로의 중복 키 처리 정책이므로, 운영 환경에서는 현재 설정값을 확인한 뒤 사용합니다.

```sql
SELECT name, value
FROM v$property
WHERE name = 'LOOKUP_APPEND_UPDATE_ON_DUPKEY';
```

## TABLE_REFRESH

영속 저장된 LOOKUP 내용을 실행 중인 메모리 테이블에 다시 반영해야 할 때는
`TABLE_REFRESH`를 실행합니다.

```sql
EXEC TABLE_REFRESH(ch9_mutation);
```

일반 SQL DML 직후마다 실행하는 명령은 아닙니다. 대상은 현재 database의 LOOKUP table이며,
READ ONLY database에서는 실행할 수 없습니다. 이름 범위·권한·오류 계약은
EXEC procedure 정본을
참고하고, 클러스터 운영 절차는 운영과 수명주기를
참고합니다.

## Lookup 데이터 삭제

단건 삭제는 PRIMARY KEY 조건을 사용합니다.

```sql
DELETE FROM ch9_mutation
WHERE code = 'PRESS';
```

일반 조건식을 사용하면 조건에 맞는 모든 행을 삭제합니다. 모든 행을 삭제하려면 WHERE 절을
생략합니다.

```sql
DELETE FROM ch9_mutation;
DROP TABLE ch9_mutation;
```

## 변경 작업 체크리스트

- 단건 변경은 PRIMARY KEY 조건을 사용합니다.
- 일반 조건식으로 일괄 변경하기 전에 같은 조건으로 대상 범위를 조회합니다.
- 모든 행을 삭제하기 전에는 백업 또는 재입력 원본을 확인합니다.
- PRIMARY KEY 값 변경은 DELETE 후 INSERT로 처리합니다.
- Append 중복 키 처리는 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정을 확인합니다.
- 영속 LOOKUP을 runtime memory에 다시 반영해야 할 때만 `EXEC TABLE_REFRESH(table_name)`을
  사용합니다.
