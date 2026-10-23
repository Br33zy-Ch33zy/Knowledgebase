---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - http, https, 80, 443, 8080, 8443
---
# HTTP / HTTPS (Hypertext Transfer Protocol)

**Default Ports:** `80` (TCP - HTTP)  |  `443` (TCP - HTTPS)  |  `8080`, `8443` (Alternative Ports)  
**Description:** Protocol for transferring web content and web applications.

---

## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing
IMPORTANT: HTTP and HTTPs Headers can produce different outputs!
Gather information directly from the web servers vhost (Server software, version, OS, redirects):

![[Curl#^47e6b0]]

### 1.2 - Deep Enumeration
![[Wafw00f#WAF-Check]]

![[Nikto#Fingerprinting Website]]

![[Whatweb#Information gathering]]

![[Scripts#ReconSpider.py]]

![[Wget#Mirror/Download website content]]
And filter it for keywords such as `username` or `password`:
```bash
grep -rnEi "user|username|login|password|pass|cred|admin" PATH-TO-DOWNLOAD
```

#### Subsites-ENUM
![[Gobuster#^c23762]]
#### Vhost-ENUM
![[Gobuster#^30f250]]

## 02 - Connecting to Service
### 2.1 - Establishing connection:

### 2.2 - Setting up HTTP Server
![[python#http server]]

![[Scripts#uploadserver]]


## Weaknesses

### Bruteforcing
![Bruteforcing HTTP (POST) - Hydra](03%20Tools/Hydra.md#Bruteforcing%20HTTP%20(POST)%20-%20Hydra)

![Bruteforcing HTTP (GET) - Hydra](03%20Tools/Hydra.md#Bruteforcing%20HTTP%20(GET)%20-%20Hydra)

![[Curl#Path traversal on Website]]