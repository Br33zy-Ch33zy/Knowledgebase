---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - ftp, ftps, 21
---
# FTP (File Transfer Protocol)

**Default Ports:** `21` (TCP - Control)  |  `20` (TCP - Data)   |  `990` (FTPS Control)
**Description:** Used for transferring files between Client and Server

---
## 00 - Common Vulnerabilities
**FTP-Anon** is active, allows "Anonymous" User to connect

## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection:
Connect to FTP-service with any port:
```bash
ftp username@10.129.140.62 port
```
#### Transferring Files from an FTP Server using PowerShell
```bash
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```
### 2.2 - FTP command sequence after establishing a connection:
ftp:
	`get` = download file
	`put` = upload file
	`passive off` = deactivate passive mode
	`delete FILENAME` = delete file

### 2.3 - Setting up FTP Server
#### Python FTP Server
Setting up listening FTP Server on local machine:
```bash
sudo python3 -m pyftpdlib --port 21
```

## Weaknesses
### Anonymous Login
An FTP-Server can be configured to allow `anonymous` login, which can provide us with additional information or file upload possibilities. The username in this case is usually:
```ftp
anonymous
```


![[Nmap#FTP Bounce Attack]]

![[Hydra#Bruteforcing FTP]]