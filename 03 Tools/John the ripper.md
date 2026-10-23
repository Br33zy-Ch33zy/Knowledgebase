---
type: tool
category: password-cracking
tags: [tool/cracking, passwords, hashes, john]
aliases: [john, john-the-ripper]
---

# Overview 
**Description:** Offline password cracker supporting hundreds of hash and cipher types, with integrated rulesets and format conversion utilities (*2john).

## Useful Commands
### Single-crack mode
```bash 
john --single PASSWORD
```

### Extract hash from file
To extract the hash of an encrypted file, there are many tools for JtR. Following tool for example is capable of extracting the hash of an office document such as .xlsx .docx:
```bash 
office2john ENCRYPTED.xlsx 
```

#### Bitlocker
```bash 
bitlocker2john -i BITLOCKER.vhd > bitlocker.txt
```
^5b5e4f

#### .psafe3
Extract hash of a "password-vault file":
```bash
pwsafe2john Employee-Passwords_OLD.psafe3 > hash.txt
```
Crack the hash:
```bash
john  --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

#### .ZIP
1. Generate hash of zip file:
```bash
zip2john Notes.zip > notes.hash
```
2. Crack hash:
```
john --wordlist=/usr/share/wordlists/rockyou.txt notes.hash
```

Output looks something like this, where in this case the password is `snowbunny24..*7`:
```bash
0g 0:00:00:02 DONE (2026-09-11 16:17) 0g/s 6929Kp/s 6929Kc/s 6929KC/s $$snowbunny24..*7¡Vamos!
```

#### .Kirbi (extracting Ticket)
1. Extract Ticket using `john`
```bash
python3 kirbi2john.py USER.kirbi
```
This will create a file called `crack_file`. We then must modify the file a bit to be able to use Hashcat against the hash.
2. Modify ticket-output for `hashcat`
```bash
sed 's/\$krb5tgs\$\(.*\):\(.*\)/\$krb5tgs\$23\$\*\1\*\$\2/' crack_file > tgs_hashcat
```
3. Check if format is correct:
```bash
cat sqldev_tgs_hashcat 
```

## Important Parameters
john
	`--incremental` = this mode generates password guesses according to probability, which ist far superior than normal brute forcing
	`--show FILE` = shows encrypted passwords of file
	`--format=FORMAT` = define format (e.g md5)
	`--wordlist=WORDLIST` = specifiy wordlist to use