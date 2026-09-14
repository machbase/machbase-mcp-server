# machadmin 명령/옵션 사전

`machadmin`은 Machbase 서버를 시작하거나 종료하고 데이터베이스 생성, 삭제 및 실행 상태를 확인하는 관리 도구입니다.

## 옵션 목록

```bash
machadmin -h
```

| 옵션 | 설명 |
|------|------|
| `-u`, `--startup` | Machbase 서버 시작 |
| `--recovery[=simple,complex,reset]` | 시작 시 복구 모드 지정 (기본값: simple) |
| `-s`, `--shutdown` | Machbase 서버 정상 종료 (graceful) |
| `-k`, `--kill` | Machbase 서버 강제 종료 |
| `-c`, `--createdb` | Machbase 데이터베이스 생성 |
| `-d`, `--destroydb` | Machbase 데이터베이스 삭제 |
| `-e`, `--check` | 서버 실행 상태 확인 |
| `-i`, `--silent` | 배너 출력 없이 실행 |
| `-r`, `--restore` | 백업에서 데이터베이스 복구 |
| `-x`, `--extract` | 백업 파일을 백업 디렉토리로 변환 |
| `-w`, `--viewimage` | 백업 이미지 파일 정보 출력 |
| `-t`, `--licinstall` | 라이선스 파일 설치 |
| `-f`, `--licinfo` | 설치된 라이선스 정보 출력 |
| `--home-path=path` | Machbase 홈 경로 지정 |

## 서버 시작

```bash
machadmin -u
```

### 복구 모드 지정

```bash
machadmin -u --recovery=simple    # 기본 복구 (전원 정상 종료 후)
machadmin -u --recovery=complex   # 전원 손실 후 재시작 시 자동 적용
machadmin -u --recovery=reset     # simple/complex 복구 실패 시 전체 검사
```

| 복구 모드 | 설명 |
|----------|------|
| `simple` | 정상 종료 후 재시작 시 기본 복구. 실행 시간이 짧음 |
| `complex` | 전원 손실 등 비정상 종료 후 재시작 시 자동 적용. `simple`보다 오래 걸림 |
| `reset` | 모든 테이블 데이터를 전체 검사하여 복구. 일부 데이터 손실 가능 |

## 서버 종료

정상 종료 (진행 중인 작업 완료 후 종료):

```bash
machadmin -s
```

강제 종료 (즉시 프로세스 종료):

```bash
machadmin -k
```

## 데이터베이스 생성 및 삭제

```bash
# 데이터베이스 생성
machadmin -c

# 데이터베이스 삭제 (확인 프롬프트 표시)
machadmin -d
```

## 서버 실행 상태 확인

```bash
machadmin -e
```

서버가 실행 중이면 PID를 출력합니다.

```
Machbase server is already running with PID (14098).
```

서버가 실행 중이 아니면 오류를 출력합니다.

```
[ERR] Server is not running.
```

## 데이터베이스 복구

백업 디렉토리에서 데이터베이스를 복구합니다.

```bash
machadmin -r /path/to/backup
```

예시:

```bash
machadmin -r /home/mach/backup/machbase_backup_20240101
```

## 라이선스 관리

라이선스 파일 설치:

```bash
machadmin -t /path/to/license.dat
```

설치된 라이선스 정보 확인:

```bash
machadmin -f
```

## 무음 모드

배너와 상태 메시지 없이 실행합니다. 스크립트에서 활용하기 좋습니다.

```bash
machadmin -i -u    # 서버 시작 (배너 없이)
machadmin -i -s    # 서버 종료 (배너 없이)
machadmin -i -e    # 상태 확인 (배너 없이)
```

## 사용 예시

```bash
# 데이터베이스 초기 설정 및 서버 시작
machadmin -c
machadmin -u

# 서버 상태 확인 후 종료
machadmin -e
machadmin -s

# 라이선스 갱신
machadmin -s
machadmin -t new_license.dat
machadmin -u
```
