# Machbase Neo HTTP Upload Files

클라이언트는 HTTP *multipart/form-data* 인코딩으로 임의의 파일을 Machbase-Neo에 업로드할 수 있습니다.
첨부된 파일은 지정한 디렉터리에 저장되고,
데이터베이스는 파일의 메타데이터를 컬럼에 JSON 문자열로 보관합니다.

*multipart/form-data* 인코딩으로 컬럼과 값을 전송하며,
각 파트의 이름은 컬럼 이름이어야 하고 값은 데이터의 문자열 표현이어야 합니다.
`X-Store-Dir` 헤더로 디렉터리를 지정해 `JSON` 타입 컬럼에 파일을 첨부합니다
파일이 저장될 위치입니다.
`X-Store-Dir`에 지정한 디렉터리가 없으면 서버가 자동으로 생성합니다.
파일 내용은 UUID 형식으로 생성된 고유 이름으로 디렉터리에 저장됩니다.

## Upload file

이 데모는 `EXAMPLE` 테이블이 이미 생성되어 있다고 가정합니다:

```sql
CREATE TAG TABLE EXAMPLE(
    NAME     VARCHAR(80)  primary key,
    TIME     DATETIME basetime,
    VALUE    DOUBLE,
    EXTDATA  JSON
)
```

**HTTP:**

이 예제는 Visual Studio Code의 REST Client 확장을 사용합니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="NAME"

camera-1
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="TIME"

now
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="VALUE"

0
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="EXTDATA"; filename="image_file.png"
X-Store-Dir: /tmp/store
Content-Type: image/png

< /data/image_file.png
------Boundary7MA4YWxkTrZu0gW--
```
~~~

**cURL:**

이 예제는 `curl`의 `-F` 옵션으로 *multipart/form-data* 인코딩 POST 요청을 보냅니다.

```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE' \
    -F 'NAME=camera-1' \
    -F 'TIME=now' \
    -F 'VALUE=0' \
    -F 'EXTDATA=@./data/image_file.png;headers="X-Store-Dir: /tmp/store"'
```

### X-Store-Dir

업로드된 파일 내용은 `X-Store-Dir` 헤더로 지정한 디렉터리에 저장되며,
파일 이름은 응답의 `ID`를 기반으로 정해집니다.
`X-Store-Dir` 헤더는 위 예제처럼 파트의 헤더에 포함할 수도 있고,
최상위 헤더로 지정할 수도 있습니다.

**`${data}`**

`X-Store-Dir` 경로에 `${data}` 변수를 사용해 데이터베이스 홈 디렉터리를 나타낼 수 있습니다. 이 디렉터리는 machbase-neo 프로세스를 실행할 때 `--data` 플래그로 지정하며, 사용하지 않으면 machbase-neo 실행 파일이 있는 디렉터리 아래의 `machbase_home` 하위 디렉터리가 기본값입니다. 명령행 플래그 문서를 참고하세요.

예를 들어 `X-Store-Dir: ${data}/store`로 설정하면 업로드된 파일은 `some/path/to/machbase_home/store/file_name_is_ID_of_the_response`에 저장됩니다.

### 응답 메시지
파일이 정상적으로 업로드되면 서버는 아래와 같이 저장된 파일 정보를 응답합니다.

- ID : 서버가 부여한 고유 id
- FN : 원본 파일 이름
- SZ : File size
- CT : Content-Type
- SD : 서버 측 저장 디렉터리 경로

```json
{
  "success": true,
  "reason": "success, 1 record(s) inserted",
  "elapse": "3.772042ms",
  "data": {
    "files": {
      "EXTDATA": {
        "ID": "1ef8a87f-96bd-6576-9ff5-972fa7638db8",
        "FN": "image_file.png",
        "SZ": 12692,
        "CT": "image/png",
        "SD": "/tmp/store"
      }
    }
  }
}
```

위 예제의 `EXTDATA` 컬럼은 일반적인 JSON 형식의 "문자열" 데이터로 접근할 수 있습니다 
업로드된 파일의 메타 정보가 담겨 있습니다.

```sql
SELECT EXTDATA FROM EXAMPLE
WHERE NAME = 'camera-1' 
```

또는 JSON 경로를 사용합니다:

```sql
SELECT EXTDATA FROM EXAMPLE
WHERE NAME = 'camera-1'
AND EXTDATA->'$.FN' = 'image_file.png';
```

`/db/query` API로 SELECT 쿼리를 사용하는 예제입니다:

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select EXTDATA from EXAMPLE where NAME = 'camera-1'
```
~~~

