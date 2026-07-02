# machdeployeradmin Deployer Management Tool

You can check the status of the Deployer, or directly issue the Deployer's startup/shutdown/stop commands.

Normally the fastest way to issue the commands is through machcoordinatoradmin, but if not possible, you must use machdeployeradmin directly.

Only exists in Cluster Edition Package.

## Options and Features

```
mach@localhost:~$ machdeployeradmin -h
```

| Options | Description |
|--|--|
| -u, --startup | Runs Deployer process |
| -s, --shutdown | Terminates Deployer process |
| -k, --kill | Stops Deployer process |
| -c, --createdb | Creates Deployer meta |
| -d, --destroydb | Deletes Deployer meta |
| -i, --silence | Runs without output |
| -e, --check | Checks to see if Deployer process is running |

## Usage Examples

### Start Deployer

```bash
machdeployeradmin -u
```

### Check Deployer status

```bash
machdeployeradmin -e
```

Output when running:

```
Machbase Deployer is running with pid(29373)!
```

### Shutdown Deployer

```bash
machdeployeradmin -s
```

### Force stop Deployer

```bash
machdeployeradmin -k
```

### Create Deployer metadata

```bash
machdeployeradmin -c
```

### Destroy Deployer metadata

```bash
machdeployeradmin -d
```
