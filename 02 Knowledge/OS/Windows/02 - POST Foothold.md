- **1. Local System Recon:** Hostname, OS-Build, Antivirus/EDR Status (`[[CMD-&-PowerShell-Basics]]`).
    
- **2. Local Credential Harvesting:**
    
    - Vault & Credential Manager (`cmdkey /list`, `SharpDPAPI`).
        
    - Registry Hives (`SAM`, `SYSTEM`, `SECURITY`).
        
    - LSASS Memory Access (`comsvcs.dll`, `mimikatz`).
        
- **3. Local Privilege Escalation:** Unquoted Service Paths, Service Permissions, DLL Hijacking.