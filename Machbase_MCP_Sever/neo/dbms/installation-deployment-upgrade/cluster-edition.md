# Cluster Edition 설치와 배포

Cluster Edition은 SQL 접속, 데이터 저장, 복제와 노드 관리를 여러 역할로 나눕니다.
설치 전에 각 역할을 어느 호스트에 배치할지, 어떤 포트와 저장 경로를 사용할지 정합니다.
일반 SQL 접속은 Broker로, 운영 명령은 해당 관리 노드로 보내야 합니다.

## 노드 역할

| 노드 | 역할 |
|------|------|
| **Coordinator** | 클러스터 메타 정보 관리, 노드 상태 감시 |
| **Deployer** | 패키지 배포 및 노드 초기화 중계 |
| **Lookup** | 참조 데이터와 조회 처리 |
| **Broker** | SQL 파싱 및 쿼리 분배, 클라이언트 접점 |
| **Warehouse** | 실제 데이터 저장 및 쿼리 실행 |

아래 YAML 예시는 세 호스트에 Coordinator 2개, Deployer 3개, Lookup 2개(master 1개,
monitor 1개), Broker 2개와 Warehouse 2개(하나의 복제 그룹)를 배치합니다.
실제 노드 수와 배치는 가용성, 처리량과 장애 시 남아 있어야 할 용량을 기준으로 정합니다.

## 배포 방식

| 방식 | 설명 | 적합한 경우 |
|------|------|------------|
| machclusterctl | cluster.yaml 기반 자동 배포 | 권장. 신규 구축 |
| 수동 (machcoordinatoradmin) | Coordinator 명령 기반 노드 등록·배포 | 세밀한 제어가 필요한 경우 |

## 설치 순서

1. Cluster Edition 구성 개요 숙지
2. 환경 준비 (SSH 키, 커널 파라미터, NTP)
3. 패키지·경로와 라이선스 적용 방식 준비
4. 배포 방식 선택 후 설치·기동하고 라이선스 확인
5. 설치 검증

---

## Cluster Edition 구성 개요

역할이 분리된 Coordinator, Deployer, Lookup, Broker, Warehouse 노드로 구성됩니다. 각 노드의 역할과 상호 관계를 이해한 후 배포 계획을 세우십시오.

### 노드 역할 상세

#### Coordinator

클러스터 메타데이터, 노드 등록과 상태 감시를 담당합니다. Primary/Secondary 이중화를
검토하십시오. 실행 중인 데이터 처리 경로와 관리 경로는 구분되지만, Coordinator 장애만으로
모든 SQL의 지속 동작을 보장할 수는 없습니다. 다른 노드 상태와 클라이언트 영향을 함께
확인하고 검증한 장애 대응 절차를 사용합니다.

- 설정 파일: `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`
- 관리 도구: `machcoordinatoradmin`
- 주요 포트: `CLUSTER_LINK_PORT_NO`, `HTTP_ADMIN_PORT`

기본값은 `CLUSTER_LINK_PORT_NO=3868`, `HTTP_ADMIN_PORT=5779`입니다. 이 장의 예제에서는 운영 중 포트 충돌을 피하기 위해 Coordinator link/admin 포트로 `5101`/`5102`를 명시합니다.

#### Deployer

Coordinator의 지시에 따라 각 노드에 패키지를 배포하고 초기화를 중계합니다. 각 노드 호스트에 하나씩 배치하거나, 별도 배포 서버로 운영합니다.

- 관리 도구: `machdeployeradmin`

#### Lookup

참조 데이터와 조회 처리를 위한 노드입니다. 구성에 따라 `master`, `monitor`, `slave`
역할을 지정합니다.

#### Broker

클라이언트의 SQL 요청을 받아 파싱하고 적절한 Warehouse로 분배합니다. 일반 애플리케이션은
Broker 주소로 연결합니다. Warehouse 직접 연결은 복제 상태 비교 같은 관리 진단 절차에서만
사용하며, 애플리케이션의 접속 경로와 구분합니다. Broker 이중화를 권장합니다.

- 클라이언트 접속 포트: 기본 5656

#### Warehouse

실제 데이터를 저장하고 쿼리를 실행합니다. 같은 그룹의 Warehouse끼리 데이터를 복제하여 고가용성을 제공합니다. 그룹당 2개 이상을 권장합니다.

### 구성 예시

