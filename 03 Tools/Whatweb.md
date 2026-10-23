---
type: tool
category: web
tags:
  - tool
---
# Overview

## Quick Commands
### Information gathering 
Grab website-information such as banner (aggressive scan):
```bash
whatweb -a 3 https://domain.com | tee whatweb
```

^91d4af


Gather information about website services of specific vhost:
```bash
whatweb -H "Host: app.inlanefreight.local" http://10.129.42.195
```


## Important Parameter
