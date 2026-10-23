---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - ssh, 22
---
# SSH (Secure Shell)

**Default Ports:** `22` (TCP)
**Description:** An encrypted network protocol for secure remote CLI control of hosts. It is often used as the primary means of access following successful credential harvesting or key extraction.

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration
![[Scripts#^2f433f]]

## 02 - Connecting to Service
### 2.1 - Establishing connection
#### id_rsa
How to use keyfile:
1. change rights, so it’s only executable for the current user
```bash
chmod 600 id_rsa
```

2. Login using the private key and credentials
```bash
ssh -i id_rsa username@10.129.155.4
```

#### Reverse Port Forwarding (SSH)
```bash
ssh -R <InternalIPofPivotHost>:8080:0.0.0.0:8000 ubuntu@<ipAddressofTarget> -vN
```

#### Linux - Dynamic Port Forwarding (SSH)
Setup listener on the client and forwarding "connections" to the target server via:
```bash
ssh -D 9050 ubuntu@10.129.202.64
```
In order for this to work we will need to setup a SOCKS-Proxy Tool like `proxychains` , so that the "connections" get `intercepted` and `forwareded` to the (in this case) ssh server: [[proxychains]]

#### Local Port Forwarding (SSH)
This command allows us to open a ssh-session on our client on port `1234` to the destination `IP` and  instruct the target to forward the traffic to `localhost:3306`.
```bash
ssh -L 1234:localhost:3306 ubuntu@10.129.202.64
```
`What is the advantage?` This way we have an established SSH-Tunnel , which allows us to bypass possible firewall rules (e.g. DENY mysql/3306). The main benefit is, that we can access these services with our local tools now, such as "DBeaver" by sending its requests to our local listener/forwarder (in this case, `1234`).

It is also possible to do this for multiple ports simultaneously:
```bash
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64
```
### 2.2 - SSH command sequence after establishing a connection

1. find specific file, whilst connected:
```bash
find / -name "filname.txt" 2>/dev/null
```

### 2.3 - Setting up SSH Server
1. enabling SSH Server:
```bash
sudo systemctl enable ssh
```
2. Starting the SSH Server:
```bash
sudo systemctl start ssh
```
3. Checking for SSH Listening port:
```bash
netstat -lnpt
```
#### Transferring files to SSH Server using SCP
```bash
scp LOCAL-FILE USERNAME@192.168.49.128:/PATH/FILENAME.txt
```


### 2.9 - Bruteforcing Credentials
![[Hydra#^ec80b8]]