```
[클라이언트]
     │ (SQL, 5656)
     ▼
[Broker ×2]  ──────────────────────────────────────────
     │ (쿼리 분배)
     ├─► [Warehouse group1-node1] ◄──복제──► [Warehouse group1-node2]
     └─► [Warehouse group2-node1] ◄──복제──► [Warehouse group2-node2]

[Coordinator Primary] ◄──HA──► [Coordinator Secondary]
     │ (메타 관리, 노드 감시)
[Deployer]
     │
[Lookup master / monitor]
```

### 에디션 비교

Standard Edition과의 상세 비교는 에디션 차이점을 참고하십시오.

---

## Cluster Edition 설치 환경 준비

배포 전에 모든 노드에 다음 환경을 준비합니다.

### 파일 디스크립터 한도

모든 노드에서 아래 설정을 적용합니다.

```bash
sudo vi /etc/security/limits.conf
```

```
*  hard  nofile  65535
*  soft  nofile  65535
```

서버 실행 계정으로 새 로그인 세션을 연 뒤 확인합니다. 서비스 관리자로 시작한다면
서비스 자체의 파일 디스크립터 한도도 확인합니다.

```bash
ulimit -Sn
# 65535
```

### OS 사용자 생성

모든 노드에 `machbase` 계정을 생성합니다.

```bash
sudo useradd -m machbase --home-dir /home/machbase
sudo passwd machbase
```

### SSH 키 기반 인증

`machclusterctl`을 사용하는 경우, 배포 서버에서 모든 노드로 비밀번호 없이 SSH 접속이 가능해야 합니다.

```bash
# 배포 서버에서 SSH 키 생성 (이미 있으면 생략)
ssh-keygen -t rsa -b 4096

# 각 노드에 공개 키 등록
ssh-copy-id machbase@192.168.1.11
```

등록 후 비밀번호 없이 접속이 되는지 확인합니다.

```bash
ssh machbase@192.168.1.11 'hostname'
```

### 네트워크 커널 파라미터

다음은 네트워크 버퍼 조정 예시이며 모든 서버에 적용할 필수값이 아닙니다. 현재 커널 설정,
메모리 사용량과 네트워크 병목을 먼저 측정합니다. 값을 늘린 뒤 처리량뿐 아니라 메모리와
지연도 비교하고 효과가 확인된 항목만 영구 적용합니다.

```bash
sudo sysctl -w net.core.rmem_default=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

영구 적용은 `/etc/sysctl.conf`에 추가합니다.

### 시간 동기화 (NTP)

모든 노드의 시스템 시간이 일치해야 합니다. NTP 또는 `chrony`로 동기화하십시오.

```bash
# chrony 사용 예
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc tracking
```

타임 서버를 사용할 수 없는 격리된 설치 환경에서는 초기 시각을 직접 설정할 수 있습니다.
다음 값은 형식 예시이므로 실제 현재 시각으로 바꾸십시오. 수동 설정만으로 노드 간 시간 차이가
지속적으로 보정되지는 않으므로 운영 전에는 시간 동기화 경로를 마련합니다.

```bash
sudo date -s "2025-01-02 12:34:56"
```

### 포트 예약

각 노드에서 Machbase가 사용할 포트를 예약합니다.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5101-5110,5201-5202,5301-5302,5401,5500-5503,5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

기존 예약 포트가 있으면 덮어쓰지 말고 쉼표로 구분해 병합합니다. 클러스터 구성에 따라 포트 범위를 조정하십시오. Cluster link, Coordinator/Deployer 관리, 서비스, Warehouse 복제 관리자 포트 등을 모두 포함해야 합니다.

---

## machclusterctl 기반 배포

`machclusterctl`은 `cluster.yaml` 파일 하나로 전체 클러스터를 자동으로 배포하고 관리하는 도구입니다. SSH를 통해 각 노드에 원격 접속하여 패키지 배포, 초기화, 시작·종료를 일괄 처리합니다.

### 사전 조건

- Primary Coordinator를 설치할 호스트에서 명령을 실행하며, 패키지와 SSH 개인키를
  해당 호스트에서 읽을 수 있어야 합니다.
- Primary 호스트에서 모든 대상 호스트로 SSH 키 기반 인증이 설정되어 있어야 합니다.
- 각 노드의 `home_path`와 `dbs_path` 상위 경로를 생성·기록할 권한이 있어야 합니다.
- 별도 라이선스가 필요하면 자동 기동 전에 배포 패키지와 라이선스 적용 절차를 준비합니다.
  YAML에 임의의 라이선스 속성을 추가하지 않습니다.
- Cluster Edition 설치 환경 준비 완료

### 작업 순서

| 단계 | 문서 |
|------|------|
| 1. cluster.yaml 작성 | cluster.yaml 작성 |
| 2. YAML 유효성 검사 | YAML 검증 |
| 3. 최초 설치 및 시작 | 최초 설치 |
| 4. 상태 확인 | 최초 설치와 상태 확인 |
| 5. (이후) 구성 변경 | Cluster 운영 |
| 6. (장애 시) 복구 | Cluster 문제 해결 |

---

### cluster.yaml 작성

`cluster.yaml`은 설치할 노드 구성과 경로를 선언합니다. 아래 주소는 예시이므로 실제 호스트로
바꿉니다. `origin_path`는 명령을 실행하는 Primary Coordinator 호스트에서 읽는 압축 파일,
`home_path`와 `dbs_path`는 해당 노드 호스트의 경로입니다. `deployer`는 그 노드를
배치·제어할 Deployer를 참조합니다.

#### 파일 구조 예시

```yaml
version: "1"

