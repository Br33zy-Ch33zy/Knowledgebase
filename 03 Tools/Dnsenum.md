---
type: tool
category: dns
tags:
  - tool
---
# Overview

## Commands
Subdomain bruteforce and enum of found subdomains:
```bash
dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r | tee dnsenum.txt
```

^eebf6c

- #speed/fast #stealth/low 

Checks domain (exampledomain.com) with domain-list for any subdomains and saves it to file “subdomains.txt”. This command is pretty fast and has up to 90 threads simultaneously:
> [!INFO] Note
DNSENUM only checks A-Records!

```bash
dnsenum --dnsserver 10.129.150.244 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt exampledomain.com --threads 90
```

^25560d

  - #speed/fast #stealth/low 
  

## Important Parameter
dnsenum:
	`-r` = enables **r**ecursive subdomain bruteforcing, meaning that if dnsenum finds a subdomain, it will then try to enumerate subdomains of that subdomain
## Useful Commands
