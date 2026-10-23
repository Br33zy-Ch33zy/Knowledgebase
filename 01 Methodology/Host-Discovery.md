---
type: knowledge
category: methodology
tags:
  - knowledge/methodology
aliases:
  - network
  - enumeration
---
# Host-Discovery
`Host-Discovery` opens the door for potential lateral and vertical movement.

---

## Methods
### fping
```bash
fping -asgq 172.16.5.0/23
```

### Nmap
![[Nmap#Hostscan/Host-Discovery (aka. Ping Sweep)]]

### Responder
![[Responder#Listen to all Traffic]]

### Wireshark
![[Wireshark#Terminal]]