# 데이터 변경 정책

테이블 타입에 따라 `UPDATE`, `DELETE`, `TRUNCATE` 지원 범위가 다릅니다. 이 페이지는
데이터 모델을 선택할 때 필요한 정책만 요약합니다. 정확한 문법과 제약은 연결된 SQL
레퍼런스를 기준으로 확인하십시오.

변경 정책은 “이 값을 수정할 수 있는가”뿐 아니라 누가 어떤 범위를 바꾸고, 실패하면
어디까지 되돌릴 수 있는지를 정하는 것입니다. 현재 상태의 수정, 원본 계측값 보정,
스키마 변경과 보관 기간 만료에 따른 삭제를 별도 작업으로 구분합니다.

## 테이블 타입별 데이터 변경 지원 범위

| 테이블 타입 | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|----------|
| TAG | Standard의 DATA 보정: 태그 선택 조건과 BASETIME 조건 필요 | `BEFORE`, 태그/축 조건 또는 전체 삭제 | X |
| LOG | X | `BEFORE`, `OLDEST`, `EXCEPT`, 전체 삭제 | O |
| TRANSACTION | O | O | O |
| VOLATILE | 기본 키 조건 | 기본 키 조건 또는 전체 삭제 | X |
| LOOKUP | 일반 조건식, PK 변경 불가 | 일반 조건식 또는 전체 삭제 | X |

LOG 테이블은 적재한 이벤트를 수정하지 않는 구조입니다. 수정이 잦은 상태·설정 정보는
VOLATILE, LOOKUP 또는 TRANSACTION 테이블에 저장하십시오.

## 변경 단위와 실패 처리

| 작업 | 모델에서 정할 사항 |
|---|---|
| 현재 설정값 갱신 | 키, 허용 값과 동시 변경자 처리 |
| 잘못된 계측값 보정 | 태그·시간 범위, 보정 사유와 ROLLUP 재계산 |
| LOG 이벤트 정정 | 원본을 남기고 보정 이벤트로 연결할지 결정 |
| 기준 키 교체 | 참조하는 데이터의 전환 순서와 중간 실패 처리 |
| 기간 삭제 | 보관 기준 시각, 삭제 범위와 필요한 백업 |

TRANSACTION의 여러 DML은 명시적 트랜잭션으로 묶을 수 있습니다. LOOKUP·VOLATILE의
변경과 LOG·TAG 입력이 그 트랜잭션에 함께 참여한다고 가정하지 마십시오. 예를 들어
TAG 이력을 저장한 뒤 VOLATILE 캐시 갱신이 실패하면 이력은 남아 있을 수 있습니다.
캐시 재구성이나 재시도 절차가 필요합니다. Append의 트랜잭션 참여는 API와 대상 유형에
따라 다르므로 SDK 지원 범위에서 확인합니다.

여러 행을 변경하기 전에는 같은 조건으로 건수와 대표 행을 조회합니다. 이 사전 조회가
행을 잠그거나 이후 변경 범위를 고정하는 것은 아니므로, 동시 입력·갱신이 있다면 작업
시간대와 대상 범위를 함께 통제합니다. 실행 결과의 영향 행 수와 변경 후 값도 확인합니다.

## UPDATE 정책

### UPDATE 정책 TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION은 일반 관계형 `UPDATE`와 트랜잭션을 지원합니다.
- VOLATILE은 기본 키 일치 조건으로 대상을 지정합니다.
- LOOKUP은 일반 조건식을 사용할 수 있지만 기본 키 컬럼 자체는 바꿀 수 없습니다.

LOOKUP UPDATE에는 WHERE 조건이 필요합니다. LOOKUP·VOLATILE의 기본 키를 바꾸려면
삭제와 새 키 입력을 별도 문장으로 처리해야 하므로, 원본 보관과 참조 전환 순서를 먼저
정합니다. 이 두 문장을 묶어 롤백할 필요가 있다면 TRANSACTION 모델을 검토합니다.

LOOKUP의 지원 predicate와 표현식은
LOOKUP predicate UPDATE를
참고하십시오.

### TAG data UPDATE

TAG의 실제 시계열 데이터와 메타데이터는 서로 다른 구문으로 수정합니다.

