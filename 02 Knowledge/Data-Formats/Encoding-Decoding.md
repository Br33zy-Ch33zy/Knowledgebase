---
type: knowledge
category: crypto-data
tags:
  - base64
  - url-encoding
  - hex
  - web
aliases:
  - Encoding
  - Decoding
  - Data Formats
---
# Encoding & Decoding Reference

**Description:** Reference guide for common data representation formats used in web applications, API parameters, payloads, and authentication tokens. Encoding alters data format for safe transport, not for secrecy (no encryption).

---

## 01 - Common Formats & Recognition

| Format                | Recognition Pattern / Syntax                                 | Primary Use Case                                                  |
| :-------------------- | :----------------------------------------------------------- | :---------------------------------------------------------------- |
| **Base64**            | Alphanumeric + `+`, `/`, ending with = or ==                 | Basic Auth, cookies, token payloads (JWT).                        |
| **URL Encoding**      | Uses `%` followed by hex values (e.g., `%20` for space)      | Safe transmission of characters in HTTP URIs/queries.             |
| **Hexadecimal (Hex)** | Pairs of hex digits (`0-9`, `a-f`), often prefixed with `\x` | Raw binary representation, shellcode, memory addresses.           |
| **HTML Entities**     | Starts with `&#` or `&` (e.g., `&lt;`, `&#x3C;`)             | Escaping special characters to prevent HTML/XSS rendering issues. |

---

## 02 - Quick CLI Cheat Sheet
### Base64
#### Encode file
Encode every line in file `ZAP.txt` and save output in file `base64.txt`:
```bash
while IFS= read -r line; do echo -n "$line" | base64 -w 0; echo; done < ZAP.txt > base64.txt
```

### ASCII Hex
#### Encode file
Encode every line in file `base64.txt` and save output in file `hex.txt`:
```bash
python3 -c "import sys; open('hex.txt', 'w').writelines(line.strip().encode('utf-8').hex() + '\n' for line in open('base64.txt') if line.strip())"
```