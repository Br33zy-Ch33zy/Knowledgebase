---
type: tool
category: web
tags:
  - tool
---
# Overview

## Quick Commands
Login to DB:
```bash
sqlplus username/password@10.129.204.235/SID
```

Login as System Database Admin as another user (if sufficient rights):
```bash
sqlplus username/password@10.129.204.235/SID as sysdba
```

## Useful commands

Get Password-Hashes:
```bash
**select name, password from sys.user$;**
```

## Important Parameter
