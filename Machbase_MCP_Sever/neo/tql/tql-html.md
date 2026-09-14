# Machbase Neo TQL HTML

`HTML()` SINK은 제공된 템플릿 언어로 서식을 적용해 HTML 문서나 요소를 출력으로 생성합니다. 이를 통해 쿼리 결과를 바탕으로 HTML 출력의 구조와 모양을 자유롭게 구성할 수 있습니다.

**문법**: `HTML(templates...)`

*버전 8.0.53 이상*

**파라미터**:
- `templates`: 하나 이상의 템플릿 문자열 또는 `file(path)` 참조입니다. 각 인자는 템플릿 문자열을 직접 주거나, `file(path)`로 파일에서 템플릿을 불러올 수 있습니다. 템플릿 내용은 Go HTML 템플릿 언어를 사용합니다. 자세한 내용은 템플릿 문서를 참고하세요.
- `cache()`: 결과 데이터를 캐시합니다. 자세한 내용은 결과 데이터 캐시 항목을 참고하세요.

템플릿 안에서는 현재 레코드의 필드 값과 행 번호를 노출하는 value 객체에 접근할 수 있습니다. HTML 템플릿 컨텍스트에서 사용할 수 있는 필드와 속성은 다음과 같습니다.

## 메서드

- `{{ .Columns }}`
- `{{ .Column <idx>}}`
- `{{ .Values }}`
- `{{ .Value <idx> }}`
- `{{ .ValueHTMLAttr <idx> }}`
- `{{ .ValueCSS <idx> }}`
- `{{ .ValueJS <idx> }}`
- `{{ .ValueURL <idx> }}`
- `{{ .ValueString <idx> }}`
- `{{ .V.<field> }}`
- `{{ .Num }}`

## 함수

### timeformat

**문법**

```
{{ timeformat <format> <timezone> }}
```

**사용 예제**

```html
SCRIPT({
    const { now } = require("@jsh/system");
    $.yield(now(), "Hello World");
})
HTML({
    <li>{{ $.Value 0 | timeformat "RFC3339" "UTC" }}
    <li>{{ $.Value 1 }}
})
```

**출력:**

```html
<li>2025-05-29T08:32:33Z
<li>Hello World
```

### format

**사용 예제**

```html
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li>{{ $.Value 0 | format "%.2f" }}
    <li>{{ $.Value 1 | format "Say: %s?" }}
})
```

**출력:**

```html
<li> 3.14
<li> Say: Hello World?
```

### param

```html
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ param "prefix" }} {{ $.Value 0 }}
    <li> {{ param "prefix" }} {{ $.Value 1 }}
})
```

**참고**: TQL 스크립트를 `?param=Line` 파라미터와 함께 호출합니다.

**출력:**

```html
<li> Line 3.1415
<li> Line Hello World
```

### paramDefault

```html
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ paramDefault "prefix1" "Line1" }} {{ $.Value 0 }}
    <li> {{ paramDefault "prefix2" "Line2" }} {{ $.Value 1 }}
})
```

**출력:**

```html
<li> Line1 3.1415
<li> Line2 Hello World
```

### toLower

```html
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ $.Value 0 | format "%.2f" }}
    <li> {{ $.Value 1 | toLower | format "Say: %s?" }}
})
```

**출력:**

```html
<li> 3.14
<li> Say: hello world?
```

### toUpper

```html
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ $.Value 0 | format "%.2f" }}
    <li> {{ $.Value 1 | toUpper | format "Say: %s?" }}
})
```

**출력:**

```html
<li> 3.14
<li> Say: HELLO WORLD?
```

## 사용 예제

### .V 사용 (필드 맵)

`.V`는 필드 이름을 키로, 해당 값을 값으로 갖는 맵 객체입니다.

```html
SQL(`SELECT NAME, TIME, VALUE FROM EXAMPLE LIMIT 5`)
HTML({
  {{ if .IsFirst }}
    <html>
    <body>
      <h2>HTML Template Example</h2>
      <hr>
      <table>
      <tr>
        {{range .Columns}}
          <th>{{ . }}</th>
        {{end}}
      </tr>
  {{ end }}
      <tr>
        <td>{{ .V.NAME }}</td>
        <td>{{ .V.TIME | timeformat "RFC3339" "Asia/Seoul"}}</td>
        <td>{{ .V.VALUE }}</td>
      </tr>
  {{ if .IsLast }}
      </table>
      <hr>
        Total: {{ .Num }}
    </body>
    </html>
  {{ end }}
})
```

### .Value 사용 (인덱스 접근)

`.Value`는 현재 레코드의 필드를 인덱스로 접근하는 함수입니다.

```html
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
HTML({
    {{ if .IsFirst }}
        <html>
        <body>
            <h2>HTML Template Example</h2>
            <hr>
    {{ end }}

    <li>{{ .Value 0 }} : {{ .Value 1 }}
    
    {{ if .IsLast }}
        <hr>
        Total: {{ .Num }}
        </body>
        </html>
    {{ end }}
})
```

### .Values 사용 (배열 접근)

`.Values`는 현재 레코드의 모든 필드 값을 담은 배열입니다.

```html
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
HTML({
    {{ if .IsFirst }}
        <html>
        <body>
            <h2>HTML Template Example</h2>
            <hr>
    {{ end }}

    <li>{{ (index .Values 0) }} : {{ (index .Values 1 ) }}
    
    {{ if .IsLast }}
        <hr>
        Total: {{ .Num }}
        </body>
        </html>
    {{ end }}
})
```

## 컨텍스트 인식 이스케이핑

템플릿은 HTML, CSS, JavaScript, URI를 이해합니다. 각 단순 액션 파이프라인에 살균(sanitizing) 함수를 자동으로 추가합니다.

`{{.Value 0}}`, `{{.Value 1}}`, `{{.Value 2}}` 각각에 필요한 이스케이프 함수가 덧붙여집니다.

**예제:**

```html
SCRIPT({
    $.yield(
        `http://maven.org/`,
        ``,
        "Java")
    $.yield(
        `http://npmjs.com/`,
        ``,
        "JavaScript")
})
HTML({
    <li>
        <a href="{{.Value 0}}">
        {{.ValueHTML 1}}{{.Value 2}}
        </a>
    </li>
})
```

**출력:**

```html
<li>
  <a href="http://maven.org/">
    Java
  </a>
</li>
<li>
  <a href="http://npmjs.com/">
    JavaScript
  </a>
</li>
```

### HTML 컨텍스트 이스케이핑

`{{.Value 0}}`이 `O'Reilly: How are <i>you</i>?`라고 할 때, 컨텍스트별로 어떻게 표시되는지 아래 예제에서 확인할 수 있습니다.

**HTML 본문에서:**

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML({
  {{.Value 0}}
})

// Output:
//  O&#39;Reilly: How are &lt;i&gt;you&lt;/i&gt;?
```

**URL 파라미터에서:**

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a href="/path?p={{.ValueHTML 0}}">`)

// Output:
//  <a href="/path?p=O%27Reilly%3a%20How%20are%20%3ci%3eyou%3c%2fi%3e%3f">
```

**JavaScript 컨텍스트에서:**

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='f("{{.Value 0}}")'>`)

// Output:
//  <a onx="f('O\u0027Reilly: How are \u003ci\u003eyou\u003c\/i\u003e?')">
```

**JavaScript 함수 예제:**

```html
SCRIPT({ $.yield(`Hello World?`, `function doMsg(msg){ console.log(msg); }`) })
HTML({
  <script>
  {{.ValueJS 1}}
  </script>
  <a onClick='doMsg("{{.Value 0}}")'>here</a>
})

// Output:
// <script>
// function doMsg(msg){ console.log(msg); }
// </script>
// <a onClick='doMsg("Hello World?")'>here</a>
```

### JavaScript에서 문자열이 아닌 값

JavaScript 컨텍스트에서는 문자열이 아닌 값도 사용할 수 있습니다. 레코드가 객체인 경우:

```html
SCRIPT({
    $.yield({A: "foo", B:"bar"})
})
HTML({
    <script>var pair = {{ .Value 0 }};</script>
})
```

**출력:**

```html
<script>var pair = {"A":"foo","B":"bar"};</script>
```

## 이스케이프하지 않는 문자열

기본적으로 템플릿은 모든 파이프라인이 평문 문자열을 생성한다고 가정합니다. 그 평문을 해당 컨텍스트에 정확하고 안전하게 삽입하기 위해 필요한 이스케이프 단계를 추가합니다.

데이터 값이 평문이 아닐 때는 타입을 표시해 과도한 이스케이프를 막을 수 있습니다.

HTML, JS, URL 등의 타입은 이스케이프에서 제외되는 안전한 내용을 담을 수 있습니다.

**예제:**

```html
SCRIPT({
    $.yield(`<b>World</b>`)
})
HTML({
    Hello, {{ .ValueHTML 0 }}!
})
```

**출력:**

```html
Hello, <b>World</b>!
```

다음과 같이 되지 않습니다:

```
Hello, &lt;b&gt;World&lt;b&gt;!
```
