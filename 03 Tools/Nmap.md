---
type: tool
category: enumeration
tags:
  - tool
  - "#enum"
"Path to scripts:": /usr/share/nmap/scripts/
---
# Overview
## Filter script
This short script filters nmap scans for the port only, and  outputs them in the format `53,88,445....` for easier followup scans:
```bash
grep "Discovered open port" nmap.txt | awk -F'/' '{print $1}' | awk '{print $4}' | sort -n | uniq | paste -sd, -
```
## Quick Commands
Adjust speed and retry parameters (all ports, without DNS resolution (reverse lookup) and live results):
```bash
nmap -p- --min-rate 5000 --max-retries 1 -v -n 10.129.139.125
```
  - #speed/fast #stealth/low
Standard-Ports (top 50) Scan stealthy:
```bash
nmap -Pn -sS --top-ports 50 --scan-delay 2s -T2 10.129.58.86
```
  - #speed/slow #stealth/high

## Important Parameter
nmap
	  **`-A`** = Performs service detection, OS detection, traceroute and uses defaults scripts to scan the target.
	  **`-sC`** = Executes standard scripts
	  **`-sV`** = Version Scan
	  **`-sA`** = ACK-Scan, can bypass Firewall
	  **`-sn`** = without port scan (for Host Enum)
	  **`--packet-trace`** = Tracks every packet sent and received
	  **`-reason`** = Displays the reason for the result
	  **`--script=banner`** = Performs banner grabbing (similar to netcat, but with more detail)
	  **`--script vuln`** = Scans found services for known vulnerabilities (only works properly in 	combination with “-sV & -sC”
	  **`--traceroute`** = Creates Tracerout (lot ouf outputs)
	  **`--T <0-5>`** = Timing interval of packets sent (0 = paranoid | 5 = insane)
	  **`-D RND:5`** = Decoy, uses sends packets from decoy IP addresses (in this case 5) and in between from our real on to “hide” it
	  **`--disable-arp-ping`** = Disables arp ping (arpping is used for hostdiscovery)
	  **`--source-port <>`**  = Define source port used
## Useful Scans
#### Hostscan/Host-Discovery (aka. Ping Sweep)
The `-sn` option is great for host-discovery. Nmap basically waits for either an SYN/ACK or RST for the port 80, 445, 3389 and 22:
```bash
sudo nmap -sn -v -PS80,445,3389,22 172.16.0.0/23
```

### UDP-Scan, top 100 Ports:
```bash
sudo nmap -sU -F --version-intensity 0 -T4 --max-retries 1 --min-rate 1000 10.129.165.204
```

### Single service scan:
```bash
nmap -sV -sC -p 2323 <IP>
```

### IMAP
Execute all IMAP-Scripts:
```bash
nmap -p 143,993 --script="imap-*" -v -oN imap-script-scan.txt 10.129.165.204
```

^6d3200

### IPMI
Scan IPMI-Version (with default port): ^d1ac01
```bash
sudo nmap -p 623 -sU --script=ipmi-version IP
```

^1b19ec
### Pivoting
#### NMAP - Pivoting as unprivileged user 
When scanning through an unprivileged proxy or tunnel, `--unprivileged` forces Nmap to use standard operating system functions instead of raw sockets, eliminating the need for root privileges. Using `-sT` performs a full TCP connect scan via a standard three-way handshake (`connect()`), which works unprivileged compared to default SYN scans. Finally, `-Pn` skips the initial host discovery and ping probes, preventing targets with blocked ICMP from being falsely flagged as offline.
```bash
nmap --unprivileged -sT -Pn -p 3389 172.16.119.10
```

### SMB
Scan target for `Eternal Blue`:
```bash
nmap -p 445 --script smb-vuln-ms17-010 IP
```

^f49db0

### SNMP
Uses UDP-Ports (161,162,10161,10162) and thus needs an UDP-Portscan for the discovery, e.g:
```bash
nmap -p 161,162,10161,10162 --min-rate 5000 --max-retries 1 -v -n -sU IP
```
^69f8fa

SNMP-Script to get more information
```bash
nmap -sUV -p 161 --script="snmp-info,snmp-brute" IP
```

^5257ff

### DNS-ENUM
```bash
sudo nmap -sU -sS -p 53 --script "dns-service-discovery,dns-recursion,dns-nsid,dns-zone-transfer" 10.129.44.95
```


### Firewall
Check Firewall Filtered & Unfiltered Ports with ACK-Scan. Is not very reliable since there needs to be either an Inbound-Policy which allows the port/service or we are working with a stateless firewall or router.
```bash
sudo nmap 10.129.2.47 -p 21,22,80,3389 -sA -Pn -n --disable-arp-ping --packet-trace
```

## Stealthy Scans #stealth/high 
Stealth OS Scan, in order for it to work, there needs to be an open (e.g 80) and closed (e.g. 3389) port , so that the OS-Scan can differentiate the results. --osscan-limit starts the os scan only if there is an open and closed port. 
```bash
nmap -O --max-retries 1 --osscan-limit -p 80,3389 --scan-delay 1s -D RND:5 10.129.58.86
```



Stealth Full-Portrange scan. Over long period of time, mainly intended to keep in the background whilst further enumerating:
```bash
nmap -Pn -sS -p- --max-retries 1 --randomize-hosts --scan-delay 3s -D RND:5 10.129.58.86
```


## Attacks
### FTP Bounce Attack
An FTP bounce attack is a network attack that uses FTP servers to deliver outbound traffic to another device on the network. The attacker uses a `PORT` command to trick the FTP connection into running commands and getting information from another device e.g. another server

The `Nmap` -b flag can be used to perform an FTP bounce attack:
```bash
nmap -Pn -v -n -p80 -b anonymous:password@10.10.110.213 172.17.0.2
```