# Machbase Neo Metrics

> **BETA 경고**  
> 이 문서에서 설명하는 기능은 변경될 수 있으며 향후 릴리스에서 갱신될 수 있습니다.

지표는 1분, 5분, 15분 샘플링 주기로 제공됩니다.

## HTTP API

RESTful API로 지표를 조회하려면 다음 엔드포인트를 사용합니다:

```
http://127.0.0.1:5654/debug/statz?interval=[1m|5m|15m]&format=[json|html]
```

이 엔드포인트에서는 지표를 수집할 구간을 1분, 5분, 15분 중에서 지정할 수 있습니다. 이 엔드포인트는 기본적으로 같은 머신(localhost)에서만 접근할 수 있다는 점에 유의하세요.

기본 출력 형식은 JSON입니다. `format=html`을 지정하면 응답이 HTML 표로 반환됩니다.

## CHART를 사용하는 TQL

아래 예제는 machbase-neo의 HTTP 지연 분포를 차트로 그리는 방법을 보여줍니다. `FAKE( statz(period, metrics...) )` SRC 함수를 사용한 뒤 `CHART()`의 입력으로 시간-값 쌍을 만듭니다.

```js
FAKE(statz("15m", 
    "machbase:http:latency_p50",
    "machbase:http:latency_p90",
    "machbase:http:latency_p99"
))
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
CHART(
    size("600px", "300px"),
    chartJSCode({
        function yformatter(val, idx){
            if (val > 1000000000)   { return `${val/1000000000} s`; }
            else if (val > 1000000) { return `${val/1000000} ms`; } 
            else if (val > 1000)    { return `${val/1000} µs`; }
            return `${val} ns`
        }
    }),
    chartOption({
        animation: false,
        yAxis: { type: "value", axisLabel:{ formatter: yformatter }},
        xAxis: { type: "time", axisLabel:{ rotate: -90 }},
        series: [
            {type: "line", data: column(3), areaStyle:{}, smooth:false, name: "p99"},
            {type: "line", data: column(2), areaStyle:{}, smooth:false, name: "p90"},
            {type: "line", data: column(1), areaStyle:{}, smooth:false, name: "p50"},
        ],
        tooltip: { trigger: "axis", valueFormatter: yformatter },
        legend: {}
    })
)
```

## Metrics

모든 지표는 선택한 샘플링 주기를 기준으로 하며, 주기는 1분(`1m`), 5분(`5m`), 15분(`15m`) 중 하나입니다.

### HTTP

| 지표                        |  설명                                                       |
|:----------------------------|:------------------------------------------------------------|
| `machbase:http:count`       |  전체 HTTP 요청 수                              |
| `machbase:http:latency_p50` |  HTTP 응답 지연 50번째 백분위(중앙값, ns) |
| `machbase:http:latency_p90` |  HTTP 응답 지연 90번째 백분위(ns)         |
| `machbase:http:latency_p99` |  HTTP 응답 지연 99번째 백분위(ns)         |
| `machbase:http:recv_bytes`  |  HTTP 요청 페이로드 총 크기                        |
| `machbase:http:send_bytes`  |  HTTP 응답 페이로드 총 크기                       |
| `machbase:http:status_1xx`  |  1xx 상태 코드 HTTP 응답 수             |
| `machbase:http:status_2xx`  |  2xx 상태 코드 HTTP 응답 수             |
| `machbase:http:status_3xx`  |  3xx 상태 코드 HTTP 응답 수             |
| `machbase:http:status_4xx`  |  4xx 상태 코드 HTTP 응답 수             |
| `machbase:http:status_5xx`  |  5xx 상태 코드 HTTP 응답 수             |

### MQTT

