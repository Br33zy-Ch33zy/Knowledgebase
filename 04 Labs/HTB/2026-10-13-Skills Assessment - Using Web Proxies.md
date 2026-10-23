---
platform: hackthebox
difficulty: unknown
status: Completed
date: 2026-10-13
tags:
---
# HTB: Skills Assessment - Using Web Proxies

**Targets:** 

| Websites                             |
| ------------------------------------ |
| http://154.57.164.76:33226/lucky.php |
| http://154.57.164.76:33226/admin.php |


---

## 01 - Scope
### Assignment:
We are performing internal penetration testing for a local company. As you come across their internal web applications, you are presented with different situations where Burp/ZAP may be helpful. Read each of the scenarios in the questions below, and determine the features that would be the most useful for each case. Then, use it to help you in reaching the specified goal.
### Objectives:
- **Primary Goals:**
  - [x] The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag.
`HTB{d154bl3d_bu770n5_w0n7_570p_m3}`
  - [x] The /admin.php page uses a cookie that has been encoded multiple times. Try to decode the cookie until you get a value with 31-characters. Submit the value as the answer.
`3dac93b8cd250aa8c1a36fffc79a17a`
  - [x] Once you decode the cookie, you will notice that it is only 31 characters long, which appears to be an md5 hash missing its last character. So, try to fuzz the last character of the decoded md5 cookie with all alpha-numeric characters, while encoding each request with the encoding methods you identified above. (You may use the "alphanum-case.txt" wordlist from Seclist for the payload)
`HTB{burp_1n7rud3r_n1nj4!}`
  - [x] You are using the 'auxiliary/scanner/http/coldfusion_locale_traversal' tool within Metasploit, but it is not working properly for you. You decide to capture the request sent by Metasploit so you can manually verify it and repeat it. Once you capture the request, what is the 'XXXXX' directory being called in '/XXXXX/administrator/..'?
`CFIDE`

---

## 02 - Procedure
1. First I browsed the webpage `http://154.57.164.76:33226/lucky.php` , intercepted the response with `BurpSuite` and changed the value `disabled` to `enabled`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013183731.png)

2. Afterwards I was able to send a request with the `getflag=true` value. I forwarded it to the Repeater and spammed it a couple of times until i received the flag:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013184108.png)

3. I then browsed the page `http://154.57.164.76:33226/admin.php`and intercepted the response again (this time with `ZAP`), containing the mentioned cookie:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013184558.png)

4. I selected the cookie-value and opened it in `Encode/Decode/Hash`, where I copied the `ASCII Hex Decode` and pasted it again, which lead me to the `Base64 Decode`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013185116.png)

![](/00-Meta/Objects/Pictures/Pasted%20image%2020261013185138.png)
Which happened to be the 31-Characters long value, we are looking for:
```incomplete-Hash
3dac93b8cd250aa8c1a36fffc79a17a
```

5. First I created a "Combolist" of `seclists` alphanumeric list and the incomplete hash:
```bash
sed 's/^/3dac93b8cd250aa8c1a36fffc79a17a/' /usr/share/seclists/Fuzzing/alphanum-case.txt > ZAP.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014084018.png)

5. I then setup a "fuzz" with the created list:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014084403.png)

6. And encoded the now complete hashes again with `Base64` and `ASCII-HEX`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014085342.png)

Unfortunately `ZAP` doesn't support `ASCII Hex` type encoding in the fuzzing-tool. I therefor encoded the values via CLI-scripts:
```bash
while IFS= read -r line; do echo -n "$line" | base64 -w 0; echo; done < ZAP.txt > base64.txt
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014090754.png)

```bash
python3 -c "import sys; open('hex.txt', 'w').writelines(line.strip().encode('utf-8').hex() + '\n' for line in open('base64.txt') if line.strip())"
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014100529.png)

I therefor started a new fuzz, with the generated hash-list `hex.txt`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014100606.png)

And like that, all of the Responses with the`Size Resp. Header 338` contained the flag:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014101059.png)

7. For the last one we need to work with a `Metasploit` scanner and inspect its request with a `Proxy`:
First I set the scanner settings, including the proxy:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014101630.png)
I then prepared the listener in `BurpSuite` on 127.0.0.1:8080 and ran the scanner. Burp intercepted it and provided the needed directory `CFIDE`
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261014103202.png)


## 10 - Lesson Learned
Even tho `ZAP` has many nice features, `BurpSuite` is much smoother. Working with `ZAP` always takes a certain amount of tinkering to make it work.