from pydantic import BaseModel


class AgentSummary(BaseModel):
    slug: str
    name: str
    version: str
    category: str
    framework: str
    status: str


class AgentListResponse(BaseModel):
    items: list[AgentSummary]


class AgentImplementation(BaseModel):
    type: str
    entrypoint: str
    framework: str
    module: str | None = None


class AgentDetail(BaseModel):
    slug: str
    name: str
    version: str
    description: str
    implementation: AgentImplementation
    input_schema: dict
    output_schema: dict
    config_schema: dict
    default_config: dict
    category: str
    tags: list[str] = []


class WorkflowUsingAgent(BaseModel):
    workflow_id: str
    slug: str
    name: str
    step_id: str
    step_order: int


class AgentStats(BaseModel):
    total_runs: int
    completed: int
    failed: int
    success_rate: float
    last_run_at: str | None
    last_status: str | None


class RecentExecution(BaseModel):
    execution_id: str
    workflow_slug: str
    status: str
    failed_step_id: str | None
    langsmith_trace_url: str | None
    started_at: str | None


class AgentDetailResponse(BaseModel):
    agent: AgentDetail
    workflows_using: list[WorkflowUsingAgent]
    stats: AgentStats
    recent_executions: list[RecentExecution]
