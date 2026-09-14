# 명령행 도구 레퍼런스

Machbase는 서버 관리, 데이터 가져오기/내보내기, 쿼리 실행을 위한 다양한 명령행 도구를 제공합니다. 이 섹션은 각 도구의 옵션과 사용법을 빠르게 찾아볼 수 있는 레퍼런스입니다.

## 도구 목록

| 도구 | 에디션 | 설명 |
|------|--------|------|
| machadmin | Standard / Cluster | 서버 시작/종료, 데이터베이스 생성/삭제, 라이선스 관리 |
| machsql | Standard / Cluster | 대화형 SQL 터미널 도구 |
| machloader | Standard / Cluster | CSV 등 텍스트 파일 가져오기/내보내기 |
| csvimport / csvexport | Standard / Cluster | CSV 파일 전용 간편 가져오기/내보내기 래퍼 |
| tagmetaimport | Standard / Cluster | TAG 테이블 메타데이터 일괄 가져오기 |
| machclusterctl | Cluster | 클러스터 전체 시작/종료/관리 도구 |
| machcoordinatoradmin | Cluster | Coordinator 노드 관리 및 클러스터 구성 도구 |
| machdeployeradmin | Cluster | Deployer 노드 관리 도구 |

## 공통 접속 옵션

다음은 `machsql`의 접속 옵션입니다. 도구마다 옵션 이름과 기본값이 다르므로 다른 도구를
사용할 때는 해당 도구의 옵션 사전이나 `--help` 출력을 확인하십시오. 특히 서버를 직접
관리하는 `machadmin`의 옵션을 SQL 클라이언트의 접속 옵션과 혼동하지 마십시오.

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `-s`, `--server` | 127.0.0.1 | 서버 IP 주소 |
| `-P`, `--port` | 5656 | 서버 포트 번호 |
| `-u`, `--user` | SYS | 사용자 이름 |
| `-p`, `--password` | MANAGER | 사용자 비밀번호 |

## 도구 위치

설치 패키지에 포함된 도구는 `$MACHBASE_HOME/bin/` 디렉터리에서 확인합니다.
사용 가능한 도구는 설치한 Edition과 패키지에 따라 다릅니다.

```bash
ls $MACHBASE_HOME/bin/
# machadmin  machsql  machloader  csvimport  csvexport  tagmetaimport  ...
```

PATH에 `$MACHBASE_HOME/bin`이 등록되어 있으면 도구 이름만으로 실행할 수 있습니다.

```bash
export PATH=$MACHBASE_HOME/bin:$PATH
machadmin -e
```
