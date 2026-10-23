---
platform: hackthebox
difficulty: Hard
status: Completed
date: 2026-08-21
tags:
  - difficulty/hard
---
# HTB: Footprinting Lab - Hard

**Target IP:** `10.129.165.204`  `10.129.166.108`
(There are several, because I did this lab in multiple sessions)
**OS:** `Unknown`  
---

## 01 - Scope
- **Assignment:**
The third server is an MX and management server for the internal network. Subsequently, this server has the function of a backup server for the internal accounts in the domain. Accordingly, a user named HTB was also created here, whose credentials we need to access.

- **Primary Goals:**
  - [x] Password of the User `HTB`

---

## 02 - Procedure
1. Fast scan and script/version scan:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821104145.png)

2. Checking cve's for ssh version, which is vulnerable to an RCE:https://ubuntu.com/security/CVE-2023-38408

3. So far so good, lets verify the version with "nc" and also grab the banners of the remaining ports to hopefully figure out their version:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821105757.png)

4. After learning about the principles of the RCE "CVE-2023-38408", I came to the conclusion that this weakness is only exploitable if a client establishes a connection with the server (and even than, the server already needs to be exploited).  Therefor this RCE is meant for the client and not useful in this case.
5. For this reason I started enumerating IMAPs further. I wasn't able to get more detailed information like accounts or exact version through "Nmap":
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821120455.png)
6. That's why I decided to try bruteforcing the accounts. Before I do that I want to make sure, if I can get the domainname through a quick "openssl" connection:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821120752.png)
7. Since this is not the case and the certificate is selfsigned, I will try my luck with "hydra" (Which didn't work out in the end):
8. Whilst "hydra" was running, I performed a top 100 UDP scan and discovered an open snmp port:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821125027.png)
9. I tried to figure out the exact version, but without success:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821130217.png)
10. Also another full port-range UDP-Scan, which I had running in the background, couldn't find anymore open ports:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821130645.png)
11. Since there are quite some CVE's for "Dovecot" (Mailserver), I tried to figure out the exact version with "Metasploit", without success:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821163652.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821163710.png)
12. After trying many different approaches I eventually found the community string "backup" of snmp: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821174447.png)
13. I then executed an "snmpwalk" and retrieved the login of "tom"...:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821175109.png)
14.  ... which I successfully used to login to pop3. And there was one message, which contained a ssh key:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821175434.png)

15. After gaining the private key I tried connecting to the server via ssh, which worked perfectly:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821180335.png)
16. After spending far to much time going through the "mail" and "Maildir" folder I started gathering information about the user & system. :
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260821184303.png)
17. I informed myself about the "Ubuntu v20.04.3" and found a privilege escalation exploit, which sounds promising: https://github.com/ly4k/PwnKit
18. I executed the exploit [[CVE-2021-4034-PKEXEC]] on the target and gained "root" access:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260824090627.png)
19. I then checked the "/etc/passwd" file to check the local accounts/service users. I noticed, that there's a local mysql-service (user). I connected to it and found a table called "users"....
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260824092722.png)
20. ... which I queried for "HTB" and retrieved the password:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260824093213.png)

## 03 - Lesson Learned
This time, I didn't make any obvious mistakes. With a little more experience, I'll probably have a better understanding of the vulnerabilities and thus be able to gain access in a more targeted manner.

The main takeaways for me are:

1. A UDP scan is an important part of the initial “enumeration” process.