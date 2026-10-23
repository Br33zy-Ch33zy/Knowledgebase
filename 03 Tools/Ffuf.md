---
type: tool
category: web
tags:
  - tool
---
# Overview
Powerful tool for finding hidden directories and subdomains.

## Quick Commands

#### Paramter fuzz (POST-Request) - ffuf
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://admin.academy.htb:33731/admin/admin.php -X POST -d 'FUZZ=test' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx
```
If we for example fuzz an `ID`, we can `curl` it as followed:
```bash
curl -X POST http://admin.academy.htb:33731/admin/admin.php -H "Content-Type: application/x-www-form-urlencoded" -d "id=73"
```

#### Parameter fuzz (GET-Request) - ffuf
`OUTDATED`
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://admin.academy.htb:33731/admin/admin.php?FUZZ=key -fs 798
```

#### Subsites and files (non recursive) - ffuf
Fuzzes website for subdomains and files such as `.php` , `.html`  and `.bak`:
```bash
ffuf -u http://154.57.164.69:31940/FUZZ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -e .php,.html,.asp,.aspx -ic 
```
^7f8891
Instead of manually defining the file-typ/endings, it is also possible to use this in combination with another wordlist:
```bash
ffuf -u http://154.57.164.83:41216/FUZZEXT -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt:FUZZ -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:EXT -ic
```

#### Subdomain fuzz - ffuf
Searching for `publicly` available subdomains:
```bash
ffuf -u https://FUZZ.inlanefreight.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -ic
```

#### VHosts fuzz - ffuf
Fuzzing VHosts (`fs = Size` of normal requests to filter out):
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u http://154.57.164.69:31940 -H "Host: FUZZ.VHOST" -fs 986
```

^6176ef

## Important Parameter
ffuf
	`-fs 120` = filter size 120, filters all pages with 120 Bytes (useful for filtering homepage, but varies)
	`-ic` = ignore Comments, skips Header "#Copyright..."
	`-H "Host: FUZZ:VHOST"` = -H allows changing the application-header. The attribute "Host:" defines the VHOST
	`-recursion` = starts a new job for found directories / recursive fuzz
	`-recursion-depth 1` = specify how the the recursive fuzz should go
