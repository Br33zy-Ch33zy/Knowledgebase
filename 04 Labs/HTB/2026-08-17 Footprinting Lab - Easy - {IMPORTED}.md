`IMPORTED FROM LIBRE OFFICE`
# Scope
We were commissioned by the company Inlanefreight Ltd to test three different servers in their internal network. The company uses many different services, and the IT security department felt that a penetration test was necessary to gain insight into their overall security posture.

The first server is an internal DNS server that needs to be investigated. In particular, our client wants to know what information we can get out of these services and how this information could be used against its infrastructure. Our goal is to gather as much information as possible about the server and find ways to use that information against the company. However, our client has made it clear that it is forbidden to attack the services aggressively using exploits, as these services are in production.

Additionally, our teammates have found the following credentials "ceil:qwer1234", and they pointed out that some of the company's employees were talking about SSH keys on a forum.

The administrators have stored a flag.txt file on this server to track our progress and measure success. Fully enumerate the target and submit the contents of this file as proof.

# Procedure
1. First I did a fast and noisy scan to check for the scope of the server:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124608.png)

2. Then I did a more thorough scan to gather information about the DNS-Service:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124620.png)

3. To make sure if the DNS is running on said BIND-Version, I did a short dig to verify:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124625.png)
 
4. After running different host-enum scripts and other methods. I figured out the potential domain-name “inlanefreight.htb”, whilst looking up the ftp-version via netcat:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124633.png)

5. In order to gather more information about the domain-infrastructer, I performed a zone-transfer request and in the background a dnsenum pn the “internal” network and decided to further check the other services in the meantime:
 ![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124638.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124644.png)

6. So I tried a quick banner-grab with netcat:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124652.png)

7.  Then I tried to connect to ssh with the given credentials of the “teammates”. And figured, that a private key is needed first:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124658.png)

8. Therefore I started enumerating the 2x FTP-services further.
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124703.png)


9. And tried to connect anonymously. And I realized, that I totally missed before, that the second FTP, is called “Ceil’s FTP”, which is the name of the possible login provided by the “teammates”: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124713.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124722.png)

10. An indeed, the credentials provided work. I then quickly found the private key “id_rsa” and downloaded it:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124729.png)

11. After that, I could easily log in to the ssh-service and find the flag and it’s content:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124736.png)
 

12. Btw. “dnsenum” found a couple of internal devices:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260918124744.png)