# Machbase Neo JavaScript Spatial Module

## haversine()

`haversine()`은 하버사인 거리를 계산합니다.
하버사인 공식은 구면 위 두 점의 위도와 경도가 주어졌을 때
두 점 사이의 대권 거리를 계산하는 데 사용됩니다.

**사용 예제**

```js
m = require("@jsh/spatial");
latLon1 = [45.04, 7.42];  // Turin, Italy
latLon2 = [3.09, 101.42]; // Kuala Lumpur, Malaysia
distance = m.haversine({radius: 6371, coordinates:[latLon1, latLon2]})
console.log(distance.toFixed(0), "Km");

// 10078 Km
```
