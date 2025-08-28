---
title: Releases
type: docs
weight: 10
toc: false
---


### Latest version {{< neo_latestver >}}

Choose the latest version for your platform.

| OS         | Architecture   |  Download |
|:-----------|:---------------|:----------|
| Linux      | arm64          | [machbase-neo-{{< neo_latestver >}}-linux-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip)   |
| Linux      | x64            | [machbase-neo-{{< neo_latestver >}}-linux-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip)   |
| Linux      | arm32          | [machbase-neo-{{< neo_latestver >}}-linux-arm32.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip)   |
| macOS      | arm64          | [machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip) |
| macOS      | x64            | [machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip) |
| Windows    | x64     | [machbase-neo-{{< neo_latestver >}}-windows-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip) |

### What about other Linux

If the pre-built packages are not compatible with your Linux distribution, you can still build from the source code on your system.

1. Ensure you have Go 1.24 and gcc installed.
2. Clone the neo-server repository from [GitHub](https://github.com/machbase/neo-server).
3. Run `go run mage.go install-neo-web` to download the web UI for Machbase Neo.
4. Run `go run mage.go machbase-neo` to build Machbase Neo.
5. Locate the executable binary in `./tmp/machbase-neo`.
6. Copy the executable binary to the directory where you want to install.

### What's Changed {{< neo_latestver >}}

[Changes](https://github.com/machbase/neo-server/releases/tag/{{< neo_latestver >}})

### How to upgrade from the previous v8.0.x version

The upgrade process is straightforward and involves replacing the executable file.

1. Shut down the machbase-neo process.
2. Replace the executable file `machbase-neo` (or `machbase-neo.exe`).
3. Start the machbase-neo process.

### Previous releases

Find previously released versions in [here](https://github.com/machbase/neo-server/releases).


{{< callout type="warning" emoji="⚠️">}}
**The edge and fog editions** of the previous **v1.5.0** -
Since v1.5.0, the editions are integrated into the single "standard" edition.<br/>
If you plan to run old version of machbase-neo on a small device such as Raspberry Pi, select the Edge edition.<br/>
For machines with larger memory and more CPU cores, such as a personal workstation or server, choose the Fog edition.
{{< /callout >}}

### SDK with CLASSIC

This releases are the legacy MACHBASE DBMS and application driver such as JDBC, ODBC and C client library.

| OS         | Architecture   |  Download |
|:-----------|:---------------|:----------|
| Linux      | x64            | [machbase-SDK-8.0.39.official-LINUX-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.39/machbase-SDK-8.0.39.official-LINUX-X86-64-release.tgz) |
| Linux      | arm64          | [machbase-SDK-8.0.31.official-LINUX-ARM_CORTEX_A53-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.31/machbase-SDK-8.0.31.official-LINUX-ARM_CORTEX_A53-64-release.tgz) |
| Windows    | x64            | [machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi](https://github.com/machbase/packages/releases/download/8.0.32/machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi)
| Windows    | x86            | [machbase-SDK-8.0.23.official-WINDOWS-X86-32-release.msi](https://github.com/machbase/packages/releases/download/8.0.23/machbase-SDK-8.0.23.official-WINDOWS-X86-32-release.msi) |
| macOS      | arm64          | [machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.2/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz) |
| macOS      | x64            | [machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.0.2/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz) |