---
type: protocol
category: networking-ad
tags: [protocol/ldap, windows, active-directory, authentication, enumeration]
aliases: [LDAP, LDAPS, Lightweight Directory Access Protocol]
---
# LDAP (Lightweight Directory Access Protocol)

**Default Ports:** `389/TCP` (LDAP) | `636/TCP` (LDAPS)  
**Global Catalog Ports:** `3268/TCP` (GC) | `3269/TCP` (GC SSL)  
**Description:** Vendor-neutral application protocol used to query, modify, and manage hierarchical directory services like Active Directory (AD). It acts as the backbone for directory enumeration, credential validation, and object manipulation in Enterprise networks.

---

---

## 00 - Core Protocol Mechanics

LDAP organizes data in a hierarchical tree structure (DIT - Directory Information Tree). Every object in Active Directory is identified by a **Distinguished Name (DN)**.

### Key Terminology
- **Base DN:** The starting point of a directory query (e.g., `DC=corp,DC=local`).
- **Bind:** The authentication process against the LDAP server.
  - **Anonymous Bind:** Querying without credentials (often disabled by default in modern AD, but valid for initial enum if misconfigured).
  - **Authenticated Bind:** Querying using domain credentials (e.g., `DOMAIN\User` or UPN `user@domain.local`).
- **LDAP Filters:** Syntax used to search for specific objects:
  - Find all users: `(&(objectCategory=person)(objectClass=user))`
  - Find Domain Admins: `(&(objectCategory=group)(cn=Domain Admins))`
  - Find Unconstrained Delegation: `(userAccountControl:1.2.840.113556.1.4.803:=524288)`

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration
```bash
Code
```

## 02 - Connecting to Service
Connections to the LDAP service are primarily used to `query` and `modify` domain objects within a directory (such as Active Directory). While objects can be searched dynamically using LDAP filters across a base domain, directly modifying or targeting a specific object typically requires knowing its exact Directory Path (Distinguished Name / DN).

### 2.1 - Query LDAP
#### List all Group-Memberships of an user
```bash
ldapsearch -x -H ldap://172.16.5.5 -D "USER@INLANEFREIGHT.LOCAL" -w 'PASSWORD' -b "DC=INLANEFREIGHT,DC=LOCAL" "(member:1.2.840.113556.1.4.1941:=$(ldapsearch -x -H ldap://172.16.5.5 -D "USER@INLANEFREIGHT.LOCAL" -w 'PASSWORD' -b "DC=INLANEFREIGHT,DC=LOCAL" "(sAMAccountName=SAPService)" dn | sed -n 's/^dn: //p'))" cn
```

### 2.2 - Modify LDAP