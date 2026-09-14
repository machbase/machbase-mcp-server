# 업그레이드

업그레이드는 실행 파일 교체뿐 아니라 기존 데이터, 설정과 애플리케이션이 새 버전에서
같은 의미로 동작하는지 확인하는 작업입니다. 먼저 지원되는 버전 간 경로를 확인하고,
복원 가능한 백업과 서비스 재개 기준을 준비합니다. 다음 예제의 8.7.0 패키지명과 경로는
제공받은 실제 배포본에 맞춥니다.

## 업그레이드 전 확인사항

- 현재 버전과 대상 버전의 호환성을 확인합니다. Minor 버전이 다르면 DB 파일 형식이 변경될 수 있습니다.
- 업그레이드 전 백업을 수행합니다. 백업 방법 참고.
- 진행 중인 INSERT·APPEND 클라이언트를 확인합니다.

### 8.7.0 업그레이드 사전 점검

8.5에서 8.7.0으로 업그레이드할 때는 바이너리를 교체하기 전에 다음 의존성을 조사하고
지원되는 방식으로 전환합니다.

1. 제거된 `HTTP_AUTH`, `HTTP_ENABLE`, `HTTP_MAX_MEM`, `HTTP_PORT_NO`, `RS_CACHE_*`,
   `STREAM_THREAD_COUNT`, `STREAM_WAIT_MS` 설정을 현재 파일에서 찾아 지원 목록과 대조합니다.
   제거된 설정은 삭제하고 유지 설정은 보존합니다. 특히 Cluster의 `HTTP_ADMIN_PORT`는
   현행 관리 포트이므로 `HTTP_*`라는 이유로 함께 제거하지 마십시오.
2. `/machbase`, `/machiot`를 호출하는 애플리케이션은 지원되는 SDK를 사용하는 백엔드로
   전환합니다.
3. `STREAM_*` 프로시저와 `FLUSH RESULT_CACHE`를 실행하는 SQL 또는 운영 스크립트를
   변경합니다.
4. `machcli.h`와 `MachCLI*()`를 사용하는 C/C++ 애플리케이션을 Machbase SQLCLI 또는
   ODBC로 이전합니다. SQLCLI와 ODBC는 서로 다른 API 집합입니다.
5. WebAdmin/MWA에 의존하는 운영 절차와 대시보드는 명령행 도구 또는 별도 애플리케이션으로
   전환합니다.

제거 항목 전체와 유지 기능은
버전 및 호환성을
참고하십시오.

## 업그레이드 경로

| 에디션 | 방식 | 링크 |
|--------|------|------|
| Standard Edition | 서버 종료 후 패키지 교체 | Standard Edition 업그레이드 |
| Cluster Edition | Broker/Warehouse 순차 업그레이드 | 온라인 업그레이드 |
| Cluster Edition | 전체 중지 | 전체 중지 업그레이드 |

Cluster Edition의 경우 데이터 가용성 요구사항에 따라 온라인 또는 전체 중지 방식을 선택합니다.

---

## Standard Edition 업그레이드

서버를 종료하고 패키지를 교체한 후 재시작합니다. 물리 DB 파일을 그대로 여는 것이
지원되는 버전 간 경로에만 이 절차를 적용합니다. 데이터 변환이나 export/import가 필요한
경로는 해당 릴리스의 마이그레이션 절차를 먼저 수행합니다.

### 업그레이드 전 준비

1. **백업 수행**: 지원되는 BACKUP 명령으로 백업을 만들고 별도 환경에서 복원 여부를
   확인합니다. 실행 중인 데이터 디렉터리의 단순 복사만으로 복구 가능한 백업을 확보했다고
   판단하지 마십시오.

2. **클라이언트 연결 종료**: 진행 중인 Append 또는 INSERT 작업을 모두 완료합니다.

3. **현재 버전 확인**:
   ```bash
   machbased -v
   ```

### 업그레이드 절차

#### 1. 서버 종료

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### 2. 기존 패키지와 설정 보관

실행 파일과 라이브러리뿐 아니라 현재 설정과 라이선스도 별도 위치에 보관합니다.
아래 경로에 이전 백업이 없는지 확인한 뒤 실행합니다.

```bash
cp -a "$MACHBASE_HOME/bin" "$MACHBASE_HOME/bin.bak"
cp -a "$MACHBASE_HOME/lib" "$MACHBASE_HOME/lib.bak"
cp -a "$MACHBASE_HOME/conf" "$MACHBASE_HOME/conf.bak"
```

