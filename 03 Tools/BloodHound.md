---
type: tool
category: web
tags:
  - tool
---
# Overview
Once we have domain credentials, we can run the [BloodHound.py](https://github.com/fox-it/BloodHound.py) BloodHound ingestor from our Linux attack host. BloodHound is one of, if not the most impactful tools ever released for auditing Active Directory security, and it is hugely beneficial for us as penetration testers. We can take large amounts of data that would be time-consuming to sift through and create graphical representations or "attack paths" of where access with a particular user may lead.
## Commands

#### Map entire domain from Linux - BloodHound
`Domain user needed!`
Targets the `domain controller`:

```bash
sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all 
```


### GUI
#### How to setup
Before using it is recommended to delete previous scans/uploads:
```bash
cd /run/media/breezy/PortableSSD/THM/Scripts/bloodhound/examples/docker-compose
sudo docker volume rm docker-compose_neo4j-data
```
1. Start the bloodhound service:
```bash
cd /run/media/breezy/PortableSSD/THM/Scripts/bloodhound/examples/docker-compose
sudo docker compose up -d
```
2. Connect to Bloodhound via webexplorer:
```localhost
http://localhost:9999/ui/explore
```
and query password:
```bash
sudo docker compose logs bloodhound | grep -i "initial password"
```
3. Upload scan Data:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020260930124406.png)
4. Now that the data is loaded, we can use the `Privlege Zones` to have an overview of the domain.

After use shutdown the docker-container:
```bash
sudo docker compose down -v
```

#### Check "Shortest paths to Domain Admin"
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261012124459.png)
#### Checking User attack paths
We can lookup the possible attack paths, when defining a user as the `source` and then select `Outbound Object Control`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261005101308.png)


## Important Parameter
bloodhound
	`-c all` = executes all checks, extracts as much data as possible