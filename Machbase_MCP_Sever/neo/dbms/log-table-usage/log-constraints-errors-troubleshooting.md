# 제약, 오류, 문제 해결

오류가 났을 때 같은 SQL을 반복 실행하면 원인은 그대로이고 상태만 더 복잡해질 수 있습니다.
먼저 지원하지 않는 작업인지, 입력값이나 객체 상태의 문제인지 구분해 보세요.
이 절에서는 확인할 대상을 증상별로 좁혀 봅니다.

## 기능 지원 범위

| 요청 | LOG 지원 여부 | 대안 |
|---|---|---|
| 일반 UPDATE | 미지원 | 정정 이벤트 설계 또는 변경 가능한 테이블 선택 |
| 임의 조건 DELETE WHERE | 미지원 | BEFORE·OLDEST·EXCEPT 또는 모델 변경 |
| PRIMARY KEY·UNIQUE 제약 | 미지원 | 수집 단계의 중복 처리 또는 다른 테이블 선택 |
| 값·범위 인덱스 | LSM 지원 | 타입과 조건에 맞춰 선택 |
| 단어 검색 | KEYWORD 지원 | VARCHAR·TEXT에 생성 후 SEARCH·ESEARCH 사용 |
| BITMAP 분석 인덱스 | 지원 조건 내 사용 | 타입·인코딩·값 분포 확인 |
| TEXT 자체의 ORDER BY·GROUP BY | 미지원 | 별도 코드·등급·시각 컬럼 사용 |

## 증상별 진단

| 증상 | 먼저 확인할 것 | 조치 |
|---|---|---|
| 명시한 도착 시각과 저장 시각이 다름 | 직전 시각과 TIME_INVERSION_MODE | 보정 여부 확인, 발생 시각은 별도 보존 |
| SEARCH에서 인덱스 관련 오류 | 해당 컬럼의 KEYWORD 인덱스 | 타입·테이블·인덱스 이름 확인 |
| 단어가 있는데 검색되지 않음 | SEARCH 토큰과 LIKE 부분 문자열의 차이 | 원문 한 행으로 두 결과 비교 |
| 인덱스를 만들었는데 조회가 느림 | 실행 계획·빌드 상태·시간 범위 | 반영 상태 확인 후 대표 부하 측정 |
| 컬럼 길이 변경 실패 | 기존 타입·새 길이 | VARCHAR 확장만 사용, 최대 길이 확인 |
| MINMAX 변경 실패 | 가변 길이 타입 여부 | LOG의 지원 고정 길이 컬럼만 대상 |
| NOT NULL 변경 실패 | 기존 NULL 행 | 기존 데이터 검사와 NOCHECK 의미 구분 |
| 같은 이벤트가 여러 번 보임 | 원본 ID·재시도·파일 재처리 | 재전송 정책 점검, 임의 행 삭제로 해결하지 않음 |
| DDL 실행 중 리소스 사용 오류 | 입력·조회 작업과 DDL 충돌 | 작업 시점 조정 후 재확인 |

서버 설정과 인덱스 목록은 다음처럼 확인할 수 있습니다.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME IN ('DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE', 'TABLE_SCAN_DIRECTION');
SHOW INDEXES;
```

설정값을 확인하는 것과 설정을 바꾸는 것은 별도 작업입니다.
원인 확인 없이 운영 서버의 전역 설정부터 바꾸지 마세요.

## 오류 재현과 해결

```sql
CREATE LOG TABLE ch7_error (event_id INTEGER, message TEXT);
INSERT INTO ch7_error VALUES (1, 'connection timeout');
SELECT event_id, message FROM ch7_error;
```

한 행이 조회됩니다. 아래는 각각 의도적으로 실패하는 SQL입니다.
정상 실습에 묶어 실행하지 말고 확인하려는 문장만 따로 실행하세요.

```sql
-- KEYWORD 인덱스가 없는 상태입니다.
SELECT event_id FROM ch7_error WHERE message SEARCH 'timeout';

-- TEXT 자체의 정렬·그룹화는 지원하지 않습니다.
SELECT message FROM ch7_error ORDER BY message;
SELECT message, COUNT(*) FROM ch7_error GROUP BY message;

-- LOG는 일반 UPDATE·조건 DELETE를 지원하지 않습니다.
UPDATE ch7_error SET message = 'fixed' WHERE event_id = 1;
DELETE FROM ch7_error WHERE event_id = 1;

-- TEXT를 VARCHAR로 변환하는 명령이 아닙니다.
ALTER TABLE ch7_error MODIFY COLUMN (message VARCHAR(4096));
```

이제 인덱스를 만들고 지원되는 검색 경로로 확인합니다.

```sql
CREATE INDEX ch7_error_msg ON ch7_error(message) INDEX_TYPE KEYWORD;
EXEC TABLE_FLUSH(ch7_error);
EXEC INDEX_FLUSH(ch7_error);

SELECT event_id, message FROM ch7_error
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;

DROP TABLE ch7_error;
```

1번 행이 조회되어야 합니다. 인덱스를 추가했다고 TEXT 정렬이나 LOG UPDATE까지
가능해지는 것은 아닙니다.

## 보존 정책 진단

기간이 지난 행이 남아 있다면 적용 정책, 실행 주기, LAST_DELETED_TIME과 실제
`_arrival_time`을 함께 확인하세요. `event_time`만 보고 삭제 실패로 판단하지 마세요.
관련 실습은 운영과 데이터 생명주기에 있습니다.

문제가 계속되면 서버 버전·Edition, 테이블 DDL, 실패 SQL, 오류 전체와 대표 입력값을
준비해 주세요. 비밀번호와 민감한 로그는 가린 뒤 공유하면 됩니다.
큰 데이터 전체를 보내기보다 같은 증상을 보이는 작은 예제가 원인 파악에 더 도움이 됩니다.