cluster:
  name: mc-prod

  hosts:
    node1:
      address: machbase@192.168.1.10
    node2:
      address: machbase@192.168.1.11
    node3:
      address: machbase@192.168.1.12

  package:
    name: machbase
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /home/machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /home/machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /home/machbase/lookup
      cluster_link_port: 5301
    broker:
      home_path: /home/machbase/broker
      cluster_link_port: 5401
      service_port: 5656
    warehouse:
      home_path: /home/machbase/warehouse
      cluster_link_port: 5501
      service_port: 5500

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

    - alias: deployer-3
      host: node3

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1
      dbs_path: /data/machbase/broker-1/dbs

    - alias: broker-2
      host: node2
      deployer: deployer-2

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2
          dbs_path: /data/machbase/warehouse-group1-1/dbs

        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
          dbs_path: /data/machbase/warehouse-group1-2/dbs
```

#### 주요 항목 설명

| 항목 | 설명 |
|------|------|
| `version` | YAML 스키마 버전입니다. 현재 `"1"`을 사용합니다. |
| `cluster.name` | 클러스터 이름입니다. `destroy` 확인 등에서 사용됩니다. |
| `cluster.hosts` | 노드에서 참조할 호스트 별칭과 SSH 접속 주소입니다. `address`는 `user@host` 형식을 사용합니다. |
| `cluster.package.name` | Coordinator에 등록할 패키지 이름입니다. |
| `cluster.package.origin_path` | `install`, `apply`, `upgrade` 실행 때 입력으로 사용할 패키지 보관 파일 경로입니다. |
| `cluster.package.registered_path` | `export`가 기록하는 Coordinator 패키지 저장소의 관찰 경로입니다. 실행 입력으로 사용하지 않습니다. |
| `cluster.ssh.key_file` | 대상 서버 접속에 사용할 개인키 경로입니다. 비밀번호 필드는 사용하지 않습니다. |
| `cluster.defaults` | 노드 타입별 `home_path`, `cluster_link_port`, `service_port` 기본값입니다. |
| `cluster.coordinators` | Coordinator 노드 목록입니다. `role`은 `primary` 또는 `secondary`를 사용합니다. |
| `cluster.deployers` | Deployer 노드 목록입니다. |
| `cluster.lookup` | Lookup 노드 목록입니다. `type`은 `master`, `monitor`, `slave`를 사용합니다. |
| `cluster.brokers` | Broker 노드 목록입니다. 클라이언트 SQL 접속 포트는 `service_port`입니다. |
| `cluster.warehouse_groups` | Warehouse 그룹과 그룹별 노드 목록입니다. |

#### 권장 구성

- Coordinator: 2개 (Primary + Secondary HA)
- Deployer: 1개 이상
- Lookup: `master` 1개, `monitor` 1개 이상
- Broker: 2개 이상 (부하 분산)
- Warehouse 그룹: 그룹당 2개 (복제를 통한 고가용성)

같은 서버에 같은 타입의 노드를 2개 이상 배치할 때는 두 번째 노드부터 `home_path`와 포트를 명시적으로 지정하여 충돌을 피합니다.

Coordinator와 Deployer의 관리 포트는 `http_admin_port`를 사용합니다.

Broker와 Warehouse 노드에는 선택적으로 `dbs_path`를 지정합니다. `dbs_path`는 노드가 설치되는 서버 기준의 데이터 파일 경로이며, 생략하면 `machcoordinatoradmin --add-node`의 기본 `DBS_PATH` 동작을 따릅니다.

기존 `cluster.package.path`는 하위 호환 입력으로 사용할 수 있지만, 새로 작성하는 YAML에서는 `origin_path`를 사용합니다.

`http_admin_port`는 Coordinator와 Deployer에만 사용합니다. Broker, Lookup, Warehouse에는
HTTP 포트 필드를 지정하지 않습니다.

작성이 완료되면 유효성을 검사합니다.

---

### YAML 검증

`cluster.yaml`을 실제 설치에 사용하기 전에 유효성 검사를 수행합니다. `validate`는 YAML 문법과 필수 값, 별칭, 포트 충돌, 토폴로지 관계를 정적으로 검사합니다.

#### 검증 명령

```bash
machclusterctl validate -f cluster.yaml
```

#### 검증 항목

| 항목 | 설명 |
|------|------|
| YAML 문법 | 파일 파싱 오류 여부 |
| 환경변수 치환 | `${VAR}` 또는 `${VAR:-default}` 표현식 해석 가능 여부 |
| 필수 필드 | 클러스터 이름, 호스트, 패키지, 노드별 필수 값 누락 여부 |
| 별칭 | 노드 별칭 중복 여부 |
| 포트 충돌 | 같은 호스트 안에서 선언된 포트 충돌 여부 |
| 토폴로지 | Primary Coordinator, Lookup master/monitor, Deployer 참조 관계 |

#### 출력 예시

```text
Validation passed.
```

오류가 있으면 메시지에 표시된 항목을 수정한 뒤 재검증합니다.

#### 설치 전 실행 계획 확인

신규 설치 전에 SSH 접속, 패키지 파일 존재 여부, 원격 디렉터리 권한까지 확인하려면 `install --dry-run --verbose`를 사용합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

설치 후 구성 변경을 검증할 때는 `apply --dry-run`을 사용합니다. 현재 클러스터 상태와 YAML의 차이를 계산해 실행 계획을 보여주며, 실제 원격 변경 작업은 수행하지 않습니다.

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

#### 일반적인 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `field ... not found` | 지원하지 않는 YAML 키 사용 | 현행 스키마의 `cluster.*` 항목으로 수정 |
| `required field ...` | 필수 값 누락 | 메시지에 표시된 필드를 추가 |
| `duplicate alias` | 노드 별칭 중복 | 모든 노드 별칭을 고유하게 변경 |
| `port conflict` | 같은 호스트에서 동일 포트 사용 | 충돌한 포트를 다르게 지정. 홈 경로만 바꾸어도 포트 충돌은 해결되지 않음 |
| `deployer ... not found` | Lookup/Broker/Warehouse가 존재하지 않는 Deployer를 참조 | `deployer` 값을 Deployer 별칭 또는 호스트:포트로 수정 |

---

### 최초 설치

`cluster.yaml` 작성과 유효성 검사가 완료되면 설치 계획을 확인한 뒤 클러스터를 설치합니다.

#### 1. 클러스터 설치

패키지를 각 노드에 배포하고 초기화하기 전에 실행 계획과 사전 점검 결과를 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

문제가 없으면 실제 설치를 실행합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

이 명령은 다음을 자동으로 처리합니다.

1. 패키지를 각 노드에 복사하고 압축 해제
2. 각 노드의 `machbase.conf` 생성 및 포트 설정
3. Coordinator 데이터베이스 초기화
4. 노드 등록 (Coordinator에 각 노드 추가)

#### 2. 클러스터 시작

`install`은 Coordinator, Deployer, Lookup, Broker, Warehouse를 준비하고 기동합니다. 설치 후 전체 클러스터를 다시 시작해야 할 때만 다음 명령을 사용합니다.

```bash
machclusterctl start
```

#### 3. 상태 확인

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
machclusterctl status
```

