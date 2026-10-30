from app.utils import session
from fastapi import FastAPI, HTTPException, status

from app.schemas import TaskCreate, TaskResponse
from app.store import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
)

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_endpoint(data: TaskCreate) -> TaskResponse:
    return create_task(data)


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    return get_all_tasks()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int) -> TaskResponse:
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int) -> None:
    if not delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )