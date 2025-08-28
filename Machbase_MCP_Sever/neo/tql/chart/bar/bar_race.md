---
title: Bar Race
type: docs
weight: 150
---

```js {{linenos=table,linenostart=1}}
CSV( file("https://docs.machbase.com/assets/example/life-expectancy-table.csv") )
CHART(
    chartOption({
        grid: {
            top: 10,
            bottom: 30,
            left: 150,
            right: 80
        },
        xAxis: {
            max: "dataMax",
            axisLabel: { }
        },
        dataset: {
            source: [],
        },
        yAxis: {
            type: "category",
            inverse: true,
            max: 10,
            axisLabel: {
                show: true,
                fontSize: 14,
                rich: {
                    flag: {
                        fontSize: 25,
                        padding: 5
                    }
                }
            },
            animationDuration: 300,
            animationDurationUpdate: 300
        },
        series: [
            {
                realtimeSort: true,
                type: "bar",
                seriesLayoutBy: "column",
                itemStyle: {
                    color:""
                },
                encode: {
                    x: 0, y: 3
                },
                label: {
                    show: true,
                    precision: 1,
                    position: "right",
                    valueAnimation: true,
                    fontFamily: "monospace"
                }
            }
        ],
        animationDuration: 0,
        animationDurationUpdate: 2000,
        animationEasing: "linear",
        animationEasingUpdate: "linear",
        graphic: {
            elements: [
                {
                    type: "text",
                    right: 40,
                    bottom: 60,
                    style: {
                        text: "loading...",
                        font: "bolder 50px monospace",
                        fill: "rgba(100, 100, 100, 0.25)"
                    },
                    z: 100
                }
            ]
        }
    }),
    chartJSCode({
        fetch("https://fastly.jsdelivr.net/npm/emoji-flags@1.3.0/data.json").then( function(rsp) {
            return rsp.json();
        }).then( function(flags) {
            const data = [];
            for (let i = 0; i < _columns[0].length; ++i) {
                var row = [];
                for (let c = 0; c < _columns.length; ++c) {
                    row.push(_columns[c][i]);
                }
                data.push(row);
            }

            const years = [];
            for (let i = 0; i < data.length; ++i) {
                if (years.length === 0 || years[years.length - 1] !== data[i][4]) {
                    years.push(data[i][4]);
                }
            }

            const updateFrequency = 2000;
            const countryColors = {
                "Australia": "#00008b",
                "Canada": "#f00",
                "China": "#ffde00",
                "Cuba": "#002a8f",
                "Finland": "#003580",
                "France": "#ed2939",
                "Germany": "#000",
                "Iceland": "#003897",
                "India": "#f93",
                "Japan": "#bc002d",
                "North Korea": "#024fa2",
                "South Korea": "#000",
                "New Zealand": "#00247d",
                "Norway": "#ef2b2d",
                "Poland": "#dc143c",
                "Russia": "#d52b1e",
                "Turkey": "#e30a17",
                "United Kingdom": "#00247d",
                "United States": "#b22234"
            };
            function getFlag(countryName) {
                if (!countryName) {
                    return '';
                }
                return (
                    flags.find(function (item) {
                        return item.name === countryName;
                    }) || {}
                ).emoji;
            }
            
            let startIndex = 10;
            let startYear = years[startIndex];
            let option = _chart.getOption()
            option.dataset.source = data.slice(1).filter(function (d) {
                return d[4] === startYear;
            });
            option.xAxis[0].axisLabel.formatter = function (n) {
                return Math.round(n) + '';
            };
            option.yAxis[0].axisLabel.formatter = function (value) {
                return value + "{flag|" + getFlag(value) + "}";
            };
            option.series[0].itemStyle.color = function (param) {
                return countryColors[param.value[3]] || "#5470c6";
            };
            option.graphic[0].elements[0].style.text = startYear;
            _chart.setOption(option);
            for (let i = startIndex; i < years.length - 1; ++i) {
                (function (i) {
                    setTimeout(function () {
                        updateYear(years[i + 1]);
                    }, (i - startIndex) * updateFrequency);
                })(i);
            }
            function updateYear(year) {
                let source = data.slice(1).filter(function (d) {
                    return d[4] === year;
                });
                option.series[0].data = source;
                option.graphic[0].elements[0].style.text = year;
                _chart.setOption(option);
            }
        }).catch(function(err){
            console.warn("data error, fetch resource", err)
        });
    })
)
```

