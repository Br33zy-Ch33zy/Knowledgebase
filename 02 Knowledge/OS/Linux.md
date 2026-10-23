---
type: knowledge
category: os, linux
tags:
  - knowledge/os
aliases:
  - linux
---
# Enumeration
The default`ttl` of a linux host is typically `64`  :
```text
PING 192.168.0.135 (192.168.0.135): 56 data bytes
64 bytes from 192.168.86.39: icmp_seq=0 ttl=64 time=102.920 ms
64 bytes from 192.168.86.39: icmp_seq=1 ttl=64 time=9.164 ms
64 bytes from 192.168.86.39: icmp_seq=2 ttl=64 time=14.223 ms
64 bytes from 192.168.86.39: icmp_seq=3 ttl=64 time=11.265 ms
```

## Ping Sweep in Linux terminal
```bash
for i in $(seq 1 254); do (ping -c 1 172.16.5.$i | grep "bytes from" &); done
```

# Pre Privilege Escalation
1. Check what the user can execute as root:
```bash
sudo -l
```
2. Check the system version for possible CVE:
```bash
lsb_release -a
```
3. Check UID & GID:
```bash
id && groups
```
4. Check SUID/SGID-Binaries:
```bash
find / -perm -4000 2>/dev/null
```
### Enum wit `linpeas`

## Check for possible attack vectors, such as: 
- Configuration files
- Databases
- Notes
- Scripts
- Cronjobs
- SSH keys

1. Search `configuration files`:
```bash
for l in $(echo ".conf .config .cnf");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done
```
We can also optimize the scan and also search for key words such as `user,password or pass` inside the found configuration files:
```bash
for i in $(find / -name *.cnf 2>/dev/null | grep -v "doc\|lib");do echo -e "\nFile: " $i; grep "user\|password\|pass" $i 2>/dev/null | grep -v "\#";done
```

2. The script can also be applied to other crucial system components, such as `databases`:
```bash
for l in $(echo ".sql .db .*db .db*");do echo -e "\nDB File extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share\|man";done
```

3. Check for `notes` in the userdirectories:
```bash 
find /home/* -type f -name "*.txt" -o ! -name "*.*"
```

4. `Scripts`:
```bash
for l in $(echo ".py .pyc .pl .go .jar .c .sh");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share";done
```

5. Enumerate `cronjobs`:
```bash
cat /etc/crontab 
```

6. Check `history` files for e.g. commands-history:
```bash
tail -n5 /home/*/.bash*
```

7. Here are some strings to use , to find interesting contents in `logs`:
```bash 
for i in $(ls /var/log/* 2>/dev/null);do GREP=$(grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null); if [[ $GREP ]];then echo -e "\n#### Log file: " $i; grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null;fi;done
```

