# 인덱스와 성능

VOLATILE 테이블의 인덱스 생성과 선택 기준을 설명합니다.

## 지원 인덱스

`PRIMARY KEY`를 선언하면 키 조회용 인덱스가 생성됩니다. 일반 컬럼에는 `REDBLACK` 인덱스를
추가할 수 있습니다. `BITMAP`과 `KEYWORD` 인덱스는 VOLATILE 테이블에서 지원하지 않습니다.

다음 예제는 생성부터 정리까지 순서대로 실행할 수 있습니다.

```sql
CREATE VOLATILE TABLE ch10_index (
    id       INTEGER PRIMARY KEY,
    name     VARCHAR(20),
    status   VARCHAR(16)
);

CREATE INDEX ch10_index_name_idx
ON ch10_index(name) INDEX_TYPE REDBLACK;

INSERT INTO ch10_index VALUES (1, 'west device', 'ACTIVE');
INSERT INTO ch10_index VALUES (2, 'east device', 'INACTIVE');

SELECT id, name
FROM ch10_index
WHERE name = 'west device';

DROP INDEX ch10_index_name_idx;
DROP TABLE ch10_index;
```

## 설계 기준

- 키 기반 단건 조회와 갱신에는 `PRIMARY KEY`를 사용합니다.
- 일반 컬럼의 동등·범위 조건이 반복될 때만 보조 인덱스를 추가합니다.
- 데이터뿐 아니라 인덱스도 메모리를 사용하므로 불필요한 인덱스를 제거합니다.
- 실제 쿼리의 조건과 행 수를 기준으로 생성 전후 응답 시간과 메모리를 비교합니다.

구문 세부사항은 인덱스 구문을
참고합니다.
