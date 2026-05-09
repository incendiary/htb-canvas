from unittest.mock import MagicMock, patch

from models.relationships import enrich_license_and_user_data

LICENSES = [{"id": 10, "name": "Lab License", "seats": 5, "assigned_seats": 1}]
USERS = [{"id": 1, "name": "Alice", "email": "alice@example.com", "role": "user"}]


def _make_client(assigned_user_ids=None):
    client = MagicMock()
    client.api_paths = {"users": "/users", "licenses": "/licenses"}
    client.get.return_value = {"data": [{"id": uid} for uid in (assigned_user_ids or [])]}
    return client


@patch("models.relationships.UserEnumerator")
@patch("models.relationships.LicenseEnumerator")
def test_users_receive_license_list(mock_lic_enum, mock_user_enum):
    mock_lic_enum.return_value.get_all_licenses.return_value = [l.copy() for l in LICENSES]
    mock_user_enum.return_value.get_all_users.return_value = [u.copy() for u in USERS]
    client = _make_client(assigned_user_ids=[1])

    _, users = enrich_license_and_user_data(client)

    assert len(users[0]["licenses"]) == 1
    assert users[0]["licenses"][0]["id"] == 10


@patch("models.relationships.UserEnumerator")
@patch("models.relationships.LicenseEnumerator")
def test_licenses_receive_user_list(mock_lic_enum, mock_user_enum):
    mock_lic_enum.return_value.get_all_licenses.return_value = [l.copy() for l in LICENSES]
    mock_user_enum.return_value.get_all_users.return_value = [u.copy() for u in USERS]
    client = _make_client(assigned_user_ids=[1])

    licenses, _ = enrich_license_and_user_data(client)

    assert len(licenses[0]["users"]) == 1
    assert licenses[0]["users"][0]["id"] == 1


@patch("models.relationships.UserEnumerator")
@patch("models.relationships.LicenseEnumerator")
def test_unknown_assigned_user_is_skipped(mock_lic_enum, mock_user_enum):
    mock_lic_enum.return_value.get_all_licenses.return_value = [l.copy() for l in LICENSES]
    mock_user_enum.return_value.get_all_users.return_value = [u.copy() for u in USERS]
    client = _make_client(assigned_user_ids=[999])

    licenses, users = enrich_license_and_user_data(client)

    assert licenses[0]["users"] == []
    assert users[0]["licenses"] == []
