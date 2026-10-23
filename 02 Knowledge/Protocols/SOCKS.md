---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - proxy
---
# SOCKS Proxy Protocol (SOCKS4 / SOCKS5)

**Default Ports:** `1080` (TCP - Standard)  |  Variable (often `10800`, `8000`, `9050` with Tor)
**Description:** A Layer 5 session protocol that routes arbitrary TCP/UDP network packets between a client and a target server through a proxy host. An essential mechanism for pivoting through internal networks.

- **SOCKS4:** Supports **TCP traffic only**. Does not support authentication or UDP.
- **SOCKS4a:** An extension of SOCKS4 that allows domain name resolution (DNS) on the proxy side.
- **SOCKS5:** A full-featured protocol. Supports **TCP, UDP, authentication** (username/password), and **remote DNS resolution** (prevents DNS leaks during pivoting).

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection

