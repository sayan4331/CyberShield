# CyberShield — Backend

FastAPI + SQLAlchemy + SQLite service layer for the CyberShield dashboard.
See the [project README](../README.md) for the full feature overview and
frontend details — this file covers the backend layout specifically.

## Layout

```
app/
├── api/          FastAPI routers — thin, no business logic. Validate input,
│                 call a service, return a schema.
├── core/         config.py (Settings), database.py (engine/session/init),
│                 security.py (filename sanitizing, log-safe masking, rate limit)
├── models/       SQLAlchemy ORM: ScanHistory, KnownThreatHash, Tip
├── schemas/      Pydantic models — one module per feature
├── services/     Business logic + persistence. This is where the actual
│                 password/url/file analysis lives, and where history rows
│                 get written.
├── utils/        Small, dependency-free helpers (hashing, validators,
│                 file-signature tables, logging setup)
└── main.py       Creates the FastAPI app, wires routers, mounts the frontend
```

The dependency direction is `api → services → models/utils`, with `core`
available everywhere. Routers never touch SQLAlchemy directly — only
services do.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy/edit `.env` if you want to change the database URL, upload limit, or
rate limit — see inline comments there for what each variable does.

## Run

```bash
uvicorn app.main:app --reload
```

The SQLite file is created at `database/cybershield.db` on first run, and
seeded with demo tips and a small known-threat-hash table.

## Test

```bash
pytest -q
```

`tests/conftest.py` points the app at a temp SQLite file for the whole test
session, so tests never touch your dev database.

## Adding a new feature

1. Add a Pydantic schema in `app/schemas/`.
2. Add the logic (and any DB access) in a new or existing `app/services/*.py`.
3. Add a thin route in `app/api/*.py` that calls the service.
4. Register the router in `app/main.py`.
5. Add a test in `app/tests/`.
