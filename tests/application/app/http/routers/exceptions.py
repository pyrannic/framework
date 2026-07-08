from fastapi import APIRouter
from starlette.exceptions import HTTPException

from pyrannic.http.exceptions.resource_not_found import ResourceNotFoundException
from pyrannic.http.exceptions.unprocessable_entity import UnprocessableEntityException

router = APIRouter(tags=["Exceptions Routes"])


@router.get(
    "/raise_unprocessable_entity/default",
    summary="Raise Unprocessable Entity Endpoint",
    description="Endpoint to raise an unprocessable entity exception.",
)
def raise_default_unprocessable_entity():
    raise UnprocessableEntityException("model_id_value", "model_id")


@router.get(
    "/raise_unprocessable_entity/custom",
    summary="Raise Unprocessable Entity Endpoint",
    description="Endpoint to raise an unprocessable entity exception.",
)
def raise_custom_unprocessable_entity():
    raise UnprocessableEntityException(
        "model_id_value",
        "model_id",
        loc_type="query",
        error_type="custom_error_type",
        message="Custom error message",
    )


@router.get(
    "/raise_resource_not_found/default",
    summary="Raise Resource Not Found Endpoint",
    description="Endpoint to raise a resource not found exception.",
)
def raise_default_resource_not_found():
    raise ResourceNotFoundException("model_id_value", "model_id")


@router.get(
    "/raise_resource_not_found/custom",
    summary="Raise Resource Not Found Endpoint",
    description="Endpoint to raise a resource not found exception.",
)
def raise_custom_resource_not_found():
    raise ResourceNotFoundException(
        "model_id_value",
        "model_id",
        loc_type="query",
        error_type="custom_error_type",
        message="Custom error message",
    )


@router.get(
    "/raise_internal_server_error/default",
    summary="Raise Internal Server Error Endpoint",
    description="Endpoint to raise an internal server error exception.",
)
def raise_internal_server_error():
    raise HTTPException(500, "This is a test exception for internal server error.")
