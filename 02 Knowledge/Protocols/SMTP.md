---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - smtp, smtps, 25, 465, 587
---
# SMTP (Simple Mail Transfer Protocol)

**Default Ports:** `25` (TCP - Plaintext/STARTTLS)  |  `465` (TCP - SMTPS)  |  `587` (TCP - Submission/STARTTLS)
**Description:** Protocol used for sending and forwarding E-Mails between server and client.

---

## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration
![[Smtp-user-enum#User-ENUM]]


#### O365-Enum Users
https://github.com/0xZDH/o365spray
## 02 - Connecting to Service
### 2.1 - Establishing connection:
Plaintext `Port 25`:
![[Telnet#^8f4db7]]

SSL/STARTTLS `Port 587`:
![[Openssl#^8b8445]]
### 2.2 - Command sequence after establishing a connection:
1. List available features:
```bash
EHLO inlanefreight.htb
```

2. Login with username and password. IMPORTANT - format is in `Base64`:
```bash
AUTH LOGIN
```
Enter Username `in Base64`, e.g:
```username
ZmlvbmFAaW5sYW5lZnJlaWdodC5odGI=
```
And Password also `in Base64`, e.g:
```password
OTg3NjU0MzIx
```

3. Logout:
```bash
QUIT
```
## Weaknesses and Misconfiguration
### Open Relay
An open relay is a Simple Mail Transfer Protocol (`SMTP`) server, which is improperly configured and allows an unauthenticated email relay. Messaging servers that are accidentally or intentionally configured as open relays allow mail from any source to be transparently re-routed through the open relay server. This behavior masks the source of the messages and makes it look like the mail originated from the open relay server.

From an attacker's standpoint, we can abuse this for phishing by sending emails as non-existing users or spoofing someone else's email. For example, imagine we are targeting an enterprise with an open relay mail server, and we identify they use a specific email address to send notifications to their employees. We can send a similar email using the same address and add our phishing link with this information. With the `nmap smtp-open-relay` script, we can identify if an SMTP port allows an open relay.

![[Hydra#Bruteforcing SMTP]]