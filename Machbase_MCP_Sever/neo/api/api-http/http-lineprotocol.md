# Machbase Neo HTTP ILP Line Protocol

Machbase Neo provides a compatibility api that accepts messages in a format of influxdata lineprotocol for writing data.
This api is convenient way to utilize existing client softwares that produce lineprotocol messages (e.g telegraf).

**Since Machbase has a different scheme from influxdb, some translations will be automatically occurred.**

**Translation**

| Machbase            | line protocol of influxdb                   |
| ------------------- | ------------------------------------------- |
| table               | db                                          |
| tag name            | measurement + `.` + field name              |
| time                | timestamp                                   |
| value               | value of the field (if it is not a number type, will be ignored and not inserted) |

**Line protocol example**

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

This example inserts data into table `example` with `name`='my-car.speed', `value`=87.6 and `time`=1782878977000 (milliseconds, from `precision=ms`)

**telegraf.conf example**

As set telegraf's output config to use http port of Machbase Neo,
the metrics that collected by telegraf are directly inserted into Machbase Neo.

```
[[outputs.http]]
url = "http://127.0.0.1:5654/metrics/write?db=example"
data_format = "influx"
content_encoding = "gzip"
```

