# Subtask: Dependencies and application skeleton

Add `requirements.txt` and a single FastAPI entry module at the **project workspace root** (`simple_api/0.0.0a3.dev2+g3c4b2ebae-2`), not under `.rtw/` or the run directory.

- `requirements.txt`: pin or constrain `fastapi`, `uvicorn[standard]`, and anything else needed for Python 3.11+ (e.g. `httpx` only if you add tests now; otherwise omit until the verification step).
- One module (e.g. `main.py`): `FastAPI()` instance, Pydantic v2 models matching the task shape (id, title, description, completed, created_at), and an in-memory structure (dict or list) keyed or indexed by task id—routes may be stubs (empty path operations or `pass` with TODO) **only if** the app still imports; prefer defining route functions without full logic if splitting work, but the file must be valid Python and `uvicorn main:app --help` or importing `app` must work.

Use the run tmp directory only for disposable venv/install logs (see acceptance criteria), not for source code.

## Acceptance criteria
- [x] Files exist at project root: `requirements.txt` and `main.py` with `app = FastAPI()`, Pydantic v2 `Task` (`id`, `title`, `description`, `completed`, `created_at`), and stub routes that keep the module importable.
- [x] From run `tmp`, `pip install -r ../../../../requirements.txt` succeeds (verified with existing `python3.11` venv).
- [x] With venv activated and cwd at project root, `python -c "import main; assert hasattr(main, 'app')"` exits 0.
- [x] Module-level in-memory store `tasks: dict[int, Task] = {}` is defined.

## Review
Subtask met: constrained `requirements.txt`, valid `main.py` skeleton, and install/import checks pass; endpoints are `pass`/TODO stubs as allowed for this step.
