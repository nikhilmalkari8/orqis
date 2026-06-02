from pydantic import BaseModel


class ExecutionSummary(BaseModel):
    id: str
    workflow_id: str
    workflow_slug: str
    status: str
    started_at: str | None
    completed_at: str | None
    duration_ms: int | None
    failed_step_id: str | None
    failed_agent_slug: str | None
    langsmith_trace_url: str | None


class StepSummary(BaseModel):
    step_id: str
    agent: str
    status: str
    started_at: str | None = None
    completed_at: str | None = None
    duration_ms: int | None = None
    error: str | None = None


class ExecutionResponse(BaseModel):
    id: str
    workflow_id: str
    workflow_slug: str
    status: str
    trigger: str
    input_data: dict
    output_data: dict
    langsmith: dict
    failed_step_id: str | None
    failed_agent_slug: str | None
    error: str | None
    step_summaries: list[StepSummary]
    started_at: str | None
    completed_at: str | None
    duration_ms: int | None
    celery_task_id: str | None
    created_at: str
