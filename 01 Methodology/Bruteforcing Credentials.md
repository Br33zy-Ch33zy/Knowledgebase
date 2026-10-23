---
type: knowledge
category: methodology
tags:
  - knowledge/methodology
aliases:
  - user-lists
  - password-lists
  - enumeration
---
# Users
Usernames-Repo: https://github.com/insidetrust/statistically-likely-usernames
Sometimes we'll enumerate the names of employees. In these cases, it can be helpful to work with them to create a `list of possible usernames`.
## Enumerating Users - from Linux
### Without valid Credentials

![[Kerbrute#Enum Users - Kerbrute]]

![[CrackMapExec#Enumerating users and "badpwdcount" (without Credentials)]]

![[Scripts#Enum Users - enum4linux-ng]]

![[Rpcclient#Enum Users with SMB Null Session]]

### With valid Credentials
![[Scripts#Enum Users - Windapsearch (LDAP)]]

## Enumerating Users - from Windows
### Without valid Credentials

### With valid Credentials

![Enum domain-users](PowerView.md#Enum%20domain-users)
## Create User-List
![[Scripts#username-anarchy.rb]]

# Passwords
## Password Generator
![Personalized Password genarator (Invoke) - Cupp](03%20Tools/Cupp.md#Personalized%20Password%20genarator%20(Invoke)%20-%20Cupp)
## Retrieving Password Policies - from Linux
### Without valid Credentials
![[Rpcclient#Retrieving Password Policies with SMB Null Session]]

![[Scripts#Retrieve Password Policies - enum4linux-ng]]
### With valid Credentials
![[CrackMapExec#Retrieving Password Policies - CrackMapExec (SMB)]]
## Password Spraying / Bruteforcing

## against Domain Controller

### from Linux

![[Rpcclient#Password Spraying - Rpcclient]]

![[Kerbrute#Password Spraying - Kerbrute]]

![[CrackMapExec#Password Spraying - CrackMapExec]]

### from Windows
![[DomainPasswordSpray#Password Spraying - DomainPassswordSpray]]
## against local Hosts

### from Linux
![[CrackMapExec#Password Spraying with Hash - CrackMapExec]]

