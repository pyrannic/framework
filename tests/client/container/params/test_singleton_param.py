from fastapi.testclient import TestClient


def test_singleton_param(http_client: TestClient):
    response_a = http_client.get("/params/singleton_memory_address")
    response_b = http_client.get("/params/singleton_memory_address")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    object_a = response_a.json()
    object_b = response_b.json()

    assert object_a[0] == object_a[1]
    assert object_b[0] == object_b[1]
    assert object_a == object_b
