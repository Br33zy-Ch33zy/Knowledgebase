---
type: knowledge
category: protocols, networking-ad
tags:
  - knowledge/protocol
aliases:
  - LLMNR
  - NBT-NS
---
# LLMNR & NBT-NS 

**Default Ports:** `5355/UDP` (LLMNR) | `137/UDP` (NBT-NS Name Service)  
**Description:** Fallback name resolution protocols used by Windows hosts when primary DNS resolution fails. LLMNR (based on DNS packet format) and NBT-NS allow hosts on the same local network segment (L2) to identify each other without a central DNS server.


---

## 00 - Core Protocol Mechanics

When a Windows client attempts to resolve a hostname (e.g., accessing `\\nonexistent-share`), it follows a fixed resolution order:

1. **Local Hosts File** (`C:\Windows\System32\drivers\etc\hosts`)
2. **DNS Server** (Configured primary/secondary DNS)
3. **LLMNR** (Multicast to `224.0.0.252:5355` / `FF02:0000:13C:5355`)
4. **NBT-NS** (NetBIOS Name Service broadcast to `255.255.255.255:137`)

### Abuse Mechanics (Poisoning / Spoofing)
Because LLMNR/NBT-NS rely on unauthenticated UDP multicasts/broadcasts, any host on the same local network can send a spoofed reply claiming to be the requested machine. 

When the victim host attempts to authenticate against the responder (e.g., via SMB or HTTP), it automatically initiates an **NTLMv2 challenge-response handshake**, exposing the victim's NetNTLMv2 hash to the attacker.

## 01 - Enumeration
### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Capturing Traffic 
### 2.1 - Poisoning LLMNR Traffic

![[Responder#Linux Default (Responder)]]

![[Inveigh#Windows default (Inveigh)]]