"""Verify task API endpoints."""

import json
import sys

from fastapi.testclient import TestClient
from main import app


def _fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    client = TestClient(app)

    r = client.get("/tasks")
    if r.status_code != 200:
        _fail(f"GET /tasks expected 200, got {r.status_code}")
    try:
        initial_list = r.json()
    except json.JSONDecodeError:
        _fail("GET /tasks response is not JSON")
    if not isinstance(initial_list, list):
        _fail("GET /tasks must return JSON list")

    r = client.post("/tasks", json={"title": "t1", "description": "d1"})
    if r.status_code != 201:
        _fail(f"POST /tasks expected 201, got {r.status_code}")
    try:
        created = r.json()
    except json.JSONDecodeError:
        _fail("POST /tasks response is not JSON")
    if "id" not in created:
        _fail("POST body missing id")
    if "created_at" not in created:
        _fail("POST body missing created_at")
    if created.get("title") != "t1":
        _fail("POST body title mismatch")
    if created.get("description") != "d1":
        _fail("POST body description mismatch")

    task_id = created["id"]

    r = client.get(f"/tasks/{task_id}")
    if r.status_code != 200:
        _fail(f"GET /tasks/{{id}} existing expected 200, got {r.status_code}")

    r = client.get("/tasks/999999")
    if r.status_code != 404:
        _fail(f"GET missing task expected 404, got {r.status_code}")
    try:
        err_get = r.json()
    except json.JSONDecodeError:
        _fail("404 GET missing response is not JSON")
    if "detail" not in err_get:
        _fail("404 GET missing JSON must contain detail")
    if not isinstance(err_get["detail"], str):
        _fail("404 GET detail must be a string")

    r = client.put(f"/tasks/{task_id}", json={"title": "updated"})
    if r.status_code != 200:
        _fail(f"PUT partial expected 200, got {r.status_code}")
    try:
        updated = r.json()
    except json.JSONDecodeError:
        _fail("PUT response is not JSON")
    if updated.get("title") != "updated":
        _fail("PUT partial did not update title")
    if updated.get("description") != "d1":
        _fail("PUT partial should preserve description")

    r = client.put("/tasks/999998", json={"title": "x"})
    if r.status_code != 404:
        _fail(f"PUT missing expected 404, got {r.status_code}")

    r = client.delete(f"/tasks/{task_id}")
    if r.status_code != 200:
        _fail(f"DELETE existing expected 200, got {r.status_code}")
    try:
        del_body = r.json()
    except json.JSONDecodeError:
        _fail("DELETE response is not JSON")
    if not isinstance(del_body, dict):
        _fail("DELETE body must be a JSON object")

    r = client.delete("/tasks/999997")
    if r.status_code != 404:
        _fail(f"DELETE missing expected 404, got {r.status_code}")

    r = client.get("/tasks")
    if r.status_code != 200:
        _fail(f"final GET /tasks expected 200, got {r.status_code}")
    try:
        final_list = r.json()
    except json.JSONDecodeError:
        _fail("final GET /tasks not JSON")
    if final_list != []:
        _fail("final GET /tasks should reflect deletion (empty list)")

    print("ALL_CHECKS_PASSED")
