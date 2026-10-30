from app.schemas import TaskCreate, TaskResponse


tasks: dict[int, TaskResponse] = {}
_next_id = 1


def create_task(data: TaskCreate) -> TaskResponse:
    global _next_id

    task = TaskResponse(
        id=_next_id,
        title=data.title,
        description=data.description,
        completed=False,
    )

    tasks[task.id] = task
    _next_id += 1

    return task


def get_task(task_id: int) -> TaskResponse | None:
    return tasks.get(task_id)


def get_all_tasks() -> list[TaskResponse]:
    return list(tasks.values())


def delete_task(task_id: int) -> bool:
    return tasks.pop(task_id, None) is not None


def reset_tasks() -> None:
    global _next_id

    tasks.clear()
    _next_id = 1