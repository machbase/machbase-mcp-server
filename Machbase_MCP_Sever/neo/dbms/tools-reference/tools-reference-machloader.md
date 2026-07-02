# machloader Import/Export Tool

machloader is used to import/export text file data to the Machbase server.
It works with CSV files by default, but it also supports other formats.

## Features

* machloader can specify a datetime type in the schema file. The datetime type specified must be of the type supported by the Machbase server. One datetime type can be applied to all fields, and each field can have a different format.
* To delete and input the input target table data, use the "-m replace" option.
* machloader does not verify the schema and data file consistency. The user must check that the schema, tables, and data files meet the consistency.
* machloader supports APPEND mode by default.
* machloader does not use the `_ARRIVAL_TIME` column by default. You must use the "-a" option to import/export the corresponding column data.

## Options

| Option | Full Option | Description |
|--|--|--|
| -i | --import | Data import mode |
| -o | --export | Data export mode |
| -c | --schema | Generate schema from existing table |
| -t | --table | Target table name |
| -f | --form | Schema file specification |
| -d | --data | Data file path |
| -m | --mode | Import method (append/replace) |
| -D | --delimiter | Field separator (default: comma) |
| -n | --newline | Record separator (default: '\n') |
| -e | --enclosure | Field enclosure character |
| -a | N/A | Include _ARRIVAL_TIME column |
| -F | --dateformat | Column datetime format specification |
| -C | --create | Auto-generate table if missing |
| -H | --header | CSV header row handling |
| -b | --badfile | Bad record output file |
| -l | --logfile | Log file path |
| -s | --server | Server IP (default: 127.0.0.1) |
| -P | --port | Server port (default: 5656) |
| -u | --user | Username (default: SYS) |
| -p | --password | User password (default: MANAGER) |
| -h | --help | Displays options |

## Import Examples

### Basic CSV import

```bash
machloader -i -t my_table -d data.csv
```

### Import with specific server

```bash
machloader -i -t my_table -d data.csv -s 192.168.1.100 -P 5656 -u SYS -p MANAGER
```

### Import with schema file

```bash
machloader -i -t my_table -d data.csv -f my_schema.fmt
```

### Replace mode (delete existing data first)

```bash
machloader -i -t my_table -d data.csv -m replace
```

### Import with date format

```bash
machloader -i -t my_table -d data.csv -F "YYYY-MM-DD HH24:MI:SS"
```

### Auto-create table

```bash
machloader -i -t my_table -d data.csv -C
```

### Import with header row

```bash
machloader -i -t my_table -d data.csv -H
```

## Export Examples

### Basic CSV export

```bash
machloader -o -t my_table -d output.csv
```

### Export with custom delimiter

```bash
machloader -o -t my_table -d output.tsv -D "\t"
```

## Schema File

### Generate schema from existing table

```bash
machloader -c -t my_table -f my_schema.fmt
```

### Schema file format

The schema file is a text file that describes the column mapping between the data file and the target table.

Key schema directives:

* `DATEFORMAT` - specify datetime format per column
* `IGNORE` - skip a column during import

### Date format tokens

Supported datetime format tokens:

| Token | Description |
|--|--|
| YYYY | 4-digit year |
| MM | Month (01-12) |
| DD | Day (01-31) |
| HH24 | Hour (00-23) |
| HH12 | Hour (01-12) |
| MI | Minute (00-59) |
| SS | Second (00-59) |
| mmm | Millisecond |
| uuuuuu | Microsecond |
| nnnnnnnnn | Nanosecond |

Special format values:

* `unixtimestamp` - Unix epoch seconds
* `nanotimestamp` - Unix epoch nanoseconds

## Bad File and Logging

When import errors occur, machloader creates:

* Bad file (-b): Contains records that failed to import
* Log file (-l): Contains detailed error information

```bash
machloader -i -t my_table -d data.csv -b bad_records.csv -l import.log
```

## Notes

* machloader does not verify schema and data file consistency
* REPLACE mode deletes all existing data before import - use with caution
* The `-a` flag is required to handle `_ARRIVAL_TIME` column data
* Default connection: 127.0.0.1:5656 with user SYS
