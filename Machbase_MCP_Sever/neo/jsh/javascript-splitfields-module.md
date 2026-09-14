# Machbase Neo JavaScript SplitFields Module

`util/splitFields` 모듈은 인용된 부분 문자열을 보존하면서 공백 구분자로 문자열을 필드로 나눕니다.

```js
const { splitFields } = require('util/splitFields');
```

## splitFields()

문자열을 필드 문자열 배열로 나눕니다.

<h6>문법</h6>

```js
splitFields(input[, options])
```

<h6>파라미터</h6>

- `input` `String` 나눌 문자열
- `options` `Object` (현재 사용되지 않음)

<h6>반환값</h6>

`String[]` 파싱된 필드 배열.

<h6>동작</h6>

- 연속된 공백은 하나의 구분자로 취급합니다.
- 빈 필드는 결과에서 제외됩니다.
- 반환 값에서 인용 문자는 제거됩니다.
- 인용 구간 안의 탭과 개행은 그대로 유지됩니다.
- 닫히지 않은 따옴표는 문자열 끝까지 텍스트를 계속 소비합니다.
- 인용 안의 이스케이프 시퀀스는 특별히 해석되지 않습니다.

<h6>사용 예제</h6>

```js
const { splitFields } = require('util/splitFields');

console.println(splitFields('hello "world foo" bar'));
// ['hello', 'world foo', 'bar']

console.println(splitFields("hello 'world foo' bar"));
// ['hello', 'world foo', 'bar']

console.println(splitFields("a \"b c\" d 'e f' g"));
// ['a', 'b c', 'd', 'e f', 'g']
```

## 동작 참고사항

- 이 함수는 완전한 명령 파싱이 필요 없을 때 셸과 유사한 토큰화를 위해 설계되었습니다.
- 작은따옴표와 큰따옴표를 모두 지원합니다.
