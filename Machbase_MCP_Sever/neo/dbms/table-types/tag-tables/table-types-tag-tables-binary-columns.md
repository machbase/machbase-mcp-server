# Binary Columns

## Overview

`BINARY(n)` in Tag tables stores fixed-length binary values for sensor frames.
It is rejected in other table types or protocols. Length must be `1~32K-1
(1~32767)` bytes. Indexes cannot be created on binary columns.

## DDL Rules

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- Valid length: `1 <= n <= 32767` (32K-1).
- Out-of-range sizes cause create-time errors (for example `BINARY(0)`).
- `LENGTH` and `DESC` show the declared byte length (not hex width).

## Input Rules (all paths)

- Input format: hex string, optional `0x` prefix, case-insensitive.
- Odd hex length pads a leading nibble with 0 (for example `0xF` → `0x0F`).
- Shorter than the declared length pads trailing `0x00`; longer raises an
  error.
- Invalid hex or over-length input returns
  `[ERR-02233: Error occurred at column (n): (Invalid insert value.)]`.
- NULL is allowed.

```sql
-- frame binary(4)
INSERT INTO t1 VALUES('k1', '2024-01-01', '0x01');        -- stores 01 00 00 00
INSERT INTO t1 VALUES('k2', '2024-01-01', '0x0FFF');      -- stores 0F FF 00 00
INSERT INTO t1 VALUES('k3', '2024-01-01', '0xFFFFFFFF');  -- OK
INSERT INTO t1 VALUES('k4', '2024-01-01', '0xF');         -- stores 0F 00 00 00
INSERT INTO t1 VALUES('k5', '2024-01-01', '0xFFFFFFFFF'); -- error: length exceeded
```

## Output and Tooling Notes

- machsql displays uppercase hex without the `0x` prefix; output width follows
  the declared length (including padding).
- machloader: declare `BINARY(n)` in the schema; odd-length hex pads, invalid
  hex or over-length values fail.
- REST append: JSON string is decoded as hex; falls back to the legacy base64
  path only if hex parsing fails.
- CLI/ODBC/Java/C#/Node drivers send/receive fixed-length buffers; metadata
  `LENGTH` is the byte length.