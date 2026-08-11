# Managing Tag Metadata

## Understanding Tag Metadata

Tag metadata represents the identity and additional information of sensors or data sources in Machbase. Think of it as a registry of all your sensors - each tag has a unique name and can have associated descriptive information.

## Basic Tag Metadata Operations

### Creating Simple Tag Metadata

When you create a tag table, you define the structure. To actually use it, you need to register tag names:

```sql
-- Create the tag table first
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
NAME                          varchar             20
TIME                          datetime            31
VALUE                         double              17
```

### Inserting Tag Names

Register a new sensor/tag:

```sql
Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.
```

### Viewing Tag Metadata

Machbase provides a special table `_tag_meta` to view all registered tags:

```sql
Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
1                    TAG_0001
[1] row(s) selected.
```

The ID is automatically assigned by the system.

### Updating Tag Names

You can modify tag names when needed:

```sql
Mach> update tag metadata set name = 'NEW_0001' where NAME = 'TAG_0001';
1 row(s) updated.

Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
1                    NEW_0001
[1] row(s) selected.
```

### Deleting Tag Metadata

Remove tag metadata when it's no longer needed:

```sql
Mach> delete from tag metadata where name = 'NEW_0001';
1 row(s) deleted.

Mach> select * from _tag_meta;
ID                   NAME
----------------------------------------------
[0] row(s) selected.
```

> **Important**: You can only delete tag metadata if no actual sensor data references it.

If the `WHERE` clause is omitted, all metadata rows in the tag table are deleted.

```sql
DELETE FROM sensors METADATA;
```

- If any matched tag still has data rows, the whole statement fails; metadata for tags that are still in use cannot be deleted.
- Even for a full metadata delete, if any target tag is still in use, the whole statement fails without partially deleting metadata rows.

To delete metadata for a tag that is still in use, delete the data rows for that tag first, then run the metadata delete again.

```sql
DELETE FROM sensors WHERE name = 'TEMP_001';
DELETE FROM sensors METADATA;
```

## Working with Additional Metadata

### Creating Rich Metadata Structure

Add descriptive information beyond just the tag name:

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized)
metadata (type short, create_date datetime, srcip ipv4);

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
NAME                          varchar             20
TIME                          datetime            31
VALUE                         double              17
[ META-COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
TYPE                          short               6
CREATE_DATE                   datetime            31
SRCIP                         ipv4                15
```

### Inserting with Partial Metadata

You can insert just the tag name - other fields will be NULL:

```sql
Mach> insert into tag metadata(name) values ('TAG_0001');
1 row(s) inserted.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL
[1] row(s) selected.
```

### Inserting Complete Metadata

Or provide all metadata fields:

```sql
Mach> insert into tag metadata values ('TAG_0002', 99, '2010-01-01', '1.1.1.1');
1 row(s) inserted.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1
[2] row(s) selected.
```

### Updating Metadata Values

Update any metadata field:

```sql
Mach> update tag metadata set type = 11 where name = 'TAG_0001';
1 row(s) updated.

Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP
-------------------------------------------------------------------------------------------------------------
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1
1                    TAG_0001              11          NULL                            NULL
[2] row(s) selected.
```

> **Note**: When updating metadata, you must include the NAME column in the WHERE clause.

## Metadata Update Time

When a metadata row is created, `_LAST_UPDATE_TIME` is recorded automatically. It is updated only when a user-defined metadata value actually changes; an update that sets the same value again is treated as a no-op and preserves `_LAST_UPDATE_TIME`. It is not the last insert time of a tag data row — it is the time the metadata row was created or its metadata value actually changed. `SELECT *` and `table_alias.*` do not include `_LAST_UPDATE_TIME`; name it explicitly in the select list to retrieve it.

`_LAST_UPDATE_TIME` is managed by the server and cannot be inserted or updated directly. The following are prohibited:

```sql
INSERT INTO sensors METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);

UPDATE sensors METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

The column also cannot be used as the TAG name, included in user-defined metadata columns, or targeted by `ALTER TABLE`. Reserved names that only share the prefix (such as `_LAST_UPDATE_TIME2`) remain usable as standard columns. The reserved behavior applies only to the TAG metadata system column — a column literally named `_LAST_UPDATE_TIME` in a normal LOG, LOOKUP, or VOLATILE table behaves as an ordinary user-defined column.

An index for time-predicate queries is provided automatically on `_LAST_UPDATE_TIME`, so you do not need to create a duplicate user index on the same column.

