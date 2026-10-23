---
type: tool
category: web-pentesting
tags: [tool/web, proxy, owasp-zap, intercept, automated-scanner, open-source]
aliases: [OWASP ZAP, zap]
---
# OWASP ZAP (Zed Attack Proxy)

**Description:** Free, open-source intercepting proxy and automated web application scanner maintained by OWASP. Ideal for automated baseline security scans, API testing, and continuous integration pipelines.

---

# How to Use
## Intercepting Requests

### Turn On and Off
In ZAP, interception is off by default, as shown by the green button on the top bar (green indicates that requests can pass and not be intercepted).
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013085904.png)

## HUD 
ZAP also has a powerful feature called `Heads Up Display (HUD)`, which allows us to control most of the main ZAP features from right within the pre-configured browser. We can enable the `HUD` by clicking its button at the end of the top menu bar:

![Toolbar with icons, 'Standard Mode' dropdown, and 'Sites' section with a plus icon.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/110/zap_enable_HUD.jpg)

![Ping interface with IP input '127.0.0.0', Ping button, and side controls for sites, start, and status indicators.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/110/zap_hud_break.jpg)

## Fuzzing
### Fuzzing Cookie-Credentials
In this example we will `fuzz` the guest-cookie, decode it and fuzz for other users:
1. Click through to the desired Request, then right click and choose `fuzz..` (not visible in the example):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013124318.png)
2. Than add the desired `fuzzing-list` in this case "top-usernames-shortlist.txt" from seclists via `Payloads.../Add.../Add`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013130418.png)
3. Now select the chosen list, select `Processors..` and chose the Type of encoding (in this example MD5). We can also check the results with `Generate Preview`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013130529.png)

4. Than start fuzzer with `Fuzz` and check `Size Resp. Body` for differentiating values  (as in our case "450", which was successful):
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013131137.png)
# How to Setup 

## Install CA Certificate
To get ZAP's certificate, we can go to (`Tools>Options>Network>Server Certificates`), then click on `Save`:
![Dynamic SSL Certificates window with options list, certificate text, and 'Generate', 'Import', 'View', 'Save' buttons.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/110/zap_cert.png)

Afterwards we can add it to the browser.