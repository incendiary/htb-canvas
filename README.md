# htb-canvas


**htb-canvas** is a Hack The Box Enterprise enumeration and access-mapping tool. It provides visibility into user-license relationships, license usage statistics, and access coverage across your organisation.


---

## 🚀 Features

* Enumerates all HTB Enterprise users and license data
* Maps users to licenses and licenses to users
* Groups users by role and shows percentage seat usage per license
* Supports both license-centric and user-centric views
* Outputs in clean tabular format

---

## 🛠 Setup

### 1. Install dependencies

```bash
pipenv install
```

### 2. Environment variables

htb-canvas requires two environment variables:

```bash
HTB_TOKEN="your-api-token"
BASE_URL="https://enterprise.hackthebox.com"
```

You can store these in either of the following files:

* `.env` – primary file for non-secrets
* `.secret` – will override `.env` put your secrets here if they aren't env vars, don't commit them. 

Example `.secret` file:

```env
HTB_TOKEN="3XXXXX1"
```

---

## ▶️ Running

```bash
pipenv run python main.py
```

This will:

* Fetch all users and licenses
* Enrich with assignment mappings
* Print:

  * Users by role
  * License usage summary
  * License assignment table
  * User access overview

---

## 📁 Project Structure

```bash
.
├── Pipfile                  # pipenv environment definition
├── client.py                # HTTP client wrapper
├── main.py                  # Entry point
├── models/
│   ├── users.py             # User enumeration
│   ├── licenses.py          # License enumeration
│   ├── relationships.py     # User-license mapping logic
│   ├── assignments.py       # Optional filtered user license assignments
│   ├── labs.py              # Lab-specific license enumeration
│   └── pagination.py        # Shared pagination helper
├── .env                     # (optional) environment variables
├── .secret                  # (optional) overrides .env
└── README.md
```

---

## 📎 Notes

* Do not share API tokens or `.secret` files.

---

## 🗺️ Roadmap

### Security Hardening

- [x] Secrets separated from code — API token loaded from `.secret` (gitignored), non-sensitive config in `.env`
- [x] Git history audited — no credentials in commit history
- [x] `.gitignore` expanded to cover `__pycache__`, `.venv`, `Pipfile.lock`, and tool caches

### Linting & Formatting

- [x] `pyproject.toml` configured with [Ruff](https://docs.astral.sh/ruff/) (linter) and [Black](https://black.readthedocs.io/) (formatter)
- [x] Ruff enforces PEP 8 (`E`, `F`, `W`) and import ordering (`I`)
- [x] Install dev tools: `pipenv install --dev`
- [ ] Run linter: `pipenv run ruff check .`
- [ ] Run formatter: `pipenv run black .`

### Pre-commit Pipeline

- [x] `.pre-commit-config.yaml` configured with:
  - **GitLeaks** — scans for accidentally committed secrets
  - **Black** — enforces consistent formatting
  - **Ruff** — lints and auto-fixes on every commit
- [ ] Install hooks: `pre-commit install`
- [ ] Run against all files: `pre-commit run --all-files`

---

