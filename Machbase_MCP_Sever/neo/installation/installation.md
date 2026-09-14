# Machbase Neo Installation & Getting Started Guide

## 플랫폼 및 아키텍처 지원

- **Raspberry Pi**: Raspberry Pi 4 + Ubuntu 22.04
- **Linux arm64**: Ubuntu 22.04, 24.04
- **Linux amd64**: Ubuntu 20.04, 22.04, 24.04
- **macOS**: Intel CPU(macOS 13), Apple Silicon(macOS 14, 15)
- **Windows**: Windows 10 Fall 2018 이상, Windows 11

## 직접 설치

### 설정 절차

1. **다운로드(권장)**
   
   한 줄 설치 스크립트:
   ```bash
   sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
   ```
   
   또는 https://docs.machbase.com/neo/releases/ 에서 플랫폼에 맞는 최신 버전을 내려받습니다.

2. **압축 해제**
   ```bash
   unzip machbase-neo-v8.5.9-linux-amd64.zip
   ```
   
   **By platform:**
   ```bash
   # Linux ARM64
   unzip machbase-neo-v8.5.9-linux-arm64.zip
   
   # macOS Apple Silicon
   unzip machbase-neo-v8.5.9-darwin-arm64.zip
   
   # macOS Intel
   unzip machbase-neo-v8.5.9-darwin-amd64.zip
   
   # Windows
   unzip machbase-neo-v8.5.9-windows-amd64.zip
   ```

3. **실행 파일 확인**
   ```bash
   machbase-neo version
   ```

## Docker 설치

### 사전 준비
- Docker

### Docker Pull

Docker로 최신 버전 machbase-neo를 설치하려면 터미널에 다음 명령을 입력합니다:

```bash
$ docker pull machbase/machbase-neo
```

특정 버전을 원하면 태그를 붙입니다:

```bash
$ docker pull machbase/machbase-neo:v8.5.9
```

> **참고**: 다른 Docker 버전은 https://hub.docker.com/r/machbase/machbase-neo/ 에서 확인하세요.

### Docker Run

#### 포그라운드 실행
```bash
$ docker run -it machbase/machbase-neo
```

**Options:**
- `-i`, `--interactive`: STDIN을 열어 둠
- `-t`, `--tty`: 의사 TTY 할당

포그라운드로 실행 중이라면 `Ctrl + c`로 바로 종료할 수 있습니다.

#### 백그라운드 실행
```bash
$ docker run -d machbase/machbase-neo
```

**Options:**
- `-d`, `--detach`: 컨테이너를 백그라운드로 실행하고 컨테이너 ID를 출력

백그라운드로 실행 중이라면 다음 명령으로 종료할 수 있습니다:

```bash
$ docker stop $(docker ps | grep machbase-neo | awk '{print $1}')
```

여러 machbase-neo 이미지를 사용 중이라면 Container ID를 직접 지정해 정지하는 것을 권장합니다:

```bash
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                   CREATED         STATUS        PORTS           NAMES
92382cf7b738   machbase/machbase-neo   "/bin/sh -c '/opt/ma…"   2 seconds ago   Up 1 second   5652-5656/tcp   exciting_volhard

$ docker stop 92382cf7b738
```

### Docker 설정

#### 볼륨 바인딩
호스트 디렉토리를 도커 안의 machbase-neo 홈 경로에 바인딩할 수 있습니다:

```bash
docker run -d \
           -v /path/to/host/data:/data \
           -v /path/to/host/file:/file \
           machbase/machbase-neo
```

**Paths:**
- `/data`: 도커 안의 machbase-neo 홈 경로
- `/file`: 도커 안의 machbase-neo tql 경로
- `-v`, `--volume`: 볼륨을 바인드 마운트

#### 포트 설정
machbase-neo는 Docker에서 여러 포트를 노출합니다:

| 포트 | 설명 |
|:-----|:------------|
| 5652 | sshd |
| 5653 | mqtt |
| 5654 | http |
| 5656 | 데이터베이스 엔진 |

#### 포트 매핑(포워딩)
```bash
$ docker run -d -p <host port>:<container port>/<protocol> machbase/machbase-neo
```

**Example:**
```bash
$ docker run -d \
             -p 5652-5652:5652-5656/tcp \
             --name machbase-neo \
             machbase/machbase-neo
```

#### SSH 키를 사용한 원격 접속

