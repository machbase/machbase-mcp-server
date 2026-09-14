# 제약, 오류, 문제 해결

다른 RDBMS에서 쓰던 SQL을 옮길 때는 이름이 비슷하다는 이유만으로 같은 기능을 기대하기
쉽습니다. 먼저 Edition과 공개 문법을 확인하고, 그다음 데이터 제약과 동시 접근 문제를
나누어 살펴보세요.

## 기능 지원 범위

TRANSACTION은 Standard Edition 전용입니다.
Cluster에서는 CREATE TABLE·CREATE TRANSACTION TABLE·CREATE TXN TABLE이 모두 거부됩니다.
LOG는 CREATE LOG TABLE로 명시해야 합니다.

| 요구 | 지원·대안 |
|---|---|
| 일반 SELECT·INSERT·UPDATE·DELETE | 지원, WHERE 없는 변경은 전체 행 대상 |
| 단일 PRIMARY KEY | 지원, 테이블당 하나 |
| 단일·복합 UNIQUE INDEX | 지원, 테이블 생성 후 별도 생성 |
| 컬럼 뒤 UNIQUE·테이블 수준 PRIMARY KEY | 해당 생성 문법 미지원 |
| FOREIGN KEY·Trigger·Stored Procedure | 미지원 |
| BEGIN·COMMIT·ROLLBACK | 지원, 중첩 BEGIN·SAVEPOINT 미지원 |
| ADD·DROP·RENAME COLUMN, RENAME TO | 지원 조건 확인 |
| MODIFY COLUMN | 미지원 |
| Append | SDK별 공개 경로와 배치 경계 확인 |
| TAG의 METADATA·BASETIME·BASEDISTANCE | TRANSACTION에는 적용하지 않음 |

Cluster에서 작은 기준 정보 변경은 LOOKUP을 검토할 수 있지만,
명시적 관계형 트랜잭션의 완전한 대체는 아닙니다.
원본 이벤트는 LOG·TAG, 관계형 트랜잭션은 별도 RDBMS 등 요구에 맞게 나누어야 합니다.

## 오류별 진단

| 증상 | 확인할 부분 | 다음 조치 |
|---|---|---|
| ERR-01418 고유성 위반 | PK·UNIQUE 키와 기존 데이터 | 입력 수정 또는 UPSERT 규칙 검토 |
| NOT NULL 위반 | 생략·NULL·빈 문자열·DEFAULT | 입력값과 제약 확인 |
| UPDATE가 0행 처리 | 키와 현재 상태 조건 | 대상 없음·이미 처리됨 등 업무 상태 확인 |
| Resource busy | 다른 쓰기, 오래된 읽기 스냅샷, 열린 커서 | 원인에 따라 대기·새 트랜잭션·커서 종료 |
| COMMIT·ROLLBACK이 busy | 같은 연결의 열린 결과 집합 | 결과 집합 정리 후 종료 재시도 |
| 오류 뒤 후속 SQL도 거부 | 롤백 전용 상태 여부 | ROLLBACK 후 새 작업 시작 |
| DDL 실패 | 참조 인덱스·VIEW·활성 트랜잭션 | 의존 관계와 변경 시점 조정 |
| 마운트에서 값이 예상과 다름 | 마운트명·소유자·테이블명 | 운영 데이터와 백업 데이터 구분 |

같은 Resource busy라도 재시도 방법은 다릅니다.
자세한 두 연결 실습은 잠금과 busy timeout에서 확인하세요.
오류 문자열에 TRANSACTION이 있다는 이유만으로 반복 실행하지 마세요.

## 제약 오류와 데이터 보존

```sql
CREATE TRANSACTION TABLE ch8_error (
    id    LONG PRIMARY KEY,
    code  VARCHAR(32) NOT NULL,
    value INTEGER
);
CREATE UNIQUE INDEX ch8_error_code ON ch8_error(code);
INSERT INTO ch8_error VALUES (1, 'A', 10);
```

아래는 각각 의도적으로 실패하는 선택 실습입니다.
정상 SQL과 묶지 말고 확인할 문장만 실행하세요.

```sql
-- PRIMARY KEY 중복
INSERT INTO ch8_error VALUES (1, 'B', 20);
-- UNIQUE 중복
INSERT INTO ch8_error VALUES (2, 'A', 20);
-- 필수값 위반
INSERT INTO ch8_error VALUES (3, NULL, 30);
-- 지원하지 않는 스키마 변경
ALTER TABLE ch8_error MODIFY COLUMN (code VARCHAR(64));
```

```sql
SELECT id, code, value FROM ch8_error ORDER BY id;
DROP TABLE ch8_error;
```

마지막 조회에는 (1, A, 10)만 남습니다.
단일 문장 실패가 상태를 보존한다는 점과, BEGIN 안의 앞선 성공 문장까지
자동으로 취소되는 것은 아니라는 점을 구분해야 합니다.
트랜잭션에 해당 비교 예제가 있습니다.

## 진단 정보 수집

서버 버전·Edition, DDL과 인덱스, 실행 SQL, 오류 코드와 전체 메시지, 실제 영향 행 수를
함께 준비하면 좋습니다. 연결 장애라면 COMMIT 요청·응답 시각과 업무 키도 필요합니다.
비밀번호·개인정보·민감한 업무 값은 가린 뒤 재현에 필요한 최소 표본만 공유하세요.

복구를 위해 내부 저장 파일을 직접 수정하거나 운영 테이블을 재생성하지 마세요.
원인과 반영 상태를 먼저 확인하는 것이 데이터 손실을 줄이는 길입니다.
