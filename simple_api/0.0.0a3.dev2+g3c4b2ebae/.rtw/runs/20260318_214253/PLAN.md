## Steps
1. **Scaffold FastAPI app, models, and in-memory CRUD** — Create the `FastAPI` app, `Pydantic` models, in-memory task store, and wire all 5 endpoints with correct status codes and 404 handling ✓
2. **Add automated tests** — Verify each endpoint’s behavior using FastAPI’s `TestClient` (create/list/get/update/delete and missing-id 404)
3. **Provide curl-based verification** — Add a small curl smoke-test procedure (commands) and ensure manual runs match the tests

## Lessons
- Keep the in-memory store implementation isolated (helpers for get-or-404 and id/timestamp creation) so later test additions are straightforward.
