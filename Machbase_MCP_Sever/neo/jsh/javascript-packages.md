# Machbase Neo JavaScript Packages

`pkg` 명령은 `package.json`을 관리하고 JSH 패키지를 설치하며 패키지 스크립트를 실행합니다.
`/work` 같은 프로젝트 디렉터리에 의존성을 두는 JSH 애플리케이션을 위한 것입니다.

## 개요

`pkg` 명령은 다음 작업을 지원합니다:

- Create a new `package.json`
- `node_modules`에 의존성 설치
- GitHub 프로젝트를 대상 디렉터리에 복사하고 그 자리에서 프로젝트 의존성 설치
- Maintain `package-lock.json`
- `package.json`의 `scripts`에 정의된 명령 실행
- 설치된 패키지의 `bin` 항목으로 실행 래퍼 생성
- 생성된 래퍼와 함께 의존성 제거

## package.json

`pkg`는 `package.json`을 선택된 패키지 루트의 매니페스트로 취급합니다.
일반 프로젝트 설치에서 그 루트는 현재 디렉터리 또는 `--dir`로 선택한 디렉터리입니다.
`pkg install -g`와 `pkg uninstall -g`에서는 패키지가 `/work/node_modules` 아래에 설치되지만, `pkg`는 `/work/package.json`이나 `/work/package-lock.json`을 만들지 않습니다.

최소한의 프로젝트 매니페스트는 다음과 같습니다.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "#tag=v1.1.0"
  }
}
```

`pkg`가 사용하는 주요 필드는 다음과 같습니다:

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `name` | `String` | 프로젝트 패키지 이름 |
| `version` | `String` | 프로젝트 버전 |
| `scripts` | `Object` | `pkg run`용 이름 붙은 명령 |
| `dependencies` | `Object` | 패키지 이름과 버전 지정자의 매핑 |

## pkg init

현재 프로젝트 디렉터리에 새 `package.json`을 만듭니다.

<h6>문법</h6>

```sh
pkg init [options] <name>
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 주어진 프로젝트 디렉터리를 사용합니다
- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > pkg init demo-app
Created /work/package.json
```

## pkg install

`package.json`의 의존성을 설치하거나, 단일 패키지 요청을 설치하고 둘 다 갱신합니다
`package.json` and `package-lock.json`.

<h6>문법</h6>

```sh
pkg install [options] [name]
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 주어진 프로젝트 디렉터리를 사용합니다
- `-g, --global` 전역 패키지 디렉터리에 설치하고 `--dir`을 무시합니다
- `-h, --help` show help

`name`을 생략하면 `pkg install`은 선택된 프로젝트 매니페스트에 이미 선언된 의존성을 설치합니다.

### 전역 설치

`pkg install -g <name>`은 `/work/node_modules`를 설치 대상으로 사용합니다.

### npm 패키지

패키지 이름이 GitHub 저장소 경로가 아니면 `pkg`는 npm 레지스트리에서 설치합니다.

```sh
/work > pkg install generic-pkg
Installed generic-pkg@1.2.0
```

### GitHub 저장소 패키지

패키지 이름이 `github.com/<org>/<repo>` 형식이면 `pkg`는 GitHub에서 저장소 내용을 직접 설치합니다.

지원하는 형식은 다음과 같습니다:

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

Behavior:

- `@<tag>` 또는 `#tag=<tag>`를 지정하면 그 태그를 사용합니다.
- `#branch=<branch>`를 지정하면 저장소에 태그가 있어도 그 브랜치를 사용합니다.
- 태그를 지정하지 않고 저장소에 태그가 있으면 GitHub 태그 API가 반환하는 최신 태그를 사용합니다.
- 태그를 지정하지 않고 저장소에 태그가 없으면 저장소의 `default_branch`를 사용합니다.

<h6>사용 예제</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

## pkg copy

저장소를 `node_modules` 아래에 설치하는 대신 GitHub 저장소 패키지를 요청한 대상 디렉터리로 복사합니다.
프로젝트 파일을 복사한 뒤 `pkg copy`는 복사된 프로젝트 루트와, 있다면 `cgi-bin`에도 의존성을 설치합니다.

<h6>문법</h6>

```sh
pkg copy [options] <source> <dest>
```

<h6>옵션</h6>

- `-f, --force` 대상 디렉터리가 이미 존재하고 비어 있지 않아도 계속 진행합니다
- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > pkg copy github.com/acme/helloapp public/hello
Copying github.com/acme/helloapp#branch=main to /work/public/hello
Installing dependencies in /work/public/hello
Installing dependencies in /work/public/hello/cgi-bin
```

## pkg run

`package.json`의 `scripts`에서 이름으로 지정한 항목을 실행합니다.

<h6>문법</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 주어진 프로젝트 디렉터리를 사용합니다
- `-h, --help` show help

`pkg run`은 스크립트를 실행하기 전에 현재 작업 디렉터리를 선택된 프로젝트 디렉터리로 변경합니다.

<h6>사용 예제</h6>

```sh
/work > pkg run start
```

## pkg uninstall

생성된 래퍼와 함께 의존성을 제거합니다.

<h6>문법</h6>

```sh
pkg uninstall [options] <name>
```

<h6>옵션</h6>

- `-C, --dir <dir>` 현재 작업 디렉터리 대신 주어진 프로젝트 디렉터리를 사용합니다
- `-g, --global` `/work/node_modules`에서 패키지를 제거하고 `--dir`을 무시합니다
- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > pkg uninstall github.com/acme/demo
Removed github.com/acme/demo
```

## 일반적인 작업 흐름

```sh
/work > pkg init demo-app
/work > pkg install github.com/acme/demo
/work > pkg install generic-pkg
/work > pkg run start
```

## Notes

- 패키지 이름 없는 `install`과 `run`에는 유효한 `package.json`이 있어야 합니다.
- `pkg run`은 POSIX 셸이 아니라 JSH 명령 해석을 통해 스크립트 줄을 실행합니다.
- 프로젝트 로컬 실행 파일에는 `./tool.js` 같은 상대 경로 명령을 권장합니다.