**cURL:**
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select EXTDATA from EXAMPLE\
    where NAME = 'camera-1'"
```

`->` 표기법으로 json 경로 조건을 사용합니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select EXTDATA from EXAMPLE where NAME = 'camera-1' and EXTDATA->'$.FN' = 'image_file.png'
```
~~~

**cURL:**
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select EXTDATA from EXAMPLE\
    where NAME = 'camera-1' \
    and EXTDATA->'$.FN' = 'image_file.png'"
```

`EXTDATA` 컬럼에는 아래와 같이 파일 정보가 담깁니다.

```json
{
  "data": {
    "columns": [ "EXTDATA" ],
    "types": [ "string" ],
    "rows": [
      [
        "{\"ID\":\"1ef8a87f-96bd-6576-9ff5-972fa7638db8\",\"FN\":\"image_file.png\",\"SZ\":12692,\"CT\":\"image/png\",\"SD\":\"/tmp/store\"}"
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "843.666µs"
}
```

JSON 타입 컬럼에서 특정 필드를 추출하려면 JSON 경로를 사용하세요:

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?format=ndjson
    &q=SELECT NAME, TIME, EXTDATA->'$.ID' as FID  FROM EXAMPLE WHERE NAME = 'camera-1'
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "format=ndjson"   \
  --data-urlencode "q=SELECT NAME, TIME, EXTDATA->'$.ID' as FID  \
    FROM EXAMPLE WHERE NAME = 'camera-1'"
```

```json
{"NAME":"camera-1","TIME":1728950208158594000,"FID":"1ef8a87f-96bd-6576-9ff5-972fa7638db8"}
{"NAME":"camera-1","TIME":1728953137384133000,"FID":"1ef8a8ec-b602-6cac-8fb1-ac9c0c1b981b"}
```

## 파일 내용 읽기

파일 내용은 조회 API로 접근할 수 있습니다:

`http://{server_address}/db/query/file/{table}/{column}/{ID}`

테이블이 TAG 테이블이면 `tag` 파라미터를 지정해 서버 응답 시간을 개선하세요:

`http://{server_address}/db/query/{tag_table}/{column}/{ID}?tag=camera-1`

테이블이 LOG 테이블이면 `ID`는 레코드가 입력된 시각을 기준으로 생성됩니다. TAG 테이블이면 `ID`는 레코드의 기준 시간 컬럼에서 파생됩니다.

`ID`에 타임스탬프 정보가 들어 있으므로 Machbase-Neo는 TAG 테이블에서는 `TIME between A and B`, LOG 테이블에서는 `_ARRIVAL_TIME between A and B` 절에 이를 사용해 검색 범위를 좁힙니다.
`ID`의 타임스탬프가 LOG 테이블의 기준 시간이나 `_ARRIVAL_TIME`과 정확히 같지는 *않지만*, 검색 성능 향상에는 여전히 유용합니다.

### HTTP GET

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```
~~~

**cURL:**
```sh
curl -o ./img-download.png \
    http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```

### HTML에서 &lt;img&gt; 사용

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8">
</body>
</html>
```

테이블이 TAG 테이블이고 태그 이름을 안다면 `tag` 쿼리 파라미터로 조회 성능을 높일 수 있습니다:

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8?tag=camera-1">
</body>
</html>
```

## 예제s

### Javascript

Javascript로 파일 업로드하기.

```js
const request = require('request');
const fs = require('fs');

let req = {
    method: 'POST',
    url: 'http://127.0.0.1:5654/db/write/EXAMPLE',
    headers: {"X-Store-Dir": "/tmp/store"},
    formData: {
        NAME: 'camera-1',
        TIME: 'now',
        VALUE: 0,
        EXTDATA:  fs.createReadStream('./image_file.png'), 
    },
};

request(req, function(err, res, body){
    if (err) { console.log(err);
    } else { console.log(body); }
})
```

### Python

Python으로 파일 업로드하기.

```python
import requests

# Define the URL to which the file will be uploaded
url = 'http://127.0.0.1:5654/db/write/EXAMPLE'

# Path to the image file
file_path = './image_file.png'

# Open the image file in binary mode
with open(file_path, 'rb') as file:
    headers = {'X-Store-Dir': '/tmp/store'}
    data = {'NAME': 'camera-1', 'TIME': 'now', 'VALUE': 0}
    files = {'EXTDATA': ('filename.png', file, 'image/png')}

    # Send the POST request
    response = requests.post(url, data=data, files=files, headers=headers)
    
    # Print the response from the server
    print(response.status_code)
    print(response.text)
```
