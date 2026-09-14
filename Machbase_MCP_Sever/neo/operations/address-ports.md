# Machbase Neo IP Address and ports

## 바인드 주소

machbase-neo는 보안을 위해 기본적으로 localhost에서만 수신합니다. 원격 호스트의 클라이언트가 네트워크로 데이터를 읽고 쓰려면 바인드 주소 옵션 `--host <bind address>`와 함께 machbase-neo를 시작해야 합니다.

모든 주소에서 수신하려면 `0.0.0.0`을 사용합니다

```sh
machbase-neo serve --host 0.0.0.0
```

특정 주소에서만 수신하려면 호스트의 IP 주소를 설정합니다.

```sh
machbase-neo serve --host 192.168.1.10
```

## 수신 포트

프로토콜 포트를 위한 플래그 옵션이 더 있습니다.

| 플래그             | 기본값          | 설명                            |
|:-----------------|:----------------:|-------------------------------- |
| `--shell-port`   | `5652`           | ssh 수신 포트                 |
| `--mqtt-port`    | `5653`           | mqtt 수신 포트                |
| `--http-port`    | `5654`           | http 수신 포트                |
| `--mach-port`    | `5656`           | JDBC/ODBC 드라이버용 machbase 네이티브 수신 포트 |

리스너가 다른 네트워크 인터페이스에서 수신해야 한다면 listen host와 port 플래그를 사용하세요.

| 플래그                   | 기본값                | 설명                            |
|:-----------------------|:-----------------------|-------------------------------- |
| `--mach-listen-host`   | value of `--host`      |                                 |
| `--mach-listen-port`   | value of `--mach-port` |                                 |
| `--shell-listen-host`  | value of `--host`      |                                 |
| `--shell-listen-port`  | value of `--shell-port`|                                 |
| `--http-listen-host`   | value of `--host`      |                                 |
| `--http-listen-port`   | value of `--http-port` |                                 |
| `--mqtt-listen-host`   | value of `--host`      |                                 |
| `--mqtt-listen-port`   | value of `--mqtt-port` |                                 |
