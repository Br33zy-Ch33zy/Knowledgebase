---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - smb, netbios, 445, 139
---
# SMB (Server Message Block)

**Default Ports:** `445` (TCP -Direct SMB)  |  `139` (TCP - NetBIOS)  
**Description:** Network-flow-protocol to share data, printers 

---

## 01 - Enumeration

### Quick Check / Banner Grabbing
![[Netcat#^5d19c8]]

### Deep Enumeration
![[Scripts#enum4Linux-ng.py#Default scan / All]]
#### Fingerprinting 
Netexec:
![[NetExec#^062dcf]]

Metasploit:
![[Metasploit#^391c96]]

#### List Shares 

![[Smbclient#^aedec0]]

![[smbmap#List Shares]]

![[smbmap#Recursive List Of All Directories]]

![[CrackMapExec#Spider Shares]]
### Post Exploitation

![[CrackMapExec#Enumerating Logged-on Users]]

![[CrackMapExec#Extract Hashes from SAM Database]]

![[CrackMapExec#Pass-the-Hash (PtH) - CrackMapExec (SMB)]]

## 02 - Connecting to Service
### 2.1 - Establishing connection
It can be helpful to record the smbsession beforehand with `script`:
```bash
script smb-session.log
```
Then connect to the share:
![[Smbclient#^d79247]]

### 2.2 - Command sequence after establishing a connection

List directory with its subdirectories and files:
```bash
recurse on
ls
```
After exiting the session we need to end the recording in our local shell with:
```bash
exit
```
Interesting files can be downloaded via:
```bash
get FILENAME
```
All accessible files can be downloaded as following:
```bash
recurse ON
prompt
mget *
```

### 2.3 - Setting up SMB Server
![[Scripts#smbserver.py]]


## Weaknesses
### Anonymous Login
An FTP-Server can be configured to allow `anonymous` login, which can provide us with additional information or file upload possibilities. The username in this case is usually:
![[Smbclient#^aedec0]]

### SMBv1
The rule of thumb is that basically every Windows system (build & hotfixes) with SMBv1 older than 2017 is affected by `Eternal Blue`.
Check if  `Eternal Blue (MS17-010)`is present:
![[Nmap#^f49db0]]

Metsploit module:
```bash
get FILENAME
```

### Bruteforcing Credentials
Best Experience so far:
![[Metasploit#^cbccf3]]


![[NetExec#^639893]]
