---
type: tool
category: web
tags:
  - tool
---
# Overview
To inform proxychains that we will use port 9050, we must modify the proxychains configuration file located at `/etc/proxychains.conf`. We can add e.g.  `socks4 127.0.0.1 9050` to the last line if it is not already there.
## Commands

For example with `Nmap`, only works reliable with full tcp scans:
```bash
proxychains nmap -v -Pn -sT 172.16.5.19
```

#### Metasploit
```bash
proxychains msfconsole
```

#### xfreerdp
```bash
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```
## Important Parameter
