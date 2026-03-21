## Steps
1. **Dependencies and application skeleton** — Add `requirements.txt` (FastAPI, Uvicorn, and compatible Pydantic stack for Python 3.11+) at the project root, plus a single Python module (e.g. `main.py`) defining the FastAPI app, Pydantic models for tasks (id, title, description, completed, created_at), and an in-memory store structure; app must import and instantiate without errors when dependencies are installed in a venv under the run tmp directory. ✓
2. **CRUD endpoints and error handling** — Implement `GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `PUT /tasks/{id}`, and `DELETE /tasks/{id}` with JSON responses, 201 on create, 404 with clear detail when a task id is missing, and sensible 200 responses for successful reads/updates/deletes. ✓
3. **Verification** — Add a small automated check (e.g. `httpx` + `TestClient`, or a `if __name__ == "__main__":` script with explicit pass/fail prints) at the project root that exercises all endpoints and status codes; run it from a venv in the run tmp directory after `pip install -r requirements.txt`. ✓

## Lessons
- Use explicit `if` checks with `sys.exit(1)` (and a clear `FAIL:` message) in standalone API verification scripts instead of bare `assert`, so checks still run under `python -O`.
