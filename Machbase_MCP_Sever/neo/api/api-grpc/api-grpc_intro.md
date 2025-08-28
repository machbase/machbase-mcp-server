---
title: gRPC API
type: docs
weight: 130
---

gRPC is the first-class-api of machbase, any program language that support gRPC can utilize it's full functionalities.

{{< callout type="warning" >}}
Since gRPC interface provides low level api, it is very critical that client program should properly use them. In any cases of mis-uses, it may lead machbase not to work properly.
{{< /callout >}}

### proto file

The latest version of .proto file is hosted in github. Please [find it from github](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

## In this chapter

{{< children_toc />}}
