# Machbase Neo HTTP Create, Drop Table

HTTP "Query" API는 "SELECT" SQL뿐 아니라 DDL도 받습니다. 따라서 HTTP API로 테이블을 만들고 삭제할 수 있습니다

## 테이블 생성

태그 테이블이 무엇인지는 관련 문서를 참고하세요

**요청**

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```

**응답**

```json
{"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
```

### IF NOT EXISTS

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```

### TAG 통계

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)"
```

**참고** "summarized" 키워드는 해당 태그 테이블에 데이터가 기록될 때 내부 태그 자료구조에 통계를 자동 생성한다는 뜻입니다. 자세한 내용은 아래 링크의 태그 통계 항목을 참고하세요.

## Drop table

**요청**

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=drop table EXAMPLE
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=drop table EXAMPLE"
```

**응답**

```json
{"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
```