| 지표                          | 설명                                          |
|:------------------------------|:----------------------------------------------|
| `machbase:mqtt:recv_bytes`    | 수신한 총 바이트 수        |
| `machbase:mqtt:send_bytes`    | 전송한 총 바이트 수            |
| `machbase:mqtt:recv_pkts`     | 수신한 publish 메시지 총수 |
| `machbase:mqtt:send_pkts`     | 전송한 모든 종류의 메시지 총수     |
| `machbase:mqtt:recv_msgs`     | 수신한 publish 메시지 총수     |
| `machbase:mqtt:send_msgs`     | 전송한 publish 메시지 총수         |
| `machbase:mqtt:drop_msgs`     | 느린 구독자로 인해 버려진 publish 메시지 총수  |
| `machbase:mqtt:retained`      | 브로커에서 활성 상태인 retained 메시지 총수       |
| `machbase:mqtt:subscriptions` | 브로커에서 활성 상태인 구독 총수           |
| `machbase:mqtt:clients`       | 영속 세션을 가진 연결/비연결 클라이언트 총수  |
| `machbase:mqtt:clients_connected`      | 현재 연결된 클라이언트 수  |
| `machbase:mqtt:clients_disconnected`   | 브로커에 등록되어 있으나 현재 연결이 끊긴 영속 클라이언트(clean session 비활성) 총수  |
| `machbase:mqtt:inflight`               | 현재 in-flight 상태인 메시지 수          |
| `machbase:mqtt:inflight_dropped`       | 버려진 in-flight 메시지 수  |

### TQL

| 지표                                           | 설명                                            |
|:-----------------------------------------------|:------------------------------------------------|
| `machbase:tql:cache:count_[avg\|max\|min]`     | TQL 캐시의 항목 수                |
| `machbase:tql:cache:data_size_[avg\|max\|min]` | TQL 캐시 총 크기(바이트)             |
| `machbase:tql:cache:evictions`                 | TQL 캐시에서 제거된 항목 수      |
| `machbase:tql:cache:insertions`                | TQL 캐시에 새로 삽입된 항목 수 |
| `machbase:tql:cache:hits`                      | TQL 캐시 히트 수           |
| `machbase:tql:cache:misses`                    | TQL 캐시 미스 수         |

### 데이터베이스 세션

| 지표                                               | 설명                                |
|:---------------------------------------------------|:------------------------------------|
| `machbase:session:append:count`                    | 사용된 appender 총수      |
| `machbase:session:append:in_use`                   | 현재 열려 있는 appender 수  |
| `machbase:session:conn:count`                      | 사용된 커넥션 총수    |
| `machbase:session:conn:in_use`                     | 현재 열려 있는 커넥션 수|
| `machbase:session:stmt:count`                      | 사용된 statement 총수     |
| `machbase:session:stmt:in_use`                     | 현재 열려 있는 statement 수 |
| `machbase:session:conn:use_time_[avg\|max\|min]`   | 커넥션 사용 시간(ns)         |
| `machbase:session:conn:wait_time_[avg\|max\|min]`  | fetch 반복 제한 대기 시간(ns)                  |
| `machbase:session:query:count`                     | 전체 질의 수(fetch 반복을 사용하는 것만) |
| `machbase:session:query:exec_time_[avg\|max\|min]` | prepared statement 실행 시간(ns)                |
| `machbase:session:query:fetch_time_[avg\|max\|min]`| Fetch 시간(ns)                                           |
| `machbase:session:query:wait_time_[avg\|max\|min]` | 반복 제한 대기 시간(ns)                        |
| `machbase:session:query:hwm:elapse`                | High Water Mark 질의의 총 소요 시간(ns)           |
| `machbase:session:query:hwm:exec_time`             | High Water Mark 질의의 statement 준비 시간(ns) |
| `machbase:session:query:hwm:fetch_time`            | High Water Mark 질의의 fetch 시간(ns)                 |
| `machbase:session:query:hwm:wait_time`             | High Water Mark 질의의 반복 제한 대기 시간(ns) |
| `machbase:session:query:hwm:sql_args`              | High Water Mark 질의의 SQL 바인드 변수([]string)    |
| `machbase:session:query:hwm:sql_text`              | High Water Mark 질의의 SQL 텍스트(string)                |

### Go

| 지표                               | 설명                                 |
|:-----------------------------------|:-------------------------------------|
| `go:heap_in_use_[avg\|max\|min]`   | 힙 사용량(바이트)                   |
| `go:cgo_call_[avg\|max\|min]`      | CGO 함수 호출 수         |
| `go:goroutine_[avg\|max\|min]`     | 고루틴 수                 |
