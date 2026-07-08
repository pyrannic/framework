from starlette.testclient import TestClient


def test_internal_server_error_exception__default(http_client: TestClient):
    response = http_client.get("/raise_internal_server_error/default")

    assert response.status_code == 500

    error_ = response.json()
    assert "This is a test exception for internal server error" in error_["detail"]
