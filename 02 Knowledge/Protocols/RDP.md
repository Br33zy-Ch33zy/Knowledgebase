---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - rdp, 3389
---
# RDP (Remote Desktop Protocol)

**Default Ports:** `3389` (TCP/UDP)   
**Description:** A Microsoft protocol for remote graphical control of Windows systems. After successful credential harvesting, it serves as a direct means of interactive GUI access.

---

## 01 - Enumeration

### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection
![[xfreerdp#^70b0b1]]


![[xfreerdp#Pass the Hash (using RDP)]]


## Weaknesses
### Bruteforcing Credentials
![[Hydra#^6b8cd0]]

### RDP Session Hijacking
To successfully impersonate a user without their password, we need to have `SYSTEM` privileges and use the Microsoft [tscon.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tscon) binary that enables users to connect to another desktop session.
1. Check if there are other active sessions and also retrieve `OUR_SESSION_NAME`:
```powershell
query user
```

2. Open a another session within ours:
```cmd
tscon #{TARGET_SESSION_ID} /dest:#{OUR_SESSION_NAME}
```

If we have local administrator privileges, we can use several methods to obtain `SYSTEM` privileges, such as [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) or [Mimikatz](https://github.com/gentilkiwi/mimikatz). A simple trick is to create a Windows service that, by default, will run as `Local System` and will execute any binary with `SYSTEM` privileges. We will use [Microsoft sc.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create) binary. First, we specify the service name (`sessionhijack`) and the `binpath`, which is the command we want to execute. Once we run the following command, a service named `sessionhijack` will be created:

```powershell
sc.exe create sessionhijack binpath= "cmd.exe /k tscon 2 /dest:OUR_SEESION_NAME"
```

To run the command, we can start the `sessionhijack` service :
```cmd
net start sessionhijack
```

