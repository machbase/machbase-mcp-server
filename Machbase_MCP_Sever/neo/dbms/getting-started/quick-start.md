# 10분 빠른 시작

실행 중인 서버에 접속해 서비스 시작 이벤트 한 건을 저장하고 다시 읽어 봅니다.
추가 중심 이벤트에 맞는 LOG 테이블을 사용하며, SQL 실행 결과와 두 시간 컬럼의 의미를
확인합니다. 설치에 필요한 시간은 이 실습의 예상 시간에 포함하지 않습니다.

## 실행 전제

- Machbase DBMS 서버가 `127.0.0.1:5656`에서 실행 중입니다.
- `machsql` 명령을 사용할 수 있습니다.
- 테이블 생성·입력·조회·삭제 권한이 있는 실습 계정으로 접속할 수 있습니다.
- 아래 명령은 초기 실습 계정 `SYS`와 비밀번호 `MANAGER`를 사용합니다. 비밀번호를
  변경했다면 실제 값으로 바꿉니다.
- `/tmp`에 SQL 파일을 저장할 수 있고, 실습용 이름 `DBMS_GS_QUICK`을 사용할 수 있습니다.

기존 업무 테이블과 이름이 겹치지 않는 실습 환경을 사용합니다. 예제 마지막의
`DROP TABLE`은 실습 테이블과 입력한 데이터를 삭제합니다.

서버가 아직 준비되지 않았다면 설치, 배포, 업그레이드와
Linux Standard Edition 설치를 먼저
참고하십시오.

## 대표 실행 예제

서비스 시작 이벤트 한 건을 LOG 테이블에 기록합니다. LOG 테이블은 `CREATE LOG TABLE`로
명시해서 생성하며, `_arrival_time` 컬럼이 자동으로 추가됩니다.

다음 명령으로 SQL 파일을 저장하고 실행합니다.

```bash
cat > /tmp/dbms_gs_quick.sql <<'SQL'
CREATE LOG TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK (EVENT_ID, EVENT_TIME, LEVEL, MESSAGE)
VALUES (
  1,
  TO_DATE('2026-07-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
  'INFO',
  'service started'
);

SELECT _arrival_time, EVENT_ID, EVENT_TIME, LEVEL, MESSAGE
FROM DBMS_GS_QUICK
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_QUICK;
SQL

machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

### 결과 확인

각 SQL 단계에 오류가 없는지 확인합니다. SELECT 결과 한 행에 `EVENT_ID`가 `1`,
`LEVEL`이 `INFO`, `MESSAGE`가 `service started`로 표시되어야 합니다.
`EVENT_TIME`은 애플리케이션이 저장한 실제 이벤트 시각이고, `_arrival_time`은 DBMS가
이 예제에서 자동 기록한 서버 입력 시각입니다. 따라서 예제를 실행할 때마다
`_arrival_time` 값은 달라지며 `EVENT_TIME`과 같을 필요가 없습니다.

`CREATE LOG TABLE`은 구조를 만들고 `INSERT`는 한 행을 추가합니다. `SELECT`는 읽을
컬럼을 지정하며, `ORDER BY EVENT_ID`는 결과 순서를 지정합니다. 마지막 `DROP TABLE`까지
성공하면 실습 테이블이 제거됩니다. 데이터를 더 살펴보려면 실행 전에 마지막 DROP 문을
제외하고, 조회를 마친 뒤 해당 실습 테이블만 정리합니다.

재실행 중 `DBMS_GS_QUICK`이 이미 존재한다는 오류가 나면 이전 실행이 `DROP TABLE`
단계에 도달하지 못했을 수 있습니다. `DESC DBMS_GS_QUICK;`으로 구조를 확인하고, 이전
실습에서 만든 테이블인 경우에만 `DROP TABLE DBMS_GS_QUICK;`을 실행한 뒤 재시도합니다.
접속 오류라면 먼저 서버 주소·포트·기동 상태와 계정 정보를 확인합니다.

## 이 예제에서 확인한 것

| 항목 | 확인 내용 |
| --- | --- |
| 서버 접속 | `machsql`로 `127.0.0.1:5656`에 접속 |
| 테이블 생성 | `CREATE LOG TABLE`로 LOG 테이블을 명시적으로 생성 |
| 데이터 입력 | `INSERT`와 `TO_DATE`로 이벤트 데이터 저장 |
| 데이터 조회 | `SELECT`와 `ORDER BY`로 입력 결과 확인 |
| 자동 컬럼 | LOG 테이블의 `_arrival_time`은 서버가 자동 기록 |
| 정리 | `DROP TABLE`로 실습 테이블 삭제 |
