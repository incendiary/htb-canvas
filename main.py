import os
from dotenv import load_dotenv
from collections import defaultdict
from tabulate import tabulate
from pprint import pprint

from client import HTBApiClient
from models.users import UserEnumerator
from models.licenses import LicenseEnumerator
from models.relationships import enrich_license_and_user_data


def setup_client() -> HTBApiClient:
    """Setup API client with environment configuration."""
    load_dotenv()
    load_dotenv(dotenv_path=".secret", override=True)

    HTB_TOKEN = os.getenv("HTB_TOKEN")
    BASE_URL = os.getenv("BASE_URL")

    if not HTB_TOKEN or not BASE_URL:
        raise RuntimeError("Missing HTB_TOKEN or BASE_URL")

    API_PATHS = {
        "licenses": os.getenv("API_PATH_LICENSES"),
        "users": os.getenv("API_PATH_USERS"),
        "channels": os.getenv("API_PATH_CHANNELS"),
        "academy_modules": os.getenv("API_PATH_ACADEMY_MODULES"),
    }

    return HTBApiClient(HTB_TOKEN=HTB_TOKEN, BASE_URL=BASE_URL, API_PATHS=API_PATHS)


def print_users_by_role(users: list[dict]):
    grouped = defaultdict(list)
    for user in users:
        grouped[user["role"]].append(user)

    for role, group in grouped.items():
        print(f"\n## Role: {role} ({len(group)} users)")
        print(tabulate(
            [[u["id"], u["name"], u["email"]] for u in group],
            headers=["ID", "Name", "Email"],
            tablefmt="github",
            showindex=True
        ))


def print_license_summary(licenses: list[dict]):
    print("\n=== License Summary ===")
    print(tabulate(
        [[
            lic["id"],
            lic["name"],
            lic["assigned_seats"],
            lic["seats"],
            f"{(lic['assigned_seats'] / lic['seats']) * 100:.1f}%" if lic["seats"] else "0%"
        ] for lic in licenses],
        headers=["ID", "Name", "Assigned", "Seats", "% Used"],
        tablefmt="github",
        showindex=True
    ))


def print_license_assignments(licenses: list[dict]):
    print("\n=== License Assignments ===")
    for lic in licenses:
        print(f"\n{lic['name']} (ID: {lic['id']}) — {len(lic.get('users', []))} users assigned")
        for user in lic.get("users", []):
            print(f"  - {user['name']} ({user['email']})")


def print_user_access(users: list[dict]):
    print("\n=== User License Access ===")
    for user in users:
        if user.get("licenses"):
            print(f"{user['name']} ({user['email']}) — {len(user['licenses'])} licenses:")
            for lic in user["licenses"]:
                print(f"  - {lic['name']} (ID: {lic['id']})")


def main():
    client = setup_client()

    # Fetch enriched data once
    licenses, users = enrich_license_and_user_data(client)

    # Output
    print_users_by_role(users)
    print_license_summary(licenses)
    print_license_assignments(licenses)
    print_user_access(users)


if __name__ == "__main__":
    main()
