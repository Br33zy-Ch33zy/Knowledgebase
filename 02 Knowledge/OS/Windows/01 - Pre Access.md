- **1. Active Service Discovery:** Portscan auf DC/Targets (`SMB`, `LDAP`, `Kerberos`, `DNS`).
    
- **2. Passive / Broadcast Recon:** Listen auf `[[LLMNR-NBT-NS]]` / IPv6 Router Advertisements (`mitm6`).
    
- **3. User Enumeration:** Kerberos User Enumeration (`kerbrute`) oder Anonyme `[[LDAP-Protocol|LDAP]]` / `[[SMB-Protocol|SMB]]` Null-Sessions.
    
- **4. Initial Access Vektoren:** Password Spraying, AS-REP Roasting, Poisoning via Responder.