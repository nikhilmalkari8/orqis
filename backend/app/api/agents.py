from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_agent_service, get_current_user_id
from app.schemas.agent import AgentDetailResponse, AgentListResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=AgentListResponse)
def list_agents(service: Annotated[AgentService, Depends(get_agent_service)]):
    return service.list_agents()


@router.get("/{slug}", response_model=AgentDetailResponse)
def get_agent(
    slug: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[AgentService, Depends(get_agent_service)],
):
    return service.get_agent_detail(slug, user_id)
