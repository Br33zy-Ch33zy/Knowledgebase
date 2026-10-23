---
type: knowledge
category: concepts
tags:
  - knowledge/concepts
aliases:
  - maildir, mbox
---
# Maildir Format


**Description:** A file format developed by Daniel J. Bernstein (1995) for storing e-mails, in which each message is saved as a separate file (replacing the error-prone `mbox` format).

---
## Structure

A **Maildir** directory must consist of three subfolders:

- `new/`: New messages that have not yet been processed or viewed by the email client.
- `cur/`: Messages already viewed/processed (*current*).
- `tmp/`: Temporary folder for write operations. Prevents email corruption in the event of system crashes by using atomic move operations to `new/`.

---

## Related Notes
- **Protocols:** [[IMAP]], [[POP3]], [[SMTP]]
- **Applications:** `[[Dovecot]]`, `[[Postfix]]`