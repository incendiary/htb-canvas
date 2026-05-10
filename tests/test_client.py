import pytest
from unittest.mock import MagicMock
from requests.exceptions import HTTPError, JSONDecodeError

from client import HTBApiClient


@pytest.fixture
def client():
    c = HTBApiClient(htb_token="test-token", base_url="https://example.com", api_paths={})
    c.session = MagicMock()
    return c


def test_get_returns_parsed_json(client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"data": []}
    client.session.get.return_value = mock_resp

    assert client.get("/endpoint") == {"data": []}


def test_get_raises_on_http_error(client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = HTTPError("404 Not Found")
    mock_resp.text = "Not Found"
    client.session.get.return_value = mock_resp

    with pytest.raises(HTTPError):
        client.get("/endpoint")


def test_get_raises_on_invalid_json(client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.side_effect = JSONDecodeError("No JSON", "doc", 0)
    mock_resp.text = "<html>error</html>"
    client.session.get.return_value = mock_resp

    with pytest.raises(JSONDecodeError):
        client.get("/endpoint")
