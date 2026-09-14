# Machbase Neo JavaScript Path Module

`path` 모듈은 JSH 애플리케이션을 위해 Node.js와 유사한 경로 조작 유틸리티를 제공합니다.

기본 export는 POSIX 기준이며 구분자로 `/`, 구분 기호로 `:`를 사용합니다.
동작을 명시적으로 제어하려면 `path.posix`와 `path.win32` 네임스페이스를 사용할 수 있습니다.

```js
const path = require('path');
```

## resolve()

여러 경로를 하나의 절대 경로로 해석합니다.

<h6>문법</h6>

```js
path.resolve([...paths])
```

## normalize()

`.`과 `..` 구간을 해석하고 경로 구분자를 정규화합니다.

<h6>문법</h6>

```js
path.normalize(p)
```

## isAbsolute()

경로가 절대 경로인지 판별합니다.

<h6>문법</h6>

```js
path.isAbsolute(p)
```

## join()

현재 경로 스타일로 경로 조각들을 이어 붙이고 결과를 정규화합니다.

<h6>문법</h6>

```js
path.join(...paths)
```

## relative()

한 위치에서 다른 위치까지의 상대 경로를 계산합니다.

<h6>문법</h6>

```js
path.relative(from, to)
```

## dirname()

경로에서 디렉터리 부분을 추출합니다.

<h6>문법</h6>

```js
path.dirname(p)
```

## basename()

경로의 마지막 구성요소를 반환하며, 선택적으로 접미사를 제거합니다.

<h6>문법</h6>

```js
path.basename(p[, ext])
```

## extname()

앞의 점을 포함한 파일 확장자를 반환합니다.

<h6>문법</h6>

```js
path.extname(p)
```

## parse()

경로를 구조화된 구성요소로 분해합니다.

<h6>문법</h6>

```js
path.parse(p)
```

<h6>반환값</h6>

`root`, `dir`, `base`, `ext`, `name`을 가진 객체를 반환합니다.

## format()

파싱된 객체로부터 경로를 재구성합니다.

<h6>문법</h6>

```js
path.format(pathObject)
```

## sep

플랫폼 경로 구분자입니다. 기본값: `/`.

## delimiter

플랫폼 경로 구분 기호입니다. 기본값: `:`.

## posix / win32

POSIX 또는 Windows 경로 처리를 명시적으로 지정하는 네임스페이스입니다.
JSH가 Windows가 아닌 시스템에서 실행 중이어도 `path.win32`로 Windows 경로를 처리할 수 있습니다.

## 사용 예제

```js
const path = require('path');

console.println(path.join('/work', 'data', 'file.txt'));  // /work/data/file.txt
console.println(path.dirname('/work/data/file.txt'));      // /work/data
console.println(path.basename('/work/data/file.txt'));     // file.txt
console.println(path.extname('file.txt'));                 // .txt
console.println(path.isAbsolute('/work'));                 // true

const parsed = path.parse('/work/data/file.txt');
console.println(parsed.dir, parsed.name, parsed.ext);     // /work/data file .txt
```

## 동작 참고사항

- 모든 공개 함수는 해당하는 경우 문자열 인자를 요구하며, 잘못된 입력에는 `TypeError`를 던집니다.
- JSH의 기본 export는 POSIX 기준입니다.
