---
type: tool
category: web
tags:
  - tool
---
Entire folder structure of Lazagne is needed. Therefor recommended to transfer as .zip file.

# Overview
LaZagne is a great tool for finding passwords on compromised systems.
It is made up of `modules` which each target different software when looking for passwords. Some of the common modules are described in the table below:



|Module|Description|
|---|---|
|browsers|Extracts passwords from various browsers including Chromium, Firefox, Microsoft Edge, and Opera|
|chats|Extracts passwords from various chat applications including Skype|
|mails|Searches through mailboxes for passwords including Outlook and Thunderbird|
|memory|Dumps passwords from memory, targeting KeePass and LSASS|
|sysadmin|Extracts passwords from the configuration files of various sysadmin tools like OpenVPN and WinSCP|
|windows|Extracts Windows-specific credentials targeting LSA secrets, Credential Manager, and more|
|wifi|Dumps WiFi credentials|
## Quick Commands
#### Windows
Run all available modules very verbose:
```cmd
start LaZagne.exe all -vv
```

#### Linux
```bash
sudo python2.7 laZagne.py all
```

^4b5ebc

## Important Parameter
