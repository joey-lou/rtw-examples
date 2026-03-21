from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskCreate(TaskBase):
    """
    Input model for task creation and updates.
    """


class TaskOut(TaskBase):
    id: int
    created_at: datetime


_tasks_store: dict[int, TaskOut] = {}
_id_counter: int = 0


def _next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks() -> list[TaskOut]:
    return [_tasks_store[task_id] for task_id in sorted(_tasks_store.keys())]


@app.get("/tasks/{id}", response_model=TaskOut)
def get_task(id: int) -> TaskOut:
    task = _tasks_store.get(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate) -> TaskOut:
    task_id = _next_id()
    now = datetime.now(UTC)
    task = TaskOut(
        id=task_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=now,
    )
    _tasks_store[task_id] = task
    return task


@app.put("/tasks/{id}", response_model=TaskOut)
def update_task(id: int, payload: TaskCreate) -> TaskOut:
    existing = _tasks_store.get(id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated = TaskOut(
        id=id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=existing.created_at,
    )
    _tasks_store[id] = updated
    return updated


@app.delete("/tasks/{id}")
def delete_task(id: int) -> dict:
    if id not in _tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks_store[id]
    return {"deleted": True, "id": id}
