---
type: tool
category: va
tags:
  - tool
download: https://www.tenable.com/downloads/nessus?loginAttempted=true
---
# Overview

## How to setup
1. Download it from the Download Page "https://www.tenable.com/downloads/nessus?loginAttempted=true" (if needed register for "Nessus Essentials" )
2. And install the .deb package 
3. Start the Nessus service:
```bash
sudo systemctl start nessusd.service
```
4. Access Nessus over the localhost (default-port 8834): `https://localhost:8834`
5. After entering the activationcode we can run the setup

## Scan-Options
### Discovery

In the Discovery section, under Host Discovery, we're presented with the option to enable scanning for fragile devices. Scanning devices such as network printers often result in them printing out reams of paper with garbage text, leaving the devices unusable. We can leave this setting disabled: 
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260826172727.png)

### Assessment

Under the `Assessment` category, web application scanning can also be enabled if required, and a custom user agent and various other web application scanning options can be specified (e.g., a URL for Remote File Inclusion (RFI) testing):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260826172933.png)

### Advanced

On the `Advanced` tab, safe checks are enabled by default. This prevents Nessus from running checks that may negatively impact the target device or network. We can also choose to slow or throttle the scan if Nessus detects any network congestion, stop attempting to scan any hosts that become unresponsive, and even choose to have Nessus scan our target IP list in random order:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260826173105.png)