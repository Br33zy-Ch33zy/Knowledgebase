---
type: tool
category: github
tags:
  - tool
---
# Overview

## Commands

### Upload local Repo (Obsidian) with Github
#### Link Github-Repo
1. Change directory to local Repo:
```bash
cd /REPO-PATH
```
2. Initialize `Git` and link it with `GitHub`:
```bash
git init
git branch -M main
git remote add origin https://github.com/Br33zy-Ch33zy/Knowledgebase.git
```

#### Upload Files
1. Change directory to local Repo:
```bash
cd /REPO-PATH
```
2. Upload files/Sync:
```bash
git add .
git commit -m "Comment, e.g. Date"
git push -u origin main
```

## Important Parameter

## Files
### .gitignore (Obsidian)
Specify files to exclude from the git-sync, such as settings and session-tokens. Location is in the root-directory of the "local" repository:
```.gitignore
# Exclude Obsidian settings & history

.obsidian/workspace.json

.obsidian/workspace-mobile.json

.obsidian/cache

.trash/

  

# Operating system files

.DS_Store

Thumbs.db
```