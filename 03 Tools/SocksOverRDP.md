---
type: tool
category: pivoting
tags:
  - tool
---
# Overview
https://github.com/nccgroup/SocksOverRDP/releases
`SocksOverRDP` utilizes the  `RDP Dynamic Virtual Channels`, which purpose is, for example, to exchange clipboard contents between the client and the server or to transmit audio and more.
## How to use
#### Dynamic Forwarding (RDP)
`Local Admin needed!`
1. We need to make sure, that windows defender doesn't detect/block the `.DLL`. An easy way to accomplish this, is to make an exemption for our "Install folder" (in this case Downloads) over `Powershell executed as Admin`:
```powershell
 Add-MpPreference -ExclusionPath "C:\Users\htb-student\Downloads"
```
2. Install `SocksOverRDP` plugin/DLL on the (first) Pivot Host. (It then waits passively for a RDP-session): https://github.com/nccgroup/SocksOverRDP/releases
```cmd
regsvr32.exe SocksOverRDP-Plugin.dll
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928085044.png)

3. Now when starting the next RDP-session there should be a popup stating that our Pivot Host will listen on `127.0.0.1:1080`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928090837.png)

4. At this point we only need to execute the `SocksOverRDP-Server.exe` on the target server and execute it with `Admin Privileges`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928091530.png)
5. We can confirm that the sock listener is started on the Pivot host:
```cmd
netstat -antb | findstr 1080
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928091655.png)

![[Proxifier#Forwarding traffic with Proxifier]]

We can now connect tot devices reach devices within the network of the target server and tunnel our network traffic over the established RDP session. Meaning, if we start another RDP session it will automatically be tunneled to the target Server
## Important Parameter
