# NEXTVAL 함수

`NEXTVAL`은 LOOKUP 테이블의 SEQUENCE 컬럼에 대해 다음 자동 증가값을 `INT64`로 반환합니다.
`INSERT`의 값 식에서만 사용할 수 있습니다.

## 문법

```sql
NEXTVAL(sequence_column)
```

- `sequence_column`은 `PROPERTY(SEQUENCE=...)` 속성으로 생성된 컬럼이어야 합니다.
- `INSERT` 문 이외의 컨텍스트(SELECT, WHERE 등)에서는 사용할 수 없습니다.
- 인자는 정확히 하나이며 같은 INSERT 대상 테이블의 SEQUENCE 컬럼을 지정합니다.

---

## Sequence 컬럼 생성

SEQUENCE 컬럼은 LOOKUP 테이블의 `LONG` 또는 `INT64` 컬럼에서 지원합니다.
`PROPERTY(SEQUENCE=1)`은 시작값을 1로 지정합니다.

```sql
CREATE LOOKUP TABLE seq_lookup (
    id   LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    name VARCHAR(64)
);
```

---

## NEXTVAL 사용

```sql
-- NEXTVAL로 자동 증가 ID 삽입
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-b');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-c');

-- 결과 확인
SELECT * FROM seq_lookup;
id    name
----------
1     sensor-a
2     sensor-b
3     sensor-c

DROP TABLE seq_lookup;
```

---

## 주의사항

- `NEXTVAL`은 `INSERT` 문에서만 사용할 수 있습니다.
- SEQUENCE 컬럼은 **LOOKUP 테이블**에서만 지원됩니다. TAG, LOG, VOLATILE, TRANSACTION
  테이블에서는 사용할 수 없습니다.
- `LONG`·`INT64` 이외의 타입, 일반 컬럼, `SELECT`·`WHERE` 호출은 오류입니다.
- Sequence 번호는 트랜잭션 롤백이나 오류 발생 시에도 재사용되지 않을 수 있습니다 (gap이 발생할 수 있음).
- 자세한 DDL 설명은 DDL - Sequence Column 문서를 참고하십시오.