| 대상 | 구문 | 핵심 제약 |
|------|------|-----------|
| 시계열 데이터 | `UPDATE tag_table SET ... WHERE ...` | 태그 선택 조건과 BASETIME 조건이 모두 필요 |
| 메타데이터 | `UPDATE tag_table METADATA SET ...` | TAG 메타데이터 전용 구문 사용 |

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서 지원합니다. 태그 이름,
BASETIME, 메타데이터 컬럼은 `SET` 대상이 될 수 없습니다. 수정한 구간에 구체화된 롤업이
있다면 `ROLLUP_REBUILD`로 다시 생성하십시오.

TAG DATA의 SET 우변은 기존 행 컬럼을 참조할 수 없습니다. 따라서
`SET value = value + 1`처럼 일괄 가산하는 방식으로 보정하지 않습니다. 계산한 보정값을
상수나 매개변수로 전달하고, 필요한 범위를 한정합니다. 여러 번 보정한 이력을 남겨야 하면
현재 값만 덮어쓰지 말고 변경 전후 값과 사유를 별도 이력으로 저장합니다.

문법과 허용 표현식은 다음 레퍼런스가 정본입니다.

- TAG data UPDATE
- TAG data UPDATE WHERE/SET 제약
- TAG 메타데이터

LOG 테이블은 `UPDATE`를 지원하지 않습니다.

## DELETE 정책

### DELETE 정책 TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION은 일반 `WHERE` 조건으로 삭제할 수 있습니다.
- VOLATILE은 기본 키 조건으로 삭제하거나 조건 없이 전체 행을 삭제할 수 있습니다.
- LOOKUP은 일반 조건식으로 삭제하거나 `WHERE` 없이 전체 행을 삭제할 수 있습니다.

LOOKUP의 지원 predicate는
LOOKUP predicate DELETE를
참고하십시오.

### LOG

LOG는 임의의 일반 `WHERE` 조건 대신 로그 보존형 삭제 구문을 사용합니다.
`OLDEST`, `EXCEPT`, `BEFORE` 또는 전체 삭제 중 목적에 맞는 형식을 선택합니다. 정확한 구문과
실행 예제는 LOG 데이터 생명주기를 참고하십시오.

### TAG/KV

TAG/KV는 `BEFORE`로 오래된 데이터를 정리하거나, 태그 이름과 축 조건을 사용해 대상을
지정합니다. `BEFORE` 시각은 현재보다 과거여야 합니다. 실행 구문은
TAG 데이터 변경을 참고하십시오.

수동 보존 삭제를 반복해야 한다면
Retention Policy를
사용하십시오.

### TAG 메타데이터

TAG 메타데이터는 `DELETE FROM table_name METADATA` 형식으로 삭제합니다. 대상 중 실제
데이터가 있는 태그가 하나라도 있으면 문장 전체가 실패합니다.

상세 조건은 TAG 메타데이터를 참고하십시오.

## TRUNCATE 정책

`TRUNCATE TABLE`은 LOG와 TRANSACTION에서만 지원합니다. 스키마와 인덱스 정의는
유지하고 모든 행을 제거합니다.

| 항목 | TRUNCATE | DELETE |
|------|----------|--------|
| 대상 | 테이블 전체 | 타입에 따라 전체 또는 조건 지정 |
| `WHERE` | 불가 | 지원 범위 안에서 가능 |
| TRANSACTION 롤백 | 명시적 트랜잭션에서 가능 | 명시적 트랜잭션에서 가능 |

삭제 전 백업과 재입력 경로를 확인하십시오. TAG는 지원되는 `BEFORE` 또는 태그/축 조건을,
VOLATILE과 LOOKUP의 전체 삭제는 조건 없는 `DELETE`를 사용합니다.

TRANSACTION의 롤백 가능 여부를 LOG의 삭제에도 적용하지 마십시오. 이미 확정한 변경은
이후 ROLLBACK으로 되돌릴 수 없습니다. 또한 삭제와 물리 디스크 공간 반환은 같은 시점의
작업이라고 가정하지 말고 저장 사용량과 해당 테이블의 정리 상태를 확인합니다.
