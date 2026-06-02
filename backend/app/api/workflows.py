from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user_id, get_workflow_service
from app.schemas.workflow import (
    RunWorkflowRequest,
    RunWorkflowResponse,
    WorkflowCreate,
    WorkflowResponse,
    WorkflowSummary,
    WorkflowUpdate,
)
from app.api.deps import get_execution_service
from app.services.execution_service import ExecutionService
from app.services.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=list[WorkflowSummary])
def list_workflows(
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
):
    return service.list_workflows(user_id)


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    body: WorkflowCreate,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
):
    return service.create(user_id, body)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
):
    return service.get_workflow(user_id, workflow_id)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: str,
    body: WorkflowUpdate,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
):
    return service.update(user_id, workflow_id, body)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    workflow_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
):
    service.delete(user_id, workflow_id)


@router.post("/{workflow_id}/run", response_model=RunWorkflowResponse, status_code=status.HTTP_202_ACCEPTED)
def run_workflow(
    workflow_id: str,
    body: RunWorkflowRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[ExecutionService, Depends(get_execution_service)],
):
    return service.trigger_run(user_id, workflow_id, body.input_data)
