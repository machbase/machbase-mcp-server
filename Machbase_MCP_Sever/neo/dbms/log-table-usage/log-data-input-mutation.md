# 데이터 입력

한두 행이 잘 들어간다고 수집 준비가 끝난 것은 아닙니다.
지속 수집에서는 전송 버퍼, 일부 행의 실패, 연결이 끊긴 뒤의 재전송까지 생각해야 합니다.
먼저 SQL로 컬럼과 시간을 확인한 뒤 실제 처리량에 맞는 입력 경로를 선택하세요.

## SQL INSERT

```sql
CREATE LOG TABLE ch7_input (
    event_time DATETIME,
    event_id   VARCHAR(32),
    device     VARCHAR(32),
    message    VARCHAR(128)
);

INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT _arrival_time, event_time, event_id, device, message
  FROM ch7_input;
```

한 행이 조회되며 `event_time`은 고정된 발생 시각입니다.
`_arrival_time`을 생략했으므로 입력 경로에서 서버 시각을 사용합니다.
기본 설정에서는 시각 역전 시 보정이 일어날 수 있으므로 항상 실제 수신 시각과 정확히
같다고 가정하지 마세요. 자세한 규칙은 시간 모델에서 확인합니다.

같은 이벤트를 다시 넣으면 어떻게 되는지도 확인해 보겠습니다.

```sql
INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT event_id, COUNT(*) AS received_rows
  FROM ch7_input
 GROUP BY event_id;

DROP TABLE ch7_input;
```

`evt-001`의 건수는 2입니다. 이름이 같아도 LOG가 중복을 제거하지 않습니다.
수집 애플리케이션의 “전송 완료”와 원본 이벤트의 “한 번만 저장”은 별도 문제입니다.

## 입력 경로 선택

| 상황 | 시작할 경로 | 함께 확인할 항목 |
|---|---|---|
| 소량 입력·기능 확인 | SQL INSERT | 컬럼 목록, 타입, 날짜 형식 |
| 애플리케이션의 지속 대량 입력 | SDK Append | 버퍼 전송, 행별 실패, 재접속 정책 |
| 클라이언트에서 읽는 CSV | csvimport·machloader | 컬럼 매핑, 실패 행 파일 |
| 서버에서 읽을 수 있는 적재 파일 | LOAD DATA INFILE | 서버 경로와 파일 접근 권한 |

SQL INSERT는 문장마다 처리 비용이 발생합니다. 지속적인 대량 입력에는 여러 행을 묶어
보내는 Append API를 검토하세요. 언어별 실행 코드는
개발 및 애플리케이션 연동에서 선택하면 됩니다.

## Append 전송과 오류 처리

Appender에 행을 전달한 시점에는 데이터가 클라이언트 버퍼에 남아 있을 수 있습니다.
사용하는 SDK의 flush·close 동작을 확인하고, 정상 종료뿐 아니라 예외 경로에서도
남은 버퍼와 연결을 처리해야 합니다.

호출이 성공했다고 모든 행이 저장되었다고 단정하지 마세요.
SDK에 따라 반환값, 오류 콜백, 종료 시 성공·실패 건수처럼 결과를 확인하는 경로가 다릅니다.
입력 길이 초과, NULL, 날짜 변환 오류를 일부러 포함한 작은 배치로 먼저 확인하는 편이 좋습니다.

실수하기 쉬운 상황은 응답을 받기 전에 연결이 끊기는 경우입니다.
이미 저장된 배치를 다시 보낼 수 있으므로 원본 이벤트 ID와 처리 위치를 기록하세요.
LOG의 INSERT·Append는 TRANSACTION 테이블 트랜잭션의 ROLLBACK 대상도 아닙니다.

## 파일 적재와 매핑

한글·빈 문자열·NULL·긴 메시지·서로 다른 시간대를 포함한 표본을 준비하세요.
원본 필드 수와 대상 컬럼 순서가 일치하는지 확인한 다음 전체 파일을 처리합니다.
실패 행 파일과 로그도 보관해야 같은 오류를 다시 분석할 수 있습니다.

전체 명령은 데이터 입력·적재·반출을
참고하세요.
과거 데이터 이관에서 `_arrival_time`을 보존하려면 정렬 순서와 기존 대상 데이터까지
확인해야 합니다. 일반 수집의 과거 발생 시각은 별도 `event_time`에 저장하는 편이 안전합니다.

막히면 전체 배치보다 실패한 원본 한 행부터 확인해 보세요.
필드 값, 대상 타입, 사용한 입력 API를 함께 보면 원인을 찾기 수월합니다.
