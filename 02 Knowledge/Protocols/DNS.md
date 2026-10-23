---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - dns, 53
---
# DNS (Domain Name System)

**Default Ports:** `53` (UDP/TCP) 
**Description:** Responsible for name resolution hostname to ip-address

```mermaid
graph TD
    classDef public fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef boundary fill:#451a03,stroke:#f97316,stroke-width:2px,stroke-dasharray: 5 5,color:#ffedd5;
    classDef internal fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    classDef nodeClass fill:#334155,stroke:#94a3b8,stroke-width:1px,color:#f8fafc;

    %% Public Apex Zone
    subgraph PUBLIC["🌐 PUBLIC ZONE (example.com)"]
        Apex["example.com"]:::public
        NS_Pub["ns1 / ns2.example.com"]:::nodeClass
        WWW["[www.example.com](https://www.example.com)"]:::nodeClass
        Mail["mail.example.com"]:::nodeClass
        VPN["vpn.example.com"]:::nodeClass

        Apex --> NS_Pub & WWW & Mail & VPN
    end

    Boundary["🔒 Split-Horizon Boundary / Firewall / VPN"]:::boundary
    PUBLIC --> Boundary

    %% Internal Zone
    subgraph INTERNAL["🏢 INTERNAL ZONE (internal.example.com)"]
        IntDomain["internal.example.com"]:::internal
        
        subgraph AD["Active Directory & Identity"]
            IntNS["ns-int1 / ns-int2"]:::nodeClass
            DCs["dc1 / dc2"]:::nodeClass
            IDP["idp"]:::nodeClass
            PKI["pki"]:::nodeClass
        end

        subgraph MS["Microservices"]
            MS_API["api.ms"]:::nodeClass
            MS_Auth["auth.ms"]:::nodeClass
            MS_DB["db1.ms"]:::nodeClass
        end

        subgraph CORP["Clients"]
            Client["client-ch-082.corp"]:::nodeClass
            Printer["print-zh-01.corp"]:::nodeClass
        end

        subgraph INFRA["Datacenter OOB"]
            ESX["esx01.infra"]:::nodeClass
            ILO["ilo-sw01.infra"]:::nodeClass
            SAN["storage-san1.infra"]:::nodeClass
        end

        IntDomain --> AD & MS & CORP & INFRA
    end

    Boundary --> IntDomain
```


---

## 01 - Enumeration

### Quick Check / Banner Grabbing


### Deep Enumeration
### Zones

![[Dig#Zone Transfer (AXFR)]]


![[Dig#Dig Standard Zones]]

#### Bind Version-Check
![[Dig#^314980]]

### OSINT enumeration
![[Subfinder#^eb9d30]]

### Bruteforce subsites
> [!INFO] Note
Better user Gobuster and check all Zone-types, e.g A, TXT, MX, etc. 

![[Dnsenum#^25560d]]![[subrute#Using subrute DNS-ENUM]]