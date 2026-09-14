# Machbase Neo JavaScript Readline Module

`readline` 모듈은 JSH 애플리케이션에 대화형 줄 입력을 제공합니다.
네이티브 JSH readline 구현을 기반으로 하는 `ReadLine` 클래스 하나를 제공합니다.

```js
const { ReadLine } = require('readline');
```

## ReadLine

대화형 줄 리더를 만듭니다.

<h6>문법</h6>

```js
new ReadLine([options])
```

<h6>옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-------|:-----|:--------|:------------|
| history | String | `readline` | JSH 설정 디렉터리에 저장되는 히스토리 파일 이름. |
| prompt | Function | 내장 프롬프트 | 각 줄의 프롬프트 문자열을 반환하는 콜백. |
| submitOnEnterWhen | Function | 항상 제출 | Enter가 현재 입력을 제출할지 결정하는 콜백. |
| autoInput | String[] | | 주로 자동 테스트에 사용하는 입력 시퀀스. |

## readLine()

논리적 입력 값 하나를 읽습니다.

- 입력이 한 줄이면 결과는 문자열 하나입니다.
- 여러 줄 입력을 받으면 결과는 줄들을 `\n`으로 이어 붙입니다.
- 네이티브 reader가 오류로 끝나면 JSH는 `Error` 객체를 반환합니다.

<h6>문법</h6>

```js
reader.readLine([options])
```

<h6>사용 예제</h6>

```js
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: () => 'input> ',
});
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
console.println(line);
```

## addHistory()

readline 히스토리에 줄을 추가합니다.

<h6>문법</h6>

```js
reader.addHistory(line)
```

같은 줄이 이미 있으면 이전 항목을 제거하고 새 항목을 끝에 추가합니다.

## close()

현재 readline 세션을 닫습니다.

`readLine()`이 입력을 기다리는 중에 `close()`를 호출하면 대기 중인 호출이 `EOF`로 끝납니다.

## prompt 옵션

`prompt`는 각 줄의 프롬프트 문자열을 생성합니다.

```js
prompt(lineno) => string
```

- `lineno`는 0부터 시작합니다.

<h6>사용 예제</h6>

```js
const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'sql> ' : '...> ',
});
```

## submitOnEnterWhen 옵션

Enter를 눌렀을 때 현재 입력을 제출할지, 여러 줄 편집을 계속할지 제어합니다.

```js
submitOnEnterWhen(lines, idx) => boolean
```

<h6>사용 예제</h6>

```js
const reader = new ReadLine({
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
```

## autoInput 옵션

미리 정의한 입력을 리더에 넣습니다. 주로 테스트와 비대화형 스크립트에 유용합니다.

```js
const reader = new ReadLine({
    autoInput: ['Hello World', ReadLine.CtrlJ],
});
```

## 여러 줄 입력 예제

```js
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: ['select *', ReadLine.Enter, 'from dual;', ReadLine.Enter],
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
const text = reader.readLine();
console.println(text);
```

## 정적 키 상수

`ReadLine`은 입력 시뮬레이션을 위한 키 상수를 제공합니다:

- 제어 키: `CtrlA` ... `CtrlZ`, `CtrlLeft`, `CtrlRight`, `CtrlUp`, `CtrlDown`
- 이동 키: `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- 편집 키: `Backspace`, `Delete`, `Enter`, `ShiftTab`, `Escape`
- Alt keys: `AltA` ... `AltZ`, `ALTBackspace`
- 기능 키: `F1` ... `F24`

## 동작 참고사항

- 이 모듈은 콜백 없는 동기 읽기를 사용합니다. `readLine()`이 완성된 값을 직접 반환합니다.
- `readLine()`은 `Error` 객체를 반환할 수 있으므로 호출자는 `line instanceof Error`를 확인해야 합니다.
- `close()`는 주로 다른 타이머나 이벤트에서 대기 중인 읽기를 취소할 때 유용합니다.
