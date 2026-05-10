from typing import List, Dict
from client import HTBApiClient
from models.pagination import paginated_fetch

class AssignmentEnumerator:
    """
    Responsible for enumerating license assignments (users per license).

    Example:
    curl -s -H "Authorization: Bearer $HTB_TOKEN" -H "Accept: application/json" \
         "https://enterprise.hackthebox.com/api/ext/v1/users?license[]=11095" | jq
    """

    def __init__(self, client: HTBApiClient, license_ids: List[int]):
        self.client = client
        self.license_ids = license_ids

    def get_all_assignments(self) -> List[Dict[str, str]]:
        def fetch_page(page: int):
            return self.client.get(
                self.client.api_paths["users"],
                params={"license[]": self.license_ids, "page": page}
            )

        raw_users = paginated_fetch(fetch_page)

        return [
            {
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role"),
            }
            for user in raw_users
        ]
