# appeals-backend
A small asynchronous FastAPI service for tracking 'appeals' – simple text requests that can contain file attachments, a life-cycle status and a per-project 'ping' counter. Built for learning purposes, but fully-functional out-of-the-box: SQLite storage via Tortoise-ORM, colourised console logging, self-contained tests and an OpenAPI (Swagger-UI) spec generated automatically by FastAPI.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Environment `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Environment `venv` using `uv`.

```shell
git clone https://github.com/grisha765/appeals-backend.git
cd downloader_tg_py
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv sync
```

## Usage

### Deploy

- Run the backend:
    ```bash
    .venv/bin/python appeals
    ```
    - Visit http://127.0.0.1:8000/docs to access Swagger UI documentation.

## Environment Variables

The following environment variables control the startup of the project:

| Variable       | Values                              | Description                            |
|----------------|-------------------------------------|----------------------------------------|
| `LOG_LEVEL`    | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Logging verbosity.                     |
| `RELOAD`       | *boolgean*                          | Auto-reload for development.           |
| `API_HOST`     | *string*                            | API bind address.                      |
| `API_PORT`     | *integer*                           | API port.                              |
| `DB_PATH`      | *string*                            | SQLite database file.                  |
| `TESTS`        | *boolgean*                          | Run tests instead of launching server. |
| `ADMIN_PASSWD` | *string*                            | Set password for admin funcs.          |

## Features

- FastAPI RESTful API with async endpoints.
- SQLite database via Tortoise ORM.
- Customizable settings via environment variables.
- Colored logging to console and logging to file.
- Built-in integration tests (without external frameworks).

