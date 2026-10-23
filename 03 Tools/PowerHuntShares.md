---
type: tool
category: windows, powershell
tags:
  - tool
---
# Overview
Powershell based tool, which scans User profile an accessable shares for valuable information, such as credentials.
https://github.com/NetSPI/PowerHuntShares
## Setup
1. Bypass Execution policy restriction
```powershell
Set-ExecutionPolicy -Scope Process Bypass
```
2. Import Module, that exists in the current directory
```powershell
Import-Module .\PowerHuntShares.psm1
```
3. Run a default directory Scan and generate report in the provided location
```powershell
Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\temp\test
```

## Important Parameter
