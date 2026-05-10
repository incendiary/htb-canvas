import requests
import ssl
import certifi
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, JSONDecodeError


class SSLAdapter(HTTPAdapter):
    """
    This class is a custom HTTPAdapter that uses a secure SSL context
    with a certificate authority bundle provided by certifi.
    """
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(cafile=certifi.where())
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


class HTBApiClient:
    """Makes API requests to the Hack The Box API with authentication and error handling."""

    def __init__(self, htb_token: str, base_url: str, api_paths: dict):
        self.token = htb_token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        })
        self.session.mount("https://", SSLAdapter())
        self.api_paths = api_paths

    def get(self, endpoint: str, params=None):
        url = f"{self.base_url}{endpoint}"
        print(f"→ GET {url} | Params: {params}")

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except JSONDecodeError:
            print("⚠️ Response is not valid JSON. Raw content:")
            print(response.text[:1000])  # Print first 1000 chars of HTML
            raise

        except HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print("Response body (truncated):")
            print(response.text[:1000])
            raise
