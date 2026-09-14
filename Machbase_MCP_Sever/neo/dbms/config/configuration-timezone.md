# Timezone 설정 사전

Machbase는 클라이언트 접속 옵션으로 타임존을 지정할 수 있습니다. datetime 값은 내부적으로 나노초 값으로 처리되며, 타임존 옵션은 문자열 입출력 변환에 영향을 줍니다.

## 지원 타임존 표현 형식

| 형식 | 예시 | 설명 |
|------|------|------|
| UTC 오프셋 | `+0900`, `-0530` | UTC 기준 시/분 오프셋 |

8.5 원본 매뉴얼과 현재 `machsql`, `machloader` 도움말 기준으로 문서화된 형식은
`+-HHMM` 오프셋입니다. `Asia/Seoul` 같은 IANA 지역명 또는
`DEFAULT_TIMEZONE` 서버 프로퍼티는 현재 배포 샘플에서 확인되지 않으므로 이 장의
지원 형식으로 다루지 않습니다.

## 클라이언트별 타임존 설정

### machsql

`-z` 옵션으로 세션 타임존을 지정합니다.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
```

### machloader

`-z` 옵션으로 가져오기/내보내기 시 datetime 변환 타임존을 지정합니다.

```bash
machloader -i -d data.csv -t table_name -z +0900
machloader -o -d data.csv -t table_name -z +0900
```

### JDBC

JDBC에서 타임존을 지정해야 하는 경우 드라이버 문서의 연결 옵션을 확인합니다.
이 페이지에서는 `machsql`/`machloader`의 `+-HHMM` 오프셋 형식을 기준으로 설명합니다.

## 타임존 우선순위

클라이언트에서 `-z +0900`처럼 타임존을 명시하면 해당 세션의 입출력 변환에 적용됩니다.

## 타임존 변환 예시

`+0900` 타임존을 사용하는 경우 다음과 같이 접속합니다.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
```
