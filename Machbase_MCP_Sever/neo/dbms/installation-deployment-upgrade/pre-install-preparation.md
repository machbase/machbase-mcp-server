# 설치 전 준비

설치 전 준비의 목적은 실행 파일을 복사할 위치뿐 아니라 데이터가 남을 위치, 서버를
실행할 계정과 클라이언트의 접속 경로를 확정하는 것입니다. 패키지와 운영체제의 호환성을
확인한 뒤 저장 공간, 네트워크와 라이선스를 준비합니다. 지원 범위는 제공받은 패키지의
릴리스 정보와 기술 지원 정책을 기준으로 판단합니다.

## 먼저 정할 배포 정보

| 항목 | 정할 내용 | 필요한 이유 |
|---|---|---|
| Edition과 버전 | Standard 또는 Cluster, 서버·SDK 버전 | 사용할 SQL 기능과 배포 방법 결정 |
| OS 계정 | 서버 실행 계정과 파일 소유자 | 설정·데이터·로그 경로의 접근 권한 일치 |
| 설치 홈 | 실행 파일과 설정이 있는 절대 경로 | 관리 명령이 조작할 인스턴스 식별 |
| 데이터 경로 | 실제 `DBS_PATH`, 파일 시스템과 여유 공간 | 재시작·업그레이드 때 보존할 데이터 식별 |
| 접속 정보 | 서버 주소, SQL 포트, 관리 포트와 허용 클라이언트 | 포트 충돌과 잘못된 인스턴스 접속 방지 |
| 복구와 라이선스 | 백업 저장소, 복원 절차, 사용할 라이선스 | 장애 대응과 운영 범위 확인 |

OS 계정 `machbase`와 DB 사용자 `SYS`는 다릅니다. 전자는 프로세스와 파일의 권한을,
후자는 SQL 접속과 데이터베이스 작업 권한을 결정합니다. 서버 시작에 성공해도 파일 권한이나
SQL 권한이 맞지 않으면 적재·백업 같은 작업은 실패할 수 있습니다.

| 항목 | 설명 |
|------|------|
| 설치 전 요구사항 | OS 버전, 하드웨어 최소 사양, 네트워크 포트 |
| 패키지 구성 이해 | 패키지 파일 명명 규칙, 디렉터리 구조, 주요 실행 파일 |
| 라이선스 설치 | license.dat 파일 배치 방법, 라이선스 상태 확인 방법 |

---

## 설치 전 요구사항

### 운영체제와 패키지

운영체제 종류와 CPU 아키텍처가 설치 패키지의 표기와 일치해야 합니다. 지원 운영체제와 최소
버전은 릴리스마다 바뀔 수 있으므로, 고정된 버전 표 대신 패키지와 함께 제공되는 릴리스 정보로
확인하십시오.

### 시스템 자원

CPU, 메모리, 디스크와 네트워크 요구량은 입력률, 보관 기간, 인덱스와 ROLLUP 구성에 따라
달라집니다. 설치 공간뿐 아니라 예상 원시 데이터, 백업과 운영 여유 공간을 포함해 산정하고,
실제 워크로드로 용량과 처리량을 검증하십시오. 초당 행 수와 보관 기간으로 원본 행 수를
예상하고, 대표 데이터를 적재해 행 크기·압축·인덱스의 실제 저장 비용을 측정합니다.
Cluster에서는 복제본 공간도 포함합니다. 같은 디스크의 다른 디렉터리는 별도의 장애
영역이나 독립적인 I/O 장치가 아닙니다.

### 기본 포트

| 포트 | 용도 |
|------|------|
| **5656** | SQL 클라이언트 접속 (Native TCP) |

