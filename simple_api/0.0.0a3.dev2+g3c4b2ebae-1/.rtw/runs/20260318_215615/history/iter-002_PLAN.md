## Steps
1. **Scaffold FastAPI app, models, and in-memory storage** — create `main.py` with the FastAPI app, Pydantic task models, module-level in-memory store, and route definitions for all endpoints (may be stubbed). ✓
2. **Implement GET/POST endpoints** — implement `GET /tasks` and `POST /tasks` with correct response payloads and status codes (200/201). ✓
3. **Implement remaining endpoints + 404 handling** — implement `GET /tasks/{id}`, `PUT /tasks/{id}`, and `DELETE /tasks/{id}` with 404 for missing tasks and correct status codes. ✓
4. **Add verification (curl/pytest)** — add a small verification routine (curl script and/or pytest) that exercises all endpoints and captures logs under `.rtw/runs/20260318_215615/tmp`.

## Lessons
- Start by matching the repository runner convention: generate code in the workspace root (alongside `main.py`/`requirements.txt`), while keeping `.rtw/` strictly for metadata and run artifacts.
