from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.arango import get_db
from app.repositories.agent_repository import AgentRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.graph_repository import GraphRepository
from app.repositories.user_repository import UserRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.services.agent_service import AgentService
from app.services.auth_service import AuthService
from app.services.execution_service import ExecutionService
from app.services.workflow_service import WorkflowService

security = HTTPBearer(auto_error=False)


def get_user_repo():
    return UserRepository(get_db())


def get_agent_repo():
    return AgentRepository(get_db())


def get_workflow_repo():
    return WorkflowRepository(get_db())


def get_execution_repo():
    return ExecutionRepository(get_db())


def get_graph_repo():
    return GraphRepository(get_db())


def get_auth_service(repo: Annotated[UserRepository, Depends(get_user_repo)]) -> AuthService:
    return AuthService(repo)


def get_agent_service(
    agent_repo: Annotated[AgentRepository, Depends(get_agent_repo)],
    graph_repo: Annotated[GraphRepository, Depends(get_graph_repo)],
    execution_repo: Annotated[ExecutionRepository, Depends(get_execution_repo)],
) -> AgentService:
    return AgentService(agent_repo, graph_repo, execution_repo)


def get_workflow_service(
    workflow_repo: Annotated[WorkflowRepository, Depends(get_workflow_repo)],
    agent_repo: Annotated[AgentRepository, Depends(get_agent_repo)],
) -> WorkflowService:
    return WorkflowService(workflow_repo, agent_repo, get_db())


def get_execution_service(
    execution_repo: Annotated[ExecutionRepository, Depends(get_execution_repo)],
    workflow_repo: Annotated[WorkflowRepository, Depends(get_workflow_repo)],
) -> ExecutionService:
    return ExecutionService(execution_repo, workflow_repo)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    token = None
    if credentials:
        token = credentials.credentials
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if not token:
        raise UnauthorizedError("Missing authentication token")
    user_id = decode_access_token(token)
    if not user_id:
        raise UnauthorizedError("Invalid or expired token")
    return user_id