SQL 클라이언트 포트를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO`를
설정합니다. `MACHBASE_PORT_NO` 환경 변수도 사용하므로 서버를 시작하는 셸이나 서비스의
환경 변수를 함께 확인합니다. 변경한 포트는 클라이언트에도 명시하고, 이미 실행 중인
서버에 새 환경 변수가 소급 적용된다고 가정하지 마십시오.

방화벽이 있는 환경에서는 위 포트를 인바운드 허용으로 열어야 합니다. Cluster Edition은 Coordinator link/admin 포트와 Broker, Warehouse, Deployer 포트도 추가로 열어야 합니다.

### 시스템 커널 파라미터 (Linux)

Linux에 설치할 경우 아래 항목을 설치 전에 점검합니다.

#### 파일 디스크립터 한도

다수의 파일을 동시에 여는 워크로드에서는 낮은 파일 디스크립터 한도가 병목이 될 수 있습니다.
기본 한도는 운영체제와 계정 설정에 따라 다르므로 서버를 실행할 계정에서 확인합니다.

```bash
# 현재 값 확인
ulimit -Sn
```

이 설치 예제에서는 65535를 사용합니다. 한도가 이보다 작으면 `/etc/security/limits.conf`를
수정한 뒤 새 로그인 세션에서 적용 여부를 확인합니다.

```
*  hard  nofile  65535
*  soft  nofile  65535
```

서버를 실행할 계정으로 다시 로그인한 뒤 값을 확인합니다. 서비스 관리자를 통해 서버를
시작한다면 해당 서비스의 파일 디스크립터 한도도 별도로 확인합니다.

```bash
ulimit -Sn
# 출력: 65535
```

#### 포트 예약

Machbase 서비스 포트가 운영체제의 임시 포트 자동 할당에 사용되지 않도록 예약합니다.
이 설정은 다른 프로세스가 같은 포트를 명시적으로 사용하는 것까지 차단하지는 않습니다.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

기존 예약 포트가 있으면 덮어쓰지 말고 쉼표로 구분해 병합합니다. 영구 적용은 `/etc/sysctl.conf`의 `net.ipv4.ip_local_reserved_ports` 항목을 다음 값과 병합합니다.

```
net.ipv4.ip_local_reserved_ports = 5656
```

### 시간 동기화

시계열 데이터를 처리하므로 서버의 시간이 정확해야 합니다. NTP 또는 `chrony`로 시스템 시간을 동기화하십시오. Cluster Edition에서는 모든 노드의 시간을 일치시켜야 합니다.

```bash
# 타임존 확인
ls -l /etc/localtime
date
```

---

## 패키지 구성 이해

### 패키지 파일 명명 규칙

패키지 파일 이름은 에디션에 따라 다음 형식을 따릅니다.

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE.EXT
```

| 항목 | 설명 | 예시 |
|------|------|------|
| EDITION | 에디션 구분 | `SDK`, `cluster` |
| VERSION | 버전 (Major.Minor.Fix.AUX) | `8.7.0.official` |
| OS | 운영체제 | `LINUX`, `WINDOWS` |
| CPU | CPU 아키텍처 | `X86` |
| BIT | 아키텍처 비트 수 | `64` |
| MODE | 빌드 모드 | `release` |
| EXT | 확장자 | `tgz` (Linux), `zip` 또는 설치 실행 파일 (Windows) |

Standard Edition Linux tarball은 `machbase-SDK-...tgz` 이름으로 생성됩니다.

