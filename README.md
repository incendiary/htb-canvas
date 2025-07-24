# htbenum


**htbenum** is a Hack The Box Enterprise enumeration and access-mapping tool. It provides visibility into user-license relationships, license usage statistics, and access coverage across your organisation.


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

htbenum requires two environment variables:

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

