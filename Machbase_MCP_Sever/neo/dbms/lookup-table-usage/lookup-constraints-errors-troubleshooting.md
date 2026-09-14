# 제약, 오류, 문제 해결

LOOKUP 테이블의 제약 사항, 발생 가능한 오류, 문제 해결 방법을 다룹니다.

## 제약 요약

| 항목 | 제약 | 대표 오류 |
|---|---|---|
| PRIMARY KEY | 필수이며 하나만 지정 | `ERR-02322`, `ERR-02171` |
| PRIMARY KEY 컬럼 | `SET` 대상으로 지정 불가 | `ERR-02176` |
| 컬럼 타입 | `TEXT`·`CLOB`·`BLOB`·`BINARY` 사용 불가 | `ERR-02173` |
| JSON 컬럼 | 일반 컬럼으로는 가능, PRIMARY KEY로는 불가 | — |
| 메모리 | VOLATILE과 하나의 한도를 공유 | `ERR-01344` |
| UPDATE | `WHERE` 필수. 생략 시 실행되지 않음 | — |

## PRIMARY KEY 오류

LOOKUP은 PRIMARY KEY 없이 만들 수 없고, 두 개 이상 지정할 수도 없습니다.
다음 두 문장은 각각 실패합니다.

```sql
-- 실패: PRIMARY KEY가 없습니다. (ERR-02322)
CREATE LOOKUP TABLE ch9_err_nopk (code VARCHAR(16), label VARCHAR(64));

-- 실패: PRIMARY KEY가 두 개입니다. (ERR-02171)
CREATE LOOKUP TABLE ch9_err_twopk (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(32) PRIMARY KEY
);
```

두 문장 모두 테이블을 만들지 않으므로 정리할 객체가 없습니다.
복합 키가 필요하면 구분자로 조합한 단일 키 컬럼을 두고,
PRIMARY KEY 정책의 설계 기준을 따릅니다.

PRIMARY KEY 컬럼은 값을 바꿀 수 없습니다.

```sql
CREATE LOOKUP TABLE ch9_err_pk (code VARCHAR(16) PRIMARY KEY, label VARCHAR(64));
INSERT INTO ch9_err_pk VALUES ('KR', '대한민국');

-- 실패: PRIMARY KEY 컬럼은 SET 대상이 아닙니다. (ERR-02176)
UPDATE ch9_err_pk SET code = 'KO' WHERE code = 'KR';
```

키를 바꿔야 하면 기존 행을 삭제하고 새 키로 다시 입력합니다.

## 지원하지 않는 컬럼 타입

`TEXT`, `CLOB`, `BLOB`, `BINARY`는 LOOKUP 컬럼으로 사용할 수 없습니다.
긴 문자열은 `VARCHAR`로 선언하고, 원문 보관이 필요하면 LOG 테이블에 분리합니다.

```sql
-- 실패: 지원하지 않는 컬럼 타입입니다. (ERR-02173)
ALTER TABLE ch9_err_pk ADD COLUMN (memo TEXT);
```

JSON은 일반 컬럼으로 사용할 수 있습니다. 사용 범위는
JSON 컬럼과 조회를 참고합니다.

```sql
DROP TABLE ch9_err_pk;
```

## 메모리 한도

LOOKUP은 디스크에 영속 저장되지만 조회 실행 경로는 메모리입니다. 서버가 기동하면 전체 행과
인덱스를 메모리에 올리므로 사용량이 한도를 넘으면 `ERR-01344`가 발생합니다.

이 한도는 **VOLATILE 테이블과 공유합니다.** 설정 이름이 `VOLATILE_`로 시작하지만 LOOKUP도
같은 한도에 포함되므로, 두 타입을 함께 쓰는 환경에서는 합계로 판단해야 합니다.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';

SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
```

한도에 가까워지면 보존 범위를 줄이거나, 사용하지 않는 보조 인덱스를 제거하거나,
대규모 기준 정보는 인덱스와 성능의 기준에 따라 다른 테이블 타입을
검토합니다.

## 다중 row 변경 범위

일반 predicate UPDATE/DELETE는 여러 row에 적용될 수 있습니다. 실행 전 같은 predicate로
대상 수를 확인하고 일반 predicate UPDATE/DELETE의 계약을
따릅니다.

## LOOKUP JSON primary key 오류

JSON column은 일반 column으로 사용할 수 있지만 PRIMARY KEY로 선언할 수 없습니다. 식별자를
별도 scalar column으로 두고 JSON 컬럼과 조회의 type·path 규칙을
따릅니다.

## 제약 및 주의사항

- PRIMARY KEY 정책은 PRIMARY KEY 정책을 참고합니다.
- memory 규모와 index 비용은 인덱스와 성능에서 측정합니다.
- 시계열 원본은 TAG, 재시작 후 사라져도 되는 cache는 VOLATILE을 선택합니다.
- Append gate는 SDK Append matrix를 따릅니다.
