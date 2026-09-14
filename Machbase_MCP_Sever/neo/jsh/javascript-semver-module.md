# Machbase Neo JavaScript Semver Module

`semver` 모듈은 JSH 애플리케이션을 위한 시맨틱 버전 비교 도우미를 제공합니다.

```js
const semver = require('semver');
```

## satisfies()

버전이 시맨틱 버전 제약 조건에 맞는지 확인합니다.

<h6>문법</h6>

```js
semver.satisfies(version, constraint)
```

<h6>반환값</h6>

`version`이 `constraint`를 만족하면 `true`, 아니면 `false`를 반환합니다.
빈 제약 조건과 `latest`는 `*`로 취급됩니다.

## maxSatisfying()

제약 조건을 만족하는 가장 높은 버전을 반환합니다.

<h6>문법</h6>

```js
semver.maxSatisfying(versions, constraint)
```

<h6>파라미터</h6>

- `versions` `String[]`
- `constraint` `String`

<h6>반환값</h6>

가장 잘 맞는 버전의 원본 문자열을 반환합니다.
맞는 버전이 없으면 빈 문자열을 반환합니다. 잘못된 후보 버전은 건너뜁니다.

## compare()

두 시맨틱 버전을 비교합니다.

<h6>문법</h6>

```js
semver.compare(left, right)
```

<h6>반환값</h6>

- `-1` if `left < right`
- `0` if `left === right`
- `1` if `left > right`

## 사용 예제

```js
const semver = require('semver');

console.println(semver.satisfies('1.4.2', '1.2 - 1.4'));
console.println(semver.satisfies('2.0.0', '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.2.0', '1.4.2', '2.0.0'], '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.0.0', '1.1.4', '1.2.0'], '~1.1'));
console.println(semver.compare('1.1.0', '1.2.0'));
console.println(semver.compare('1.2.0', '1.1.0'));
console.println(semver.compare('1.2.0', '1.2.0'));
```

## 동작 참고사항

- `version`, `left`, `right`, `constraint` 값이 잘못되면 오류가 발생합니다.
- 파싱 전에 앞뒤 공백이 제거됩니다.
- 제약 조건 파싱은 `1.2 - 1.4`, `~1.1` 같은 범위 표현을 포함한 시맨틱 버전 규칙을 따릅니다.
