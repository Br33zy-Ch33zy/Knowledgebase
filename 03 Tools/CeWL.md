---
type: tool
category: reconnaissance
tags: [tool/recon, wordlists, passwords, OSINT]
aliases: [cewl]
---

# Overview
**Description:** Ruby app that spider-crawls a given URL to a specified depth and returns a custom wordlist based on the unique words found on the site (ideal for targeted password cracking).

## Commands
Example:
```
cewl https://URL/ -d 4 -m 6 --lowercase -w test.txt
```