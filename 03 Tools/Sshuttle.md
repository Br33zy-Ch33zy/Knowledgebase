---
type: tool
category: pivoting
tags: [tool/pivoting, ssh, vpn, tunneling, linux, traffic-redirection]
aliases: [sshuttle]
---
# Sshuttle

**Description:** A transparent proxy server that works as a lightweight, agentless VPN over a standard SSH connection. Unlike standard SOCKS proxies (which require `proxychains` or browser settings), `sshuttle` redirects entire IP subnets and DNS requests directly through iptables/nftables on the local Linux attacker machine.

---

## Commands

#### Dynamic Forwarding (SSH - without proxychains)
In this example we include the network (172.16.5.0/23) we want to route through the pivot host/ssh session. This way there's no need for proxychains:
```bash
sudo sshuttle -r ubuntu@10.129.202.64 172.16.5.0/23 -v
```