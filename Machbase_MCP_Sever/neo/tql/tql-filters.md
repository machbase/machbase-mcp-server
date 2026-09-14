# Machbase Neo TQL Filters

## 센서 측정

우리가 관찰하는 IoT 데이터는 센서로 측정한 값들로 이루어집니다. 모든 센서에는 피할 수 없는 오차인 노이즈가 어느 정도 섞여 있습니다. 노이즈가 전혀 없는 데이터는 이론적으로만 존재하며, 수학적으로 만들어낸 가상 데이터로만 가능합니다.

### 순수 신호

**SCRIPT 사용:**
```js
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2 * 2 * PI * value(0)) )
MAPVALUE(1, $sig)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
        ],
        legend: { bottom: 10 },
    })
)
```

### 노이즈의 특성

일반적으로 노이즈는 아래 그래프처럼 우리가 관찰하려는 데이터보다 주파수가 높은 경향이 있습니다.

**SCRIPT 사용:**
```js
SCRIPT({
    $.result = { columns: ["val", "sig", "noise"], types: ["double", "double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig, noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig)
MAPVALUE(2, $noise)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 }
    })
)
```

### 노이즈가 섞인 신호

결국 센서로 측정한 값은 노이즈가 섞인 아래와 같은 그래프가 됩니다.

데이터베이스에 저장된 값에는 이러한 노이즈가 섞여 있으며, 분석 과정에서는 노이즈를 어느 정도 제거한(노이즈 필터링) 데이터를 보고 싶을 때가 많습니다.

**SCRIPT 사용:**
```js
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 }
    })
)
```

## 평균 필터

센서의 영점 조정 과정을 떠올려 보세요. 연속된 값을 누적해 평균을 구하면, 아래처럼 사인파가 결국 0으로 수렴하는 것을 볼 수 있습니다.

**SCRIPT 사용:**
```js
SCRIPT({
    const filter = require("@jsh/filter")
    const avg = new filter.Avg();
    const { arrange } = require("@jsh/generator");
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, avg.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"AVG" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_AVG(2, value(1))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"AVG" },
        ],
        legend: { bottom: 10 }
    })
)
```

## 이동평균 필터

누적된 전체 샘플의 평균을 구하는 대신, 고정 크기의 윈도우에 담긴 샘플로 평균을 계산합니다. 주식 차트에서 흔히 보는 며칠 단위 이동평균과 같은 개념입니다.

**SCRIPT 사용:**
```js
SCRIPT({
    const filter = require("@jsh/filter")
    const movavg = new filter.MovAvg(10);
    const { arrange } = require("@jsh/generator");
    $.result = { columns: ["val", "sig", "ma10"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, movavg.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_MOVAVG(2, value(1), 10)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 }
    })
)
```

## 저역통과 필터

이동평균은 쓰기 쉽고 이해하기 쉽지만 몇 가지 한계가 있습니다:

- 윈도우 안의 모든 샘플에 같은 가중치를 주기 때문에 최근 추세를 반영하는 속도가 느립니다.
- 값이 크게 변할 때 반응이 둔합니다.

이를 보완하기 위해 평균을 계산할 때 윈도우 안의 최근 값과 오래된 값에 서로 다른 가중치를 주는 방법을 흔히 사용합니다.

**SCRIPT 사용:**
```js
SCRIPT({
    const filter = require("@jsh/filter")
    const lowpass = new filter.Lowpass(0.40);
    const { arrange } = require("@jsh/generator");
    $.result = { columns: ["val", "sig", "lpf"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, lowpass.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_LOWPASS(2, $sig + $noise, 0.40)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 }
    })
)
```

## 칼만 필터

`MAP_KALMAN()` 함수의 `model()` 인자는 수학적 시스템 변수를 나타내는 값을 받습니다. 최적의 시스템 값을 결정하는 방법은 이 문서의 범위를 벗어납니다. 다만 실무에서는 TQL에서 간단한 칼만 필터 모델을 적용해보며 경험적으로 최적 파라미터를 찾아갈 수 있습니다.

아래 예제는 모델 값을 바꿨을 때 그래프가 어떻게 달라지는지 보여줍니다. 여러 모델 값을 바꿔가며 그래프의 반응을 확인해 보세요.

**SCRIPT 사용:**
```js
SCRIPT({
    const filter = require("@jsh/filter")
    const kalman = new filter.Kalman(0.1, 0.5, 1.0);
    const { arrange } = require("@jsh/generator");
    var ts = require("@jsh/system").now();
    $.result = { columns: ["val", "sig", "kalman"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        ts = ts.Add(1000000000)
        $.yield( val, sig+noise, kalman.eval(ts, sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"kalman" },
        ],
        legend: { bottom: 10 },
    })
)
```

**SET-MAP 사용:**
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_KALMAN(2, $sig + $noise, model(0.1, 0.6, 1.0))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"kalman" },
        ],
        legend: { bottom: 10 }
    })
)
```
