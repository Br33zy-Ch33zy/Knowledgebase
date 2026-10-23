---
type: tool
category: web
tags:
  - tool
---
# Overview

## Quick Commands
Scans Webserver “10.10.10.121” for hidden **subsites** which are listed in the wordlist “common.txt”:
```bash
gobuster dir -u http://TARGET/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

^c23762

## Important Parameter
gobuster
	`vhost` = changes the mode to "vhost mode" (needs the "--domain" variable if target is an IP, e.g. in HTB-Lab)
	`--domain DOMAIN/VHOST` = can be used to define which VHOST needs to be scanned
	`--ppend-domain` =  is very important if the brute-force list should be appended to the VHOST or domain instead of, for example the entered IP address.

## Useful Commands
Searches via local DNS (which is in the “etc/resolv.txt” file in Kali) for many common subdomains, which are listed in the “namelist.txt” file
```bash
gobuster dns -domain domain.ch -w /usr/share/seclists/Discovery/DNS/namelist.txt
```

#### Vhosts-Mode
Vhost mode allows you to specify the Vhost via the `--domain` attribute. The `--append-domain` is crucial, so that the flag appends the base domain/vhost to each word in the wordlist:
 
```bash
gobuster vhost -u http://<target_IP_address> -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt --append-domain --domain inlanefreight.htb
```

^30f250

