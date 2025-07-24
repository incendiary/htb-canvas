from typing import List, Dict, Any
from client import HTBApiClient
from models.pagination import paginated_fetch

UserDict = Dict[str, Any]

class UserEnumerator:
    """Responsible for enumerating users from the Hack The Box API."""
    """ This class is responsible for enumerating users from the Hack The Box API.
    example curl: curl -s \\n -H "Authorization: Bearer $HTB_TOKEN" \\n -H "Accept: application/json" \\n "https://enterprise.hackthebox.com/api/ext/v1/users?per_page=100&page=1" | jq"""

    def __init__(self, client: HTBApiClient):
        self.client = client

    def get_all_users(self) -> List[UserDict]:
        def fetch_page(page: int):
            return self.client.get(self.client.api_paths["users"], params={"page": page})

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