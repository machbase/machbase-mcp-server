# Machbase Neo Bridge - PostgreSQL

## PostgreSQL 브리지 등록

PostgreSQL 데이터베이스에 연결하는 브리지를 등록합니다.

```
bridge add -t postgres pg host=127.0.0.1 port=5432 user=dbuser dbname=postgres sslmode=disable;
```

연결 옵션

| 옵션            | 설명                            | 예시         |
| :-----------      | :---------------------------------     | :-------------  |
| `dbname`          | 접속할 데이터베이스 이름 |                 |
| `user`            | 로그인할 사용자                 |                 |
| `password`        | 사용자 비밀번호                    |                 |
| `host`            | 접속할 호스트. /로 시작하는 값은 unix 도메인 소켓입니다. 기본값은 localhost | `host=127.0.0.1` |
| `port`            | 바인딩할 포트. 기본값 `5432` |     |
| `sslmode`         | SSL 사용 여부 (기본값 `require`)  | (아래 참고) |
| `connect_timeout` | 연결 최대 대기 시간(초). 0이거나 지정하지 않으면 무한 대기합니다. |  |
| `sslcert`         | 인증서 파일 위치. PEM 인코딩 데이터여야 합니다.   |  |
| `sslkey`          | 키 파일 위치. PEM 인코딩 데이터여야 합니다.    |  |
| `sslrootcert`     | 루트 인증서 파일 위치. PEM 인코딩 데이터여야 합니다. |  |

`sslmode`에 유효한 값은 다음과 같습니다:

| sslmode       |  설명                      |
|:------------  | :---------------------------------|
| `disable`     | No SSL                            |
| `require`     | 항상 SSL (검증 생략)    |
| `verify-ca`   | 항상 SSL (서버가 제시한 인증서가 신뢰된 CA의 서명인지 검증) |
| `verify-full` | 항상 SSL (서버 인증서가 신뢰된 CA의 서명이고 서버 호스트명이 인증서와 일치하는지 검증)|

## 테이블 생성

machbase-neo 셸을 열고 아래 명령을 실행해 `pg` 브리지로 `pg_example` 테이블을 만듭니다.

```sh
bridge exec pg CREATE TABLE IF NOT EXISTS pg_example(
    id         SERIAL PRIMARY KEY,
    company    VARCHAR(50) UNIQUE NOT NULL,
    employee   INT,
    discount   REAL,
    plan       FLOAT(8),
    code       UUID,
    valid      BOOL,
    memo       TEXT,
    created_on TIMESTAMP NOT NULL
);
```

`psql` 명령행 도구로 테이블이 생성되었는지 확인할 수 있습니다

```
postgres=# \d pg_example;
                                        Table "public.pg_example"
   Column   |            Type             | Collation | Nullable |                Default                 
------------+-----------------------------+-----------+----------+----------------------------------------
 id         | integer                     |           | not null | nextval('pg_example_id_seq'::regclass)
 company    | character varying(50)       |           | not null | 
 employee   | integer                     |           |          | 
 discount   | real                        |           |          | 
 plan       | real                        |           |          | 
 code       | uuid                        |           |          | 
 valid      | boolean                     |           |          | 
 memo       | text                        |           |          | 
 created_on | timestamp without time zone |           | not null | 
Indexes:
    "pg_example_pkey" PRIMARY KEY, btree (id)
    "pg_example_company_key" UNIQUE CONSTRAINT, btree (company)

```

## PostgreSQL에 *TQL*로 쓰기

```js
BYTES(payload() ?? `{
  "company": "acme",
  "employee": 10
}`)
SCRIPT("tengo", {
  // get current time
  times := import("times")
  ts := times.now()
  // get tql context
  ctx := import("context")
  val := ctx.value()
  // parse json
  json := import("json")
  msg := json.decode(val[0])
  ctx.yield(msg.company, msg.employee, ts)
})
INSERT(bridge("pg"), table("pg_example"), "company", "employee", "created_on")
```

```
postgres=# select * from pg_example;
 id | company | employee | discount | plan | code | valid | memo |         created_on         
----+---------+----------+----------+------+------+-------+------+----------------------------
  1 | acme    |       10 |          |      |      |       |      | 2023-08-09 11:05:30.039961
(1 row)
```

## PostgreSQL에서 *TQL*로 읽기

```js
SQL(bridge('pg'), "select * from pg_example")
CSV()
```