### Gathering Credenitals
with `laZagne`:
![[LaZagne#^4b5ebc]]

# Domain joined Linux
## Pass the certificate
## Pass the Ticket

Quick and easy way to gather information such as users, tickets, etc.
![[Linikatz#^fd2104]]
### Identify AD integration
```bash
realm list
```

```bash
ps -ef | grep -i "winbind\|sssd"
```
### Finding KeyTab files
> [!INFO] Note
A Linux ticket is represented as a keytab file located by default at `/etc/krb5.keytab` and can only be read by the root user.

A simple way is to search for files containing `keytab` in the name:
```bash
find / -name *keytab* -ls 2>/dev/null
```

or via `cronjobs`:
```bash
crontab -l
```
###
### Show currently active Ticket
```bash
klist
```
#### Checking ccache files
Once a user authenticates to the domain, a ccache file is created that stores the ticket information. The path to this file is placed in the `KRB5CCNAME` environment variable. This variable is used by tools that support Kerberos authentication to find the Kerberos data. The environment variable can be located like that:
```bash
env | grep -i krb5
```

The systemwide ccache-files are located in /tmp and often contain `krb5c`:
```bash
ls -la /tmp | grep -i krb5c
```

#### Loading Ccache file 
```bash
export KRB5CCNAME="FILE:/tmp/jpinkman.ccache"
```

Making sure it is loaded:
```
klist
```
### Using KeyTab files
To use a keytab file, we need to know which user it was created for. `klist` is another application used to interact with Kerberos on Linux. This application reads information from a `keytab` file.
```bash 
klist -k -t /opt/specialfiles/carlos.keytab
```
![[Scripts#TicketConverter]]
#### Loading Keytab file into klist
In order to impersonate another user, we will need to request their TGT (with e.g. a locally stored keytab file) and load it into our `klist`:
1. Replace the ccache environmental variable with a new file (so the currently active sessions doesn't get overwritten) 
```bash
export KRB5CCNAME=/tmp/krb5cc_script_temp
```
2. Request a new TGT with the keytab of another user and load it into the previously created ccache:
```bash
kinit svc_workstations@INLANEFREIGHT.HTB -k -t /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt
```

![[Smbclient#Connect to SMB-Share with Kerberos TGT]]

![[Scripts#Extracting KeyTabe hashes]]

A quick way to decrypt passwords can be with online repositories such as [https://crackstation.net/](https://crackstation.net/), which contains billions of passwords.

![[xfreerdp#Pass the Hash (using RDP)]]


![[xfreerdp#Pass the Ticket (using RDP)]]
### Example
1. 
# Post Privilege Escalation
1. Check for other users, such as e.g. "mysql"
```bash
cut -d: -f1 /etc/passwd
```

## Decrypt local passwords
1. Make a copy of  `/etc/passwd` and `etc/shadow`:
```bash
sudo cp /etc/passwd /tmp/passwd.bak
```

```bash
sudo cp /etc/shadow /tmp/shadow.bak
```

2. combine the to files into one, so we can crack it later:
```bash
unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes
```

3. Decrypt paswords with hashcat:
![[Hashcat#^220f8c]]
# File Transfer & Fileless attacks
## Using Base64
1. Check the MD5-hashvalue to ensure the integrity of the data later:
```bash
md5sum FILENAME
```
2. Encode file/data in base64
```bash
cat FILENAME |base64 -w 0;echo
```
3. Copy&Paste the encoded data to the target system (linux) and decode file/data:
```bash
echo -n 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo=' | base64 -d > FILENAME
```
4. Confirm the hashvalue from step "1." to make sure, that the data hasn't changed:
```bash
md5sum FILENAME
```

## Using SMB Server

![[Scripts#smbserver.py]]

## Using FTP Server

![[FTP#Python FTP Server]]

## Using HTTP Server
![[Scripts#http server]]

## Using SSH Server
![[SSH#2.2 - Setting up SSH Server]]
## Local files explained
## General Information about Processes
Every process (like e.g. bash) receives 3x standard datachannels from the operatingsystem:

| File Descriptor | Stream Name  | Purpose / Direction                        | Behavior with Pipes (e.g. bind shell)               |
| :-------------- | :----------- | :----------------------------------------- | :-------------------------------------------------- |
| **`0`**         | **`stdin`**  | Reads commands/data **INTO** the process   | Receives input from the pipe (`cat /tmp/f \|`)      |
| **`1`**         | **`stdout`** | Writes regular output **FROM** the process | Forwards results via `\|` to the destination (`nc`) |
| **`2`**         | **`stderr`** | Writes error messages **FROM** the process | Is redirected to `stdout` via `2>&1`                |

### Living off The Land
[GTFOBins for Linux Binaries](https://gtfobins.github.io/)

### /bin/bash
This is the "normal" shell in many linux distributions.

### /etc/passwd
Contains system users (e.g., `mysql`, `www-data`) as well as regular user accounts.
```bash
mysql:x:109:117:MySQL Server,,,:/nonexistent:/bin/false
  1   2  3   4          5              6            7
```

| Field | Field Name | Meaning / Description | Example Value |
| --- | --- | --- | --- |
| **1** | Username | The user's login name. | `mysql` |
| **2** | Password | An `x` indicates that the encrypted password is stored in `/etc/shadow`. | `x` |
| **3** | UID | User ID (`0` = root, `<1000` = system user, `>=1000` = regular user). | `109` |
| **4** | GID | Group ID of the user's primary group. | `117` |
| **5** | GECOS | Comment field (description, full name, room number, etc.). | `MySQL Server,,,` |
| **6** | Home Directory | Path to the home directory (`/nonexistent` = no directory). | `/nonexistent` |
| **7** | Default Shell | Login shell (`/bin/false` or `/usr/sbin/nologin` blocks logins). | `/bin/false` |
When this file is writable, it is possible to e.g. remove the `Password` field for root and thus allow us to use sudo without password.
### /etc/resolve.conf
Defines the DNS-Server responsible for local nameresolution on the linux machine.

### /etc/security/opasswd
The PAM library (`pam_unix.so`) can prevent users from reusing old passwords. These previous passwords are stored in the `/etc/security/opasswd` file.
```
Ezyrlyb@htb[/htb]$ sudo cat /etc/security/opasswd

cry0l1t3:1000:2:$1$HjFAfYTG$qNDkF0zJ3v8ylCOrKB0kt0,$1$kcUjWZJX$E9uMSmiQeRh4pAAgzuvkq1
```
### /etc/shadow
Is the default location for hashed passwords.
The `/etc/shadow` file is also only readable by users with administrative privileges. The format of this file is divided into the following `nine fields`:

```bash
htb-student:$y$j9T$3QSBB6CbHEu...SNIP...f8Ms:18955:0:99999:7:::
```

|Field|Value|
|---|---|
|Username|`htb-student`|
|Password|`$y$j9T$3QSBB6CbHEu...SNIP...f8Ms`|
|Last change|`18955`|
|Min age|`0`|
|Max age|`99999`|
|Warning period|`7`|
|Inactivity period|`-`|
|Expiration date|`-`|
|Reserved field|`-`|

If the `Password` field contains a character such as `!` or `*`, the user cannot log in using a Unix password. However, other authentication methods such as Kerberos or key-based authentication can still be used. The same applies if the `Password` field is empty, meaning no password is required for login.

The `Password` field also follows a particular format, from which we can extract additional information:

- `$<id>$<salt>$<hashed>`

As we can see here, the hashed passwords are divided into three parts. The `ID` value specifies which cryptographic hash algorithm was used, typically one of the following:

|ID|Cryptographic Hash Algorithm|
|---|---|
|`1`|[MD5](https://en.wikipedia.org/wiki/MD5)|
|`2a`|[Blowfish](https://en.wikipedia.org/wiki/Blowfish_\(cipher\))|
|`5`|[SHA-256](https://en.wikipedia.org/wiki/SHA-2)|
|`6`|[SHA-512](https://en.wikipedia.org/wiki/SHA-2)|
|`sha1`|[SHA1crypt](https://en.wikipedia.org/wiki/SHA-1)|
|`y`|[Yescrypt](https://github.com/openwall/yescrypt)|
|`gy`|[Gost-yescrypt](https://www.openwall.com/lists/yescrypt/2019/06/30/1)|
|`7`|[Scrypt](https://en.wikipedia.org/wiki/Scrypt)|
### Named Pipe (mkfifo)
A `Named Pipe` is essentially a file on the hard drive that serves as a buffer between two system processes: Process A writes data into the top of the file, and Process B reads it out from the bottom in exactly the same order (first in, first out).

A named pipe is created with  the command "make First in, First Out" (`mkfifo`) .

It is mainly used for setting up shells manually as described here:
[[Bind-Shells#Establishing a Basic Bind Shell with `Netcat`and `Named Pipe`]]

## Commands
