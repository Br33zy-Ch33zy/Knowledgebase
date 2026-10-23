---
type: tool
category: shares,smb
tags:
  - tool
---
# Overview
Great tool to scrapp network shares for keywords such as `password` or `user`.
https://github.com/blacklanternsecurity/MANSPIDER
## How to use
1. Start docker container, search for keywords on accessible shares and download all files containing them:
```bash
sudo docker run --rm -v ./manspider:/root/.manspider blacklanternsecurity/manspider 10.129.234.173 -f passw user admin account login logon cred -u 'USER' -p 'PASSWORD'
```
2. To further narrow down the results, filter the folder containing the scan-files (located in the folder running the docker container) for keywords such as `admin`:
```bash
grep -rni 'admin'
```
## Important Parameter
manspider
	`-f` = searches for words which follow after parameter