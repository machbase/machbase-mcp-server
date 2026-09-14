# Standard Edition 설치

Standard Edition은 한 서버에서 SQL 처리와 데이터 저장을 수행합니다. 설치는 패키지 준비,
서버 실행 환경 설정, 데이터베이스 생성, 라이선스 확인, 시작과 SQL 검증 순서로 진행합니다.
단일 서버라고 해서 소량 데이터만 다루는 것은 아니며, 처리량과 보관 기간에 필요한 자원을
실제 워크로드로 확인해야 합니다.

## 설치 경로

운영체제에 따라 아래 경로 중 하나를 선택합니다.

| OS | 설치 방식 | 링크 |
|----|-----------|------|
| Linux | Tarball (.tgz) | Tarball 설치 |
| Linux | Docker 컨테이너 | Docker 설치 |
| Windows | ZIP 또는 설치 실행 파일 | Windows 패키지 설치 |

설치 전에 Linux 환경 준비 또는 Windows 환경 준비를 먼저 확인하십시오.

---

## Linux 설치

Linux에서 Standard Edition을 설치하는 방법은 두 가지입니다.

| 방식 | 적합한 상황 |
|------|------------|
| Tarball 설치 | 실제 서버 환경, 데이터 디렉터리를 직접 관리해야 하는 경우 |
| Docker 설치 | 개발·테스트 환경, 빠른 구동이 필요한 경우 |

Tarball 설치는 설치 전 준비를 먼저 완료해야 합니다. Docker
설치는 Docker Engine과 볼륨·포트 권한을 준비하십시오.

---

### Linux 환경 준비

파일 디스크립터 한도, 시간 동기화, 포트 예약과 방화벽 설정은 Edition 공통 작업입니다.
설치 전 준비에서 서버를 실행할 계정과 운영 환경에 맞게
설정한 뒤 다음 설치 절차를 진행합니다.

---

### Tarball 설치

Linux 환경에 tarball(.tgz)을 압축 해제하여 Standard Edition을 설치하는 절차입니다.

#### 1. 사용자 생성

Machbase 전용 OS 사용자를 생성합니다.

```bash
sudo useradd -m -d /home/machbase machbase
sudo passwd machbase
```

이후 `machbase` 계정으로 로그인하여 작업합니다.

#### 2. 패키지 다운로드 및 압축 해제

예제에서는 패키지를 `/home/machbase/packages/`에 다운로드한 것으로 가정합니다.
아래 패키지 이름을 실제 배포본으로 바꾸고, 아직 인스턴스가 없는 새 설치 디렉터리에
압축을 해제합니다. 기존 설치의 갱신은 업그레이드 절차를 사용합니다.

```bash
machbase_package=/home/machbase/packages/machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz
test -r "$machbase_package" &&
mkdir /home/machbase/machbase_home &&
tar zxf "$machbase_package" -C /home/machbase/machbase_home &&
cd /home/machbase/machbase_home
```

압축 해제 후 디렉터리 구조를 확인합니다.

```bash
ls -l
# bin/  conf/  dbs/  doc/  include/  lib/  trc/  ...
```

#### 3. 환경 변수 설정

`~/.bashrc`에 환경 변수를 추가합니다.

```bash
export MACHBASE_HOME=/home/machbase/machbase_home
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

적용합니다.

```bash
source ~/.bashrc
```

#### 4. 데이터베이스 생성

`machadmin -c`는 물리 인스턴스의 데이터베이스 파일을 생성합니다. SQL의
`CREATE DATABASE`로 논리 데이터베이스를 추가하는 작업과 구분하십시오. 실행 전에
`MACHBASE_HOME`, `conf/machbase.conf`와 실제 `DBS_PATH`가 새 설치 대상인지 확인합니다.
기존 데이터베이스가 있다는 오류가 나면 삭제·재생성하지 말고 대상 경로부터 확인합니다.

```bash
machadmin -c
# Database created successfully.
```

#### 서버 시작 전 설정과 라이선스 확인

`conf/machbase.conf`에서 `PORT_NO`와 `DBS_PATH`를 확인합니다. 별도 라이선스를 사용하는
경우 라이선스 설치의 파일 복사 또는
`machadmin -t` 방법으로 설치하고 `machadmin -f`로 확인한 뒤 시작합니다.

#### 5. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

프로세스 확인:

```bash
machadmin -e
```

#### 6. 접속 테스트

`machsql`로 서버에 접속합니다. 기본 관리자 계정은 `SYS / MANAGER`입니다.

```bash
machsql
# Machbase server address (Default:127.0.0.1) :
# Machbase user ID  (Default:SYS)
# Machbase User Password :
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

간단한 테스트를 수행합니다.

```sql
CREATE LOG TABLE install_check (id INTEGER, val DOUBLE);
INSERT INTO install_check (id, val) VALUES (1, 3.14);
SELECT id, val FROM install_check;
DROP TABLE install_check;
```

