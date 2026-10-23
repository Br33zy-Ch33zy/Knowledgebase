---
type: tool
category: smtp
tags:
  - tool
---
# Overview

## Commands
#### User-ENUM
> [!INFO] Note
Only works if the features "VRFY, EXPN and RCPT" are active! 
And don't forget to switch between the different Modus (-M).


Automate User-ENUM with username list and `VRFY`:
```bash
smtp-user-enum -M VRFY -U /home/breezy/Downloads/footprinting-wordlist.txt -t 10.129.203.12 -w 15 -m5
```
Depending on the server implementation and enumeration mode, we need to add the domain for the email address with the argument `-D`:
```bash
smtp-user-enum -M VRFY -U /home/breezy/Downloads/footprinting-wordlist.txt -D inlanefreight.htb -t 10.129.203.12 -w 15 -m5
```
## Important Parameter
