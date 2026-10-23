---
type: tool
category: dns
tags:
  - tool
---
# Overview

## Quick Commands
Fast check over all zones. Googles NS is used here because ISP's such as Swisscom often block "Any requests" :
```bash
dig @8.8.8.8 TARGET.COM any > dig-any.txt
```
^ad19f8

  - #speed/fast #stealth/low

DNS-Server Version ENUM. Asks for the Bind-Version over the “chaosnet” (used for management and control requests) inside the txt record. (Counterintuitively “version.bind” also works for other DNS-applications e.g. “NSD”, but not all of them e.g. MS DNS)
```bash
dig @10.129.2.48 version.bind txt ch
```

^314980

  - #speed/fast #stealth/low
#### Dig Standard Zones
```bash
dig ANY inlanefreight.htb @10.129.203.6
```

```bash
dig TXT inlanefreight.htb @10.129.203.6
```

```bash
dig MX inlanefreight.htb @10.129.203.6
```
#### Zone Transfer (AXFR)
If the NS-Server is poorly configured, it is possible to query the zonetransfer (AXFR) request, which can contain precious information about the domain-structure and possible hosts:
```bash
dig @10.129.44.95 inlanefreight.htb AXFR
```

And don't forget to query any found sub-zones/subsites for zone transfer. Just because the main domain doesn't allow zone transfers doesn't mean that's also the case for subzones:

```bash
dig @10.129.44.95 ns.inlanefreight.htb AXFR
```


## Important Parameter

## Useful Commands
Bruteforce subdomains via dig-script and subdomain-lists:
```bash
for sub in $(cat /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.dev.inlanefreight.htb @10.129.154.89 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done
```