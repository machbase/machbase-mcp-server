
# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [Password Policy](#password-policy)
* [AUTH KEY Authentication](#auth-key-authentication)
* [Uppercase User Name Storage](#uppercase-user-name-storage)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [Managing User Example](#managing-user-example)

## CREATE USER

**create_user_stmt:**

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
                     [ 'WITH AUTH KEY' '(' key_options ')' ]
                     [ 'PASSWORD POLICY' { 'NONE' | 'LOW' | 'HIGH' } ]
```

The syntax for creating a user is:

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```

The optional `PASSWORD POLICY` clause enforces a password strength level (see [Password Policy](#password-policy)), and the optional `WITH AUTH KEY` clause registers a public key for challenge authentication (see [AUTH KEY Authentication](#auth-key-authentication)). User names are stored in uppercase (see [Uppercase User Name Storage](#uppercase-user-name-storage)).

## DROP USER

**drop_user_stmt:**

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

The syntax for deleting a user is as follows. The SYS user can not be deleted, and if there is a table already created by the user to be deleted, an error is displayed.

```sql
-- Example
DROP USER old_user
```

## ALTER USER

**alter_user_pwd_stmt:**

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

The user can change the password through the following syntax.

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```

## Password Policy

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Password policy validates password strength for `CREATE USER` and `ALTER USER ... IDENTIFIED BY ...`. If no policy is specified, `NONE` is used for backward compatibility.

Policy levels:

- `NONE`
  - No password strength restriction is applied.
  - Password expiration time (`VALID_BEFORE`) is `NULL`.
- `LOW`
  - The password must be at least 10 characters long.
  - The password must include uppercase letters, lowercase letters, and special characters.
  - Five or more contiguous digits, increasing or decreasing digit sequences, and keyboard sequences are not allowed.
  - Password expiration time (`VALID_BEFORE`) is `NULL`.
- `HIGH`
  - All `LOW` rules are applied.
  - The current password and the most recent 24 historical passwords cannot be reused.
  - The expiration time (`VALID_BEFORE`) is automatically set to 90 days after the password is set.

```sql
CREATE USER user1 IDENTIFIED BY "Aa!StrongPwd1";
CREATE USER user2 IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY LOW;
CREATE USER user3 IDENTIFIED BY "Cc#StrongPwd3" PASSWORD POLICY HIGH;

ALTER USER user2 IDENTIFIED BY "Dd$NewPwd44";
ALTER USER user2 IDENTIFIED BY "Ee%NewPwd55" PASSWORD POLICY LOW;
ALTER USER user3 IDENTIFIED BY "Ff#NewPwd66" PASSWORD POLICY NONE;
```

Notes:

- `ALTER USER ... IDENTIFIED BY ...` validates the new password with the policy currently stored for that user.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...` validates the new password with the new policy. To change the policy you must supply a new password together with it; a policy-only statement such as `ALTER USER user_name PASSWORD POLICY HIGH` (without `IDENTIFIED BY`) is not allowed.
- When a policy is set to `HIGH`, or when the password of a `HIGH` policy user is changed, `VALID_BEFORE` is updated to 90 days from the current time.
- When a policy is set to `LOW` or `NONE`, `VALID_BEFORE` is updated to `NULL`.
- An expired account cannot log in, so the user cannot change the password with that account. Reset the password from an administrator account.

You can check the policy and expiration time in `M$SYS_USERS`.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
FROM M$SYS_USERS;
```

`PWD_POLICY_LEVEL` means `0 = NONE`, `1 = LOW`, and `2 = HIGH`. `VALID_BEFORE` is displayed in `YYYY-MM-DD` format when it has a value.

## AUTH KEY Authentication

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Machbase can register an AUTH KEY for public-key challenge authentication together with password authentication. AUTH KEY authentication uses a client-side private key file and a public key registered to the Machbase user. In normal operation, generate the key pair with `openssl`, keep the private key on the client host, and register only the public key in Machbase.

A user may own both a password and one or more AUTH KEY entries. The actual authentication method is chosen by the client's `AUTH_MODE`, and there is no automatic fallback from one method to the other on failure.

### Create a User with AUTH KEY

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    PUBKEY = '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE = '2047-12-31',
    COMMENT = 'initial key'
);
```

- `PUBKEY` must contain a PEM public key or an X.509 certificate (see [Register from an X.509 Certificate](#register-from-an-x509-certificate)).
- In SQL text, PEM line breaks can be written as `\n`.
- `VALID_BEFORE` uses the `YYYY-MM-DD` format and does not accept a datetime value with a time portion such as `YYYY-MM-DD HH24:MI:SS`.
- `COMMENT` is required by the current AUTH KEY syntax.
- The first key created by `CREATE USER ... WITH AUTH KEY` is registered as active (`ACTIVATED=1`).

### Manage AUTH KEY

Add an AUTH KEY. An added key is created as active immediately (`ACTIVATED=1`). During key rollover, a user can have multiple active AUTH KEY entries.

```sql
ALTER USER app_user ADD AUTH KEY (
    PUBKEY = '-----BEGIN RSA PUBLIC KEY-----\n...\n-----END RSA PUBLIC KEY-----\n',
    VALID_BEFORE = '2048-01-31',
    COMMENT = 'rollover candidate'
);
```

Activate or deactivate an AUTH KEY by its ID. A deactivated key cannot be used for challenge authentication.

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

Change the expiration of an AUTH KEY. The input format is `YYYY-MM-DD`; a key past `VALID_BEFORE` cannot be used for authentication.

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

Drop an AUTH KEY. A dropped key cannot be used for authentication immediately. When a user is dropped, the user's AUTH KEY metadata is also removed.

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

### Register from an X.509 Certificate

`PUBKEY` accepts three PEM input formats:

- `-----BEGIN PUBLIC KEY-----` — ECDSA or RSA public key in SubjectPublicKeyInfo (SPKI) format.
- `-----BEGIN RSA PUBLIC KEY-----` — PKCS#1 RSA public key.
- `-----BEGIN CERTIFICATE-----` — X.509 certificate; the public key and expiration date are taken from the certificate.

```sql
CREATE USER app_x509 IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    PUBKEY = '-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n',
    VALID_BEFORE = '2036-07-12',
    COMMENT = 'x509 certificate key'
);
```

- For a key registered from an X.509 certificate, `VALID_BEFORE` cannot be later than the certificate `notAfter`; registration (or a later `ALTER`) fails if this is not met.
- During authentication the client still uses the matching **private key file** (via `-K` / `AUTH_KEY_FILE`), not the certificate file. The registered certificate and the client-side private key must belong to the same key pair.
- Machbase extracts and stores the public key from the certificate; it does **not** perform certificate chain or CA trust validation — the certificate is only an input format carrying a public key and an expiration date.
- The input must contain exactly one PEM block. Chain PEM input, private-key PEM input, raw OpenSSH public keys, unsupported PEM headers, and non-whitespace trailing text after a valid PEM block are rejected.

### Generate AUTH KEY Files

ECDSA P-256 key example:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384 and P-521 key examples:

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048-bit key example (pass `3072` or `4096` as the last argument for a larger key):

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

To produce a PKCS#1 RSA public key (`-----BEGIN RSA PUBLIC KEY-----`) instead of the default SPKI form, add `-RSAPublicKey_out`:

```bash
openssl rsa -in app_user_rsa.key -RSAPublicKey_out -out app_user_rsa_pkcs1.pub
```

To register an X.509 certificate, create a self-signed certificate with the same private key and use the certificate PEM as `PUBKEY`:

```bash
openssl req -new -x509 \
    -key app_user_ecdsa.key \
    -out app_user_ecdsa.crt \
    -days 3650 \
    -subj "/CN=app_user"
```

Raw OpenSSH public keys (`ssh-rsa ...`, `ecdsa-sha2-nistp256 ...`) cannot be registered directly in `PUBKEY`; convert them to a PEM public key first with `ssh-keygen -e -m PKCS8`.

To embed the public key in SQL, convert the PEM file into a single SQL string with escaped line breaks, then use the output as the `PUBKEY` value in `CREATE USER ... WITH AUTH KEY` or `ALTER USER ... ADD AUTH KEY`:

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

### Supported Algorithms and Key Sizes

| Public key algorithm | Supported key parameters | Supported signature scheme | Hash |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

If `AUTH_SIG_SCHEME` is omitted, Machbase uses the default scheme for the key algorithm: `ECDSA` for an ECDSA key and `RSA_PKCS1_V15` for an RSA key. To use RSA-PSS, specify `AUTH_SIG_SCHEME=RSA_PSS` in the client connection options. Authentication fails if the registered public key type does not match the requested signature scheme.

### Query AUTH KEY Metadata

Registered AUTH KEY metadata can be queried from `V$USER_AUTH_KEYS`. Major columns: `KEY_ID` (identifier), `USER_NAME` (owner), `KEY_ALGO` (`RSA` or `ECDSA`), `KEY_PARAM` (RSA bit length such as `2048`, or EC curve name such as `P-256`), `ACTIVATED`, `VALID_AFTER` / `VALID_BEFORE`, `COMMENT`, `PUBKEY` (PEM public key body), and `ADDITIONAL_INFO` (input source: `type=PUBLIC_KEY`, or `type=CERTIFICATE; cert_not_after=YYYY-MM-DD` when registered from an X.509 certificate).

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

## Uppercase User Name Storage

User names are converted to uppercase when they are created. For example, `CREATE USER app_user ...` is stored and displayed as `APP_USER` in metadata tables and `V$` views. Later connection and privilege statements refer to the same user name.

## CONNECT

**user_connect_stmt:**

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

The user can reconnect to another user via the following syntax without terminating the application.

```sql
-- Example
CONNECT user1/password;
```

## GRANT/REVOKE

Grants authority to the table to the user through the GRANT statement.

```sql
-- Grant user1 SELECT privileges on mytable
GRANT SELECT ON mytable TO user1;
 
-- Grant user1 all privileges on mytable
GRANT ALL ON mytable TO user1;
```

Revokes the privilege granted to a user through the REVOKE statement.

```sql
-- Revoke UPDATE privilege on mytable granted to user1
REVOKE UPDATE ON mytable FROM user1;
 
-- Revoke all privileges on mytable granted to user1
REVOKE ALL ON mytable FROM user1;
```

## Managing User Example

Here is an example of the above query and its results.

```
############################################
## Connect with SYS account
############################################
Mach> create user demo identified by 'demo';
Created successfully.
 
Mach> drop user demo;
Dropped successfully.
 
Mach> create user demo1 identified by 'demo1';
Created successfully.
 
Mach> create user demo2 identified by 'demo2';
Created successfully.
 
Mach> alter user demo2 identified by 'demo22';
Altered successfully.
 
Mach> create table demo1_table (id integer);
Created successfully.
 
Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.
 
Mach> insert into demo1_table values(99991);
1 row(s) inserted.
 
Mach> insert into demo1_table values(99992);
1 row(s) inserted.
 
Mach> insert into demo1_table values(99993);
1 row(s) inserted.
 
Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.
 
#Error: Can't drop the user connected.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]
 
############################################
## Connect DEMO1
############################################
Mach> connect demo1/demo1;
Connected successfully.
 
#Error: can't alter other's account password
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]
 
Mach> alter user demo1 identified by demo11;
Altered successfully.
 
#Error: wrong password
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]
 
## Correct password
Mach> connect demo1/demo11;
Connected successfully.
 
Mach> create table demo1_table (id integer);
Created successfully.
 
Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.
 
Mach> insert into demo1_table values(1);
1 row(s) inserted.
 
Mach> insert into demo1_table values(2);
1 row(s) inserted.
 
Mach> insert into demo1_table values(3);
1 row(s) inserted.
 
Mach> select * from demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
############################################
## Connect SYS again
############################################
Mach> connect SYS/MANAGER;
Connected successfully.
 
Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.
 
Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.
 
Mach> drop user demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]
 
Mach> connect demo1/demo11;
Connected successfully.
 
Mach> drop table demo1_table;
Dropped successfully.
 
Mach> connect SYS/MANAGER;
Connected successfully.
 
Mach> drop user demo1;
Dropped successfully.
```
