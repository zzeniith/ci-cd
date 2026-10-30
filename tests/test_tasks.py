def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 500
    assert response.json() == {"status": "ok"}


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn CI/CD",
            "description": "Build a GitHub Actions pipeline",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn CI/CD",
        "description": "Build a GitHub Actions pipeline",
        "completed": False,
    }


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task one"})
    client.post("/tasks", json={"title": "Task two"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task_with_invalid_title(client):
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Delete this task"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
