from pydantic import BaseModel, Field


class WorkflowDefinition(BaseModel):
    schema_version: str = "1.0"
    inputs: dict = Field(default_factory=dict)
    state_keys: list[str] = Field(default_factory=list)
    steps: list[dict]


class WorkflowCreate(BaseModel):
    slug: str
    name: str
    description: str = ""
    is_template: bool = False
    definition: WorkflowDefinition


class WorkflowUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_template: bool | None = None
    definition: WorkflowDefinition | None = None


class WorkflowSummary(BaseModel):
    id: str
    slug: str
    name: str
    description: str
    is_template: bool
    step_count: int
    updated_at: str


class WorkflowResponse(BaseModel):
    id: str
    user_id: str
    slug: str
    name: str
    description: str
    version: int
    is_template: bool
    definition: dict
    created_at: str
    updated_at: str


class RunWorkflowRequest(BaseModel):
    input_data: dict = Field(default_factory=dict)


class RunWorkflowResponse(BaseModel):
    execution_id: str
    status: str
    celery_task_id: str | None = None
