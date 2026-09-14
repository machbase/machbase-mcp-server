# Machbase Neo JavaScript ParseArgs Module

`util/parseArgs` 모듈은 JSH 애플리케이션을 위해 명령행 방식의 인자 배열을 파싱합니다.

```js
const { parseArgs } = require('util/parseArgs');
```

## parseArgs()

하나 이상의 설정 객체로 인자 배열을 파싱합니다.

<h6>문법</h6>

```js
parseArgs(args, ...configs)
```

`command` 필드가 있는 설정이 여러 개 주어지면 파서가 `args[0]`을 대조해 어떤 설정을 쓸지 결정합니다.

<h6>설정 옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-------|:-----|:--------|:------------|
| `options` | Object | | 사용 가능한 플래그와 그 타입을 정의합니다 |
| `strict` | Boolean | `true` | 알 수 없는 옵션을 검증합니다 |
| `allowPositionals` | Boolean | `false` | 위치 인자를 허용합니다 |
| `positionals` | Array | | 위치 인자 구조를 정의합니다 |
| `allowNegative` | Boolean | `false` | 불리언 플래그에 `--no-` 접두를 허용합니다 |
| `tokens` | Boolean | `false` | 상세 토큰 정보를 반환합니다 |
| `command` | String | | 다중 설정 분기를 위한 하위 명령 이름 |

<h6>옵션 타입</h6>

지원 타입: `boolean`, `string`, `integer`, `float`.

각 옵션 정의에는 다음을 포함할 수 있습니다:
- `type` 옵션 타입
- `short` 한 글자 짧은 플래그
- `default` 기본값
- `description` 도움말 설명
- `longDescription` 다중 명령 도움말에서 사용하는 긴 설명

파서는 camelCase 이름을 kebab-case 플래그로 자동 변환합니다. 예를 들어 `maxRetryCount`는 `--max-retry-count`에 대응합니다.

<h6>반환값</h6>

다음을 담은 객체를 반환합니다:
- `values` 파싱된 옵션 값
- `positionals` 순서대로의 위치 인자
- `namedPositionals` 이름 붙은 위치 값 (`positionals` 설정이 있을 때 포함). 키는 kebab-case에서 camelCase로 변환됩니다
- `tokens` 토큰 세부 정보 (`tokens: true`일 때)
- `command` 매칭된 하위 명령 이름 (해당하는 경우)

<h6>사용 예제</h6>

```js
const { parseArgs } = require('util/parseArgs');

const result = parseArgs(['--name', 'Alice', '--verbose', 'file.txt'], {
    options: {
        name: { type: 'string', short: 'n' },
        verbose: { type: 'boolean', short: 'v' }
    },
    allowPositionals: true
});

console.println(result.values.name);     // Alice
console.println(result.values.verbose);  // true
console.println(result.positionals[0]);  // file.txt
```

## parseArgs.formatHelp()

설정 구조로부터 사람이 읽기 쉬운 도움말 문서를 생성합니다.

<h6>문법</h6>

```js
parseArgs.formatHelp(config)
```

## parseArgs.toKebabCase()

camelCase를 kebab-case 형식으로 변환합니다.

<h6>문법</h6>

```js
parseArgs.toKebabCase(name)
```

## 동작 참고사항

- `integer`는 소수점이 포함된 값을 거부합니다.
- `integer`와 `float` 타입 모두 JavaScript 숫자를 반환합니다.
- 파서는 옵션 종결자 `--`와 `-abc` 같은 불리언 묶음을 지원합니다.
- `strict`가 `true`이면 알 수 없는 옵션은 오류를 발생시킵니다.
