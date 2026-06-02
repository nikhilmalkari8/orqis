from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.execution import ExecutionResponse, ExecutionSummary, StepSummary
from app.schemas.workflow import RunWorkflowResponse
from app.tasks.workflow_tasks import execute_workflow


class ExecutionService:
    def __init__(
        self,
        execution_repo: ExecutionRepository,
        workflow_repo: WorkflowRepository,
    ):
        self.execution_repo = execution_repo
        self.workflow_repo = workflow_repo

    def _to_response(self, doc: dict) -> ExecutionResponse:
        summaries = [
            StepSummary(
                step_id=s.get("step_id", ""),
                agent=s.get("agent", ""),
                status=s.get("status", ""),
                started_at=s.get("started_at"),
                completed_at=s.get("completed_at"),
                duration_ms=s.get("duration_ms"),
                error=s.get("error"),
            )
            for s in doc.get("step_summaries") or []
        ]
        return ExecutionResponse(
            id=doc["id"],
            workflow_id=doc["workflow_id"],
            workflow_slug=doc.get("workflow_slug", ""),
            status=doc["status"],
            trigger=doc.get("trigger", "api"),
            input_data=doc.get("input_data") or {},
            output_data=doc.get("output_data") or {},
            langsmith=doc.get("langsmith") or {},
            failed_step_id=doc.get("failed_step_id"),
            failed_agent_slug=doc.get("failed_agent_slug"),
            error=doc.get("error"),
            step_summaries=summaries,
            started_at=doc.get("started_at"),
            completed_at=doc.get("completed_at"),
            duration_ms=doc.get("duration_ms"),
            celery_task_id=doc.get("celery_task_id"),
            created_at=doc["created_at"],
        )

    def _to_summary(self, doc: dict) -> ExecutionSummary:
        ls = doc.get("langsmith") or {}
        return ExecutionSummary(
            id=doc["id"],
            workflow_id=doc["workflow_id"],
            workflow_slug=doc.get("workflow_slug", ""),
            status=doc["status"],
            started_at=doc.get("started_at"),
            completed_at=doc.get("completed_at"),
            duration_ms=doc.get("duration_ms"),
            failed_step_id=doc.get("failed_step_id"),
            failed_agent_slug=doc.get("failed_agent_slug"),
            langsmith_trace_url=ls.get("trace_url"),
        )

    def trigger_run(self, user_id: str, workflow_id: str, input_data: dict) -> RunWorkflowResponse:
        workflow = self.workflow_repo.get_by_key(workflow_id, user_id)
        if not workflow:
            raise NotFoundError("Workflow not found")

        definition = workflow.get("definition") or {}
        if not definition.get("steps"):
            raise ValidationError("Workflow has no steps")

        execution = self.execution_repo.create(
            {
                "user_id": user_id,
                "workflow_id": workflow_id,
                "workflow_slug": workflow["slug"],
                "workflow_version": workflow.get("version", 1),
                "trigger": "api",
                "input_data": input_data,
            }
        )
        self.execution_repo.create_execution_edge(execution["_key"], workflow_id)

        task = execute_workflow.delay(execution["_key"])
        self.execution_repo.update(execution["_key"], {"celery_task_id": task.id})

        return RunWorkflowResponse(
            execution_id=execution["id"],
            status="pending",
            celery_task_id=task.id,
        )

    def get_execution(self, user_id: str, execution_id: str) -> ExecutionResponse:
        doc = self.execution_repo.get_by_key(execution_id, user_id)
        if not doc:
            raise NotFoundError("Execution not found")
        return self._to_response(doc)

    def list_executions(
        self,
        user_id: str,
        *,
        workflow_id: str | None = None,
        agent: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[ExecutionSummary]:
        docs = self.execution_repo.list_by_user(
            user_id,
            workflow_id=workflow_id,
            agent_slug=agent,
            status=status,
            limit=limit,
        )
        return [self._to_summary(d) for d in docs]
