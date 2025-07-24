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
    """
    This class is responsible for making API requests to the Hack The Box API.
    It handles authentication, session management, and error handling.

    """


    def __init__(self, HTB_TOKEN: str, BASE_URL: str, API_PATHS: dict):
        self.token = HTB_TOKEN
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        })
        self.session.mount("https://", SSLAdapter())
        self.api_paths = API_PATHS

    def get(self, endpoint: str, params=None):
        url = f"{self.base_url}{endpoint}"
        print(f"GET: {url}")

        print(f"→ GET {url} | Params: {params}")  # Optional: remove if too noisy

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
