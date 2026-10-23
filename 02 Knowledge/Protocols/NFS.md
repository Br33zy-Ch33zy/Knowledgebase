---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - nfs, rpc, rpcbind, 111, 2049
---
# NFS (Network File System)

**Default Ports:** `2049` (TCP/UDP - NFS Service)  |  `111` (TCP/UDP - Portmapper / rpcbind)  
**Description:** A distributed file system protocol that allows client systems to access files over a network and mount them as if they were part of a local file system.

---

## 01 - Enumeration

![[Obj-tpl#^040e70]]
### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration


## 02 - Connecting to Service
### 2.1 - Establishing connection:
1. Check if there’s a share available:
```bash
showmount -e 10.129.202.41
```

2. Create folder for mapping:
```bash
mkdir /tmp/nfs_target
```

3. Map shared folder:
```bash
sudo mount -t nfs 10.129.202.41:/SHARED-FOLDER-NAME /tmp/nfs_target -o nolock
```

4. Check the UID (st_uid) of mounted share-folder via pyhton:
```bash
python3 -c "import os; print(os.stat('/tmp/MOUNTED-FOLDER'))"
```
