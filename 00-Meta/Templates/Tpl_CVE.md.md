---
type: knowledge
category: exploits
tags:
  - knowledge/exploit
  - os/linux
aliases:
cve:
affected_software:
vulnerability_type: Local Privilege Escalation (LPE)
---
# PwnKit (CVE-2021-4034) - Polkit LPE

**CVE:** `CVE-2021-4034`  
**Affects:** Polkit's `pkexec` 
**Impact:** Immediate local privilege escalation 

---

## 01 - Vulnerability Details & Prerequisites

- **Vector:** empty `argv[]` array in `pkexec`.
- **Requirements:**
  - `pkexec` must be installed

---

## 02 - Manual C-Exploit (No-Dependencies Execution)

```bash
Skript
```
