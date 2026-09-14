# 다중 데이터베이스

Standard Edition에서는 한 서버 안에 여러 논리 데이터베이스를 만들고 객체와 접근 권한을
분리할 수 있습니다. 이 페이지는 도입과 운영 흐름만 설명합니다. SQL 문법, 권한, SDK 옵션과
백업 절차는 연결된 상세 문서를 참고합니다.

## 적용 범위

- 다중 데이터베이스는 Standard Edition 기능입니다.
- 논리 데이터베이스는 별도 서버 프로세스나 자원 할당량을 만들지 않습니다.
- 객체 이름은 `object`, `owner.object`, `database.owner.object`의 최대 세 부분입니다.
- 다른 데이터베이스를 지정할 때 소유자를 생략하지 않습니다.
- 마운트된 데이터베이스는 활성 데이터베이스와 다른 읽기 전용 백업 조회 경로입니다.

## 도입 전 결정 사항

1. 데이터베이스별 소유자와 애플리케이션 사용자를 정합니다.
2. `CONNECT`와 객체별 최소 권한을 정의합니다.
3. 연결 풀이 현재 데이터베이스를 어떻게 초기화·복원하는지 확인합니다.
4. 백업 단위, 복구 순서와 마운트된 데이터베이스 이름 규칙을 정합니다.
5. 데이터베이스별 사용량과 장애를 구분할 모니터링 기준을 마련합니다.

## 빠른 검증

다음 예제는 두 데이터베이스가 분리되는지 확인한 뒤 모두 정리합니다.

```sql
CREATE DATABASE IF NOT EXISTS manual_multidb_a;
CREATE DATABASE IF NOT EXISTS manual_multidb_b;

USE manual_multidb_a;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-a');

USE manual_multidb_b;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-b');

SELECT message FROM manual_multidb_a.SYS.sensor_event;
SELECT message FROM manual_multidb_b.SYS.sensor_event;

USE MACHBASEDB;
DROP DATABASE manual_multidb_a CASCADE FORCE;
DROP DATABASE manual_multidb_b CASCADE FORCE;
```

`USE database_name`은 현재 연결의 데이터베이스를 변경합니다. 트랜잭션, 열린 커서,
준비된 문장(*prepared statement*)과 Appender가 있는 상태에서 전환하지 마십시오. 다른 데이터베이스의 객체는
`database.owner.object`로 명시합니다.

## 권한 경계

사용자는 대상 데이터베이스의 `CONNECT` 권한과 실제 객체 작업에 필요한 권한을 모두 가져야
합니다. 데이터베이스 생성·삭제·권한 SQL은
계정과 권한을 참고합니다. 운영 계정에
관리자 권한을 일괄 부여하지 않습니다.

## 애플리케이션 연결

SDK마다 초기 데이터베이스를 지정하는 옵션 이름과 연결 풀 초기화 동작이 다릅니다. 각 SDK의
연결 문서에서 지원 여부를 확인하고, 연결을 빌린 직후 다음 값을 검증합니다.

```sql
SELECT CURRENT_DATABASE();
```

언어별 설정은 개발 및 애플리케이션 연동을,
서버·SDK 호환성은
서버와 SDK 호환성을
참고하십시오.

## 백업과 복구

백업 전에 포함할 활성 데이터베이스와 복구 순서를 기록합니다. 마운트된 데이터베이스는 `USE`할 수
있으나 읽기 전용(*read-only*)로 `SELECT`만 가능합니다. 정확한 명령과
검증 절차는 백업, 복원, 마운트를 사용하십시오.

## 운영 체크리스트

- 연결 직후와 연결 풀 재사용 직후 `CURRENT_DATABASE()`가 기대값인가
- SQL과 모니터링이 동일 이름의 다른 데이터베이스 객체를 혼동하지 않는가
- 사용자에게 대상 데이터베이스와 객체의 최소 권한만 부여했는가
- 백업·복구 훈련에서 모든 대상 데이터베이스를 확인했는가
- 데이터베이스 삭제 전에 열린 연결, 객체와 백업 보존 조건을 확인했는가

정확한 `CREATE/DROP/USE DATABASE` 문법은
DATABASE 문법을 참고하십시오.
