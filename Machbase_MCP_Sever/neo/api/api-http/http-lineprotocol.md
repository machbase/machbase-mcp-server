# Machbase Neo HTTP ILP Line Protocol

Machbase Neo는 데이터 쓰기용으로 influxdata 라인 프로토콜 형식의 메시지를 받는 호환 API를 제공합니다.
이 API는 라인 프로토콜 메시지를 생성하는 기존 클라이언트 소프트웨어(예: telegraf)를 활용하기에 편리한 방법입니다.

**Machbase는 influxdb와 스키마가 다르므로 일부 항목이 자동으로 변환됩니다.**

**변환 규칙**

| Machbase            | influxdb 라인 프로토콜                   |
| ------------------- | ------------------------------------------- |
| table               | db                                          |
| 태그 이름            | measurement + `.` + 필드 이름              |
| 시간                | 타임스탬프                                   |
| 값               | 필드의 값 (숫자 타입이 아니면 무시되어 입력되지 않습니다) |

**라인 프로토콜 예제**

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/metrics/write?db=example&precision=ms

my-car speed=87.6 1782878977000
```
~~~

**cURL:**
```sh
curl -o - -X POST "http://127.0.0.1:5654/metrics/write?db=example&precision=ms" \
    --data-binary 'my-car speed=87.6 1782878977000'
```

이 예제는 `example` 테이블에 `name`='my-car.speed', `value`=87.6, `time`=1782878977000(`precision=ms`이므로 밀리초)로 데이터를 입력합니다

**telegraf.conf 예제**

telegraf의 출력 설정을 Machbase Neo의 http 포트를 쓰도록 지정하면,
telegraf가 수집한 지표가 Machbase Neo에 바로 입력됩니다.

```
[[outputs.http]]
url = "http://127.0.0.1:5654/metrics/write?db=example"
data_format = "influx"
content_encoding = "gzip"
```

