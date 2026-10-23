---
type: tool
category: pivoting
tags:
  - tool
---
# Overview

## How to use
#### Installer
https://github.com/jpillora/chisel/releases
```bash
cd /run/media/breezy/PortableSSD/THM/Scripts/chisel/chisel_1.12.0_linux_amd64.gz
```
#### Dynamic Forwarding with Chisel (HTTP)
##### Pivot Host as Server
1. Upload `chisel binary` to `Pivot Host` and start server on it:
```bash
./chisel_1.12.0_linux_amd64 server -v -p 1234 --socks5
```
2. Starting client on attack box and connecting to server:
```bash
./chisel client -v 10.129.225.9:1234 socks
```
3. Add used port to the `/etc/proxychains4.conf` so we can use `proxychains`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925160527.png)
```/etc/proxychains4.conf
socks5 127.0.0.1 1080
```
> [!INFO] Note
There should only be one active socks entry at the time in `/etc/proxychains4.conf` 

##### Attack box as Server
1. Start server on attack box:
```bash
sudo chisel server --reverse -v -p 1234 --socks5
```
2. Start client on pivot host and connect to server:
```bash
./chisel_1.12.0_linux_amd64 client -v 10.10.14.17:1234 R:socks
```
3. Add port `/etc/proxychains4.conf ` in order to use proxychains:
```/etc/proxychains4.conf 
socks5 127.0.0.1 1080
```
> [!INFO] Note
There should only be one active socks entry at the time in `/etc/proxychains4.conf `

## Important Parameter