한 서버에서 여러 Coordinator 홈을 번갈아 확인할 때는 직접 지정합니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

출력은 `machcoordinatoradmin --cluster-status-full --verbose` 형식입니다. 아래는 출력 열을
보여 주는 일부 행의 예시이며 YAML의 전체 노드 목록이 아닙니다. Coordinator와 Broker는
`primary`, `leader` 같은 역할 상태를 가질 수 있으므로 모든 행이 `normal`인지가 아니라
등록 노드 수와 역할별 목표 상태·실제 상태가 맞는지 확인합니다.

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

#### 4. 클라이언트 접속 테스트

Broker 노드의 IP와 포트로 접속합니다.

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
# Mach>
```

#### 클러스터 종료

```bash
machclusterctl stop
```

---

### 설치 후 운영

최초 설치와 접속 검증이 끝난 뒤의 노드 구성 변경, 노드 추가·제거와 상태 복구는
Cluster 운영을 따릅니다. 장애 원인 분류와
복구 판단은 Cluster 문제 해결을 참고하십시오.

## machcoordinatoradmin 기반 수동 배포

`machclusterctl`을 사용할 수 없을 때는 Coordinator와 Deployer를 직접 준비하고 패키지와
노드를 등록합니다. 자동 배포가 끝난 환경에 아래 생성 명령을 다시 실행하지 마십시오.
수동 예제는 YAML과 별개의 구성입니다. 역할별 실행 위치를 바꾸어 명령을 수행합니다.

| 호스트 | 역할 |
|---|---|
| `192.168.1.10` | Primary Coordinator, Deployer, Lookup master |
| `192.168.1.11` | Deployer, Lookup monitor, Broker |
| `192.168.1.13` | Deployer, Warehouse group1 첫 노드 |
| `192.168.1.14` | Deployer, Warehouse group1 복제 노드 |
| `192.168.1.20` | 선택적인 Secondary Coordinator |

같은 호스트의 역할마다 홈과 포트를 분리합니다. Deployer는 데이터 처리 노드가 설치될
각 호스트에서 준비하며, 아래 `--deployer` 주소도 대상 호스트와 맞춥니다.

### 수동 배포 순서

1. Package 준비와 등록 — 전체 패키지 설치와 경량 패키지 등록 준비
2. Coordinator / Deployer 설치 — 핵심 관리 노드 구동
3. Package 등록 — 실행 중인 Coordinator에 경량 패키지 등록
4. Lookup / Broker / Warehouse 설치 — 데이터 처리 노드 등록 및 구동
5. 전체 상태 확인 — 등록·구동 후 최초 상태 검증

### machclusterctl 대비 차이점

| 항목 | machclusterctl | 수동 배포 |
|------|---------------|----------|
| 설정 방식 | cluster.yaml 단일 파일 | 각 노드 machbase.conf 직접 편집 |
| 패키지 배포 | 자동 원격 복사 | Coordinator/Deployer는 직접 설치, Broker/Warehouse는 Deployer가 배포 |
| 노드 등록 | 자동 | `machcoordinatoradmin --add-node` 수동 실행 |
| 일괄 시작·종료 | `machclusterctl start/stop` | 노드별 개별 실행 |

수동 배포는 유연성이 높지만 실수 가능성도 높습니다. 신규 구축에는 `machclusterctl`을 권장합니다.

---

### Package 준비와 등록

Cluster Edition 수동 배포의 패키지 준비와 등록 절차입니다. Coordinator와 Deployer에는 전체 패키지를 설치하고 환경 변수를 설정합니다. Broker와 Warehouse 배포에 사용할 경량 패키지는 Coordinator가 기동된 후에 등록합니다.

#### 패키지 종류

Cluster Edition에는 두 가지 패키지가 있습니다.

| 패키지 | 대상 노드 | 특징 |
|--------|-----------|------|
| 전체 패키지 | Coordinator, Deployer | 모든 실행 파일 포함 |
| 경량 패키지 (lightweight) | Broker, Warehouse | 데이터 처리에 필요한 파일만 포함, 크기 작음 |

파일명 예시:
- 전체: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`
- 경량: `machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz`

