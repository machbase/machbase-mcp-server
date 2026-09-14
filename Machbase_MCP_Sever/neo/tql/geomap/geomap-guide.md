# Machbase Neo GEOMAP()

**버전 8.0.44부터 사용 가능**

**문법**: `GEOMAP( [geomapID()] [, tileTemplate()] [, size()] )` 

`GEOMAP`은 지도를 생성하고, 주어진 좌표를 기준으로 마커와 도형을 표시합니다.
`CHART`와 비슷하게 동작하지만 스칼라 값 대신 좌표를 사용합니다. 지원하는 좌표계는 WGS84입니다.

`GEOMAP()` 함수는 JavaScript 객체 형식의 입력 데이터를 처리합니다.
각 입력 객체는 `type`과 `coordinates` 필드를 반드시 포함해야 하며, `properties` 필드는 선택입니다.

`GEOMAP()` 함수의 레이어는 지정된 타입에 따라 지도 위에 렌더링되는 객체입니다.
예를 들어 타입이 `circle`인 레이어는 주어진 속성에 따라 지도에 원을 표시합니다.

## tileTemplate()

**문법**: `tileTemplate(url_template)`

지도 타일 서버 URL 템플릿입니다.
기본값은 `https://tile.openstreetmap.org/{z}/{x}/{y}.png` 입니다.

**중요:** 방화벽이나 조직 보안 정책 때문에 지도 클라이언트(웹 브라우저)가 기본 타일 서버에 접근할 수 없다면, 조직 내부에 자체 타일 서버를 운영하고 `tileTemplate()`으로 그 URL을 지정해야 합니다. 타일 서버 운영 방법은 이 문서의 범위를 벗어납니다. 자세한 내용은 다음을 참고하세요: https://wiki.openstreetmap.org/wiki/Tile_servers

## tileGrayscale()

**문법**: `tileGrayscale(scale)`

- `scale` *float* 타일 이미지의 회색조를 설정합니다. 0 ≤ scale ≤ 1.0 범위여야 합니다. (기본값: `0`)

## geomapID()

**문법**: `geomapID(id)`

자동 생성 대신 지도 id(*string*)를 직접 지정할 때 사용합니다.

## size()

**문법**: `size(width, height)`

- `width` *string* HTML 문법의 지도 너비, 예) `'800px'`
- `height` *string* HTML 문법의 지도 높이, 예) `'800px'`

## Layers

레이어는 `GEOMAP`이 지도에 표시하는 마커와 도형입니다.
`GEOMAP()`의 입력 데이터는 JavaScript 객체로 표현된 딕셔너리 구조여야 합니다.

객체는 `type`과 `coordinates` 필드를 반드시 가져야 하며, `properties` 필드는 선택입니다.

**syntax**

```js
{
    type: "circle", // marker, circleMarker, polyline ...
    coordinates: [Lat, Lon],
    properties: {
        radius: Radius,
        color: "#FF0000",
        weight: 1
    }
}
```

| 이름            | 타입          | 설명   |
|:--------------- |:--------------|:--------------|
| `type`          | `String`      | 레이어의 타입. <br/> 예: `marker`, `circle`, `circleMarker` 등 |
| `coordinates`   | `[]Float`,<br/> `[][]Float`, ... | 해당 `type`의 좌표, [위도, 경도] 순서 |
| `properties`    | `Dictionary` | `type`에 따른 다양한 옵션.<br/>Properties 참고 |

## marker

```js
FAKE(json({
    [38.9934, -105.5018]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "marker",
        coordinates: [lat, lon]
    });
})

GEOMAP()
```

## circleMarker

**속성**

| 속성        | 기본값          | 설명   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | 원형 마커의 반지름(픽셀). |

```js
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties:{
            radius: 40
        }
    });
})

GEOMAP()
```

## circle

**속성**

| 속성        | 기본값          | 설명   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | 원의 반지름(미터). |

```js
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties:{
            radius: 400
        }
    });
})

GEOMAP()
```

## polyline

```js
FAKE(json({
    [45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

## polygon

```js
FAKE(json({
    [37, -109.05],
    [41, -109.03],
    [41, -102.05],
    [37, -102.05]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polygon",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

## Properties

## 레이어 속성

| 속성        | 타입   | 기본값   | 설명   |
|:--------------- |:-------|:----------|:--------------|
| `stroke`        | Boolean| `true`    | 경로를 따라 선을 그릴지 여부. false로 두면 다각형·원의 테두리가 사라집니다. |
| `color`         | String | `'#3388ff'` | 선 색상  |
| `weight`        | Number | `3`       | 선 두께(픽셀) |
| `opacity`       | Number | `1.0`     | 마커의 불투명도.|
| `fillColor`     | String |           | 채움 색상. 기본값은 color 속성의 값입니다. |
| `fillOpacity`   | Number | `0.2`     | 채움 불투명도. |
| `popup`         | Object | `null`    | Popup 참고. |
| `tooltip`       | Object | `null`    | Tooltip 참고. |

## Popup

레이어 속성에 `popup` 객체가 있으면 사용자가 레이어를 클릭할 때 팝업 메시지를 표시합니다.

| 속성        | 타입   | 기본값    | 설명   |
|:--------------- |:-------|:-----------|:--------------|
| `content`       | String |            | 팝업 내용(텍스트/HTML). |
| `open`          | Boolean| `false`    | 초기 열림 상태 지정 |
| `maxWidth`      | Number | `300`      | 팝업 최대 너비(픽셀). |
| `minWidth`      | Number | `50`       | 팝업 최소 너비(픽셀). |

```js
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))

SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>'+name+'</b>'
            }
        }
    });
})

GEOMAP()
```

## Tooltip

**버전 8.0.44부터 사용 가능**

지도 레이어 위에 짧은 텍스트를 표시할 때 사용합니다.

| 속성         | 타입   | 기본값    | 설명   |
|:--------------- |:-------|:-----------|:--------------|
| `content`       | String |            | 팝업 내용(텍스트/HTML). |
| `open`          | Boolean| `false`    | 초기 열림 상태 지정 |
| `direction`     | String | `auto`     | 툴팁이 열릴 방향. `right,left,top,bottom,center,auto` |
| `permanent`     | Boolean| `false`    | 툴팁을 항상 열어둘지, 마우스오버 시에만 열지 |
| `opacity`       | Number | `0.9`      | 툴팁 컨테이너 불투명도 |

```js
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))
SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            tooltip: {
                content: '<b>'+name+'</b>',
                direction: "auto",
                permanent: true
            }
        }
    });
})
GEOMAP()
```

## Examples

CSV 파일에서 테스트 데이터를 불러와 "TRIP" 테이블에 넣습니다.
이 TQL은 주어진 URL에서 CSV 파일을 내려받아, 
CSV 문자열을 적절한 데이터 타입으로 변환하고,
레코드를 TRIP 테이블에 삽입합니다.

```js
// CSV Format: TIME, LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))
DROP(1) // skip header
SCRIPT({
    // create trip table, if not exists
    $.db().exec("CREATE TAG TABLE IF NOT EXISTS TRIP ("+
        "name varchar(100) primary key, "+
        "time datetime basetime, "+
        "value double summarized, "+
        "lat double, "+
        "lon double "+
    ")")
    // parse time form csv string '23-04-21 16:53:21:123000'
    function parseTime(str) { 
        y = "20"+str.substr(0,2);
        m = str.substr(3,2) - 1;
        d = str.substr(6,2);
        hours = str.substr(9, 2);
        mins = str.substr(12,2);
        secs = str.substr(15, 2);
        milli = str.substr(18, 3)
        var D = new Date(y, m, d, hours, mins, secs, milli);
        return (D.getFullYear() == y && D.getMonth() == m && D.getDate() == d) ? D : 'invalid date';
    }
}, {
    var ts = parseTime($.values[0]).getTime(); // epoch mills
    var lat = parseFloat($.values[1]);
    var lon = parseFloat($.values[2]);
    // yield name, time, value, lat, lon
    $.yield("firenze", ts, 0, lat, lon)
})
// epoch from milli to nano and to datetime type
MAPVALUE(1, time(value(1)*1000000))
// insert into trip table
INSERT("name", "time", "value", "lat", "lon", table("TRIP"))
```

## Trajectory

### SQL

```js
SQL(`SELECT time, lat, lon FROM TRIP
     WHERE name = 'firenze' ORDER BY time`)
SCRIPT({
    // time to epoch nanos to Date (javascript)
    var timestamp = new Date($.values[0].UnixNano()/1000000); 
    // coordinate [lat, lon]
    var coord = [$.values[1], $.values[2]]; 
    $.yield({
        type:"circle",
        coordinates: coord,
        properties: {
            radius: 15,
            tooltip: {
                content: ""+timestamp
            }
        }
    });
})
GEOMAP()
```

### CSV

```js
// CSV Format: TIME, LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))

DROP(1) // skip header

SCRIPT({
    var timestamp = $.values[0];
    var coord = [
        parseFloat($.values[1]), 
        parseFloat($.values[2])
    ];
    $.yield({
        type:"circle",
        coordinates: coord,
        properties: {
            radius: 15,
            tooltip: {
                content: timestamp
            }
        }
    });
})

GEOMAP()
```

## 거리와 속도

하버사인 공식으로 두 지점 사이의 이동 거리를 미터 단위로 계산하고,
두 지점의 시간 차이를 이용해 이동 속도를 시속(Km/H)으로 구합니다.

### SQL

```js
SQL(`SELECT time, lat, lon FROM TRIP
     WHERE name = 'firenze' ORDER BY time`)
// calculate the distance and speed
SCRIPT({
    var EarthRadius = 6378137.0; // meters
    function degreesToRadians(d) { return d * Math.PI / 180; }
    function distance(p1, p2) {  // haversine distance
        lat1 = degreesToRadians(p1[0]);
        lon1 = degreesToRadians(p1[1]);
        lat2 = degreesToRadians(p2[0]);
        lon2 = degreesToRadians(p2[1]);
        diffLat = lat2 - lat1;
        diffLon = lon2 - lon1;
        a = Math.pow(Math.sin(diffLat/2), 2) + Math.cos(lat1)*Math.cos(lat2)*Math.pow(Math.sin(diffLon/2), 2);
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return c * EarthRadius;
    }
    var prevLoc, prevTs, dist;
},{
    var ts = $.values[0].Unix(); // unix epoch sec.
    var coord = [$.values[1], $.values[2]];
    dist = prevLoc === undefined ? 0 : distance(prevLoc, coord);
    speed = prevTs === undefined ? 0 : dist*3.600 / (ts - prevTs);
    prevLoc = coord;
    prevTs = ts;
    $.yield({
        type:"circleMarker",
        coordinates: coord,
        properties: {
            radius: 4,
            tooltip: {
                content: "speed: "+speed.toFixed(0)+" KM/H<br/>"+
                         "dist: "+dist.toFixed(0)+" m",
            }
        }
    });
})
GEOMAP()
```

### CSV

```js
// CSV Format: TIME("23-04-21 16:53:21:568000"), LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))

// skip header, the first line
DROP(1) 

// parse time, and coordinates from strings
SCRIPT({
    function parseTime(str) { // parse '23-04-21 16:53:21'
        y = str.substr(0,2)+2000;
        m = str.substr(3,2) - 1;
        d = str.substr(6,2);
        hours = str.substr(9, 2);
        mins = str.substr(12,2);
        secs = str.substr(15, 2);
        var D = new Date(y, m, d,hours, mins, secs);
        return (D.getFullYear() == y && D.getMonth() == m && D.getDate() == d) ? D : 'invalid date';
    }
},{ 
    var ts = parseTime($.values[0]).getTime()/1000; // epoch seconds
    var lat = parseFloat($.values[1]);
    var lon = parseFloat($.values[2]);
    $.yield(ts, lat, lon);
})

// calculate the distance and speed
SCRIPT({
    var EarthRadius = 6378137.0; // meters
    function degreesToRadians(d) { return d * Math.PI / 180; }
    function distance(p1, p2) {  // haversine distance
        lat1 = degreesToRadians(p1[0]);
        lon1 = degreesToRadians(p1[1]);
        lat2 = degreesToRadians(p2[0]);
        lon2 = degreesToRadians(p2[1]);
        diffLat = lat2 - lat1;
        diffLon = lon2 - lon1;
        a = Math.pow(Math.sin(diffLat/2), 2) + Math.cos(lat1)*Math.cos(lat2)*Math.pow(Math.sin(diffLon/2), 2);
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return c * EarthRadius;
    }
    var prevLoc, prevTs, dist;
},{
    var ts = $.values[0];
    var coord = [$.values[1], $.values[2]];
    dist = prevLoc === undefined ? 0 : distance(prevLoc, coord);
    speed = prevTs === undefined ? 0 : dist*3.600 / (ts - prevTs);
    prevLoc = coord;
    prevTs = ts;
    $.yield({
        type:"circleMarker",
        coordinates: coord,
        properties: {
            radius: 4,
            tooltip: {
                content: "speed: "+speed.toFixed(0)+" KM/H<br/>"+
                         "dist: "+dist.toFixed(0)+" m",
            }
        }
    });
})
GEOMAP()
```
