# Machbase Neo MQTT Python Client

## 준비

### paho 설치

```sh
pip install paho-mqtt
```

### 프로젝트 디렉터리 생성

```sh
mkdir python-mqtt && cd python-mqtt
```

## 발행자

### 클라이언트

```python
import paho.mqtt.client as mqtt

mqttClient = mqtt.Client("python_pub") # name of publisher
```

### 접속 콜백

```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("CONNACK OK")
    else:
        print("CONNACK KO code=", rc)
```

### 접속 (비 TLS)

MQTT 일반 소켓으로 machbase-neo에 접속합니다.

```python
mqttClient = mqtt.Client("python_pub", clean_session=True)
mqttClient.on_connect = on_connect
mqttClient.connect("127.0.0.1", port=5653, keepalive=10, clean_session=True)
mqttClient.loop_start()
```

### 접속 종료

```python
mqttClient.disconnect()
mqttClient.loop_stop()
```

### 발행 콜백

```python
def on_publish(client, userdata, mid):
    print("PUBACK mid=",mid)
```

### Publish

```python
mqttClient.on_publish = on_publish

mqttClient.publish("db/append/example", """[
    ["temperature",1677033057000000000, 21.1],
    ["humidity",   1677033057000000000, 0.53]
]""", qos=1)
```

## 전체 소스 코드

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("CONNACK OK")
    else:
        print("CONNACK KO code:", rc)

def on_publish(client, userdata, mid):
    print("PUBACK mid:",mid)

mqttClient = mqtt.Client("python_pub", clean_session=True)
mqttClient.on_connect = on_connect
mqttClient.on_publish = on_publish
mqttClient.connect("127.0.0.1", port=5653, keepalive=10)
mqttClient.loop_start()

mqttClient.publish("db/append/example", """[
    ["temperature",1677033057000000000, 21.1],
    ["humidity",   1677033057000000000, 0.53]
]""", qos=1)

time.sleep(1)

mqttClient.disconnect()
mqttClient.loop_stop()
```
