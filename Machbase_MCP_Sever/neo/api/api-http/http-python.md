# Machbase Neo HTTP Python Client

## 조회

### GET CSV

```python
import requests
params = {"q":"select * from example", "format":"csv", "heading":"false"} 
response = requests.get("http://127.0.0.1:5654/db/query", params)
print(response.text)
```

## 쓰기

### POST CSV

```python
import requests
csvdata = """temperature,1677033057000000000,21.1
humidity,1677033057000000000,0.53
"""
response = requests.post(
    "http://127.0.0.1:5654/db/write/example?heading=false", 
    data=csvdata, 
    headers={'Content-Type': 'text/csv'})
print(response.json())
```

## 예제 - matplotlib

**테스트 데이터를 쓰려면 셸에서 파형 쓰기 항목의 아래 명령을 사용하세요.**

```sh
sh gen_wave.sh | machbase-neo shell import --timeformat=s EXAMPLE
```

**Python code**

```python
import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

url = "http://127.0.0.1:5654/db/query"
querystring = {"q":"select * from example order by time limit 200"} 
response = requests.request("GET", url, params=querystring)
data = json.loads(response.text)

sinTs, sinSeries, cosTs, cosSeries = [], [], [], []
for row in data["data"]["rows"]:
    ts = datetime.datetime.fromtimestamp(row[1]/1000000000)
    if row[0] == 'wave.cos':
        cosTs.append(ts)
        cosSeries.append(row[2])
    else:
        sinTs.append(ts)
        sinSeries.append(row[2])

plt.plot(sinTs, sinSeries, label="sin")
plt.plot(cosTs, cosSeries, label="cos")
plt.title("Tutorial Waves")
plt.legend()
plt.show()
```

## 예제 - pandas

### 테이블에서 데이터프레임 불러오기

- machbase-neo HTTP API로 pandas 데이터프레임을 불러옵니다.

```python
from urllib import parse
import pandas as pd

query_param = parse.urlencode({
    "q": "select * from example order by time limit 500",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://127.0.0.1:5654/db/query?{query_param}")
df
```

### 데이터프레임을 테이블에 쓰기

- machbase-neo HTTP API로 pandas 데이터프레임을 태그 테이블에 씁니다.

```python
import io, requests

stream = io.StringIO()
df.to_csv(stream, encoding='utf-8', header=False, index=False)
stream.seek(0)

file_upload_resp = requests.post(
    "http://127.0.0.1:5654/db/write/example?timeformat=s&method=append",
    headers={'Content-type':'text/csv'},
    data=stream )

print(file_upload_resp.json())
```

```python
{'success': True, 'reason': 'success, 500 record(s) appended', 'elapse': '2.288791ms'}
```

### CSV 불러오기

pandas와 urllib를 임포트합니다.

```py
from urllib import parse
import pandas as pd
```

`"format": "csv"` 옵션으로 쿼리 URL을 만든 뒤 `read_csv`를 호출합니다.
`timeformat`으로 시간 데이터의 정밀도를 지정합니다. `s`, `ms`, `us`, `ns`(기본값)를 사용할 수 있습니다.

```py
query_param = parse.urlencode({
    "q":"select * from example order by time limit 500",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://127.0.0.1:5654/db/query?{query_param}")
df
```

### 압축된 CSV 불러오기

HTTP API에서 gzip 압축된 CSV를 읽습니다.

```py
from urllib import parse
import pandas as pd
import requests
import io
```

```py
query_param = parse.urlencode({
    "q":"select * from example order by time desc limit 1000",
    "format": "csv",
    "timeformat": "s",
    "compress": "gzip",
})
response = requests.get(f"http://127.0.0.1:5654/db/query?{query_param}", timeout=30, stream=True)
df = pd.read_csv(io.BytesIO(response.content))
df
```