예시:
- Standard Edition: `machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz`
- Cluster Edition: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`

Minor 버전이 다르면 DB 파일과 프로토콜의 호환성이 달라질 수 있습니다. Fix 버전 변경을
포함한 실제 업그레이드 가능 경로는 대상 릴리스의 호환성 안내와
업그레이드 절차에서 확인합니다.

### 설치 디렉터리 구조

tarball 압축을 해제하면 `$MACHBASE_HOME` 아래에 다음 구조가 생성됩니다.

```
$MACHBASE_HOME/
├── bin/        실행 파일
├── conf/       설정 파일 (machbase.conf 등)
├── dbs/        데이터 저장 공간
├── doc/        라이선스 문서
├── include/    C/C++ 헤더 파일
├── install/    Makefile용 mk 파일
├── lib/        공유 라이브러리
├── package/    Cluster Edition 추가 패키지 경로
├── sample/     예제 파일
├── trc/        서버 로그 및 트레이스 파일
├── tutorials/  튜토리얼
├── utility/    유틸리티 파일
└── 3rd-party/  Grafana 플러그인 등
```

### 주요 실행 파일

| 실행 파일 | 설명 |
|-----------|------|
| `machbased` | 서버 데몬 |
| `machadmin` | 서버 관리 (시작·종료·DB 생성) |
| `machsql` | CLI 쿼리 도구 |
| `machloader` | 대용량 파일 적재·추출 도구 |
| `csvimport` | CSV 파일 가져오기 |
| `csvexport` | CSV 파일 내보내기 |
| `tagmetaimport` | TAG 메타 데이터 일괄 등록 |

Cluster Edition 패키지에는 `machcoordinatoradmin`, `machdeployeradmin` 등의 관리 도구가 추가됩니다.
`machclusterctl`은 해당 도구를 포함하도록 빌드된 패키지에서 사용할 수 있습니다.

### 설정 파일

`$MACHBASE_HOME/conf/` 아래에 에디션별 샘플 설정 파일이 있습니다.

```bash
ls $MACHBASE_HOME/conf/
# machbase.conf
# machbase.conf.sample.standard
# machbase.conf.sample.edge
# machloader.conf.sample
```

실제 사용 파일은 `machbase.conf`입니다. Standard full 패키지는 빌드 과정에서 `machbase.conf.sample.standard`를 복사해 `machbase.conf`를 포함합니다. 실제 파일이 없는 패키지에서는 에디션에 맞는 샘플 파일을 복사하여 수정합니다.

Standard/Edge 샘플에는 TRANSACTION 쓰기 충돌과 내구성 정책을 제어하는 `TRANSACTION_BUSY_TIMEOUT_MS`,
`TRANSACTION_SYNCHRONOUS`, `TRANSACTION_JOURNAL_MODE` 설정이 포함됩니다. TRANSACTION 테이블을 사용하는 환경에서는
기본값을 먼저 사용하고, 동시 쓰기와 내구성 요구를 검토한 뒤 값을 조정합니다.

---

## 라이선스 설치

라이선스 파일이 없으면 서버는 기본 `COMMUNITY` 라이선스 정보를 사용합니다. 설치 전에
이 범위가 예정한 기능·용량에 맞는지 확인하고, 별도 라이선스가 필요한 환경에서는
첫 서버 시작 전에 해당 파일을 준비합니다. 서버가 기동된다는 사실만으로 운영에 필요한
라이선스 조건을 충족했다고 판단하지 마십시오.

### 라이선스 상태 확인

설치된 라이선스의 상태와 제한 위반 여부는 `V$LICENSE_INFO`의 `VIOLATE_STATUS`와
`VIOLATE_MSG`로 확인합니다. 라이선스 파일의 본문은 수정하지 마십시오.

### 설치 방법

#### 방법 1: 파일 복사 (서버 시작 전)

`license.dat` 파일을 `$MACHBASE_HOME/conf/`에 복사합니다. 서버가 시작될 때 자동으로 인식합니다.

```bash
cp license.dat $MACHBASE_HOME/conf/license.dat
```

#### 방법 2: machadmin 명령

`machadmin`으로 라이선스 파일을 검증하고 설치합니다. 서버가 실행 중이면 라이선스 reload 요청을 함께 보냅니다.

```bash
machadmin -t /path/to/license.dat
```

#### 방법 3: SQL 쿼리 (서버 실행 중)

서버가 이미 실행 중인 경우 machsql에서 쿼리로 설치합니다.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/license.dat';
```

### 설치 확인

#### machadmin 확인

```bash
machadmin -f
```

#### V$LICENSE_INFO 뷰 조회

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`가 0이면 정상입니다.

machsql에서는 다음 명령으로도 라이선스 정보를 확인합니다.

```sql
SHOW LICENSE;
```
