---
type: tool
category: web-pentesting
tags: [tool/web, proxy, burp-suite, intercept, repeater, intruder]
aliases: [Burp Suite, burp]
---
# Burp Suite

**Description:** Industry-standard intercepting proxy and web vulnerability assessment platform. Used for man-in-the-middle traffic inspection, manual testing via Repeater, automated parameter fuzzing via Intruder, and extension-based auditing.

---

# How to Use

## Intercepting Requests

### Turn On and Off
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013085806.png)

## Responder
### Turn On and Off
`Intercept responses based on the following rules:`
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013100039.png)
# How to Setup 

## Install CA Certificate
We can install Burp's certificate once we select Burp as our proxy in `Foxy Proxy`, by browsing to `http://burp`, and downloading the certificate from there by clicking on `CA Certificate`:
http://burp

![Burp Suite Community Edition header with 'CA Certificate' button.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/110/burp_cert.jpg)

Afterwards we can add it to the browser.