---
type: tool
category: va
tags:
  - tool
---
# Overview

## How to setup
1. Download OpenVAS:
```bash
sudo apt-get install gvm && openvas
```
2. Start the setup process (can take up to 30 minutes):
```bash
gvm-setup
```
3. After the setup is completed, we can start OpenVas:
```bash
gvm-start
```
4. Access webapp via: 
```text
https://< IP >:8080
```
## Scan-Options
OpenVAS has various scan configurations to choose from for scanning a network. We recommend only leveraging the ones below, as other options could cause system disruptions on a network:

- `Base`: This scan configuration is meant to enumerate information about the host's status and operating system information. This scan configuration does not check for vulnerabilities.
- `Discovery`: This scan configuration is meant to enumerate information about the system. The configuration identifies the host's services, hardware, accessible ports, and software being used on the system. This scan configuration also does not check for vulnerabilities.
- `Host Discovery`: This scan configuration solely tests whether the host is alive and determines what devices are `active` on the network. This scan configuration does not check for vulnerabilities as well. _OpenVAS leverages ping to identify if the host is alive._
- `System Discovery`: This scan enumerates the target host further than the 'Discovery Scan' and attempts to identify the operating system and hardware associated with the host.
- `Full and fast`: This configuration is recommended by OpenVAS as the safest option and leverages intelligence to use the best NVT checks for the host(s) based on the accessible ports.

### Export Scans
Scans can be exported e.g. as "Anonymous xml" under: `Scans / Last Report`
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260826185741.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020260826185331.png)