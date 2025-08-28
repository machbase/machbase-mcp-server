---
title: Client in JavaScript
type: docs
weight: 61
---

## Query

**JSON**

Set `format=json` or omit it for the default.

```js {{linenos=table}}
q = "select * from example"
fetch(`http://127.0.0.1:5654/db/query?q=${encodeURIComponent(q)}`)
  .then(res => {
    return res.json();
  })
  .then(data => {
    console.log(data)
  });
```

**CSV**

Set `format=csv` explicitly.

```js {{linenos=table}}
q = "select * from example"
fetch(`http://127.0.0.1:5654/db/query?q=${encodeURIComponent(q)}&format=csv`)
  .then(res => {
    return res.text();
  })
  .then(data => {
    console.log(data)
  });
```

## Write

**JSON**

```js  {{linenos=table,hl_lines=[14]}}
payload = {
    data: {
        columns: ["NAME", "TIME", "VALUE"],
        rows: [
            ['temperature',1677033057000000000,21.1],
            ['humidity',1677033057000000000,0.53]
        ]    
    }
}

fetch('http://127.0.0.1:5654/db/write/example', {
    method: 'POST',
    headers: {
        'Content-Type':'application/json'
    },
    body: JSON.stringify(payload)
  });
```

**CSV**

```js  {{linenos=table,hl_lines=[7]}}
payload = `temperature,1677033057000000000,21.1
humidity,1677033057000000000,0.53`

fetch('http://127.0.0.1:5654/db/write/example', {
    method: 'POST',
    headers: {
        'Content-Type':'text/csv'
    },
    body: payload
  });
```
