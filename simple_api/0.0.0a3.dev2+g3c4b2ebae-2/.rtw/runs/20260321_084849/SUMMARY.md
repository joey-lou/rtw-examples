# Summary: Simple REST API (todo tasks)

## Delivered

- **FastAPI app** in `main.py`: in-memory `dict[int, Task]` store; Pydantic models for create/update and full task shape with `id`, `title`, `description`, `completed`, `created_at`.
- **Endpoints** (JSON): `GET /tasks`, `GET /tasks/{id}`, `POST /tasks` (201), `PUT /tasks/{id}`, `DELETE /tasks/{id}`; missing id returns **404** with `detail` string.
- **Dependencies** in `requirements.txt` (Python 3.11+): FastAPI, Uvicorn, Pydantic stack.
- **Automated check** in `verify_api.py`: `TestClient` against `app`, explicit `if`/`sys.exit(1)` failure paths, success token `ALL_CHECKS_PASSED`.

## How to run

1. Create a venv, install: `pip install -r requirements.txt`.
2. Serve: `uvicorn main:app --reload` (or equivalent).
3. Verify: `python verify_api.py` → exit 0 and `ALL_CHECKS_PASSED`.

## Success criteria mapping

- All five CRUD endpoints behave as specified; status codes include 200, 201, 404 as appropriate.
- Manual or scripted checks via `curl` or `verify_api.py` are supported.
