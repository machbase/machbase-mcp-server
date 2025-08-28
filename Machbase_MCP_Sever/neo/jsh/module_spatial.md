---
title: "@jsh/spatial"
type: docs
weight: 70
---

{{< neo_since ver="8.0.52" />}}

## haversine()

`haversine()` is for calculating the Haversine distance.
The Haversine formula is used to calculate the great-circle distance
between two points on a sphere, given their latitudes and longitudes.

**Usage example**

```js {linenos=table,hl_lines=[4],linenostart=1}
m = require("@jsh/spatial");
latLon1 = [45.04, 7.42];  // Turin, Italy
latLon2 = [3.09, 101.42]; // Kuala Lumpur, Malaysia
distance = m.haversine({radius: 6371, coordinates:[latLon1, latLon2]})
console.log(distance.toFixed(0), "Km");

// 10078 Km
```
