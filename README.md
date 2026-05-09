# htb-canvas

**htb-canvas** is a command-line tool for HTB Enterprise administrators. It maps every user to their assigned licenses and every license to its assigned users, producing a clear picture of access coverage and seat utilisation across your organisation.

---

## Why

The HTB Enterprise web UI shows users and licenses in isolation. htb-canvas joins them — so you can answer questions like:

- Which users have no license assigned?
- Which licenses are over- or under-utilised?
- Who holds the `admin` role, and across which licenses?

---

## Features

- Enumerates all users and licenses via the HTB Enterprise API
- Cross-references users and licenses bidirectionally
- Groups users by role with seat utilisation percentage per license
- Handles paginated API responses transparently
- Outputs clean tabular views suitable for the terminal or pipe-to-file

---

## Architecture

```
main.py
  └── setup_client()                loads config from .env / .secret
  └── enrich_license_and_user_data(client)
        ├── LicenseEnumerator       fetches all licenses (paginated)
        ├── UserEnumerator          fetches all users (paginated)
        └── per-license GET         fetches assigned users, cross-links both objects

Output functions
  ├── print_users_by_role()         grouped user table
  ├── print_license_summary()       seat utilisation per license
  ├── print_license_assignments()   users listed under each license
  └── print_user_access()           licenses listed under each user
```

```
models/
  pagination.py      generic paginated_fetch helper (no API coupling)
  relationships.py   enrich_license_and_user_data()
  users.py           UserEnumerator
  licenses.py        LicenseEnumerator
  assignments.py     AssignmentEnumerator (filtered, optional)
  labs.py            LabEnumerator (lab-specific licenses)

client.py            HTBApiClient — session, Bearer auth, SSL via certifi, error handling
```

---

## Setup

### 1. Install dependencies

```bash
pipenv install
```

### 2. Configure credentials

Create two files in the project root:

**.env** — non-sensitive config (safe to commit):

```env
BASE_URL=https://enterprise.hackthebox.com/api/ext/v1
API_PATH_LICENSES=/licenses
API_PATH_USERS=/users
API_PATH_CHANNELS=/channels
API_PATH_ACADEMY_MODULES=/academy/modules
```

**.secret** — your API token (gitignored, never commit):

```env
HTB_TOKEN=your-api-token-here
```

Your token is available in the HTB Enterprise dashboard under **Settings → API**.

---

## Running

```bash
pipenv run python main.py
```

Output includes:

- Users grouped by role
- License utilisation summary (assigned / total seats, % used)
- Per-license user assignment list
- Per-user license access list

---

## Development

### Run tests

```bash
pipenv install --dev
pipenv run pytest -v
```

### Lint and format

```bash
pipenv run ruff check .
pipenv run black .
```

### Pre-commit hooks

Hooks run gitleaks, black, and ruff automatically on every commit.

```bash
pre-commit install
pre-commit run --all-files
```

---

## Contributing

PRs are welcome. A few guidelines:

- Open an issue first for anything beyond a small fix
- Keep changes surgical — every diff line should trace to a specific finding
- Add test coverage for new logic (`tests/`)
- Run `pre-commit run --all-files` before pushing

> **Note:** This project was built with heavy assistance from [Claude Code](https://claude.com/claude-code). Things should work, but some paths haven't been fully verified end-to-end — PRs and fixes are very welcome.

---

## Project Structure

```
.
├── client.py                  # HTTP client — auth, SSL, error handling
├── main.py                    # Entry point and output formatting
├── models/
│   ├── pagination.py          # Shared paginated_fetch helper
│   ├── relationships.py       # User ↔ license cross-reference
│   ├── users.py               # UserEnumerator
│   ├── licenses.py            # LicenseEnumerator
│   ├── assignments.py         # AssignmentEnumerator (filtered)
│   └── labs.py                # LabEnumerator
├── tests/
│   ├── test_client.py
│   ├── test_pagination.py
│   └── test_relationships.py
├── .env                       # Non-sensitive config (committed)
├── .secret                    # API token (gitignored)
├── .pre-commit-config.yaml    # gitleaks + black + ruff hooks
├── pyproject.toml             # Black, Ruff, and pytest configuration
└── Pipfile                    # Dependency definitions
```

---

## Roadmap

| Issue | Status | Description |
|-------|--------|-------------|
| [#1](https://github.com/incendiary/htb-canvas/issues/1) | ✅ Closed | Secret scanning and git history audit |
| [#2](https://github.com/incendiary/htb-canvas/issues/2) | ✅ Closed | PEP 8 compliance and bug fixes |
| [#3](https://github.com/incendiary/htb-canvas/issues/3) | ✅ Closed | Ruff, Black, and pre-commit pipeline |
| [#4](https://github.com/incendiary/htb-canvas/issues/4) | ✅ Closed | Professional README and architectural overview |
| [#6](https://github.com/incendiary/htb-canvas/issues/6) | ✅ Closed | Unit test suite for pagination, enrichment, and HTTP client |

### Security Hardening

- [x] Secrets separated from code — API token loaded from `.secret` (gitignored), non-sensitive config in `.env`
- [x] Git history audited — no credentials in commit history ([#1](https://github.com/incendiary/htb-canvas/issues/1))
- [x] `.gitignore` covers `__pycache__`, `.venv`, `Pipfile.lock`, and tool caches
- [x] Branch protection on `main` — PRs required, no force pushes, no deletions

### Linting, Formatting & Pipeline ([#3](https://github.com/incendiary/htb-canvas/issues/3))

- [x] `pyproject.toml` configured with [Ruff](https://docs.astral.sh/ruff/) and [Black](https://black.readthedocs.io/)
- [x] `.pre-commit-config.yaml` with GitLeaks, Black, and Ruff

### Tests ([#6](https://github.com/incendiary/htb-canvas/issues/6))

- [x] 10 unit tests across `pagination`, `relationships`, and `client`
- [x] `pytest` and `pytest-mock` in dev dependencies
