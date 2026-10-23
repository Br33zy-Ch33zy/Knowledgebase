---
type: knowledge
category: methodology
tags:
  - knowledge/methodology
  - pivoting
  - lateral-movement
aliases:
  - pivoting
  - lateral-movement
---
# Pivoting
## Port Forwarding

### Reverse Port Forwarding
Allows us to make a service on our client available to the remote network. E.g. when we want to setup a `reverse shell` upload files with a `local python-webserver`.
![[Socat#Reverse Listener / Relay (Socat)]]

![[SSH#Reverse Port Forwarding (SSH)]]

![[Metasploit#Full Pivoting Example with Reverse Shell (Metasploit)]]
### Dynamic
`Dynamic Port Forwarding` means, that we can also access other reachable devices within the `target network` .

![[Ligolo-ng#Setup Layer-3 dynamic port forwarding (Ligolo)]]

![[Nmap#NMAP - Pivoting as unprivileged user]]

![[SocksOverRDP#Dynamic Forwarding (RDP)]]

![[Chisel#Dynamic Forwarding with Chisel (HTTP)]]

![[Sshuttle#Dynamic Forwarding (SSH - without proxychains)]]

![[SSH#Linux - Dynamic Port Forwarding (SSH)]]

![[Plink#Windows - Dynamic Port Forwarding (SSH)]]

![[Scripts#Dynamic forwarder to HTTP-Server (Rpivot)]]


### Static
Forwards all traffic on  a specific port of the pivot host to a defined target .

![[Netsh#Windows - Static Port Forwarding (Netsh)]]
### Local
`Local Port Forwarding` means, that we can only access services on  the `remote localhost`.

![[SSH#Local Port Forwarding (SSH)]]


# Lateral-Movement