#### Coordinator와 Deployer에 패키지 배포

전체 패키지 파일을 Coordinator와 Deployer 노드에 복사하고 압축 해제합니다.

##### Coordinator 노드

```bash
# Coordinator 노드에서 실행
mkdir -p /home/machbase/coordinator
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/coordinator
```

##### Deployer 노드

```bash
mkdir -p /home/machbase/deployer
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/deployer
```

Broker와 Warehouse 노드에는 이 단계에서 경량 패키지를 직접 압축 해제하지 않습니다. 경량 패키지를 Coordinator에 등록하면, 이후 `--add-node`로 지정한 Deployer가 대상 노드의 `--home-path`에 패키지를 배포합니다.

#### Coordinator에 패키지 등록

Broker와 Warehouse를 Coordinator에서 기동하려면 경량 패키지를 Coordinator에 등록해야 합니다. Coordinator와 Deployer를 설치하고 Coordinator가 실행 중인 상태에서 다음 명령을 실행합니다.

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz"
```

등록된 패키지는 이후 Broker와 Warehouse를 `--add-node`로 등록할 때 `--package-name=machbase`로 참조합니다.

#### 환경 변수 설정

`package-host`와 `/path/to/`는 실제 패키지 보관 위치로 바꿉니다. Coordinator와 Deployer를
같은 호스트에서 관리하더라도 별도의 셸에서 역할에 맞는 환경을 사용합니다.
다음은 각 셸에 적용할 값이며, 서비스나 로그인 초기화 파일에도 같은 값을 반영합니다.

```bash
# Coordinator 노드
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

