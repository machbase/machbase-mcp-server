# Machbase Neo HTTP API Guide

machbase-neo는 HTTP API로 두 가지 주요 기능을 제공합니다.
하나는 모든 종류의 SQL 문을 실행할 수 있는 `query`이고, 다른 하나는 `INSERT INTO...` SQL 문에 해당하는 `write`입니다.

HTTP API의 주된 목적은 사용자의 서비스 애플리케이션과 데이터 분석 도구가 machbase 데이터베이스에 저장된 데이터에 접근할 수 있도록 기능을 노출하는 것이며,
센서와 사물 기기는 MQTT와 HTTP로 machbase에 데이터를 저장합니다.

## Endpoints

애플리케이션과 센서는 HTTP API로 데이터를 읽고 쓸 수 있습니다.

### 데이터베이스 조회

| 메서드  | 경로             | 설명                           |
| :-----: | :--------------- | :-------------------------------------|
| GET     | `/db/query`      | `q` 파라미터로 쿼리 실행          |
| POST    | `/db/query`      | JSON·폼 데이터로 쿼리 실행 |

### 데이터베이스 쓰기

| 메서드  | 경로             | 설명                           |
| :-----: | :--------------- | :-------------------------------------|
| POST    | `/db/write`      | JSON·CSV 형식으로 데이터 쓰기  |
| POST    | `/metrics/write` | ILP(influx line protocol)로 데이터 쓰기 |

### TQL 엔드포인트

| 메서드  | 경로                      | 설명                           |
| :-----: | :------------------------ | :-------------------------------------|
| GET     | `/db/tql/{tql_file_path}` | 경로로 지정한 tql 파일 실행    |
| POST    | `/db/tql/{tql_file_path}` | 요청 페이로드와 함께 tql 파일 실행 |
| POST    | `/db/tql`                 | 요청 페이로드로 전달된 tql 실행 |
| POST    | `/db/tql?$={tql_script}`  | 쿼리 파라미터 `$`로 전달된 tql을 요청 페이로드와 함께 실행 |

## HTTP API 테스트

Machbase-neo 웹 UI에는 마크다운과 TQL 안에서 바로 HTTP API를 테스트할 수 있는 REST API 클라이언트가 내장되어 있으며,
다음 예제와 같이 사용합니다.

- 워크시트의 마크다운.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select count(*) from example
    &format=ndjson
```
~~~

- TQL

```
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=select count(*) from example
        &format=ndjson
})
TEXT()
```
