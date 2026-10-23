---
type: tool
category: network, network-traffic
tags:
  - tool
---
# Overview

## How to use
#### Terminal
```bash
sudo tcpdump -i ens224 
```

## Useful Filters
Filters for HTTP POST requests. It may be the case that passwords or other sensitive information (e.g. credit card, etc) is contained within.
```bash
http.request.method == "POST"
```