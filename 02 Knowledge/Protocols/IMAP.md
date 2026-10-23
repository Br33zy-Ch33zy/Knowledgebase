---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - imap, imaps, 143, 993
---
# IMAP (Internet Message Access Protocol)

**Default Ports:** `143` (TCP - Plaintext/STARTTLS)  |  `993` (TCP - IMAPS | SSL/TLS)  
**Description:** A protocol for retrieving and managing emails directly on the mail server. Unlike POP3, emails remain on the server and are synchronized.

---
Can usually only be exploited, if "credentials" are obtained (e.g. through bruteforcing).
## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration
![[Nmap#^6d3200]]

It is sometimes possible to retrieve the domainname while connecting to IMAPS `993`:
[[imap#2.1 - Establishing connection]]
## 02 - Connecting to Service
### 2.1 - Establishing connection:
Plaintext `Port 143`:
![[Telnet#^22d05c]]

SSL/TLS `Port 993`:
![[Openssl#^077373]]
![[Openssl#^0f401f]]
### 2.2 - Command sequence after establishing a connection:
1. Login with user
```bash
? login username password 
```

2. Lists all Inboxes
```bash
? List
```
or
```bash
? List "" "*"
```

3. INBOX = Inbox Name
```bash
? select INBOX
```

4. Counts the amount of messages in this INBOX
```bash
? status INBOX (Messages)
```

5. Outputs the available messages
```bash
? fetch 1 all 
```

6. Shows the content of ALL available messages
```bash
? fetch 1:* body[]
```

7. Logout
```bash
? logout
```

## 03 - Exploitation
### 3.1 - Bruteforcing Credentials
![[Hydra#^af4fd2]]