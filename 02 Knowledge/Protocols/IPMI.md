---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - ipmi, rcp , 623
---
# IPMI (Intelligent Platform Management Interface)

**Default Ports:** `623` (UDP - RMCP / IPMI-over-LAN)  
**Description:** Hardware-based management interface (Baseboard Management Controller / BMC, such as iDRAC or iLO). Enables out-of-band management (power cycle, console, remote media) independently of the operating system.

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing
![[Nmap#^1b19ec]]


### 1.2 - Deep Enumeration
![[Metasploit#^0c38f9]]
## 02 - Connecting to Service
### 2.1 - Establishing connection:

## 03 - Exploitation
![[Hashcat#IPMIv2 (7300 - RAKP)]]
