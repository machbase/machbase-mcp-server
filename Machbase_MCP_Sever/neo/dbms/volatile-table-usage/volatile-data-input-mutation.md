# 데이터 입력과 변경

VOLATILE 테이블의 `INSERT`, 중복 키 갱신, `DELETE`를 실행 가능한 예제로 설명합니다.

## 데이터 입력과 갱신

다음 예제는 마지막 정리 구문까지 순서대로 실행할 수 있습니다. 최신 상태처럼 같은 키의 값을
계속 바꿔야 한다면 `PRIMARY KEY`를 정의하고 `ON DUPLICATE KEY UPDATE`를 사용합니다.

```sql
CREATE VOLATILE TABLE ch10_mutation (
    id         INTEGER PRIMARY KEY,
    direction  VARCHAR(10),
    refcnt     INTEGER
);

INSERT INTO ch10_mutation VALUES (1, 'west', 0);
INSERT INTO ch10_mutation VALUES (2, 'east', 0);

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE;

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE SET refcnt = 1;

SELECT * FROM ch10_mutation ORDER BY id;
```

중복 키가 없으면 새 행이 입력됩니다. 중복 키가 있으면 `SET` 절이 없는 구문은 입력값으로
행 전체를 갱신하고, `SET` 절이 있는 구문은 지정한 컬럼만 갱신합니다. `PRIMARY KEY` 자체는
갱신 대상으로 지정할 수 없습니다.

대량 입력 API는 언어와 드라이버에 따라 초기화·바인딩·오류 처리가 다릅니다. 불완전한 코드
조각을 복사하지 말고 SDK 및 통합의 해당 드라이버 예제를
사용합니다.

## 조건부 갱신

이미 있는 행의 일부 컬럼만 바꿀 때는 `UPDATE`를 사용합니다. `INSERT ... ON DUPLICATE KEY
UPDATE`가 "없으면 넣고 있으면 바꾼다"인 것과 달리, `UPDATE`는 대상 행이 있을 때만 값을
바꿉니다.

VOLATILE 테이블의 `UPDATE`에는 `WHERE`가 필요하며, 조건은 삭제와 마찬가지로
`PRIMARY KEY = 값` 형태만 지원합니다. 다른 컬럼 조건이나 복합 조건은 사용할 수 없습니다.
`WHERE`를 생략한 전체 갱신도 지원하지 않습니다.

```sql
UPDATE ch10_mutation SET refcnt = refcnt + 1 WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
```

`SET` 절에는 `PRIMARY KEY` 컬럼을 지정할 수 없습니다. 키를 바꿔야 하면 기존 행을 삭제하고
새 키로 다시 입력합니다.

## 데이터 삭제

조건부 삭제는 `PRIMARY KEY = 값` 형태만 지원합니다. 다른 컬럼 조건이나 복합 조건은 사용할 수
없습니다.

```sql
DELETE FROM ch10_mutation WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
DROP TABLE ch10_mutation;
```

테이블 정의를 유지한 채 모든 행을 비우려면 `DELETE FROM 테이블명`처럼 WHERE를 생략합니다.
스키마까지 초기화해야 하면 DROP 후 다시 생성합니다. 서버를 재시작하면 데이터만 사라지고
테이블 정의는 남으므로, 재생성이 아니라 재적재 스크립트를 별도로 관리합니다.