```sql
SELECT name, location, _last_update_time
  FROM sensors METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

## JSON Metadata Columns

A metadata column can be declared as `JSON`. Do not specify a length for a `JSON` metadata column; invalid JSON text raises an error, and no automatic index is created for the raw JSON column itself.

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);

INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

### Query JSON Paths

Use the `->` operator (or JSON dot shorthand) to query JSON metadata; the same path expression also works in normal tag queries.

```sql
SELECT name, info->'$.name', info->'$.ship.status'
  FROM ships METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;

SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY';
```

Path notation rules:
- Simple key `$.name`, nested key `$.ship.status`.
- Use bracket notation when the key name contains `.` or `-`: `info->'$[''ship.owner'']'`, `info->'$[''ship-owner'']'`.

### JSON Path Indexes

Define frequently queried paths at table-creation time. Strings inside `INDEX(...)` are interpreted as JSON paths (`'name'` → `$.name`, `'ship.status'` → `$.ship.status`); use full JSONPath for special keys.

```sql
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
)
-- special key: info JSON INDEX('$[''ship.owner'']')
```

Add or drop an index later:

```sql
CREATE INDEX idx_ship_owner ON ships METADATA (info->'$.owner');
DROP INDEX idx_ship_owner;
```

JSON path indexes work mainly for string comparisons. A string-literal comparison (`info->'$.num' = '10'`) can use the index; a numeric-literal comparison (`info->'$.num' = 10`) may fall back to a full scan.

### Partial JSON Updates

Update part of a JSON metadata document without rewriting the whole document.

```sql
-- Store a SQL scalar as a JSON scalar
UPDATE ships METADATA SET info = JSON_SET(info, '$.ship.status', 'DONE') WHERE name = 'SHIP_001';

-- Parse a string as JSON and store it as an object/array
UPDATE ships METADATA SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}') WHERE name = 'SHIP_001';

-- Remove a member or subtree
UPDATE ships METADATA SET info = JSON_REMOVE(info, '$.owner.team') WHERE name = 'SHIP_001';
```

Rules:
- `JSON_SET(..., path, NULL)` stores JSON `null`; `JSON_SET_JSON(..., path, NULL)` returns SQL `NULL`.
- If the JSON document argument is `NULL`, the result is SQL `NULL`. If the path is `NULL` or empty, an error is raised.
- `JSON_REMOVE` on a missing path is a no-op; `JSON_REMOVE(..., '$')` is not allowed.
- Partial mutation is supported for object paths; array-element mutation such as `$.items[0]` is not supported.

## RESTful API for Tag Metadata

### Getting All Tags

Retrieve a list of all tags via HTTP:

```bash
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/list"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"NAME": "TAG_0001"},
          {"NAME": "TAG_0002"}]}
```

### Getting Tag Time Ranges

Find the min and max timestamp for a tag (useful for charting):

```bash
# Time range for all tags
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/range/"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}

# Time range for a specific tag
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0001"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-01-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
```

## Real-World Example

Here's a complete example showing how to set up temperature sensor metadata:

```sql
-- Create tag table with metadata
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(50),
    sensor_type VARCHAR(20),
    installed_date DATETIME,
    ip_address IPV4
);

-- Register sensors with full metadata
INSERT INTO sensors METADATA VALUES (
    'TEMP_BUILDING_A_FLOOR1', 'Building A - Floor 1', 'Temperature', '2024-01-15', '192.168.1.101'
);

INSERT INTO sensors METADATA VALUES (
    'TEMP_BUILDING_A_FLOOR2', 'Building A - Floor 2', 'Temperature', '2024-01-15', '192.168.1.102'
);

-- View all registered sensors
SELECT * FROM _sensors_meta;
```

## Best Practices

1. **Use Descriptive Names**: Tag names should be meaningful and follow a consistent naming convention
2. **Leverage Metadata**: Store static information in metadata columns to avoid redundancy in sensor data
3. **Plan Your Schema**: Define all needed metadata columns when creating the tag table
4. **Regular Cleanup**: Remove unused tag metadata to keep the registry clean
5. **API Access**: Use the RESTful API for integration with external applications

## Next Steps

- Learn about [Inserting Tag Data](../inserting-data) to start recording sensor readings
- Explore [Querying Tag Data](../querying-data) for data retrieval
- Understand [Tag Indexes](../tag-indexes) for performance optimization
