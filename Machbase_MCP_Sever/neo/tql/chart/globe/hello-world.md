---
title: Hello World
type: docs
weight: 1000
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["world.topo.bathy.200401.jpg", "starfield.jpg", "pisa.hdr"]
}) )

MAPVALUE(0, "https://docs.machbase.com/assets/example/"+value(0))
MAPVALUE(1, "https://docs.machbase.com/assets/example/"+value(1))
MAPVALUE(2, "https://docs.machbase.com/assets/example/"+value(2))

CHART(
    plugins("gl"),
    chartOption({
        backgroundColor: "#000",
        globe: {
            baseTexture: column(0)[0],
            heightTexture: column(0)[0],
            displacementScale: 0.04,
            shading: "realistic",
            environment: column(1)[0],
            realisticMaterial: {
                roughness: 0.9
            },
            postEffect: {
                enable: true
            },
            light: {
                main: {
                    intensity: 5,
                    shadow: true
                },
                ambientCubemap: {
                    texture: column(2)[0],
                    diffuseIntensity: 0.2
                }
            }
        }
    })
)
```

