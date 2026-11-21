# SNMS-VT-2026

Design and Implementation of a Small Network Monitoring System for Velma Telcom. This first deliverable provides a localhost-only Flask app, automatically created SQLite tables, a database-backed dashboard, and a database health endpoint. Device registration and active monitoring are subsequent steps.

## Requirements

- Windows 10/11
- Python 3.11 or later
- Visual Studio Code (recommended)
- Git for Windows (recommended)

## Setup in PowerShell

```powershell
cd SNMS-VT-2026
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Open <http://127.0.0.1:5000/>. The app binds to localhost only. If PowerShell blocks virtual environment activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell window and activate again.

The application creates `instance/monitoring.db` and its three empty tables (`devices`, `monitoring_checks`, `connectivity_events`) when it starts. Visit <http://127.0.0.1:5000/health> to run a database connectivity check. No monitoring records or devices are fabricated. Do not monitor devices unless you are authorized to test them. The next implementation step is device inventory and management.

## Project layout

```text
app.py                 Flask application factory, dashboard, and health route
config.py              Environment-based configuration with .env loading
models.py              Device, monitoring check, and connectivity event tables
requirements.txt       Python dependencies
.env.example           Local configuration template
templates/             Base layout and database-backed dashboard
static/css/            Dashboard styles
static/js/              Dashboard script placeholder
instance/              Generated SQLite database (ignored by Git)
```

## Current scope

This foundation does not yet perform ping checks or claim test results. The dashboard reads actual values from SQLite and remains empty until records are added by future features. ICMP non-response can reflect firewall policy, so status labels describe observations rather than assert physical downtime. See the supplied Project Execution Guide for the full planned implementation sequence.

## Foundation verification record

Verified locally with the project virtual environment on 2026-11-21 using Flask's test client and Python's SQLite library:

| Check | Actual result |
| --- | --- |
| Import application and initialize database | Passed |
| `GET /` dashboard | HTTP 200; rendered zero registered devices |
| `GET /health` | HTTP 200; `status=running`, `database=connected` |
| SQLite database file | `instance/monitoring.db` created |
| Initial tables | `devices`, `monitoring_checks`, `connectivity_events` present |

These checks exercised the Flask test client, not a separately launched development server or browser. Manual browser verification remains to be done.
