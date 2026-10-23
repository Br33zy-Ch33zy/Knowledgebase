---
type: tool
category: shares,smb
tags:
  - tool
---
# Overview
Additionally to listing shares, `smbmap`  also shows which share the current user has access to.
## Commands
#### List Shares
##### Without Credentials - smbmap
List Shares and access right for anonymous "user":
```bash
smbmap -H 10.129.14.128
```
##### With Credentials - smbmap
```bash
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5
```

#### Recursive List Of All Directories
Lists directories only (no files):
```bash
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'Department Shares' --dir-only
```

## Important Parameter
smbmap
	`--dir-only` = lists only directories 