**데이터 디렉터리(`dbs/`)와 별도로 지정한 `DBS_PATH`는 보존합니다.** 위 복사는 실행 파일과
설정의 보관이며 DB 백업을 대체하지 않습니다. 새 버전이 데이터를 변경한 뒤에는 이전
실행 파일만 되돌려 복구할 수 있다고 가정하지 말고, 검증한 백업 복원 경로를 사용합니다.

#### 3. 새 패키지 압축 해제

새 패키지는 별도 작업 디렉터리에 해제하여 구성과 설정 변경 사항을 먼저 확인합니다.

```bash
upgrade_stage=$(mktemp -d)
tar zxf machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz -C "$upgrade_stage"
```

압축 해제만으로 기존 설치의 실행 파일이 바뀌지는 않습니다. 다음은 `bin/`, `lib/`,
`include/`를 포함하는 Standard tarball에서 실행 파일·라이브러리·헤더를 반영하는 예입니다.
먼저 서버가 종료되었는지 확인하고, 명령이 실패하면 다음 시작 단계로 넘어가지 않습니다.

```bash
(
  set -e
  test -n "$MACHBASE_HOME"
  test -x "$upgrade_stage/bin/machbased"
  test -d "$upgrade_stage/lib"
  test -d "$upgrade_stage/include"
  test -d "$MACHBASE_HOME/bin"
  test -d "$MACHBASE_HOME/lib"
  test -d "$MACHBASE_HOME/include"
  cp -a "$upgrade_stage/bin/." "$MACHBASE_HOME/bin/"
  cp -a "$upgrade_stage/lib/." "$MACHBASE_HOME/lib/"
  cp -a "$upgrade_stage/include/." "$MACHBASE_HOME/include/"
  "$MACHBASE_HOME/bin/machbased" -v
)
```

기존 `conf/machbase.conf`, 라이선스와 실제 `DBS_PATH`의 데이터는 보존하고 새 설정 항목은
기존 설정에 병합합니다. 복사는 같은 이름의 배포 파일을 교체하며 이전 버전에서만 있던
파일을 자동 삭제하지 않습니다. SDK나 플러그인은 새 버전에 맞는 파일을 명시적으로 선택하고,
추가 교체 대상과 제거 항목은 릴리스 안내를 확인합니다. 출력된 바이너리 버전과 설정 검토가
완료된 뒤에만 서버를 시작합니다.

#### 4. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

#### 5. 버전 확인

```bash
machbased -v

# 서버 접속
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT EDITION, BINARY_DB_MAJOR_VERSION, BINARY_DB_MINOR_VERSION FROM V$VERSION;
```

### 주의사항

- `dbs/` 디렉터리를 절대 삭제하거나 초기화(`machadmin -d`)하지 마십시오.
- Minor 버전 간 업그레이드는 DB 파일 마이그레이션이 필요할 수 있습니다. 릴리스 노트를 반드시 확인하십시오.
- Windows 환경에서는 새 패키지 또는 설치 실행 파일을 적용하기 전에 Machbase 서비스를 중지합니다.

---

## Cluster Edition 업그레이드

서비스 중단 여부에 따라 두 가지 방식을 선택합니다.

| 방식 | 서비스 중단 | 적합한 상황 |
|------|-----------|------------|
| 온라인 업그레이드 | Broker/Warehouse 순차 재기동 | Broker와 Warehouse만 교체하는 운영 환경 |
| 전체 중지 업그레이드 | 있음 | 유지보수 창이 허용되는 경우, Major 버전 변경 |

### 업그레이드 전 공통 주의사항

- 업그레이드 중에는 DDL 또는 DELETE를 실행하지 마십시오.
- 업그레이드 중 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- 온라인 업그레이드는 Broker와 Warehouse를 대상으로 합니다. Coordinator, Deployer, Lookup까지 교체하려면 전체 중지 업그레이드를 사용합니다.
- 업그레이드 전 백업을 권장합니다.

---

### 온라인 업그레이드

실행 중인 클러스터에서 Broker와 Warehouse를 순차적으로 업그레이드합니다. Coordinator, Deployer, Lookup까지 포함한 전체 바이너리 교체가 필요하면 전체 중지 업그레이드를 사용합니다.

#### 업그레이드 절차

##### 1. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 패키지 내용이
바뀌면 패키지 이름과 압축 파일 이름도 함께 고유하게 바꿉니다.

