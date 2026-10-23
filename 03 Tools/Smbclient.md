---
type: tool
category: smb
tags:
  - tool
---
# Overview
## Quick Commands
**L**ist shares (of IP) with the so called **N**ull Session, which is anonymous access without user or password:
```bash
smbclient -N -L //10.129.14.128
```
^aedec0

^688f5d
### Connect to share with anonymous user:
```bash
smbclient //172.16.1.11/dev-share -U ""
```
^d79247

### Connect to SMB-Share with Kerberos TGT
If there is a TGT stored in the `credential cache` it is possible to use it to connect to another system:
```bash
smbclient //dc01/carlos -k --no-pass
```

> [!INFO] Note
To keep the ticket from the current session, before importing the keytab, save a copy of the ccache file present in the environment variable `KRB5CCNAME`.
## Important Parameter & Information
smbclient
	``\\\\`` = **"\\\\"**, because in bash a backslash means, that the next character is “escaped” 
	`-N` = suppresses the password prompt
	`-L` = Retrieves a list of available Shares on remote host
	`-k` = specifies kerberos authentication to be used (from credential cache)
	`-c COMMAND` = executes one command and closes session afterwards

### After initial connection
After connecting via smbclient an new subshell opens, which has limited commands. Here are some of the most important ones to navigate properly
	`help` = Lists available commands
	`!<cmd>` = Lets you execute commands on your local machine (e.g. !cat flag.txt)