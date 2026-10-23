---
type: tool
category: windows
tags:
  - tool
---
# WES-NG
## Example Usage

### WES-NG with  `Systeminfo` Output
1. Get `Systeminfo` output from target and for example copy paste it into the file *sysinfo.txt* (At least "OS Name" and "Hotfixes" should be included).
2. Set the filters needed, it's recommended to use `-e`, this way only CVE's which have public available exploits are shown:
```bash
python3 wes.py sysinfo.txt --impact "Elevation of Privilege" -e > cves-privilege.txt
```

## Important Parameter
python3 wes.py
	`--impact` = allows filtering for e.g. "Elevation of Privilege"
	`-e` = only shows CVE's with publicly available exploits