"""FastAPI task API."""

from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


tasks: dict[int, Task] = {}
_next_id: int = 1


def _task_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


@app.get("/tasks")
def list_tasks() -> list[dict]:
    ordered = sorted(tasks.values(), key=lambda t: t.id)
    return [t.model_dump(mode="json") for t in ordered]


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> dict:
    if task_id not in tasks:
        raise _task_not_found()
    return tasks[task_id].model_dump(mode="json")


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> dict:
    global _next_id
    task_id = _next_id
    _next_id += 1
    task = Task(
        id=task_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=datetime.utcnow(),
    )
    tasks[task_id] = task
    return task.model_dump(mode="json")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate) -> dict:
    if task_id not in tasks:
        raise _task_not_found()
    current = tasks[task_id]
    data = current.model_dump()
    updates = payload.model_dump(exclude_unset=True)
    data.update(updates)
    updated = Task(**data)
    tasks[task_id] = updated
    return updated.model_dump(mode="json")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    if task_id not in tasks:
        raise _task_not_found()
    del tasks[task_id]
    return {"ok": True}
