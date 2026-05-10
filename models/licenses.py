from typing import Any, Dict, List

from client import HTBApiClient
from models.pagination import paginated_fetch
# This class is responsible for enumerating licenses from the Hack The Box API.
# curl -s \\n -H "Authorization: Bearer $HTB_TOKEN" \\n -H "Accept: application/json" \\n "https://enterprise.hackthebox.com/api/ext/v1/licenses" |jq
LicenseDict = Dict[str, Any]

class LicenseEnumerator:
    def __init__(self, client: HTBApiClient):
        self.client = client

    def get_all_licenses(self) -> List[LicenseDict]:
        def fetch_page(page: int):
            return self.client.get(self.client.api_paths["licenses"], params={"page": page})

        raw_licenses = paginated_fetch(fetch_page)

        return [
            {
                "id": license.get("id"),
                "name": license.get("name"),
                "starts_at": license.get("starts_at", None),
                "ends_at": license.get("ends_at"),
                "active": license.get("active", None),
                "expired": license.get("expired", None),
                "seats": license.get("seats"),
                "assigned_seats": license.get("assigned_seats"),
                "content_type": license.get("content_type"),
                "is_on_trial": license.get("is_on_trial"),
                "is_private": license.get("is_private"),
                "is_locked": license.get("is_locked"),
                "description": license.get("description"),
                "product": license.get("product"),
                "addons": license.get("addons")
            }
            for license in raw_licenses
        ]