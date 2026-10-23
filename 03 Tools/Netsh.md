---
type: tool
category: windows-builtin
tags: [tool/windows, pivoting, firewall, lolbin, network]
aliases: [netsh, netsh.exe]
---
# Netsh

Native Windows command-line scripting utility (LOLBin) used for network configuration, firewall rule manipulation, and native TCP port forwarding without downloading external tools.

---

## Commands
### Windows Defender / Firewall
#### Show Firewall Status
```cmd
netsh advfirewall show allprofiles state
```

#### Allow a specific incoming port
```cmd
netsh advfirewall firewall add rule name="Allow_Pivot" dir=in action=allow protocol=TCP localport=8080
```

### Pivoting
#### Windows - Static Port Forwarding (Netsh)
Forwards all traffic pointed to the `Pivot Host:8080` to the `connectaddress` and its `connectport`:
```cmd
netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=10.129.15.150 connectport=3389 connectaddress=172.16.5.25
```
We can verify it (forwarding table) like this:
```cmd
netsh.exe interface portproxy show v4tov4
```