---
type: tool
category: dns
tags:
  - tool
---
# Overview

#### Using subrute DNS-ENUM
1. Feed `resolver.txt` with the known dns-server:
```bash
echo "10.129.203.6" > /run/media/breezy/PortableSSD/THM/Scripts/subbrute/resolvers.txt
```

2. Execute the script:
```python
python3 /run/media/breezy/PortableSSD/THM/Scripts/subbrute/subbrute.py inlanefreight.com -s /run/media/breezy/PortableSSD/THM/Scripts/subbrute/names.txt -r /run/media/breezy/PortableSSD/THM/Scripts/subbrute/resolvers.txt
```
## Important Parameter
