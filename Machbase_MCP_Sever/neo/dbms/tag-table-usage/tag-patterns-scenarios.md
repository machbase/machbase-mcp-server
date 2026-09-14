# 활용 패턴과 시나리오

각 예제는 별도 실습입니다. 테이블을 생성하기 전에 같은 이름의 객체가 없는지 확인합니다.
태그 이름, 관측 한 건의 의미, 값의 단위와 결측 정책을 먼저 정하고 DDL을 적용합니다.

## 활용 사례

### IoT 센서 데이터

공장, 빌딩, 인프라에 설치된 다양한 센서 데이터를 단일 TAG 테이블에서 관리합니다.

```sql
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(128) PRIMARY KEY,
    time        DATETIME     BASETIME,
    temperature DOUBLE,
    vibration   DOUBLE,
    current     DOUBLE
);

-- One row groups measurements from the same equipment observation.
INSERT INTO factory_sensor VALUES (
    'F01/LINE-A/MOTOR-01',
    NOW,
    75.3, 0.15, 2.4
);
```

이 모델은 한 장비의 같은 시각 관측을 여러 컬럼에 저장합니다. 항목별 태그
`.../TEMP`, `.../VIBRATION`을 사용하려면 `name, time, value` 형태의 단일 값 모델을
검토합니다. 항목별 측정 시각이 다르면 NULL과 품질 상태로 그 차이를 표현하십시오.

### 에너지 모니터링

전력, 가스, 수도 계량기 데이터를 시간별로 수집합니다.

```sql
CREATE TAG TABLE energy_meter (
    meter_id  VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
);
```

`kwh`가 누적 계량값이면 AVG(kwh)는 지시값의 평균이지 구간 사용량이 아닙니다.
소비량은 구간 경계값의 차이에 초기화·교체·누락 처리 규칙을 적용해 계산합니다.
전력 kW와 전력량 kWh를 구분하고 메타데이터나 수집 계약에 단위를 명시합니다.

### 차량·이동체 추적

GPS 좌표와 속도를 시계열로 기록합니다.

```sql
CREATE TAG TABLE vehicle_track (
    vehicle_id VARCHAR(32) PRIMARY KEY,
    time       DATETIME    BASETIME,
    lat        DOUBLE,
    lon        DOUBLE,
    speed      DOUBLE,
    heading    DOUBLE
);
```

좌표계, 위도·경도와 속도의 단위를 수집 계약에 명시합니다. 위치 결측을 숫자 0으로
대체하면 실제 좌표와 구분할 수 없습니다. 이 테이블을 만들었다고 공간 인덱스나 경로 매칭이
자동 제공되는 것은 아니며, 차량·시간 구간으로 먼저 조회하고 필요한 분석을 수행합니다.

### 부적합한 경우

- 태그 이름이 매 레코드마다 달라지는 경우 (태그 수 폭발)
- 태그/시간 범위 없이 전체 데이터를 자주 UPDATE해야 하는 경우
- 단순 이벤트 로그 (LOG 테이블 권장)

## 결과 확인과 정리

IoT 예제는 다음 조회에서 세 측정값이 같은 한 행으로 나오는지 확인합니다.

```sql
SELECT name, time, temperature, vibration, current FROM factory_sensor;
DROP TABLE factory_sensor;
DROP TABLE energy_meter;
DROP TABLE vehicle_track;
```

정리는 이 페이지에서 실제로 생성한 테이블에만 적용합니다.
