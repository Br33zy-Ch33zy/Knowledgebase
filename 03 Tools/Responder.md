---
type: tool
category:
tags:
  - tool
---
# Overview

## Quick Commands
#### Linux Default (Responder)
```bash
sudo responder -I tun0 
```

^aea661

#### Listen to all Traffic
Start the `responder` in the analyze mode, which is passive:
```bash
sudo responder -I ens224 -A 
```
## Important Parameter
responder
	`-h` = help message
	`-A` = starts in "Analyze mode", which means, that he stays silent and doesn't answer requests