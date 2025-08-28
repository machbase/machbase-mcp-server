---
title: Sankey
type: docs
weight: 930
---

```js {{linenos=table,linenostart=1}}
FAKE(csv(
`a,a1,5
a,a2,3
b,b1,8
a,b1,3
b1,a1,1
b1,c,2
`))
SCRIPT({
    data = [];
},{
    data.push({source: $.values[0], target: $.values[1], value: $.values[2]})
},{
    $.yield({
        series: {
            type: "sankey",
            layout: "none",
            emphasis: {
                focus: "adjacency"
            },
            links: data,
            data: [
                {name: "a"}, {name: "b"}, {name: "a1"}, {name: "a2"}, {name: "b1"}, {name: "c"}
            ]
        }
    })
})
CHART()
```

