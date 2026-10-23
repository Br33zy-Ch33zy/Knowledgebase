`IMPORTED FROM LIBRE OFFICE`
# Scope
This second server is a server that everyone on the internal network has access to. In our discussion with our client, we pointed out that these servers are often one of the main targets for attackers and that this server should be added to the scope.

Our customer agreed to this and added this server to our scope. Here, too, the goal remains the same. We need to find out as much information as possible about this server and find ways to use it against the server itself. For the proof and protection of customer data, a user named HTB has been created. Accordingly, we need to obtain the credentials of this user as proof.

# Procedure
1. First I did a fast TCP-scan to see what we are dealing with:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124926.png)

2. I will start enumerating “smb” properly. But whilst I’m at it I also try to get the version (and service) of the other ports:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124932.png)
Guest login is not possible...
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124939.png)
The more thorough scan mentions the smb2-version 3.1.1, which is has a potential RCE-vulnerability.
 3. I want to further check, if I can gain more information about the windows-infrastructure with “samrdump.py” and “enum4Linux-ng.py”:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124949.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125002.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125017.png)

4. Metasploit also verifies the OS-version 10.0.17763 and smb2 version 3.1.1:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125025.png)
According to MS only Version 1903 and 1909 are affected by this vulnerability. Therefore this is probably not that case here (but would be worth checking in the post exploitation phase). Since it is also a pretty aggressive attack, I will leave it here. https://msrc.microsoft.com/update-guide/en-US/advisory/CVE-2020-0796


5. After reviewing the Nmap-scan again I decided to focus on RPC(NFS) next. 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125032.png)

6. I checked for available shares, mounted it and tried to access it. Which currently is not possible, because of missing access rights of my local user.
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125037.png)

7. It’s difficult to get a foothold to this system: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125047.png)

8. Also further efforts to gather more information, such as the UID of the mounted folder doesn’t work out (UID “65534” = user “nobody”):
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125051.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125059.png)
 
9. Since the initial port scan was mainly for TCP/Ports, I also checked the UDP/Ports now, which was basically the same result:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125104.png)
   
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125112.png)

10. After further evaluating the different ports/services and additional scanning of rpc-services via “rpcdump.py” I wasn’t sure anymore if I maybe have overlooked something or made a mistake. That’s why I decided to check a “walkthrough” for help and continued without it afterwards. 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125120.png)


11. This is, when I realized, that “root” was needed in order to access the contents of the share:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125125.png)


12. At first glance, it was clear that all but one file was “O bytes” in size. I therefor checked the contents of this file and found some credentials:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125131.png)

13. Which happened to be windows credentials for the Server. After connecting to the server I checked the groups of “alex” and if there are any other local users like “HTB”, but that was not the case:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125137.png)

14. After checking the local folders and files I found the credentials of an sql DB:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125141.png)

15. I tried to login to the DB with the credentials, but it didn’t work. I than checked if it could be a hash and it is probably a “DES” hash.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125150.png)
  
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125156.png)

16. After trying to decrypt it via “DES” it didn’t work. So I rechecked the with “hashid” and “nth” and both couldn’t specify a hashvalue.
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125201.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125208.png)
 
17. Whilst trying to get access to possibly unencrypted DB-files on the system, I was prompted to enter the admin password. I just entered the found password and it worked:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125214.png)

18. After further investigating the folder contents I found a possible “SQL-Admin”:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125223.png)

19. But that didn’t work as expected: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125233.png)

20. I now connected over RDP directly as “Administrator” and realized, that here his “Windows Authentication” is used for login to the sql-server:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125244.png)

21. After manually checking the contents of the DB I found a DBO called “accounts”, which looked pretty promising. In Order to analyze it quicker I exported the contents:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125251.png)

22. After figuring out how to export it, I was quickly able to get the credentials of user “HTB”:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918125302.png)

# Lessons-Learned
In this exercise I made some small mistakes, which led to bigger hurdles:
1. “mount” is only possible as privileged user, because else it would be possible as normal user to prepare “SUID-binaries”, mount them and escalate the privileges to root.
This is why the error “failed to apply fstab options” appears. The system checks if the executing user is listed in the “/etc/fstab” file. If this is not the case he simply has no rights to execute the mount command…

2. It’s not possible to execute “sudo cd” since “cd” is no program and therefor has no binary file such as e.g. “ls  (/usr/bin/ls)”. 
It would also make no sense even if it would be  a program. Because “sudo cd” would create a new process and would only change the location of this newly created process and than kill the process. Thus, nothing would change in the original terminal window.

3. My local user “breezy” couldn’t access the NFS-share, because “no_root_squash” was active on the nfs-server and that only affects the root-UID “0”.

4. A simple check of folder/file permissions would have shown, that only the root-user has access to them.

5. After checking how others obtained the content of the “HTB” user. I realized, that it would have been much saver and quicker to export the user contents directly (without exporting all users into the file) with the query:
SELECT * FROM accounts.dbo.devsacc WHERE NAME = ‘HTB’

*6. I’m aware, that in a real Pentest-scenario, sensitive data like passwords and login-credentials are handled more carefully and not just added as screenshot into the “Pentest-report”. But for the time being my main focus is on the technical aspect.