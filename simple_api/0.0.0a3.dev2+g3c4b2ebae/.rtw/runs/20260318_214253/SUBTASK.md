# Subtask: Scaffold FastAPI app, models, and in-memory CRUD
Implement the FastAPI todo/task REST API end-to-end in the project root (workspace root). Do not place code under `.rtw/` or the run directory.

## Implementation requirements (executor)
- Create a single FastAPI app in `main.py` at the workspace root.
- Add `requirements.txt` at the workspace root.
- Implement in-memory storage:
  - A module-level `dict[int, Task]` (or similar) to hold tasks.
  - A simple id generator (incrementing integer).
  - `created_at` set on creation (use timezone-aware UTC `datetime.now(timezone.utc)`).
- Define Pydantic models:
  - `Task` with fields `id`, `title`, `description`, `completed`, `created_at`
  - Input models for create/update (e.g. `TaskCreate`, `TaskUpdate`) matching the required fields except `id`/`created_at` for create.
- Implement the 5 endpoints with proper status codes and 404 handling:
  - `GET /tasks` -> `200` (list)
  - `GET /tasks/{id}` -> `200` (task) or `404` if missing
  - `POST /tasks` -> `201` (created task)
  - `PUT /tasks/{id}` -> `200` (updated task) or `404` if missing
  - `DELETE /tasks/{id}` -> `200` (deleted task) or `404` if missing
- Use FastAPI/Pydantic validation; missing ids must raise `HTTPException(status_code=404, ...)`.

## Verification requirements (must use scratch tmp)
- Use `.rtw/runs/20260318_214253/tmp` for any venv, installed packages, or generated logs during verification.
- Run a small curl smoke test against a locally started server and confirm status codes and JSON shapes for each endpoint.

## Acceptance criteria
- [ ] After installing dependencies in `.rtw/runs/20260318_214253/tmp` (venv), `python -c "from main import app; print('ok')"` succeeds and `app` exposes `GET /tasks`.
- [ ] A curl smoke test run while `uvicorn` is active returns: `GET /tasks` -> `200`, `POST /tasks` -> `201`, `GET /tasks/{id}` -> `200`, and `GET /tasks/999999` -> `404` (same for `PUT`/`DELETE` on a missing id).
