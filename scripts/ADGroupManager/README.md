# ADGroupManager.py

**ADGroupManager** is a python script that allows red teamers, penetration testers, and security professionals
to add or remove Active Directory users from domain groups via LDAP. It leverages ldap3 and NTLM authenication,
and is ideal for exploiting misconfigured ACLS (i.e 'GenericWrite', 'WriteMember', 'GenericAll')


# Features
- Add a user to an AD Group via LDAP
- Remove a user from and AD Group
- Verifies group membership (with case-insensitive DN Handling)
- Supports domain user authenication (NTLM)
- Lightweight and easy to drop into any environment
- Perfect for abusing AD ACL privilege esclation paths 



# Usage
bash
Python3 ADGroupManager.py
--dc-ip [ip] \
--domain [domain name@xxx] \
--username [user] \
--password [password] \
-- group-dn 'CN=GroupName,DC=domain,DC=local' \
--user-dn 'CN=User Name,OU=OUName,DC=domain,DC=local' \
--action add/remove


Actions
- add - add user to group 
- remove - remover user from group

# Requirements
- Python 3.x
- ldap3 module

* Recommended: run inside a virtual environment to avoid tool conflicts

# python3 -m venv ldap-env
# source ldap-env/bin/activate




## Disclaimer


This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use of this script against systems you do not own or have explicit permission to test
IS ILLEGAL and may result in criminal charges.


Always ensure you ahve proper authorization before preforming any action involving Active Directory, LDAP, or network exploitation.

The author is not responsible for any misuse or damage caused by this script. 

Westside Jedi