```yaml
cluster:
  package:
    name: machbase-v8.7.0
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

`registered_path`는 `machclusterctl export`가 기록하는 Coordinator 패키지 저장소 경로입니다.
업그레이드할 압축 파일을 지정할 때는 `origin_path`를 사용합니다.

##### 2. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

##### 3. 온라인 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`--online`을 생략해도 온라인 모드로 처리되지만, 운영 절차를 명확히 하기 위해 옵션을 명시하는 것을 권장합니다.

##### 4. 전체 상태 확인

```bash
machclusterctl status
```

#### 수동 업그레이드 참고

`machcoordinatoradmin --upgrade-node`를 직접 사용하는 경우에는 대상 노드와 패키지 이름을 함께 지정합니다.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
```

온라인 대상은 Broker와 Warehouse로 제한합니다. Broker가 하나만 남아 있을 때 해당 Broker를 업그레이드하면 그 시간 동안 클라이언트 접속이 끊길 수 있습니다.

온라인 모드는 전체 클러스터 중지를 생략하는 방식이며 무중단을 보장하는 HA-aware rolling
upgrade는 아닙니다. Warehouse 그룹이 일시적으로 읽기 전용이 될 수 있으므로 애플리케이션의
재접속·재시도와 쓰기 지연을 검증해야 합니다. 프로토콜 호환성이 달라지거나 모든 역할의
바이너리를 맞춰야 한다면 전체 중지 방식을 사용합니다.

모든 대상 노드의 역할 상태와 버전을 확인한 뒤 대표 조회·입력과 복제 상태까지 검증합니다.

---

### 전체 중지 업그레이드

클러스터를 완전히 종료한 후 모든 노드를 일괄 업그레이드합니다. Coordinator, Deployer, Lookup까지 포함해 전체 바이너리를 교체해야 하거나 DB 파일 형식 변경이 수반되는 경우에 사용합니다.

#### 업그레이드 절차

##### 1. 클라이언트 연결 종료

모든 INSERT·APPEND·SELECT 작업이 완료되었는지 확인합니다.

##### 2. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 업그레이드 전에는 노드 추가, 삭제, 포트 변경 같은 토폴로지 변경이 없어야 합니다. 토폴로지 변경이 있으면 먼저 `apply`로 반영한 뒤 업그레이드를 수행합니다.

`machclusterctl upgrade --full-stop`은 Coordinator와 Deployer를 포함한 모든 노드 홈에
같은 패키지를 교체 반영합니다. 따라서 `origin_path`에는 `machcoordinatoradmin`과
`machdeployeradmin`이 포함된 전체 Cluster 패키지를 지정합니다.

##### 3. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run --verbose
```

##### 4. 전체 중지 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

`machclusterctl`은 전체 클러스터 중단을 전제로 패키지를 임시 준비 경로에 해제한 뒤
노드 홈에 교체 반영합니다.

#### 수동 배포 참고

수동 배포 환경에서 직접 교체해야 하는 경우, Coordinator에 새 패키지를 등록합니다.

```bash
machcoordinatoradmin --add-package=machbase-v8.7.0 \
  --file-name=/home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

Warehouse → Broker → Lookup → Deployer → Coordinator 순으로 종료합니다.

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machcoordinatoradmin --shutdown-node=192.168.1.10:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

각 노드 홈을 새 패키지로 교체할 때는 기존 `conf/machbase.conf`, `dbs/`, `meta/`, `package/`
디렉터리를 보존합니다. 별도 작업 경로에 새 패키지를 해제한 뒤 보존 대상 경로를 제외하고
교체합니다.

Coordinator → Deployer → Lookup → Broker → Warehouse 순으로 시작합니다.

```bash
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.10:5301
machcoordinatoradmin --startup-node=192.168.1.11:5401
machcoordinatoradmin --startup-node=192.168.1.13:5501
machcoordinatoradmin --startup-node=192.168.1.14:5501
```

재시작 후 Broker와 Warehouse의 패키지 메타데이터를 새 패키지 이름으로 동기화합니다.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.13:5501 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.14:5501 --package-name=machbase-v8.7.0
```

##### 5. 상태 확인

```bash
machclusterctl status
```

노드 상태뿐 아니라 Broker 접속, 대표 데이터 조회·입력, 복제, 라이선스와 설정값을 확인한
뒤 서비스를 재개합니다. 설치 검증 결과를 변경 전 기록과
비교하고, 검증이 끝날 때까지 이전 패키지·설정과 백업을 보존합니다.

#### 주의사항

- Major 버전 업그레이드는 DB 파일 형식이 변경될 수 있습니다. 릴리스 노트를 반드시 확인하고, 업그레이드 전 백업을 수행하십시오.
- `conf/machbase.conf`, `dbs/`, `meta/`, `package/` 경로를 절대 삭제하거나 초기화하지 마십시오.
