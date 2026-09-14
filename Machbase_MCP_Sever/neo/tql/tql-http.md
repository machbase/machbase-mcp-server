# Machbase Neo TQL HTTP

`HTTP()` SRC를 사용하면 TQL 스크립트 안에서 직접 HTTP 요청을 보내고 응답을 확인할 수 있습니다. 외부 API를 연동하거나 데이터 워크플로의 일부로 HTTP 엔드포인트를 테스트할 때 유용합니다.

**문법**: `HTTP(text)`

*버전 8.0.53 이상*

**파라미터:**
- `text` - 문자열, HTTP 요청 내용

## TQL 사용법

문법은 RFC 2616을 따르며 요청 메서드, 헤더, 본문을 지정할 수 있습니다.

### 예제 1: TEXT 출력

```js
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=select * from example limit 3
        &format=csv
        &timeformat=default
        &tz=UTC
})
TEXT()
```

### 예제 2: HTML 단순 출력

```html
HTTP({
    POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

    {
        "q": "select * from example limit 3",
        "format": "csv",
        "timeformat": "default"
    }
})
HTML(`<pre>{{ .Value 0 }}</pre>`)
```

요청을 작성한 뒤 TQL을 실행하면, 결과 화면에 헤더와 본문을 포함한 HTTP 응답이 표시됩니다.

**응답:**

```
HTTP/1.1 200 OK
Content-Length: 212
Content-Type: text/csv; charset=utf-8
Date: Mon, 02 Jun 2025 03:42:33 GMT

NAME,TIME,VALUE
work-11-0,2025-03-19 01:56:19.824,0.00
work-11-0,2025-03-19 01:56:19.824,1.00
work-11-0,2025-03-19 01:56:19.824,2.00
```

### 워크시트 사용법

마크다운 셀 안에서 `http` 코드펜스를 사용합니다.

**예제:**

~~~text
### HTTP Client Example

```http
POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

{
    "q": "select * from example limit 3",
    "format": "box",
    "timeformat": "default"
}
```
~~~

### 마크다운 사용법

`http` 코드펜스는 마크다운 파일(`.md`)에서도 동작합니다.

~~~
## HTTP Example

Code fence with `http`.

```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from example limit 2
    &format=ndjson
    &timeformat=default&tz=local
```
~~~

## 쿼리 문자열

요청 라인에 쿼리 문자열을 직접 포함할 수 있습니다:

~~~
```http
GET https://example.com/comments?page=2&pageSize=10
```
~~~

쿼리 파라미터가 많으면 여러 줄로 나눠 가독성을 높일 수 있습니다. 요청 라인 바로 다음에 오는 줄이 `?` 또는 `&`로 시작하면 쿼리 파라미터로 해석됩니다:

~~~
```http
GET https://example.com/comments
    ?page=2
    &pageSize=10
```
~~~

## 요청 헤더

요청 라인(그리고 쿼리 문자열 줄) 다음부터 첫 빈 줄까지의 내용은 요청 헤더로 해석됩니다. 헤더는 표준 `field-name: field-value` 형식으로 한 줄에 하나씩 작성합니다.

**예제:**

```
User-Agent: http-client
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4
Content-Type: application/json
```

## 요청 본문

요청 본문을 지정하려면 헤더 다음에 빈 줄을 하나 넣습니다. 이 빈 줄 이후의 모든 내용이 요청 본문으로 처리됩니다.

**예제:**

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```
~~~

### 외부 파일

줄 시작에 `<`를 쓰고 파일 탐색기에 표시되는 경로를 이어 적으면 파일을 요청 본문으로 지정할 수 있습니다. 또는 경로 앞에 `@` 접두를 붙이면 운영체제의 절대 경로로 해석됩니다.

**파일 경로 예:**
- `< /doc.xml` — TQL 루트 디렉터리에 있는 파일을 가리킵니다.
- `< @/home/data/doc.xml` — 운영체제의 절대 경로에 있는 파일을 가리킵니다.

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

< /data/demo.xml
```
~~~

## Multipart Form Data

요청 본문이 `multipart/form-data`인 경우, 텍스트와 파일 업로드를 함께 사용할 수 있습니다:

~~~
```http
POST https://api.example.com/user/upload
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text"

title
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="1.png"
Content-Type: image/png

< /data/1.png
------Boundary7MA4YWxkTrZu0gW--
```
~~~

## x-www-form-urlencoded

`application/x-www-form-urlencoded` 본문은 여러 줄로 나눌 수 있습니다. 각 키-값 쌍을 한 줄에 하나씩 쓰되, 첫 줄 이후로는 `&`로 시작합니다:

~~~
```http
POST https://api.example.com/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=foo
&password=bar
```
~~~

---

이 유연한 HTTP 요청 문법을 통해 TQL 스크립트에서 직접 API 호출을 테스트하고 자동화할 수 있으며, 다양한 HTTP 기능과 형식을 지원합니다.
