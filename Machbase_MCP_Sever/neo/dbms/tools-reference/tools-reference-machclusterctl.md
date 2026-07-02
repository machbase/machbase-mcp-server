# machclusterctl Cluster Management Tool

`machclusterctl` is a command-line tool for installing and operating Machbase Cluster Edition with a YAML file. Operators declare the desired cluster layout in `cluster.yaml`; `machclusterctl` compares the desired state with the current state and executes only the necessary operations.

> **Note**: machclusterctl and the YAML-based cluster workflow were added in Machbase 8.5.3.

## Subcommands

| Command | Purpose |
|---------|---------|
| `validate` | Check YAML syntax, required values, port conflicts, and topology |
| `install` | Install a new cluster into an empty environment |
| `apply` | Apply YAML changes to a running cluster |
| `upgrade` | Upgrade nodes when the package changes |
| `status` | Show the current cluster state |
| `connect` | Connect with machsql using a broker or warehouse alias |
| `start` | Start all nodes, nodes by type, or a specific node |
| `stop` | Stop all nodes, nodes by type, or a specific node |
| `export` | Export the running cluster topology as YAML |
| `destroy` | Remove cluster installation traces |

## Global Options

| Option | Description |
|--------|-------------|
| `-f`, `--file` | YAML file to use (default: `./cluster.yaml`) |
| `--dry-run` | Print checks and the execution plan without changing anything |
| `-y`, `--yes` | Run without confirmation prompts |
| `-v`, `--verbose` | Print detailed progress logs |
| `-s`, `--silent` | Suppress progress logs |
| `--coordinator` | Primary coordinator home for commands run without a YAML file |

## Typical Workflow

Validate, preview, and install a new cluster:

```bash
machclusterctl validate -f cluster.yaml
machclusterctl install -f cluster.yaml --dry-run
machclusterctl install -f cluster.yaml --yes
machclusterctl status
```

After installation, edit the YAML file and apply the changes:

```bash
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

## cluster.yaml Structure

The YAML file describes the whole cluster topology.

- `version` — schema version (use `"1"`).
- `cluster` — the main cluster definition:
  - `name` — cluster identifier.
  - `hosts` — host alias to address mappings.
  - `package` — installation package name and path.
  - `ssh` — common SSH settings (e.g. `key_file`).
  - `defaults` — per-type default ports and paths.
  - `coordinators[]`, `deployers[]`, `lookup[]`, `brokers[]`, `warehouse_groups[]` — node definitions.

Node fields by role:

- **Coordinator / Deployer**: `alias`, `host`, `role` (coordinator only: `primary` / `secondary`), `cluster_link_port`, `http_admin_port`, `home_path`.
- **Lookup**: `alias`, `host`, `deployer`, `type` (`master` / `monitor` / `slave`), `cluster_link_port`, `http_admin_port`, `home_path`.
- **Broker / Warehouse**: `alias`, `host`, `deployer`, `cluster_link_port`, `http_admin_port`, `service_port`, `home_path`, `dbs_path`.

### Minimal Example

```yaml
version: "1"

cluster:
  name: mc-minimal

  hosts:
    node1:
      address: machbase@192.168.0.11
    node2:
      address: machbase@192.168.0.12

  package:
    name: machbase
    path: /machbase/packages/machbase-ent-release-lightweight.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /machbase/lookup
      cluster_link_port: 5301
      http_admin_port: 5302
    broker:
      home_path: /machbase/broker
      cluster_link_port: 5401
      http_admin_port: 5402
      service_port: 5656
    warehouse:
      home_path: /machbase/warehouse
      cluster_link_port: 5501
      http_admin_port: 5502
      service_port: 5500

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
```
