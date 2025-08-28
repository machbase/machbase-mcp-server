---
title: Airline on Globe
type: docs
weight: 1010
---

```js {{linenos=table,linenostart=1}}
CSV(file("https://docs.machbase.com/assets/example/flights.csv"))
DROP(1) // skip header
// |   0         1     2    3      4     5    6
// +-> flights   name1 lon1 lat1   name2 lon2 lat2
// |
MAPVALUE(0, latlon( parseFloat(value(2)), parseFloat(value(3))))
MAPVALUE(1, latlon( parseFloat(value(5)), parseFloat(value(6))))
// |   0     1      2    3      4     5    6
// +-> loc1  loc2   lon1 lat1   name2 lon2 lat2
// |
MAPVALUE(0, list(value(0), value(1)))
// |   0            1         2    3      4     5    6
// +-> [loc1,loc2]  (lat,lon) lon1 lat1   name2 lon2 lat2
// |
POPVALUE(1, 2, 3, 4, 5, 6)
// |   0
// +-> [loc1,loc2]
// |
CHART(
    plugins("gl"),
    chartOption({
        backgroundColor: "#000",
        globe: {
            baseTexture: "https://docs.machbase.com/assets/example/world.topo.bathy.200401.jpg",
            heightTexture: "https://docs.machbase.com/assets/example/bathymetry_bw_composite_4k.jpg",
            shading: "lambert",
            light: {
                ambient: {
                    intensity: 0.4
                },
                main: {
                    intensity: 0.4
                }
            },
            viewControl: {
                autoRotate: false
            }
        },
        series: {
            type: "lines3D",
            coordinateSystem: "globe",
            blendMode: "lighter",
            lineStyle: {
                width: 0.5,
                color: "rgb(50, 50, 150)",
                opacity: 0.1
            },
            data: column(0)
        }
    })
)
```

