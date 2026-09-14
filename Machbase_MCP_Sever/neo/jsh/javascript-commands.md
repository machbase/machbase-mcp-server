# Machbase Neo JavaScript Commands

이 문서는 기본 JSH 명령들을 사용 목적별로 묶어 설명합니다.

## 개요

명령들을 사용자 관점의 기능에 따라 분류했습니다.

**참고**

- 이 명령들은 기본적으로 호스트 OS 파일시스템이 아니라 JSH 가상 파일시스템 안에서 동작합니다.
- 상대 경로는 현재 JSH 작업 디렉터리를 기준으로 해석됩니다.
- 일부 명령은 현재 디렉터리나 환경 변수처럼 활성 셸 세션에 직접 영향을 줍니다.
- 일부 명령은 의도적으로 Unix 대응 명령보다 기능을 줄여 제공합니다.

## 파일시스템 명령

### cd

활성 JSH 셸 세션의 현재 작업 디렉터리를 변경합니다.

<h6>문법</h6>

```sh
cd [directory]
```

인자가 없으면 `cd`는 `$HOME`으로 이동합니다.
대상 경로가 없으면 오류를 출력하고 0이 아닌 상태를 반환합니다.

<h6>사용 예제</h6>

```sh
/work > cd subdir
/work/subdir >
/work/subdir > cd
/work >
```

### cat

파일들을 표준 출력으로 이어 붙여 출력합니다.
줄 번호, 줄 끝·탭 표시, 빈 줄 축약, 구문 강조를 지원합니다.

<h6>문법</h6>

```sh
cat [OPTION]... [FILE]...
```

<h6>옵션</h6>

- `-n, --number` 모든 출력 줄에 번호를 매깁니다
- `-E, --showEnds` 각 줄 끝에 `$`를 표시합니다
- `-T, --showTabs` 탭 문자를 `^I`로 표시합니다
- `-s, --squeeze` 반복되는 빈 줄을 줄입니다
- `-c, --color` 구문 강조를 활성화합니다
- `-h, --help` show help

`-c`를 쓰면 `.js`, `.json`, `.ndjson`, `.sql`, `.csv`, `.yaml`, `.yml`, `.toml`에 구문 강조가 적용됩니다.

<h6>사용 예제</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

### ls

디렉터리 내용을 나열합니다.
기본적으로 항목을 열 형태로 출력하며 숨김 항목, 상세 목록 모드, 시간 정렬, 재귀, 간단한 와일드카드를 지원합니다.

<h6>문법</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>옵션</h6>

- `-l, --long` 상세 목록 보기를 사용합니다
- `-a, --all` 숨김 항목을 포함합니다
- `-t, --time` 수정 시각 기준 내림차순으로 정렬합니다
- `-R, --recursive` 하위 디렉터리를 재귀적으로 나열합니다

경로 인자에는 `*`, `?` 같은 간단한 와일드카드 패턴을 쓸 수 있습니다.

<h6>사용 예제</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

### mkdir

하나 이상의 디렉터리를 만듭니다.

<h6>문법</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>옵션</h6>

- `-p, --parents` 필요한 상위 디렉터리를 함께 만듭니다
- `-v, --verbose` 생성한 디렉터리마다 메시지를 출력합니다
- `-h, --help` show help

`-p` 없이 이미 있는 디렉터리를 만들려 하면 오류가 발생합니다.

<h6>사용 예제</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

### pwd

현재 작업 디렉터리를 출력합니다.

<h6>문법</h6>

```sh
pwd
```

<h6>사용 예제</h6>

```sh
/work > pwd
/work
```

### rm

파일이나 디렉터리를 삭제합니다.

<h6>문법</h6>

```sh
rm [OPTION]... FILE...
```

<h6>옵션</h6>

- `-r, -R, --recursive` 디렉터리와 그 내용을 재귀적으로 삭제합니다
- `-d, --dir, --directory` 빈 디렉터리를 삭제합니다
- `-f, --force` 없는 경로와 인자 누락 오류를 무시합니다
- `-v, --verbose` 삭제한 경로마다 메시지를 출력합니다
- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## 환경 명령

### env

환경 변수를 출력합니다.
인자가 없으면 전체 환경을 정렬해 출력합니다. 이름을 하나 이상 주면 해당 변수만 출력합니다.

<h6>문법</h6>

```sh
env [NAME]...
```

<h6>사용 예제</h6>

```sh
/work > env
/work > env HOME PWD
```

### alias

현재 셸 세션의 명령 별칭을 정의하거나 표시합니다.
인자가 없으면 `alias`는 현재 정의된 별칭을 정렬해 출력합니다. `alias NAME`은 하나의 별칭을 출력합니다.
`alias NAME COMMAND [ARG]...`는 별칭을 정의하며, 같은 셸 세션의 이후 입력에서 명령 앞부분이 확장됩니다.

