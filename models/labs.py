from typing import List, Dict
from client import HTBApiClient
from models.pagination import paginated_fetch

class LabEnumerator:
    """Responsible for enumerating lab licenses via the HTB API."""

    def __init__(self, client: HTBApiClient):
        self.client = client

    def get_all_labs(self) -> List[Dict[str, str]]:
        def fetch_page(page: int):
            return self.client.get(self.client.api_paths["licenses"], params={"page": page})

        raw_labs = paginated_fetch(fetch_page)

        return [
            {
                "id": lab.get("id"),
                "name": lab.get("name"),
                "starts_at": lab.get("starts_at"),
                "ends_at": lab.get("ends_at"),
                "active": lab.get("active"),
                "expired": lab.get("expired"),
                "seats": lab.get("seats"),
            }
            for lab in raw_labs
        ]