`id=1`, `val=3.14` 한 행이 반환되고 마지막 DROP이 성공하는지 확인합니다.
`install_check`가 이미 있으면 기존 객체를 삭제하지 말고 사용하지 않는 실습 이름으로 바꿉니다.

#### 서버 종료

설치 확인이 끝난 뒤 서버를 중지해야 할 때만 실행합니다.

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### 포트 변경

기본 포트(5656)를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO`를 수정하거나 환경 변수를 설정합니다.

```bash
export MACHBASE_PORT_NO=7878
```

서버를 종료한 상태에서 설정을 적용하고 다시 시작합니다. 이 환경 변수는 현재 셸에만
적용되므로 서비스로 시작한다면 서비스의 환경에도 반영합니다. 접속에는
`machsql -s 127.0.0.1 -P 7878 -u SYS`처럼 바뀐 포트를 지정합니다.

---

### Docker 설치

Docker 이미지를 사용하면 서버와 실행 환경을 컨테이너로 배포할 수 있습니다. 개발·테스트
환경에서도 호스트의 Docker Engine, 저장 볼륨, 포트와 파일 디스크립터 한도를 준비해야 합니다.

Docker가 사전에 설치되어 있어야 합니다. 배포 튜토리얼은 `machbase/machbase` 이미지를 사용합니다. 소스에서 Docker 이미지를 직접 빌드한 경우에는 로컬 이미지 이름(`machbase:latest` 등)으로 바꾸십시오.

#### 이미지 확인

```bash
docker pull machbase/machbase
docker image ls machbase/machbase
```

#### 컨테이너 실행

```bash
docker create \
  --name machbase \
  --ulimit nofile=65535 \
  -p 5656:5656 \
  -v /data/machbase:/home/machbase/machbase/dbs \
  machbase/machbase
