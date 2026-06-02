from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user_id, get_execution_service
from app.schemas.execution import ExecutionResponse, ExecutionSummary
from app.services.execution_service import ExecutionService

router = APIRouter(prefix="/executions", tags=["executions"])


@router.get("", response_model=list[ExecutionSummary])
def list_executions(
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[ExecutionService, Depends(get_execution_service)],
    workflow_id: str | None = None,
    agent: str | None = None,
    status: str | None = None,
    limit: int = Query(default=20, le=100),
):
    return service.list_executions(
        user_id,
        workflow_id=workflow_id,
        agent=agent,
        status=status,
        limit=limit,
    )


@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(
    execution_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[ExecutionService, Depends(get_execution_service)],
):
    return service.get_execution(user_id, execution_id)
