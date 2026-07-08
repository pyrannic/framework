from starlette.testclient import TestClient


def test_forget_scoped_instances__no_scoped(http_client: TestClient):
    response_a = http_client.get("/object_memory_address")
    response_b = http_client.get("/object_memory_address")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    object_a = response_a.json()
    object_b = response_b.json()

    assert object_a != object_b


def test_forget_scoped_instances__scoped(http_client: TestClient):
    response_a = http_client.get("/scoped_memory_address")
    response_b = http_client.get("/scoped_memory_address")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    object_a = response_a.json()
    object_b = response_b.json()

    assert object_a != object_b


def test_forget_scoped_instances__singleton(http_client: TestClient):
    response_a = http_client.get("/singleton_memory_address")
    response_b = http_client.get("/singleton_memory_address")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    object_a = response_a.json()
    object_b = response_b.json()

    assert object_a == object_b