```

| 옵션 | 설명 |
|------|------|
| `-p 5656:5656` | 호스트 SQL 포트:컨테이너 SQL 포트 매핑 |
| `--ulimit nofile=65535` | 컨테이너 안에서 서버가 사용할 파일 디스크립터 한도 |
| `-v /data/machbase:...` | 데이터 디렉터리를 호스트에 보존하는 볼륨 마운트 |

데이터가 컨테이너의 쓰기 계층에만 있으면 컨테이너 삭제 시 함께 제거됩니다. 실제 데이터
경로가 볼륨에 연결되었는지 확인하고, 볼륨 자체의 삭제나 디스크 장애에 대비한 백업도 준비합니다.

`docker create`는 아직 서버를 시작하지 않습니다. `/data/machbase`는 컨테이너의 서버
실행 계정이 쓸 수 있어야 하며, 기존 DB 파일이 있으면 버전과 인스턴스가 맞는지 확인합니다.
이미지의 실제 버전과 `MACHBASE_HOME` 경로를 확인한 뒤 운영에서는 검증한 이미지 태그나
digest를 고정합니다. 태그 없는 공개 이미지가 항상 8.7.0이라고 가정하지 마십시오.

별도 라이선스를 사용하는 경우 시작 전에 다음처럼 준비한 파일을 복사합니다.

```bash
docker cp /path/to/license.dat machbase:/home/machbase/machbase/conf/license.dat
```

준비가 끝나면 컨테이너를 시작합니다.

```bash
docker start machbase
```

#### 컨테이너 상태 확인

```bash
docker ps
docker logs machbase
```

#### 접속 테스트

##### machsql (컨테이너 내부)

```bash
docker exec -it machbase machsql
# Mach>
```

##### 호스트에서 접속

호스트에 machsql이 설치된 경우:

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

#### 컨테이너 종료 및 재시작

```bash
docker stop machbase
docker start machbase
```

#### 라이선스 설치

실행 중 라이선스를 갱신할 때는 컨테이너에 파일을 복사한 뒤 라이선스 설치 명령을
실행합니다. 컨테이너의 설정 파일과 라이선스는 데이터 볼륨과 별개이므로 컨테이너를
재생성할 때도 다시 적용할 수 있도록 원본을 보관합니다.

```bash
docker cp /path/to/license.dat machbase:/tmp/license.dat
docker exec machbase machadmin -t /tmp/license.dat
docker exec machbase machadmin -f
```

---

## Windows 설치

### 설치 전 확인

- **지원 OS**: 제공받은 Windows 패키지의 릴리스 정보에서 지원 버전을 확인합니다.
- **아키텍처**: 배포 패키지의 비트 수와 운영체제 아키텍처가 일치해야 합니다.

설치 전에 Windows 환경 준비를 먼저 완료하십시오.

### 설치 방식

| 방식 | 설명 |
|------|------|
| Windows 패키지 설치 | 설치 마법사를 통한 설치. 환경 변수와 바로가기 생성 |

---

### Windows 환경 준비

Windows에 설치하기 전에 방화벽 설정을 확인합니다.

#### 방화벽 포트 열기

Machbase가 사용하는 포트를 Windows 방화벽 인바운드 규칙에 추가합니다.

| 포트 | 프로토콜 | 용도 |
|------|---------|------|
| 5656 | TCP | SQL 클라이언트 접속 |

##### 설정 방법

1. **제어판 → Windows Defender 방화벽 → 고급 설정**을 엽니다.

2. 왼쪽 패널에서 **인바운드 규칙**을 선택하고, 오른쪽 패널에서 **새 규칙**을 클릭합니다.

3. 규칙 유형으로 **포트**를 선택하고 **다음**을 클릭합니다.

4. **TCP**를 선택하고, **특정 로컬 포트** 필드에 `5656`을 입력한 후 **다음**을 클릭합니다.

5. **연결 허용**을 선택하고 **다음**을 클릭합니다.

6. 접속을 허용할 네트워크의 프로필(**도메인**, **개인**, **공용**)만 선택하고 **다음**을 클릭합니다.

7. 규칙 이름(예: `Machbase`)을 입력하고 **마침**을 클릭합니다.

규칙을 만든 뒤 속성의 원격 주소 범위도 실제 클라이언트 주소로 제한합니다.
원격 접속을 사용하지 않는 환경에서는 인바운드 허용 규칙을 만들 필요가 없습니다.

##### PowerShell로 설정 (관리자 권한)

GUI 대신 PowerShell로 빠르게 설정합니다.

```powershell
New-NetFirewallRule -DisplayName "Machbase SQL" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
```

#### Visual C++ 재배포 패키지

실행에 Visual C++ Redistributable이 필요합니다. 설치 실행 파일을 사용하는 경우 자동으로 처리될 수 있지만, 문제가 발생하면 Microsoft 공식 사이트에서 최신 버전을 수동으로 설치하십시오.

---

### Windows 패키지 설치

Windows 버전은 ZIP 패키지 또는 설치 실행 파일로 제공됩니다. ZIP 패키지는 압축 파일 루트에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 포함하며, 설치 실행 파일은 설치 경로 아래에 `machbase_home\`을 만들고 환경 변수와 실행 바로가기를 생성합니다.

#### 설치 절차

1. Windows 배포 패키지를 다운로드합니다.

2. ZIP 패키지를 사용하는 경우 원하는 설치 디렉터리에 압축을 해제합니다.

   ```cmd
   mkdir C:\machbase
   tar -xf machbase-SDK-8.7.0.official-WINDOWS-X86-64-release.zip -C C:\machbase
   ```

3. 설치 실행 파일이 제공된 경우 파일을 실행합니다. 설치 시작 화면이 표시되면 **Next**를 클릭합니다.

4. 설치 경로를 선택합니다. 기본값은 `C:\machbase-<short_version>\` 형식입니다. 변경이 필요하면 경로를 수정한 후 **Next**를 클릭합니다.

5. 설치가 진행됩니다. 완료되면 **Next** → **Close**를 클릭합니다.

#### ZIP 패키지 초기화

ZIP을 해제했다면 명령 프롬프트에서 해당 디렉터리를 설치 홈으로 지정합니다. 다음은
`C:\machbase`에 새로 설치한 예제입니다. 실제 설정 파일과 라이선스를 먼저 확인하고,
기존 DB가 없는 새 인스턴스에서만 `-c`를 실행합니다.

```cmd
set "MACHBASE_HOME=C:\machbase"
set "PATH=%MACHBASE_HOME%\bin;%PATH%"
machadmin.exe -c
machadmin.exe -f
machadmin.exe -u
machadmin.exe -e
```

위 `set` 명령은 현재 창에 적용됩니다. 이후 다른 창이나 서비스에서 실행할 때도 같은
설치 홈과 실행 파일 경로를 사용해야 합니다. 설치 실행 파일이 이미 데이터베이스를
만들었다면 ZIP용 생성 명령을 반복하지 마십시오.

#### 서버 시작과 종료

설치 실행 파일을 사용한 경우 바탕화면과 시작 메뉴에 바로가기가 생성됩니다.

- **start Machbase**: `machadmin.exe -u`를 실행해 서버를 시작합니다.
- **stop Machbase**: `machadmin.exe -s`를 실행해 서버를 종료합니다.
- **machsql**: SQL 콘솔을 실행합니다.

#### 명령줄 접속

설치 후 명령 프롬프트에서 `machsql`을 실행하여 서버에 접속합니다. 설치 실행 파일을 사용한 경우 `<설치 경로>\machbase_home\bin`이 시스템 `PATH`에 추가됩니다. ZIP 패키지를 사용한 경우 압축을 해제한 디렉터리의 `bin\`을 `PATH`에 추가하거나 전체 경로로 실행합니다.

```cmd
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

기본 관리자 계정: `SYS` / `MANAGER`

#### 설치 경로 구조

ZIP 패키지는 압축 해제 경로 바로 아래에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 배치합니다.
설치 실행 파일은 설치 경로 아래의 `machbase_home\`에 같은 구성을 생성합니다.
패키지 구성 참고.
