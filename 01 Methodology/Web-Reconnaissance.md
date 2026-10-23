---
type: knowledge
category: methodology
tags: [knowledge/methodology, web, recon]
aliases: [web-recon, web-enumeration]
---
# Web Reconnaissance Methodology (Theory)
In the first part, “**01 - Passive Recon**” and “**02 - Active Recon**” we will describe in more detail the theory behind the various approaches and the associated tools.

In the second part, “**Playbook**,” we will take a closer look at the practical approach, using examples of a possible workflow.

## 01 - Passive Recon
### 1.1 - Websites Historical Data
Websites such as: "https://web.archive.org/" provide useful information about previous contents and states of a website and can contain sensitive files such as `.php, .bak, ,env`.

Websites such as "https://whoisfreaks.com/tools/whois/lookup/pmbbau.ch" document changes to domains.

### 1.2 - Passive Subdomain-Enumeration
There are many ways to gain information about the target, without interacting directly with its systems:
- **Certificate Transparency Logs (CT-Logs):** Search for CAs based on issued certificates .
	- _Tools:_ `subfinder`, `ctfr`, `crt.sh`, `Certspotter API`
  
- **Passive DNS & Threat Intelligence:** Query databases that scan the Internet.
	- _Tools:_ `AlienVault OTX`, `VirusTotal`, `Shodan`, `SecurityTrails`

- **Search Engine Scraping (Google Dorks):** Search search engine indexes (e.g., `site:target.com -www`).

## 02 - Active Recon
### 2.1 - Active DNS-Enumeration
In this stage we will query the official NS of the target via:
- **Standard DNS Queries:** Querying A, CNAME, TXT, and MX records.
	- _Tools:_ `dig`, `nslookup`.

- **DNS Zone Transfer (AXFR):** Asking the nameserver to disclose its _entire_ database (misconfiguration exploitation).
	- _Tools:_ `dig axfr @ns1.target.com`, `dnsrecon -t axfr`.

- **DNS Brute-Force:** Try a wordlist (e.g., `admin`, `dev`, `mail`) to see which names return an IP address from the DNS server.
	- _Tools:_ `dnsenum`, `gobuster dns`, `puredns`, `shuffledns`.

### 2.2 - VHost Fuzzing
Hidden subdomains often exist on the web server but have **no public DNS entry**. The web server distinguishes them solely based on the HTTP Host header.
- **How it works:** We send HTTP requests directly to the **IP address** of the web server and manipulate the header (`Host: FUZZ.target.com`) with each request.
	- _Tools:_ `ffuf` , `gobuster vhost`.

### 2.3 - Permutation & Wildcard / Recursion (Further Processing)
After carefully analyzing the DNS and web server and identifying as many subdomains/subsites as possible (e.g., `api.target.com`), we use them for the second wave:
- **DNS Permutation (Alteration):** Combine words (e.g., `api` becomes `api-dev`, `api-v2`, `test-api`).
    - _Tools:_ `altdns`, `gotator`.



# Playbook

## 1. External Reconnaissance and Infrastructure (OSINT)

- [ ] **WHOIS & Registrar / IANA ID**
**Objective:** Record the registrar, abuse contact, and unique IANA ID:
```bash
whois domainname.ch > whois.txt
```

- [ ] **Certificate Transparency (CT Logs)**
**Objective:**  Passively search for historical subdomains/SANs in the SSL certificate.
![[Subfinder#^eb9d30]]

## 2. DNS & Subdomain Discovery

- [ ] **DNS Record Listing**
**Objective:** Check MX servers, TXT/SPF records, and CNAMEs:
![[Dig#^ad19f8]]

- [ ] **Listing of Public Subdomains (DNS)**
**Objective:** Deep DNS-Enum. Find all subdomains registered in the public DNS (recursive) and check for zone transfers.
![[Dnsenum#^eebf6c]]
 

## 3. Tech Stack Fingerprinting & Crawling

- [ ] **HTTP Headers & Web Server Software**
**Objective:** Identify web server type (Nginx, Apache, Lighttpd) and versions:
![[Whatweb#^91d4af]]

- [ ] ==**Technology Stack Identification**==

- ==*Tool:* Wappalyzer / WhatWeb==

- ==*Goal:* Document CMS (WordPress, Drupal), frameworks (React, Laravel), and JS libraries.==

- [ ] ==**Standard Configurations (`.well-known`)**==

- ==*Command:* `curl -s http://target.com/.well-known/openid-configuration`==

- ==*Command:* `curl -s http://target.com/.well-known/security.txt`==

- ==*Goal:* Discover authentication endpoints (OAuth/OIDC), API keys, and contacts.==

- [ ] **Webpage Crawling & Endpoint Extraction**
	**Objective:** Map the visible application structure by following links, parsing JavaScript files, and extracting parameters.
  ![[Scripts#^fae765]]

## 4. Active Target Fuzzing 

- [ ] **Virtual Host Enumeration (VHosts)**
**Objective:** Find hidden/internal subdomains without a DNS entry on the server.

Bruteforce subsites with ffuf:
![[Ffuf#^6176ef]]


- ==*Command:* `gobuster vhost -u http://<IP> -w <wordlist> --domain target.com`==

*Manually grab for the "robots.txt" or "sitemap.xml" for additional information:
![[Curl#^89def0]]


- [ ] **Directory & File Busting**
**Objective:** Find hidden folders, admin panels, backups, and API endpoints.
![[Ffuf#^7f8891]]