```bash
# 별도 Deployer 관리 셸
export MACHBASE_DEPLOYER_HOME=/home/machbase/deployer
export MACHBASE_HOME=$MACHBASE_DEPLOYER_HOME
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

---

### Coordinator / Deployer 설치

패키지 배포가 완료되면 Coordinator를 먼저 설치·시작한 후 Deployer를 등록합니다.

#### Coordinator 설치

##### 1. machbase.conf 설정

`$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`를 편집합니다.

```bash
vi $MACHBASE_COORDINATOR_HOME/conf/machbase.conf
```

주요 설정:

```
CLUSTER_LINK_HOST    = 192.168.1.10   # 이 노드의 IP
CLUSTER_LINK_PORT_NO = 5101
HTTP_ADMIN_PORT      = 5102
```

##### 2. 메타 데이터베이스 생성 및 서비스 시작

```bash
machcoordinatoradmin -c
machcoordinatoradmin -u
```

##### 3. 자기 자신을 Coordinator 노드로 등록

```bash
machcoordinatoradmin --add-node="192.168.1.10:5101" \
  --node-type=coordinator \
  --http-admin-port=5102
```

##### 4. 등록 확인

```bash
machcoordinatoradmin --cluster-status
```

#### Secondary Coordinator 설치 (선택)

고가용성을 위해 Secondary Coordinator를 추가합니다.

Secondary 노드에서 패키지를 배포하고 `machbase.conf`를 설정한 후, **Primary Coordinator에서** 먼저 노드를 등록합니다.

```bash
# Primary Coordinator에서 먼저 등록
machcoordinatoradmin --add-node="192.168.1.20:5101" \
  --node-type=coordinator \
  --http-admin-port=5102

# 그 다음 Secondary 노드에서 시작 (--primary 옵션으로 Primary 지정)
machcoordinatoradmin -u --primary=192.168.1.10:5101
```

Secondary를 시작하기 전에 반드시 Primary에서 노드 등록을 완료해야 합니다.

#### Deployer 설치

수동 구성표의 각 Deployer 호스트에서 이 절차를 수행합니다. 아래 설정의
`CLUSTER_LINK_HOST`는 그 호스트 자신의 IP로 바꿉니다. 다른 호스트의 주소를 그대로
복사하면 노드의 통신 주소와 실제 실행 위치가 달라집니다.

##### 1. machbase.conf 설정

```
CLUSTER_LINK_HOST    = 192.168.1.10   # Deployer 노드 IP
CLUSTER_LINK_PORT_NO = 5201
HTTP_ADMIN_PORT      = 5202
```

##### 2. 시작

```bash
machdeployeradmin -c
machdeployeradmin -u
```

##### 3. Coordinator에 Deployer 노드 등록

모든 Deployer가 시작되면 Primary Coordinator 관리 셸에서 등록합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.10:5201" \
  --node-type=deployer \
  --http-admin-port=5202

machcoordinatoradmin --add-node="192.168.1.11:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.13:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.14:5201" \
  --node-type=deployer --http-admin-port=5202
```

---

### Lookup / Broker / Warehouse 설치

Coordinator와 Deployer가 준비된 후 Lookup, Broker, Warehouse 노드를 Coordinator에 등록하고 시작합니다. Broker와 Warehouse를 등록하기 전에 경량 패키지를 Coordinator에 `--add-package`로 등록해야 합니다.

