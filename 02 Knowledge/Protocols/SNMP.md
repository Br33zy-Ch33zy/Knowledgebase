---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - snmp, 161, 162, 10161, 10162
---
# SNMP (Simple Network Management Protocol)

**Default Ports:** `<161 & 10161>` (UDP - Requests Queries)  |  `<162 & 10162>` (UDP - Traps/Notifications)  
**Description:** A UDP-based protocol for monitoring and managing network devices (routers, switches, servers, printers). SNMP uses “community strings” as passwords to access data trees (MIBs / OIDs).

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing
![[Nmap#^69f8fa]]

### 1.2 - Deep Enumeration
![[snmpwalk#^c7e35a]]

![[Nmap#^5257ff]]
## 02 - Connecting to Service
### 2.1 - Establishing connection:

## 03 - Exploitation
### Get hands on Community String
Bruteforce via script:
![[Scripts#^ed337d]]
