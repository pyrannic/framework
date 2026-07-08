from starlette.testclient import TestClient


def test_resource_not_found_exception__default(http_client: TestClient):
    response = http_client.get("/raise_resource_not_found/default")

    assert response.status_code == 404

    error_ = response.json()
    error_detail = error_["detail"][0]

    assert error_["resource_id"] == "model_id_value"
    assert "model_id" in error_detail["loc"]
    assert error_detail["type"] == "value_error.resource_not_found"
    assert error_detail["msg"] == "resource has not been found"


def test_resource_not_found_exception__custom(http_client: TestClient):
    response = http_client.get("/raise_resource_not_found/custom")

    assert response.status_code == 404

    error_ = response.json()
    error_detail = error_["detail"][0]

    assert error_["resource_id"] == "model_id_value"
    assert "query" in error_detail["loc"]
    assert "model_id" in error_detail["loc"]
    assert error_detail["type"] == "custom_error_type"
    assert error_detail["msg"] == "Custom error message"
