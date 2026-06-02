from datetime import datetime, timedelta, timezone

from app.core.exceptions import NotFoundError
from app.repositories.agent_repository import AgentRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.graph_repository import GraphRepository
from app.schemas.agent import (
    AgentDetail,
    AgentDetailResponse,
    AgentImplementation,
    AgentListResponse,
    AgentStats,
    AgentSummary,
    RecentExecution,
    WorkflowUsingAgent,
)


class AgentService:
    def __init__(
        self,
        agent_repo: AgentRepository,
        graph_repo: GraphRepository,
        execution_repo: ExecutionRepository,
    ):
        self.agent_repo = agent_repo
        self.graph_repo = graph_repo
        self.execution_repo = execution_repo

    def list_agents(self) -> AgentListResponse:
        items = []
        for doc in self.agent_repo.list_active():
            impl = doc.get("implementation") or {}
            items.append(
                AgentSummary(
                    slug=doc["slug"],
                    name=doc["name"],
                    version=doc.get("version", "1.0.0"),
                    category=doc.get("category", ""),
                    framework=impl.get("framework", ""),
                    status=doc.get("status", "active"),
                )
            )
        return AgentListResponse(items=items)

    def get_agent_detail(self, slug: str, user_id: str) -> AgentDetailResponse:
        doc = self.agent_repo.get_by_slug(slug)
        if not doc:
            raise NotFoundError(f"Agent '{slug}' not found", details={"slug": slug})

        impl = doc.get("implementation") or {}
        since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        stats_raw = self.graph_repo.agent_stats(slug, since)
        workflows_using = [
            WorkflowUsingAgent(**row) for row in self.graph_repo.workflows_using_agent(slug)
        ]

        recent_docs = self.execution_repo.list_by_user(user_id, agent_slug=slug, limit=10)
        recent = []
        for ex in recent_docs:
            ls = ex.get("langsmith") or {}
            recent.append(
                RecentExecution(
                    execution_id=ex["id"],
                    workflow_slug=ex.get("workflow_slug", ""),
                    status=ex["status"],
                    failed_step_id=ex.get("failed_step_id"),
                    langsmith_trace_url=ls.get("trace_url"),
                    started_at=ex.get("started_at"),
                )
            )

        return AgentDetailResponse(
            agent=AgentDetail(
                slug=doc["slug"],
                name=doc["name"],
                version=doc.get("version", "1.0.0"),
                description=doc.get("description", ""),
                implementation=AgentImplementation(
                    type=impl.get("type", "python"),
                    entrypoint=impl.get("entrypoint", ""),
                    framework=impl.get("framework", ""),
                    module=impl.get("module"),
                ),
                input_schema=doc.get("input_schema") or {},
                output_schema=doc.get("output_schema") or {},
                config_schema=doc.get("config_schema") or {},
                default_config=doc.get("default_config") or {},
                category=doc.get("category", ""),
                tags=doc.get("tags") or [],
            ),
            workflows_using=workflows_using,
            stats=AgentStats(**stats_raw),
            recent_executions=recent,
        )
