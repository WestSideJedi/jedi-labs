from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE, NTLM
import argparse
import sys


def connect_to_ldap(dc_ip, domain, username, password):
    try:
        server = Server(dc_ip, get_info=ALL)
        conn = Connection(
            server,
            user=f"{domain}\\{username}",
            password=password,
            authentication=NTLM,
            auto_bind=True
        )
        return conn
    except Exception as e:
        print(f"[!] LDAP bind failed: {e}")
        sys.exit(1)





def get_group_members(conn, group_dn):
    conn.search(search_base=group_dn,
                search_filter='(objectClass=group)',
                attributes=['member'])
    if not conn.entries:
        print(f"[!] Group not found: {group_dn}")
        return []

    members = conn.entries[0]['member'].values if 'member' in conn.entries[0] else []

    print(f"\n[+] Current members of {group_dn}:")
    if not members:
        print("    [*] No members found.")
    else:
        for i, member in enumerate(members, 1):
            print(f"    {i}. {member}")

    return members


def modify_group_members(conn, group_dn, user_dn, action):
    change_type = MODIFY_ADD if action == 'add' else MODIFY_DELETE


    conn.modify(
        dn=group_dn,
        changes={
            'member': [(change_type, [user_dn])]
        }
    )

    if conn.result['result'] == 0:
        print(f"[+] Successfully {action}ed {user_dn} to/from {group_dn}")
    else:
        print(f"[!] Failed to {action} {user_dn} to/from {group_dn}: {conn.result['description']}")
        


def main():
    parser = argparse.ArgumentParser(description="AD Group Member via LDAP")
    parser.add_argument("--dc-ip", required=True, help="Domain Controller IP")
    parser.add_argument("--domain", required=True, help="Domain name")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--group-dn", required=True, help="Full DN of the group") #i.e "CN=GroupName,OU=Groups,DC=domain,DC=com"
    parser.add_argument("--user-dn", required=True, help="Full DN of the user") #i.e "CN=UserName,OU=Users,DC=domain,DC=com"
    parser.add_argument("--action", choices=['add', 'remove'], required=True, help="Action to perform: add or remove user from group")


    args = parser.parse_args()

    conn = connect_to_ldap(args.dc_ip, args.domain, args.username, args.password)


print(f"[+] Fetching and displaying current members of {args.group_dn}...")
before = get_group_members(conn, args.group_dn)

print("\n[+] Attempting group membership modification...")
modify_group_members(conn, args.group_dn, args.user_dn, args.action)
print("\n[+] Verifying results...")
after = get_group_members(conn, args.group_dn)
print(f"[+] Verifying reslults...")

user_dn_lower = args.user_dn.lower()
after_lower = [dn.lower() for dn in after]

if args.action == 'add':
    if user_dn_lower in after_lower:
        print(f"[+] {args.user_dn} is now a member of {args.group_dn}")
    else:
        print(f"[!] {args.user_dn} was not added to {args.group_dn}")
elif args.action == 'remove':
    if user_dn_lower not in after_lower:
        print(f"[+] {args.user_dn} has been removed from {args.group_dn}")
    else:
        print(f"[!] {args.user_dn} is still a member of {args.group_dn}")
conn.unbind()

if __name__ == "__main__":
    main()