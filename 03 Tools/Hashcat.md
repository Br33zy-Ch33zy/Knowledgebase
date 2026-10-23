---
type: tool
category: hash
tags:
  - tool
---
# Overview

## How to use it
1. Put hash-value into file:
```bash
echo "d033e22ae348aeb5660fc2140aec35850c4da997" > hash.txt
```
2. Define Hashing-algorithm via -m  (https://hashcat.net/wiki/doku.php?id=example_hashes)
```bash
hashcat -m 100 hash.txt /usr/share/wordlists/rockyou.txt
```

## Important Parameter
hashcat
	`- r rules/best64.rule` = Modifies passwords according to the top 64 hashcat-rules, e.g. transforms “E” to “3” or changes capslock of certain letters.
	`-m 000` = Define which hashing-algorithm to use  (https://hashcat.net/wiki/doku.php?id=example_hashes)
	`-b` = Perform a benchmark test 

## Bruteforcing
### Kerberos 5 TGS-REP etype 23 (RC4-HMAC) 
```bash
hashcat -m 13100 sqldev_tgs /usr/share/wordlists/rockyou.txt 
```

#### Kerberos 5, etype 23, AS-REP
```bash
hashcat -m 18200 groce /usr/share/wordlists/rockyou.txt
```

### IPMIv2 (7300 - RAKP)
Bruteforcing found password hash offline via hashcat:
```bash
sudo hashcat -m 7300 hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule
```


### Bitlocker
```bash
hashcat -a 0 -m 22100 bit.txt /usr/share/wordlists/rockyou.txt
```
^4fb3f5

### NTLM-Hash
From e.g. SAM-DB:
```bash
hashcat -m 1000 it.txt /usr/share/wordlists/rockyou.txt 
```

^8e92ef
### NTLMv2-SSP
```bash
hashcat -m 5600 it.txt /usr/share/wordlists/rockyou.txt 
```

### SHA-512 Unix
```bash
hashcat -m 1800 -a 0 /tmp/unshadowed.hashes /usr/share/wordlists/rockyou.txt -o /tmp/unshadowed.cracked
```

^220f8c


### Mask Attack
`Mask Attack` is a type of brute-force attack in which the keyspace is explicitly defined by the user. For example, if we know that a password is eight characters long, rather than attempting every possible combination, we might define a mask that tests combinations of six letters followed by two numbers.

| Symbol | Charset                             |
| ------ | ----------------------------------- |
| ?l     | abcdefghijklmnopqrstuvwxyz          |
| ?u     | ABCDEFGHIJKLMNOPQRSTUVWXYZ          |
| ?d     | 0123456789                          |
| ?h     | 0123456789abcdef                    |
| ?H     | 0123456789ABCDEF                    |
| ?s     | «space»!"#$%&'()*+,-./:;<=>?@[]^_`{ |
| ?a     | ?l?u?d?s                            |
| ?b     | 0x00 - 0xff                         |
Let's say that we specifically want to try passwords which start with an uppercase letter, continue with four lowercase letters, a digit, and then a symbol. The resulting hashcat mask would be `?u?l?l?l?l?d?s`.

```bash
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'
```
## Useful Commands

Perform a benchmark-test for your system, in order to figure out how many password-attempts/sec are possible (in this case with mode 7300, which is IPMI2). If output ist e.g. “51717.6 kH/s” this would be 51Mio attempts/sec :
```bash
hashcat -b -m 7300
```

### Bitlocker - Reveal Hash
