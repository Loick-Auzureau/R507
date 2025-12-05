## Docker

Si vous voulez containeriser l'application, voici des commandes utiles (PowerShell) :

Construire l'image depuis la racine du projet :
```pwsh
docker build -t r507-app .
```

Lancer le conteneur et mapper le port 8000 :
```pwsh
docker run --rm -p 8000:8000 r507-app
```

# R507 — Monitoring / Supervision API

A small FastAPI-based monitoring backend for managing hosts, servers, indicators and actions. It provides a REST API to create/read/update/delete hosts and servers, manage indicators, run basic reachability checks (ping) and store data via a SQLModel/SQLite database.

**Key features**
- **Hosts & Servers**: CRUD endpoints for hosts (`/hosts`) and servers (`/srvs`).
- **Indicators**: Create and manage indicators per host.
- **Actions**: Store and manage monitoring actions (scripts).
- **Ping checks**: Endpoints to test reachability of hosts and servers.
- **SQLite backend**: Lightweight storage via `sqlmodel` (see `database.py`).

**Repository layout (important files)**
- `serveur/` : FastAPI application and main API implementation (`serveur/main.py`).
- `models/` : Data models (`host.py`, `server.py`, `indicator.py`, `action.py`).
- `serveur/database.py` : Database configuration and initialization helper.
- `bruno/tests-app/` : Test collections and sample requests (Bru/REST client files).
- `supervision.db.bak` : Example or backup SQLite database file.
- `requirements.txt` : Python dependencies (if present).

## Requirements
- Python 3.10+ recommended.
- Install dependencies (if a `requirements.txt` file exists):

```pwsh
python -m pip install -r requirements.txt
```

If you don't have a `requirements.txt`, the project uses FastAPI, Uvicorn and SQLModel. You can install the essentials with:

```pwsh
python -m pip install fastapi uvicorn sqlmodel
```


## Simple Web Interface

A minimalist web interface is available in `serveur/static/index.html`:

- Title "R507 API"
- Three buttons: "Get Stats", "List Hosts", and "List Servers"
- Displays the JSON result

How to use:
1. Start the FastAPI server (see below).
2. Open `http://localhost:8000/static/index.html` in your browser.
3. Click the buttons to query the API:
   - **Get Stats**: fetch `/stats` endpoint
   - **List Hosts**: fetch `/hosts` endpoint
   - **List Servers**: fetch `/srvs` endpoint

## Run locally

Start the API with Uvicorn (from repository root):

```pwsh
uvicorn serveur.main:app --reload --host 0.0.0.0 --port 8000
```

By default the server listens on port `8000`. Open `http://localhost:8000/docs` to view the automatic OpenAPI docs.

## Docker

Build the Docker image (PowerShell):

```pwsh
docker build -t r507-app .
```

Run the container and publish port 8000:

```pwsh
docker run --rm -p 8000:8000 r507-app
```

## API Endpoints (selected)
- `GET /hosts` — list all hosts
- `GET /host/{id}` — get a host by id
- `POST /host` — create a host (send JSON body matching `Host` model)
- `PUT /host/{id}` — update a host
- `DELETE /host/{id}` — delete a host

- `GET /srvs` — list servers
- `GET /srv/{id}` — get server
- `POST /srv` — create server
- `PUT /srv/{id}` — update server
- `DELETE /srv/{id}` — delete server

- `GET /indicators` — list all indicators
- `GET /host/{host_id}/indicators` — list indicators for a host
- `POST /host/{host_id}/indicator` — add indicator to host
- `DELETE /indicator/{indicator_id}` — remove indicator

- `GET /host/{host_id}/ping` — ping a host
- `GET /srv/{srv_id}/ping` — ping a server

Example curl to list hosts:

```bash
curl http://localhost:8000/hosts
```

## Database

The app uses `sqlmodel` and a SQLite database configured in `serveur/database.py`. The repository contains `supervision.db.bak` as an example backup. On first run the database will be created/initialized by `configure_db()` used in app startup.

## Tests & API collections

The `bruno/tests-app/` folder contains `.bru` request collections and example requests you can use with compatible REST tools.

## Development notes
- The FastAPI application entry point is `serveur/main.py`.
- Models live in `models/` and follow SQLModel patterns.
- Actions scripts can be added under `serveur/actions/` and referenced from the API.

## Contributing
If you want to contribute, please open an issue or a pull request. Add tests or update existing ones in `bruno/tests-app/` when relevant.

## License
Add a license file to the repository and update this section.

---

If you want, I can tweak the README (project name, license, or add examples). Tell me what to change.
