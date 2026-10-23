---
type: tool
category: pivoting
tags: [tool/pivoting, ssh, tunneling, windows]
aliases: [plink, plink.exe]
---
# Plink

Command-line connection tool for PuTTY, heavily used on Windows targets for SSH tunneling, local/remote port forwarding, and pivoting without GUI access.

---

## Commands
#### Windows - Dynamic Port Forwarding (SSH)
Setup a listener/forwarder on the client and connect to the target:
```bash
plink -ssh -D 9050 ubuntu@10.129.15.50
```
Followed by a SOCKS tunnel e.g. via `Proxifier`:
![[Proxifier#^c63fdb]]
