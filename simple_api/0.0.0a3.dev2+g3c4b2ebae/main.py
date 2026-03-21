from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=0)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=0)
    completed: bool


_tasks: dict[int, Task] = {}
_next_task_id: int = 1


def _get_task_or_404(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.get("/tasks", response_model=list[Task], status_code=200)
def list_tasks() -> list[Task]:
    return list(_tasks.values())


@app.get("/tasks/{task_id}", response_model=Task, status_code=200)
def get_task(task_id: int) -> Task:
    return _get_task_or_404(task_id)


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    global _next_task_id

    task_id = _next_task_id
    _next_task_id += 1

    task = Task(
        id=task_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=datetime.now(UTC),
    )
    _tasks[task_id] = task
    return task


@app.put("/tasks/{task_id}", response_model=Task, status_code=200)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    existing = _get_task_or_404(task_id)

    updated = Task(
        id=existing.id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=existing.created_at,
    )
    _tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", response_model=Task, status_code=200)
def delete_task(task_id: int) -> Task:
    existing = _get_task_or_404(task_id)
    del _tasks[task_id]
    return existing