<h6>문법</h6>

```sh
alias
alias NAME
alias NAME COMMAND [ARG]...
```

<h6>사용 예제</h6>

```sh
/work > alias ll ls -l
/work > ll
/work > alias
/work > alias ll
```

### setenv

현재 셸 세션에 환경 변수를 설정합니다.

<h6>문법</h6>

```sh
setenv NAME VALUE
setenv NAME=VALUE
```

변수 이름은 문자 또는 `_`로 시작해야 하며 이후에는 문자, 숫자, `_`를 쓸 수 있습니다.

<h6>사용 예제</h6>

```sh
/work > setenv GREETING hello
/work > setenv MESSAGE='hello world'
```

### unsetenv

현재 셸 세션에서 환경 변수를 제거합니다.

<h6>문법</h6>

```sh
unsetenv NAME
```

이름이 잘못되었거나 인자가 없으면 사용법 오류가 발생합니다.

<h6>사용 예제</h6>

```sh
/work > unsetenv GREETING
```

## 시스템 명령

### pkg

JSH 패키지와 프로젝트 매니페스트를 관리합니다.
하위 명령, 옵션, 작업 흐름은 패키지 관리자 문서를 참고하세요.

<h6>문법</h6>

```sh
pkg <command> [options] [args...]
```

### servicectl

서비스 컨트롤러를 통해 장시간 실행되는 JSH 서비스를 관리합니다.
하위 명령, 옵션, 서비스 관리 작업 흐름은 서비스 관리자 문서를 참고하세요.

<h6>문법</h6>

```sh
servicectl [--controller=<addr>] <command> [args...]
```

**servicectl controller**

서비스 컨트롤러의 RPC 런타임 지표를 보여주고 초기화합니다.

<h6>문법</h6>

```sh
servicectl [--controller=<addr>] controller [metrics|get|reset]
```

<h6>동작</h6>

- `controller`와 `controller metrics`는 같습니다.
- `controller get`은 `controller metrics`의 별칭입니다.
- `controller reset`은 누적 카운터를 초기화하고 새 누적 구간을 시작합니다.
- `high_water_mark_connections`는 마지막 초기화 이후 동시 RPC 연결의 최고치를 기록합니다.

<h6>사용 예제</h6>

```sh
servicectl controller metrics
servicectl controller reset
servicectl controller get
```

## 텍스트 및 유틸리티 명령

### echo

인자를 공백으로 구분해 출력하고 줄바꿈으로 끝냅니다.

<h6>문법</h6>

```sh
echo [ARG]...
```

현재 구현은 `-n` 같은 셸 스타일 플래그나 이스케이프 시퀀스 해석을 지원하지 않습니다.

<h6>사용 예제</h6>

```sh
/work > echo hello world
hello world
```

### sleep

지정한 초만큼 기다린 뒤 반환합니다.

<h6>문법</h6>

```sh
sleep [OPTION] <sec>
```

<h6>옵션</h6>

- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > sleep 5
```

### tail

파일의 마지막 부분을 출력합니다.
`-f`를 쓰면 파일에 덧붙여지는 새 내용을 계속 출력합니다.

<h6>문법</h6>

```sh
tail [OPTION]... <file>
```

<h6>옵션</h6>

- `-n, --lines <N>` 마지막 N줄을 출력합니다. 기본값 `10`
- `-f, --follow` 파일이 커지는 대로 따라갑니다. `SIGINT`나 `SIGTERM`에서 멈춥니다
- `-h, --help` show help

<h6>사용 예제</h6>

```sh
/work > tail app.log
/work > tail -n 20 app.log
/work > tail -f app.log
```

### viz

vizspec 문서(ADVN)를 보고, 검증하고, 내보냅니다.
JSH 또는 Machbase Neo 작업 흐름이 만든 렌더러 중립 분석 출력을 위한 것입니다.

<h6>문법</h6>

```sh
viz <command> [options] <file>
```

<h6>하위 명령</h6>

- `viz view [options] <file>` vizspec을 TUI 블록으로 렌더링합니다
- `viz validate <file>` vizspec 파일을 검증합니다
- `viz export [options] <file>` vizspec을 SVG로 내보냅니다

<h6>`view` options</h6>

- `--compact` 시리즈 요약과 원시 데이터 표를 숨깁니다
- `--rows <n>` 블록당 상세 행 수를 제한합니다
- `--width <n>` 스파크라인·막대·타임라인 너비를 조절합니다
- `--verbose-meta` 블록 메타데이터를 표시합니다
- pretty-table 옵션도 사용할 수 있습니다

<h6>`export` options</h6>

- `--format svg` 내보내기 형식. 현재 `svg`만 지원합니다
- `-o, --output <file>` 표준 출력 대신 파일로 SVG를 씁니다
- `--width <n>` SVG 너비(픽셀)
- `--height <n>` SVG 높이(픽셀)
- `--padding <n>` SVG 바깥 여백(픽셀)
- `--title <text>` 선택적 SVG 제목
- `--background <color>` SVG 배경 색상
- `--font-family <name>` SVG 글꼴 계열
- `--font-size <n>` SVG 기본 글꼴 크기(픽셀)
- `--hide-legend` 범례 렌더링을 생략합니다

<h6>사용 예제</h6>

```sh
/work > viz validate sensor-overview.json
/work > viz view --width 80 sensor-overview.json
/work > viz export --title "CPU Overview" --output cpu.svg sensor-overview.json
```

### wc

각 파일의 줄·단어·바이트·문자 수를 셉니다.
파일을 주지 않거나 `-`를 쓰면 표준 입력을 읽습니다.

<h6>문법</h6>

```sh
wc [OPTION]... [FILE]...
```

<h6>옵션</h6>

- `-l, --lines` 줄 수를 출력합니다
- `-w, --words` 단어 수를 출력합니다
- `-c, --bytes` 바이트 수를 출력합니다
- `-m, --chars` 문자 수를 출력합니다
- `-h, --help` show help

카운트 옵션을 지정하지 않으면 `wc`는 줄·단어·바이트 수를 출력합니다.

<h6>사용 예제</h6>

```sh
/work > wc notes.txt
/work > wc -l *.log
/work > cat notes.txt | wc -w -
```

### which

JSH 명령 경로에서 명령이 어디로 해석되는지 출력합니다.

<h6>문법</h6>

```sh
which <command>
```

명령을 찾을 수 없으면 `which`는 오류를 출력하고 0이 아닌 상태를 반환합니다.

<h6>사용 예제</h6>

```sh
/work > which ls
/sbin/ls.js
```

## 메시징 명령

### mqtt_pub

MQTT 브로커로 메시지를 발행합니다.

<h6>문법</h6>

```sh
mqtt_pub [OPTION]...
```

<h6>옵션</h6>

- `-t, --topic` 발행할 토픽
- `-b, --broker` 브로커 주소, 기본값 `tcp://localhost:5653`
- `-m, --message` 인라인 메시지 페이로드
- `-f, --file` 페이로드가 담긴 파일
- `-q, --qos` MQTT QoS 수준. `0`, `1`, `2` 중 하나
- `-d, --debug` 디버그 로그를 출력합니다
- `-h, --help` show help

`-m`과 `-f`는 함께 쓸 수 없습니다.

<h6>사용 예제</h6>

```sh
/work > mqtt_pub -t sensors/temp -m '{"value":21.5}'
/work > mqtt_pub -b tcp://broker:1883 -t logs/app -f payload.json -q 1
```

### nats_pub

NATS subject로 메시지를 발행합니다.
명시적 응답 subject나 request 모드를 사용해 응답 하나를 기다릴 수도 있습니다.

<h6>문법</h6>

```sh
nats_pub [OPTION]...
```

<h6>옵션</h6>

- `-t, --topic` 발행할 subject
- `-s, --subject` alias for `--topic`
- `-b, --broker` 브로커 주소, 기본값 `nats://localhost:4222`
- `-m, --message` 인라인 메시지 페이로드
- `-f, --file` 페이로드가 담긴 파일
- `-r, --reply` 기다릴 응답 subject
- `--request` 임시 inbox subject를 만들고 응답 하나를 기다립니다
- `--timeout` 연결 및 응답 타임아웃(밀리초), 기본값 `10000`
- `-d, --debug` 디버그 로그를 출력합니다
- `-h, --help` show help

`-m`과 `-f`는 함께 쓸 수 없습니다.

<h6>사용 예제</h6>

```sh
/work > nats_pub -t events.demo -m 'hello'
/work > nats_pub -s rpc.echo -m 'ping' --request
/work > nats_pub -s rpc.echo -m 'ping' -r reply.demo --timeout 3000
```

## 대화형 명령

### repl

JSH JavaScript REPL을 시작합니다.
명령 중심의 셸 프롬프트가 아니라 대화형 JavaScript 평가 환경입니다.

<h6>문법</h6>

```sh
repl
```

### shell

새 JSH 셸 세션을 시작합니다.
현재 프로세스 환경과 분리된 셸 루프에 들어가고 싶을 때 사용합니다.

<h6>문법</h6>

```sh
shell
```
