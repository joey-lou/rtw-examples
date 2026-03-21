# Subtask: Add verification (curl/pytest)
Implement endpoint verification for all CRUD routes using a small Python script that exercises the FastAPI app via `fastapi.testclient.TestClient`.

Write the script as a scratch artifact under `.rtw/runs/20260318_215615/tmp/verify_api.py`. The script must:
- Import `app` from `main.py` (workspace root).
- Call, in order, and assert the expected HTTP status codes:
  - `GET /tasks` (expect `200`)
  - `POST /tasks` with `title`/`description`/`completed` (expect `201`, capture `id`)
  - `GET /tasks/{id}` (expect `200`, validate response fields: `id`, `title`, `description`, `completed`, `created_at`)
  - `PUT /tasks/{id}` updating `completed` (expect `200`)
  - `DELETE /tasks/{id}` (expect `200`)
  - `GET /tasks/{id}` after delete (expect `404`)
- Write outputs into the same tmp directory:
  - `.rtw/runs/20260318_215615/tmp/verification_report.json`
  - `.rtw/runs/20260318_215615/tmp/verification.log`
- Exit non-zero if any assertion fails.

Explicit verification command (run from the workspace root `simple_api/<version>/`):
```sh
python .rtw/runs/20260318_215615/tmp/verify_api.py
```

## Acceptance criteria
- [x] Running `python .rtw/runs/20260318_215615/tmp/verify_api.py` exits `0` and creates `.rtw/runs/20260318_215615/tmp/verification_report.json` containing `status_codes` and `created_task`
- [x] The report confirms the expected status codes: `200, 201, 200, 200, 200, 404` for the sequence `GET /tasks`, `POST /tasks`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`, `GET /tasks/{id}` after delete

## Review
Ran `verify_api.py` successfully; it exited `0`, wrote `verification_report.json`/`verification.log`, produced `status_codes` matching `[200, 201, 200, 200, 200, 404]`, and `created_task` contained the expected fields.
