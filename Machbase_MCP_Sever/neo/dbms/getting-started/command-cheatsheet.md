# 기본 명령 치트시트

접속 명령은 운영체제의 터미널에서 실행하고, SQL은 접속한 `machsql`에서 실행합니다.
서버 주소, 포트와 계정은 실제 환경에 맞춥니다. 아래 접속 예제의 `MANAGER`는 빠른 시작에서
사용하는 초기 실습 비밀번호이며, 변경한 환경에서는 해당 계정의 비밀번호를 사용합니다.

## 터미널에서 실행할 명령

| 작업 | 명령 |
|---|---|
| 대화형 접속 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| SQL 파일 실행 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |

## machsql에서 실행할 SQL

| 작업 | 명령 |
|---|---|
| 테이블 목록 | `SHOW TABLES;` |
| 컬럼과 타입 확인 | `DESC table_name;` |
| TRANSACTION 테이블 생성 | `CREATE TRANSACTION TABLE table_name (...);` |
| LOG 테이블 생성 | `CREATE LOG TABLE table_name (...);` |
| 데이터 입력 | `INSERT INTO table_name VALUES (...);` |
| 조건에 맞는 데이터 조회 | `SELECT ... FROM table_name WHERE ...;` |
| 조회 결과 정렬 | `SELECT ... FROM table_name ORDER BY ...;` |
| 테이블과 데이터 삭제 | `DROP TABLE table_name;` |

`table_name`과 `...`은 실제 이름과 정의로 바꿔야 하는 자리 표시자입니다.
그대로 실행할 수 있는 SQL은 빠른 시작에 있습니다.
`DROP TABLE`은 테이블의 데이터도 삭제하므로 정리할 실습 테이블인지 먼저 확인합니다.

Machbase DBMS 8.7.0의 `CREATE TABLE`은 유형을 생략하면 TRANSACTION 테이블을 생성합니다.
TRANSACTION은 Standard Edition에서 지원합니다. 사용하려는 유형을 명시하면 예제의 의도가
분명해집니다. 전체 명령은 machsql 레퍼런스를
참고하십시오.