1. **SSH 키 생성:**
   ```bash
   $ ssh-keygen -t rsa
   ```

2. **machbase-neo 실행:**
   ```bash
   $ docker pull machbase/machbase-neo
   $ docker run -d \
                -p 5652-5656:5652-5656/tcp \
                --name machbase-neo \
                machbase/machbase-neo
   ```

3. **SSH 키 등록:**
   ```bash
   $ ssh -l sys -p 5652 192.168.0.116 ssh-key add `cat ~/.ssh/id_rsa.pub`
   sys@192.168.0.116's password? manager
   Add sshkey success
   ```

#### Docker Compose 사용

Create `docker-compose.yml` file:

```yml
# docker-compose.yml
version: '3'
services:
  machbase-neo:
    image: machbase/machbase-neo
    container_name: machbase-neo
    hostname: machbase
    volumes:
      - /data:/data
      - /file:/file
    ports:
      - "5652:5652" # sshd
      - "5653:5653" # mqtt
      - "5654:5654" # http
      - "5656:5656" # database engine
```

**Commands:**
```bash
# Start
$ docker compose up -d

# Or specify file
$ docker compose -f docker-compose.yml up -d

# Stop
$ docker compose down
```

## 시작과 정지

### Linux & macOS

#### Start
```bash
machbase-neo serve
```

#### 포트 노출
machbase-neo는 보안상 기본적으로 localhost에서만 동작합니다. 원격 클라이언트 접속을 허용하려면:

**모든 주소에서 접속 허용:**
```bash
machbase-neo serve --host 0.0.0.0
```

**특정 주소만 허용:**
```bash
machbase-neo serve --host 192.168.1.10
```

#### Stop
포그라운드 모드로 실행 중이라면 `Ctrl+C`를 누릅니다.

또는 shutdown 명령을 사용합니다:
```bash
machbase-neo shell shutdown
```

### Windows

Windows에서는 "neow.exe"를 더블 클릭한 뒤 창 좌측 상단의 "machbase-neo serve" 버튼을 누릅니다.

#### Windows 서비스 등록

> **중요**: 관리자 모드에서 실행해야 합니다.

**Install:**
```
.\machbase-neo service install --host 127.0.0.1 --data C:\neo-server\database --file C:\neo-server\files --log-filename C:\neo-server\machbase-neo.log --log-level INFO
```

**Start/Stop:**
```
.\machbase-neo service start
.\machbase-neo service stop
```

**Remove:**
```
.\machbase-neo service remove
```

## 배포 모드

### Head Only 모드

`--data` 플래그 값으로 다른 Machbase DBMS의 mach 포트를 가리키는 URL을 사용합니다:

```bash
machbase-neo serve --data machbase://sys:manager@192.168.1.100:5656
```

또는 환경 변수를 사용합니다:
```bash
SECRET="sys:manager" \
machbase-neo serve --data machbase://${SECRET}@192.168.1.100:5656
```

### Headless 모드

DBMS 프로세스만 시작합니다(mach 포트 5656만 사용):

```bash
machbase-neo serve-headless
```

## 웹 UI 접속

### Login

웹 브라우저에서 http://127.0.0.1:5654/ 로 접속합니다.

**기본 계정:** ID `sys`, 비밀번호 `manager`

### 비밀번호 변경

보안을 위해 기본 비밀번호를 변경하는 것을 권장합니다.

#### Via Web UI:
1. 좌측 하단 메뉴에서 "Change password"를 선택합니다
2. 새 비밀번호를 입력하고 확인합니다

#### Via SQL:
```sql
ALTER USER sys IDENTIFIED BY new_password;
```

#### 명령행으로:
```bash
machbase-neo shell "ALTER USER SYS IDENTIFIED BY new_password"
```

## 빠른 참조

| 방식 | 명령/동작 | 설명 |
|--------|----------------|-------------|
| **직접 설치** | `curl install.sh` 스크립트 | 권장하는 한 줄 설치 |
| **Docker 설치** | `docker pull machbase/machbase-neo` | 컨테이너 기반 설치 |
| **서비스 시작** | `machbase-neo serve` | localhost에서만 시작 |
| **원격 접속** | `--host 0.0.0.0` | 원격 연결 허용 |
| **웹 UI** | http://127.0.0.1:5654 | 기본 웹 인터페이스 |
| **기본 로그인** | sys/manager | 최초 로그인 후 비밀번호 변경 |
