---
title: Word Cloud
type: docs
weight: 940
---

```js {{linenos=table,linenostart=1}}
SCRIPT({
    counter = {};
    data = [];
},{
    const http = require("@jsh/http");
    req = http.request("https://docs.machbase.com/assets/example/wordcount.txt")
    req.do((rsp) => {
        content = rsp.text();
        words = content.split(/\s+/)
        for(w of words) {
            w = w.toLowerCase();
            if(counter[w]) {
                counter[w].count++;
            } else {
                counter[w] = {count:1}
            }
        }
    })
},{
    Object.keys(counter).forEach(w =>{
        data.push({name: w, value: counter[w].count})
    })
    $.yield({
        series: {
            type: "wordCloud",
            gridSize: 4,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: "circle",
            width: 580,
            height: 580,
            drawOutOfBound: false,
            left: "center",
            top: "center",
            data: data,
            emphasis: {
                focus: "self",
                textStyle: {
                    textShadowBlur: 10,
                    textShadowColor: "#333"
                }
            },
            layoutAnimation: true,
            textStyle: {
                fontFamily: "sans-serif",
                fontWeight: "bold",
            }
        }
    })
})
CHART(
    plugins("wordcloud"),
    chartOption({}),
    chartJSCode({
        _chartOption.series.textStyle.color = function() {
            let r = Math.round(Math.random() * 160);
            let g = Math.round(Math.random() * 160);
            let b = Math.round(Math.random() * 160);
            return `rgb(${r},${g},${b})`;
        }
        _chart.setOption(_chartOption);
    })
)
```

```js
FAKE(csv(
`Deep Learning,6181
Computer Vision,4386
Artificial Intelligence,4055
Neural Network,3500
Algorithm,3333
Model,2700
Supervised,2500
Unsupervised,2333
Natural Language Processing,1900
Chatbot,1800
Virtual Assistant,1500
Speech Recognition,1400
Convolutional Neural Network,1325
Reinforcement Learning,1300
Training Data,1250
Classification,1233
Regression,1000
Decision Tree,900
K-Means,875
N-Gram Analysis,850
Microservices,833
Pattern Recognition,790
APIs,775
Feature Engineering,700
Random Forest,650
Bagging,600
Anomaly Detection,575
Naive Bayes,500
Autoencoder,400
Backpropagation,300
TensorFlow,290
word2vec,280
Object Recognition,250
Python,235
Predictive Analytics,225
Predictive Modeling,215
Optical Character Recognition,200
Overfitting,190
JavaScript,185
Text Analytics,180
Cognitive Computing,175
Augmented Intelligence,160
Statistical Models,155
Clustering,150
Topic Modeling,145
Data Mining,140
Data Science,138
Semi-Supervised Learning,137
Artificial Neural Networks,125
`))
SCRIPT({
    data = [];
},{
    data.push({name: $.values[0], value: $.values[1]})
},{
    $.yield({
        series: {
            type: "wordCloud",
            gridSize: 8,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: "circle",
            width: 580,
            height: 580,
            drawOutOfBound: false,
            left: "center",
            top: "center",
            data: data,
            emphasis: {
                focus: "self",
                textStyle: {
                    textShadowBlur: 10,
                    textShadowColor: "#333"
                }
            },
            layoutAnimation: true,
            textStyle: {
                fontFamily: "sans-serif",
                fontWeight: "bold",
            }
        }
    })
})
CHART(
    plugins("wordcloud"),
    chartOption({}),
    chartJSCode({
        _chartOption.series.textStyle.color = function() {
            return 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')';
        }
        _chart.setOption(_chartOption);
    })
)
```

