---
type: tool
category: ssl/tls
tags:
  - tool
---
# Overview

## Useful commands
### Connect to Services
#### IMAPS
Connecting to IMAPS-Server over SLL/TLS:
```bash
openssl s_client -crlf -connect 10.129.155.175:993
```
^0f401f

#### POP3
```bash
openssl s_client -crlf -connect 10.129.155.175:995
```
^0cf4ad

#### SMTP
Connect and ignore certificate errors:
```bash
openssl s_client -connect 10.129.203.6:587 -starttls smtp -ign_eof
```

^8b8445

### Encrypt & Decrypt Files Using Openssl
To encrypt a file using `openssl` we can select different ciphers, see [OpenSSL man page](https://www.openssl.org/docs/man1.1.1/man1/openssl-enc.html). Let's use `-aes256` as an example. We can also override the default iterations counts with the option `-iter 100000` and add the option `-pbkdf2` to use the Password-Based Key Derivation Function 2 algorithm. When we hit enter, we'll need to provide a password.
1. Encrypt:
```bash
openssl enc -aes256 -iter 100000 -pbkdf2 -in /PATH/TOFILE.TXT -out ENC-FILE.TXT
```
2. Decrypt:
```bash
openssl enc -d -aes256 -iter 100000 -pbkdf2 -in /PATH/ENC-FILE.TXT -out DEC-FILE.TXT
```