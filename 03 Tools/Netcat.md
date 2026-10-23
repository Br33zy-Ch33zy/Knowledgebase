---
type: tool
category: enumeration
tags:
  - tool
  - enum
---
# Overview

## Quick Commands
Simple banner grabbing:
```bash
nc IP Port
```
  - #speed/fast #stealth/low
Stealth Single-Port, with port-spoofing Service Enum:
```bash
sudo ncat -nv --source-port 53 10.129.2.47 50000
```
  - #stealth/high
UDP  banner grabbing:
```bash
nc -uv IP Port
```

^5d19c8

  - #speed/fast #stealth/low
### Filetransfer with Netcat
1. Start listener on compromised machine:
```bash
	nc -l -p 8000 > TARGETFILE.TXT
```
2. Retrieve the provided file and close the connection afterwards with `--recv-only`:
```bash
ncat -l -p 8000 --recv-only > TARGETFILE.TXT
```

### Setup NC Listener
Setup simple Listener  on `port 1234` (Kali) **l**=listening, **v** =verbose so we know about connection status, **n**=disable dns resolution:
```bash
nc -lvnp 1234
```

^d13c2d

## Important Parameter
nc
	`-n` = without dns resolution
	`-v` = verbose, more details
	`-l` = listening 
	`-p` = port
	`-u` = switches to UDP mode