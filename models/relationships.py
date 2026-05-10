from typing import Tuple, List, Dict
from client import HTBApiClient
from models.licenses import LicenseEnumerator
from models.users import UserEnumerator


def enrich_license_and_user_data(client: HTBApiClient) -> Tuple[List[Dict], List[Dict]]:
    """
    Enrich both license and user objects with cross-references.

    Each license object gains a `users` list.
    Each user object gains a `licenses` list.

    Returns:
        Tuple containing (licenses_with_users, users_with_licenses)
    """
    license_enum = LicenseEnumerator(client)
    user_enum = UserEnumerator(client)

    licenses = license_enum.get_all_licenses()
    users = user_enum.get_all_users()
    user_lookup = {user["id"]: user for user in users}

    # Initialise license list on each user
    for user in users:
        user["licenses"] = []

    # For each license, fetch assigned users and enrich both objects
    for license in licenses:
        license_id = license["id"]
        license["users"] = []

        response = client.get(
            client.api_paths["users"],
            params={"license[]": license_id}
        )
        assigned_users = response.get("data", [])

        for u in assigned_users:
            user = user_lookup.get(u["id"])
            if user:
                user["licenses"].append(license)
                license["users"].append(user)

    return licenses, users
