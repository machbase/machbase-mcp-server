# 네트워크 타입 조회

IP 주소를 문자열로 보관하면 눈으로 읽기는 편하지만, 문자열 정렬과 주소 범위의 순서가
같다고 가정하기 쉽습니다. 주소 비교가 목적이라면 IPV4·IPV6 타입을 사용하고,
원문 표기까지 필요할 때만 별도 문자열을 함께 보관하세요.

## 네트워크 데이터 준비

```sql
CREATE LOG TABLE ch7_network (
    event_id INTEGER,
    src_ip   IPV4,
    dst_ip   IPV6,
    dst_port INTEGER
);
INSERT INTO ch7_network VALUES (1, '192.0.2.1',   '2001:db8::1', 80);
INSERT INTO ch7_network VALUES (2, '192.0.2.255', '2001:db8::2', 65535);
INSERT INTO ch7_network VALUES (3, '198.51.100.1', '2001:db8::3', 443);
INSERT INTO ch7_network VALUES (4, NULL, NULL, NULL);

SELECT event_id, src_ip, dst_ip, dst_port FROM ch7_network ORDER BY event_id;
```

네 행이 조회됩니다. 포트는 INTEGER를 사용합니다.
USHORT의 최댓값 65535는 NULL 예약값이므로 포트 전체 범위를 그대로 표현하기에 맞지 않습니다.

## 동등 비교와 범위 조회

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip BETWEEN '192.0.2.1' AND '192.0.2.255'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IN ('192.0.2.1', '198.51.100.1')
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip = '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip BETWEEN '2001:db8::1' AND '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IS NULL
 ORDER BY event_id;
```

| 조건 | 선택되는 event_id |
|---|---|
| IPv4 BETWEEN | 1, 2 |
| IPv4 IN | 1, 3 |
| IPv6 동등 비교 | 2 |
| IPv6 BETWEEN | 1, 2 |
| IPv4 IS NULL | 4 |

BETWEEN은 양 끝 주소를 포함합니다. 이 예제의 IPv4 범위는 CIDR 대역의 의미를
자동 적용한 것이 아니라, 직접 지정한 두 주소 사이의 범위입니다.
대역 자체로 판정하려면 아래 `CONTAINED`를 사용하세요.
NULL은 `= NULL`이 아니라 `IS NULL`로 검사하세요.

## CIDR 대역 판정

주소가 특정 네트워크에 속하는지 검사할 때는 `CONTAINED`를 사용합니다. 대역은 반드시
`주소/prefix` 형태로 지정하며 IPv4와 IPv6 모두 사용할 수 있습니다.

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip CONTAINED '192.0.2.0/24'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip CONTAINED '2001:db8::/32'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip NOT CONTAINED '192.0.2.0/24'
 ORDER BY event_id;
```

| 조건 | 선택되는 event_id |
|---|---|
| IPv4 `CONTAINED '192.0.2.0/24'` | 1, 2 |
| IPv6 `CONTAINED '2001:db8::/32'` | 1, 2, 3 |
| IPv4 `NOT CONTAINED '192.0.2.0/24'` | 3 |

방향을 뒤집은 `'192.0.2.0/24' CONTAINS src_ip`도 같은 의미입니다. 좌변에 네트워크,
우변에 주소가 오는 형태가 `CONTAINS`이고 그 반대가 `CONTAINED`입니다.

prefix 표기를 빼고 `CONTAINED '192.0.2.0'`처럼 쓰면 네트워크로 해석하지 못해 오류입니다.
NULL 주소인 4번은 어느 조건에도 선택되지 않으므로, 미수집 주소를 함께 세야 하면
`IS NULL` 조건을 따로 두십시오.

## 주소 형식과 원문 보존

IPv4만 들어오면 IPV4로, IPv6가 들어오면 IPV6로 스키마를 정합니다.
두 종류를 함께 다루는 경우에는 입력 변환·컬럼 분리 정책을 먼저 정하고 실제 표본으로
검증하세요. 암시적 변환이 원본 주소를 항상 의도대로 정규화해 줄 것이라고 가정하지 마세요.

실수하기 쉬운 부분은 출력 문자열입니다. 같은 IPv6 주소라도 원문 압축 표기와 조회 결과의
표기가 다를 수 있습니다. 원문을 증빙으로 남겨야 한다면 주소 타입 컬럼과 원문 컬럼을
분리하는 편이 명확합니다.

대량 데이터에서는 주소 조건과 함께 `_arrival_time` 범위를 제한하고 실행 계획을
확인하세요. 메시지의 정규식 검색은
텍스트 검색과
SQL 함수 사전에서 이어서 살펴볼 수 있습니다.

```sql
DROP TABLE ch7_network;
```

주소 조회가 예상과 다르면 원본 문자열, 입력 타입, 범위의 양 끝부터 나란히 비교해 보세요.
문자열 표현의 차이인지 실제 주소 범위의 차이인지 구분하기 쉬워집니다.
