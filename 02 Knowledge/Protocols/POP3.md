---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - pop3, pop3s, 110, 995
---
# POP3 (Post Office Protocol 3)

**Default Ports:** `110` (TCP - Plaintext/STARTTLS)  |  `995` (TCP - POP3S | SSL/TLS)  
**Description:** Protocol responsible for downloading E-Mails from mailserver. Unlike IMAP, emails are stored locally after they are retrieved and are deleted from the server by default.

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing
- **Nmap:** `![[Nmap#^<BLOCK-ID>]]`
- **Manual Check:** `nc -vn <IP> <PORT>`

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection:
Plaintext `Port 110`:
![[Telnet#^1c4b0a]]

SSL/TLS `Port 995`:
![[Openssl#^0cf4ad]]

### 2.2 - POP3 command sequence after establishing a connection:

1. Provide username...
```bash
user username
```

2. ... and password
```bash
pass password
```

3. Show the number and size of emails
```bash
stat
```

4. List messages
```bash
list
```

5. List message e.g. "1"
```bash
retr 1
```

6.  Disconnect
```bash
quit
```

## Weaknesses 
### Bruteforcing
![[Hydra#^e4dc09]]