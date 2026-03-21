# Subtask: CRUD endpoints and error handling

Implement full behavior in **`main.py` at the project workspace root** (`simple_api/0.0.0a3.dev2+g3c4b2ebae-2`). Do not place application code under `.rtw/` or the run directory.

**Behavior (TASK.md):**

- In-memory store: keep using `tasks: dict[int, Task]` (or equivalent) keyed by integer `id`.
- **GET /tasks** — Return `200` and a JSON array of all tasks (serialize Pydantic models to dicts, e.g. `.model_dump()` with a JSON-friendly `created_at` if needed).
- **GET /tasks/{id}** — Return `200` and the task JSON; if missing, `404` with JSON body including a clear `detail` string (e.g. FastAPI `HTTPException`).
- **POST /tasks** — Accept JSON body with at least `title` and `description` (optional `completed` defaulting to `false`). Server assigns monotonic integer `id` and `created_at`. Return `201` and the created task JSON.
- **PUT /tasks/{id}** — Full or partial update of `title`, `description`, `completed` as appropriate; return `200` and updated task JSON; missing id → `404` with `detail`.
- **DELETE /tasks/{id}** — Remove task; return `200` (per success criteria) with a small JSON payload (e.g. `{"ok": true}` or the deleted task); missing id → `404`.

Use Pydantic v2 models for request/response as needed (e.g. separate create/update schemas so clients cannot set `id`/`created_at` on create). Remove `pass` / TODO stubs from route handlers.

**Disposable verifier (scratch only):** Create `.rtw/runs/20260321_084849/tmp/crud_verify.py` that imports `TestClient` from `starlette.testclient` (or `fastapi.testclient`), imports `app` from `main`, and uses **explicit `if` checks** (not bare `assert`) printing `FAIL: ...` and `sys.exit(1)` on failure; on success print `ALL_CHECKS_PASSED` and exit `0`. The script must exercise: empty list `GET /tasks`; `POST` → `201` and body contains expected fields; `GET` existing → `200`; `GET` missing → `404` with `detail`; `PUT` existing → `200`; `PUT` missing → `404`; `DELETE` existing → `200`; `DELETE` missing → `404`; second `GET /tasks` reflects deletes. Do not add this file to `requirements.txt` (TestClient is available via FastAPI/Starlette already installed).

## Acceptance criteria
- [x] In `main.py` at project root, all five routes are implemented (no `pass`/TODO left for these handlers); missing-task paths raise or return `404` with JSON `detail`; `POST /tasks` returns `201`; successful read/update/delete return `200` with JSON.
- [x] Symbols to inspect: `main.py` contains `@app.get("/tasks")`, `@app.get("/tasks/{task_id}")` (or `{id}`), `@app.post("/tasks")`, `@app.put("/tasks/{task_id}")`, `@app.delete("/tasks/{task_id}")`, and uses the in-memory `tasks` dict.
- [x] Create a venv under `.rtw/runs/20260321_084849/tmp` (e.g. `python3.11 -m venv .rtw/runs/20260321_084849/tmp/.venv`), activate it, `pip install -r requirements.txt` with cwd at project root, then run `python .rtw/runs/20260321_084849/tmp/crud_verify.py` with cwd at project root: **exit code 0** and stdout contains a line exactly `ALL_CHECKS_PASSED`.

## Review
`main.py` implements full CRUD with `Task`/`TaskCreate`/`TaskUpdate`, monotonic ids, JSON via `model_dump(mode="json")`, and `HTTPException` 404 with string `detail`. Disposable `crud_verify.py` uses explicit `if` checks and prints `ALL_CHECKS_PASSED`; run with the tmp venv succeeded (exit 0).
