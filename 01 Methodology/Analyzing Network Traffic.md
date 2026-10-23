---
type: knowledge
category: methodology
tags:
  - knowledge/methodology
aliases:
  - network
  - network-traffic
  - enumeration
---

# Unencrypted Network Traffic
The table below lists several common protocols alongside their encrypted counterparts. While it is now more common to encounter the secure versions, there was a time when plaintext protocols were widely used.

| Unencrypted Protocol | Encrypted Counterpart      | Description                                                                 |
| -------------------- | -------------------------- | --------------------------------------------------------------------------- |
| `HTTP`               | `HTTPS`                    | Used for transferring web pages and resources over the internet.            |
| `FTP`                | `FTPS/SFTP`                | Used for transferring files between a client and a server.                  |
| `SNMP`               | `SNMPv3 (with encryption)` | Used for monitoring and managing network devices like routers and switches. |
| `POP3`               | `POP3S`                    | Retrieves emails from a mail server to a local client.                      |
| `IMAP`               | `IMAPS`                    | Accesses and manages email messages directly on the mail server.            |
| `SMTP`               | `SMTPS`                    | Sends email messages from client to server or between mail servers.         |
| `LDAP`               | `LDAPS`                    | Queries and modifies directory services like user credentials and roles.    |
| `RDP`                | `RDP (with TLS)`           | Provides remote desktop access to Windows systems.                          |
| `DNS (Traditional)`  | `DNS over HTTPS (DoH)`     | Resolves domain names into IP addresses.                                    |
| `SMB`                | `SMB over TLS (SMB 3.0)`   | Shares files, printers, and other resources over a network.                 |
| `VNC`                | `VNC with TLS/SSL`         | Allows graphical remote control of another computer.                        |

## Analyzing unecrpyted Network Traffic
Analyzing unencrypted network traffic captured with `wireshark` with `Pcredz`
![[Pcredz#^968c87]]