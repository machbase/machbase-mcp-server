# Machbase Neo TQL FFT

## 고속 푸리에 변환(Fast Fourier Transform)

### 사전 준비

원활한 실습을 위해 아래 쿼리를 실행해 테이블과 데이터를 준비합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## 샘플 데이터 생성

웹 UI에서 새 TQL 에디터를 열고 아래 코드를 붙여넣어 실행합니다.

이 예제에서 `oscillator()`는 15Hz 1.0과 24Hz 1.5가 합성된 파형을 생성합니다. 그리고 `CHART_SCATTER()`의 `dataZoom()` 옵션 함수는 x축 아래에 슬라이더를 제공합니다.

```js
FAKE( 
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
CHART_SCATTER( size("600px", "350px"), dataZoom('slider', 95, 100) )
```

## 데이터베이스에 저장

생성한 데이터를 'signal'이라는 태그 이름으로 데이터베이스에 저장합니다.

```js
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
INSERT( 'time', 'value', table('example'), tag('signal') )
```

"Result" 창에 "10000 rows inserted." 메시지가 표시됩니다.

참고로 테스트 장비(Apple mac mini M1)에서 약 270ms가 걸렸는데, 아래 예제처럼 `APPEND()` 방식을 쓰면 65ms로 **4배 빨랐습니다**.

```js
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
PUSHVALUE(0,'signal')
// |    0         1      2
// +--> 'signal' time   magnitude
// |
APPEND( table('example') )
```

**주의:** `APPEND`는 입력 레코드의 필드가 테이블 컬럼과 **순서와 타입까지 정확히 일치**할 때만 동작합니다.

## 데이터베이스에서 읽기

아래 코드는 'example' 테이블에 저장된 데이터를 읽습니다.

```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
CHART_LINE( size("600px", "350px"), dataZoom('slider', 95, 100))
```

## 고속 푸리에 변환

`SQL_SELECT()` 소스와 `CHART_LINE()` 싱크 사이에 데이터 변환 함수 몇 개를 추가합니다.

### GROUPBYKEY 사용

```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```

### SCRIPT 사용

```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
SCRIPT({
    var times = [];
    var values = [];
},{
    ts = $.values[0];
    val = $.values[1];
    times.push(ts);
    values.push(val);
},{
    const ana = require("@jsh/analysis");
    result = ana.fft(times, values);
    for(i = 0; i < result.x.length; i++) {
        $.yield(result.x[i], result.y[i]);
    }
})
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```

## 동작 원리

### 1단계: SQL_SELECT()

`SQL_SELECT(...)`는 쿼리 결과를 `{key: rownum, value: (time, value) }` 형태의 레코드로 내보냅니다.

### 2단계: MAPKEY('sample')

`MAPKEY('sample')`은 모든 레코드에 'sample'이라는 상수 문자열을 새 키로 지정합니다. 그 결과 모든 레코드가 같은 키 `'sample'`과 값 `(time, value)`를 갖습니다. `{key: 'sample', value:(time, value)}`

### 3단계: GROUPBYKEY()

`GROUPBYKEY()`는 같은 키를 가진 레코드를 병합합니다. 이 예제에서는 모든 쿼리 결과가 'sample'이라는 같은 키를 가진 하나의 레코드로 합쳐지고, 값은 튜플 배열이 됩니다. `{key: 'sample', value:[ (time1, value1), (time2, value2), ..., (timeN, valueN) ]}`

### 4단계: FFT()

`FFT()`는 레코드의 값에 고속 푸리에 변환을 적용해 (시간-값)을 (주파수-진폭) 튜플 배열로 변환합니다. `{key: 'sample', value:[ (Hz1, Ampl1), (Hz2, Ampl2), ... ]}`

## 시간축 추가하기

```js
SQL_SELECT( 'time', 'value', from('example', 'signal'), between('last-10s', 'last'))

MAPKEY( roundTime(value(0), '500ms') )
GROUPBYKEY()
FFT(minHz(0), maxHz(100))
FLATTEN()
PUSHKEY('fft')
CHART_BAR3D(
      xAxis(0, 'time', 'time'),
      yAxis(1, 'Hz'),
      zAxis(2, 'Amp'),
      size('600px', '600px'), visualMap(0, 1.5), theme('westeros')
)
```

## 시간축이 있을 때의 동작 원리

### 1단계: SQL_SELECT()

`SQL_SELECT(...)`는 쿼리 결과를 레코드로 내보냅니다. `{key: time, value: (value) }`

### 2단계: MAPKEY()

`MAPKEY( roundTime(value(0), '500ms'))`는 `value(0)`을 500밀리초 단위로 반올림한 결과를 새 키로 지정합니다. 그 결과 레코드는 `{key: (time/500ms)*500ms, value:(time, value)}` 형태로 변환됩니다.

### 3단계: GROUPBYKEY()

`GROUPBYKEY()`는 레코드를 500ms 단위로 묶습니다. `{key: time1In500ms, value:[(time1, value1), (time2, value2)...]}`

### 4단계: FFT()

`FFT()`는 각 레코드에 고속 푸리에 변환을 적용합니다. 선택 함수인 `minHz(0)`과 `maxHz(100)`은 시각화를 개선하기 위해 출력 범위를 제한합니다. `{key:time1In500ms, value:[(Hz1, Ampl1), ...]}`, `{key:'time2In500ms', value:[(Hz1, Ampl1), ...]}`, ...

### 5단계: FLATTEN()

`FLATTEN()`은 값 배열을 여러 레코드로 나눠 차원을 낮춥니다.

### 6단계: PUSHKEY()

`PUSHKEY('fft')`는 모든 레코드에 'fft'라는 상수 문자열을 새 키로 지정하고, 이전 키는 값 배열의 맨 앞으로 "밀어 넣습니다". `{key:'fft', value:(time1In500ms, Hz1, Ampl1)}`, `{key:'fft', value:(time1In500ms, Hz2, Ampl2)}`...
