from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import OrqisError


async def orqis_error_handler(_request: Request, exc: OrqisError) -> JSONResponse:
    status = 500
    if exc.code == "NOT_FOUND" or exc.code == "AGENT_NOT_FOUND":
        status = 404
    elif exc.code == "VALIDATION_ERROR" or exc.code == "WORKFLOW_INVALID":
        status = 422
    elif exc.code == "UNAUTHORIZED":
        status = 401
    return JSONResponse(
        status_code=status,
        content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
    )
