---
type: methodology
category: fuzzing
tags:
  - methodology/fuzzing
  - discovery
  - subdomains
  - smb
  - web
aliases:
  - Fuzzing Methodology
  - Multi-Domain Fuzzing
---
# Fuzzing Methodology

**Description:** Systematic discovery approach using automated input variation to uncover hidden assets, endpoints, shares, or records across different protocols and layers.

---

## Fuzzing Domains & Objectives

| Domain               | Target / Objective                                                        | Typical Tools                     |
| :------------------- | :------------------------------------------------------------------------ | :-------------------------------- |
| **Web Discovery**    | Directories, files, parameters, extensions.                               | `ffuf`,`gobuster`                 |
| **DNS / Subdomains** | Finding hidden hostnames or internal entry points (`vhost`, `subdomain`). | `ffuf`, `gobuster dns`, `dnsenum` |
| **SMB Shares**       | Enumerating accessible or hidden network shares via brute-forcing.        | `netexec`, `smbmap`               |
| **SNMP / UDP**       | Finding active community strings or responsive services.                  | `onesixtyone`, `nmap`             |

---

## Web Discovery
### Subsites

![Subsites and files (non recursive) - ffuf](ffuf.md#Subsites%20and%20files%20(non%20recursive)%20-%20ffuf)

### Parameter
![Paramter fuzz (POST-Request) - ffuf](03%20Tools/Ffuf.md#Paramter%20fuzz%20(POST-Request)%20-%20ffuf)

![Parameter fuzz (GET-Request) - ffuf](03%20Tools/Ffuf.md#Parameter%20fuzz%20(GET-Request)%20-%20ffuf)

## Domain
### Subdomain
![Subdomain fuzz - ffuf](03%20Tools/Ffuf.md#Subdomain%20fuzz%20-%20ffuf)

### VHosts
![VHosts fuzz - ffuf](Ffuf.md#VHosts%20fuzz%20-%20ffuf)
