from typing import List, Dict, Any
from client import HTBApiClient
from models.pagination import paginated_fetch

UserDict = Dict[str, Any]

class UserEnumerator:
    """Responsible for enumerating users from the Hack The Box API."""

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