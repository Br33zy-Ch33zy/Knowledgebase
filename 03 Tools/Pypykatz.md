---
type: tool
category: hash
tags:
  - tool
---
# Overview

## Quick Commands
The command initiates the use of `pypykatz` to parse the secrets hidden in the LSASS process memory dump. We use `lsa` in the command because LSASS is a subsystem of the `Local Security Authority`, then we specify the data source as a `minidump` file, proceeded by the path to the dump file stored on our attack host. Pypykatz parses the dump file and outputs the findings:
```bash
pypykatz lsa minidump lsass.DMP 
```
^ed5e20

## Important Parameter
