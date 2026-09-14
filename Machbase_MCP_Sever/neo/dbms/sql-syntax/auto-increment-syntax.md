# AUTO_INCREMENT

`AUTO_INCREMENT`는 단일 64비트 정수 PRIMARY KEY 값을 서버가 자동으로 생성하도록 하는
컬럼 속성입니다.

<span class="badge-since">Machbase 8.7.0부터 LOOKUP과 VOLATILE에서도 지원</span>

## 지원 범위

| 항목 | 지원 범위 |
|---|---|
| Edition | Standard Edition |
| 테이블 | TRANSACTION, LOOKUP, VOLATILE |
| 컬럼 타입 | `LONG`, `INT64` |
| 키 | 컬럼 단위 단일 `PRIMARY KEY` |

테이블 단위·복합 PRIMARY KEY에는 사용할 수 없습니다. LOOKUP의 같은 컬럼에
`PROPERTY(SEQUENCE)`를 함께 지정하거나 `NEXTVAL()`을 사용하지 않습니다.

```sql
CREATE TRANSACTION TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32)
);

CREATE LOOKUP TABLE lookup_order (
    id   INT64 PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_order (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

명시적 transaction이 진행 중이면 TRANSACTION 테이블 DDL을 실행할 수 없습니다. 먼저
`COMMIT` 또는 `ROLLBACK`한 뒤 테이블을 생성합니다.

## 자동값 생성

자동 생성 컬럼을 생략하거나 `NULL`로 입력하면 서버가 값을 생성합니다.

```sql
INSERT INTO device_master(device_name, site_code)
VALUES ('compressor-01', 'SEOUL-A');

INSERT INTO device_master(id, device_name, site_code)
VALUES (NULL, 'pump-02', 'SEOUL-A');
```

`NULL`이 아닌 값을 직접 지정할 수도 있습니다. 지정한 값이 현재 다음 값 이상이면 다음 자동값은
그보다 큰 값부터 진행하고, 작은 값을 지정해도 순번은 되감기지 않습니다. `0`은 유효합니다.
`INT64_MAX` 뒤에는 더 생성할 값이 없어 자동 INSERT가 실패합니다.

중복 키와 실패한 INSERT 뒤의 번호 재사용 여부에 의존하지 마십시오. 이 값은 행 식별자이며
빠짐없는 업무 순번이 아닙니다.

## 테이블별 차이

| 동작 | TRANSACTION | LOOKUP | VOLATILE |
|---|:---:|:---:|:---:|
| 행과 다음 자동값의 재시작 후 유지 | O | O | X |
| 명시적 transaction | O | X | X |
| `INSERT ... SELECT` 자동값 생성 | O | X | X |
| 단일 INSERT 결과 ROWID | O | O | O |

VOLATILE 테이블은 서버 재시작 시 테이블과 값이 사라집니다. TRANSACTION의 데이터 이관에서만
자동 컬럼을 생략한 `INSERT ... SELECT`를 사용할 수 있습니다.

```sql
INSERT INTO device_master(device_name, site_code)
SELECT device_name, site_code
  FROM staging_device
 ORDER BY device_name;
```

## INSERT 결과 확인

지원 SDK는 성공한 단일 `INSERT ... VALUES`의 실행 결과에서 생성된 식별자를 제공할 수
있습니다. batch, Append, loader, `INSERT ... SELECT`와 UPSERT에서는 단일 값을 반환하지
않습니다. 자세한 조건은 ROWID를, 언어별 API는
SDK 기능 지원 범위를 참고하십시오.

## 관련 문서

- TRANSACTION 테이블 구조
- LOOKUP 테이블 구조
- VOLATILE 테이블 구조
- LOOKUP SEQUENCE
