# LDAP Tools 🛠️

This directory contains custom Python tools for interacting with Active Directory via LDAP, specifically focused on enumeration and user/group manipulation.

---

## 🧩 Tools

### 🔹 `ADGroupManager.py`

**Purpose:**  
Adds or removes a specified user from a specified Active Directory group using `GenericAll` or `GenericWrite` privileges via LDAP.

**Usage:**

```bash
python3 ADGroupManager.py \
  --dc-ip 10.10.11.69 \
  --domain fluffy.htb \
  --username p.agila \
  --password prometheusx-303 \
  --group-dn "CN=Service Accounts,CN=Users,DC=fluffy,DC=htb" \
  --user-dn "CN=Prometheus Agila,CN=Users,DC=fluffy,DC=htb" \
  --action add
```

---

### 🔹 `reset_password_ldap.py`

**Purpose:**  
Resets the password of a target AD user by directly modifying the `unicodePwd` attribute via LDAP. Requires specific privileges (not just GenericWrite).

**Features:**
- Lists group memberships and managed objects
- Interactively prompts for new password (with confirmation)
- Validates success/failure of the reset operation

**Usage:**

```bash
python3 reset_password_ldap.py \
  --dc-ip 10.10.11.69 \
  --domain fluffy.htb \
  --username p.agila
```

---

## 🧠 Notes

- These tools are designed for post-exploitation or internal red team scenarios where LDAP interaction is possible.
- Ensure `ldap3` is installed:
  ```bash
  pip install ldap3
  ```

---

**Author:** [@WestSideJedi on GitHub](https://github.com/WestSideJedi)  
**Bluesky:** [@WestSideJedi.bsky.social](https://bsky.app/profile/westsidejedi.bsky.social)  
**Repo Root:** [jedi-labs](https://github.com/WestSideJedi/jedi-labs)

---

## ⚠️ Disclaimer

These tools are intended for **educational and authorized security testing purposes only**.

Do not use this code against systems you do not own or have explicit written permission to assess.  
The author is not responsible for any misuse or damage caused by improper use of this software.
