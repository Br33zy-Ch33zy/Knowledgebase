---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - rpc, rpcbind, portmap, ms-rpc, 111, 135
---
# RPC (Remote Procedure Call)

**Default Ports:** `111` (TCP/UDP - SunRPC / rpcbind)  |  `135` (TCP/UDP - MS-RPC End Mapper)  
**Description:** A protocol that allows a program to execute code on a remote computer without having to explicitly control the network details. It serves as the basis for NFS (Unix) as well as SMB, Active Directory, and WMI (Windows).

---

## 01 - Enumeration
### 1.1 - Quick Check / Banner Grabbing
![[Scripts#^d54b7c]]
### 1.2 - Deep Enumeration
![[Scripts#enum4Linux-ng.py]]


## 02 - Connecting to Service
### 2.1 - Establishing connection:
![[Rpcclient#^6a4596]]
### 2.2 - RPC command sequence after establishing a connection:
1. `enumdomusers`