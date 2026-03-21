# Subtask: Verification

Add **`verify_api.py` at the project workspace root** (`simple_api/0.0.0a3.dev2+g3c4b2ebae-2`). Do not place this file under `.rtw/` or the run directory.

**Behavior:**

- Import `app` from `main` and `TestClient` from `fastapi.testclient` (or `starlette.testclient`).
- Under `if __name__ == "__main__":`, exercise every endpoint and status code with **explicit `if` checks** (not bare `assert`, so behavior is unchanged under `python -O`): on failure print `FAIL: <reason>` to stderr or stdout and call `sys.exit(1)`; on full success print a line exactly `ALL_CHECKS_PASSED` and exit `0`.
- Cover at minimum: empty `GET /tasks` → `200` and JSON list; `POST /tasks` with `title`/`description` → `201` and body includes assigned `id`, `created_at`, and fields; `GET /tasks/{id}` existing → `200`; missing id → `404` with JSON containing string `detail`; `PUT /tasks/{id}` partial update → `200`; `PUT` missing → `404`; `DELETE` existing → `200` with JSON; `DELETE` missing → `404`; final `GET /tasks` reflects deletions.
- Do not add new dependencies to `requirements.txt` (use TestClient from the existing FastAPI/Starlette install).

**Scratch:** Use `.rtw/runs/20260321_084849/tmp` only for a disposable venv (e.g. `python3.11 -m venv .rtw/runs/20260321_084849/tmp/.venv`), logs, or other generated artifacts—not for `verify_api.py`.

## Acceptance criteria
- [x] File `verify_api.py` exists at the project root (same directory as `main.py` and `requirements.txt`).
- [x] Inspect `verify_api.py`: defines `if __name__ == "__main__":`, uses `TestClient`, uses explicit `if`/`sys.exit(1)` failure paths (no reliance on bare `assert` for the required checks), and prints the exact success token `ALL_CHECKS_PASSED` on success.
- [x] With cwd at project root: create or reuse a venv under `.rtw/runs/20260321_084849/tmp` (e.g. `.venv`), activate it, run `pip install -r requirements.txt`, then run `python verify_api.py`: **exit code 0** and stdout contains a line exactly `ALL_CHECKS_PASSED`.

## Review
`verify_api.py` meets the spec: `TestClient`, `_fail` + explicit `if` checks (no bare asserts for required paths), full endpoint coverage including `detail` string on 404 GET, and `ALL_CHECKS_PASSED` on success. Reviewer ran venv install under `.rtw/runs/20260321_084849/tmp/.venv` and `python verify_api.py` exited 0 with the success token.