#### Lookup 노드

Lookup master와 monitor를 각각 등록하고 시작합니다. 다음 예제는 Primary 호스트와 Broker
호스트에 배치하며, 각 호스트의 Deployer를 사용합니다. 같은 홈이 기존 Lookup에 사용 중이
아닌지 확인합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.10:5301" \
  --node-type=lookup \
  --lookup-type=master \
  --deployer="192.168.1.10:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --add-node="192.168.1.11:5301" \
  --node-type=lookup \
  --lookup-type=monitor \
  --deployer="192.168.1.11:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --startup-node="192.168.1.10:5301"
machcoordinatoradmin --startup-node="192.168.1.11:5301"
```

#### Broker 설치

##### 1. 등록 파라미터 확인

Broker 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다.
등록 전에 클러스터 통신 포트와 서비스 포트를 확정합니다. Broker에는 HTTP 관리 포트를
지정하지 않습니다.

```
CLUSTER_LINK_HOST    = 192.168.1.11   # Broker 노드 IP
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656           # 클라이언트 접속 포트
```

##### 2. Coordinator에 노드 등록

Coordinator 노드에서 실행합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.11:5401" \
  --node-type=broker \
  --deployer="192.168.1.11:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/broker" \
  --dbs-path="/data/machbase/broker_dbs" \
  --port-no=5656
```

| 파라미터 | 설명 |
|---------|------|
| `--add-node` | 등록할 노드의 IP:CLUSTER_LINK_PORT_NO |
| `--node-type` | `broker` / `warehouse` / `lookup` |
| `--deployer` | 해당 노드를 설치하고 제어할 Deployer의 IP:CLUSTER_LINK_PORT_NO |
| `--package-name` | Coordinator에 등록한 패키지 이름 |
| `--home-path` | 노드 홈 디렉터리 |
| `--dbs-path` | Broker/Warehouse의 데이터 파일 경로. 생략하면 기본 `DBS_PATH`를 사용 |
| `--port-no` | 클라이언트 또는 노드 서비스 포트 |
| `--replication` | Warehouse 복제 관리자 주소입니다. `host:port` 형식을 사용합니다. |

##### 3. 노드 시작

Coordinator에서 해당 노드를 시작합니다.

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

#### Warehouse 설치

Warehouse 노드는 그룹 단위로 구성합니다. 같은 그룹의 노드끼리 데이터를 복제합니다.

##### 1. 등록 파라미터 확인

Warehouse 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다. 등록 전에 클러스터 통신 포트, 서비스 포트, 복제 관리자 주소를 확정합니다.

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5501
PORT_NO              = 5500
```

##### 2. 노드 등록

```bash
machcoordinatoradmin --add-node="192.168.1.13:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.13:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_1" \
  --dbs-path="/data/machbase/warehouse_g1_1_dbs" \
  --port-no=5500 \
  --replication=192.168.1.13:5502 \
  --group=group1 \
  --no-replicate

machcoordinatoradmin --add-node="192.168.1.14:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.14:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_2" \
  --dbs-path="/data/machbase/warehouse_g1_2_dbs" \
  --port-no=5500 \
  --replication=192.168.1.14:5502 \
  --group=group1
```

별도 `--add-group` 명령은 사용하지 않습니다. Warehouse 그룹 이름은 각 Warehouse 노드를 등록할 때 `--group`으로 지정합니다.

##### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5501"
machcoordinatoradmin --startup-node="192.168.1.14:5501"
```

#### 전체 상태 확인

모든 노드 등록 후 상태를 확인합니다.

```bash
machcoordinatoradmin --cluster-status
```

Coordinator, Lookup, Broker, Warehouse가 각 역할에 맞는 정상 상태로 표시되면 클러스터가 정상 구동 중입니다. Coordinator는 `primary`, Broker는 `leader`, Warehouse는 `normal`, `sync-active`, `sync-standby` 등으로 표시됩니다.

#### 최초 접속 확인

Broker 네이티브 포트로 접속해 `SELECT CURRENT_DATABASE();`와 표본 조회를 실행합니다. 최초 설치 검증이 끝난 뒤의 개별 노드 시작·종료와 상태 복구는 Cluster 운영과 Cluster 문제 해결을 사용하십시오.
