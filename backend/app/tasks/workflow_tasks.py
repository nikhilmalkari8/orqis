import asyncio
import os
import time
from datetime import datetime, timezone

from app.config import get_settings
from app.core.agent_registry import AgentRegistry
from app.core.exceptions import StepFailedError
from app.core.output_truncator import truncate_output
from app.core.workflow_compiler import WorkflowCompiler
from app.db.arango import get_db
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.tasks.celery_app import celery_app


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _capture_langsmith() -> dict:
    try:
        from langsmith import get_current_run_tree

        tree = get_current_run_tree()
        if tree:
            return {
                "trace_url": tree.get_url() if hasattr(tree, "get_url") else None,
                "run_id": str(tree.id) if hasattr(tree, "id") else None,
                "project": get_settings().langsmith_project,
            }
    except Exception:
        pass
    return {"trace_url": None, "run_id": None, "project": get_settings().langsmith_project}


@celery_app.task(bind=True, name="execute_workflow")
def execute_workflow(self, execution_id: str) -> None:
    settings = get_settings()
    if settings.langsmith_tracing and settings.langsmith_api_key:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project

    db = get_db()
    execution_repo = ExecutionRepository(db)
    workflow_repo = WorkflowRepository(db)

    ex = execution_repo.get(execution_id)
    if not ex:
        return

    started = time.monotonic()
    execution_repo.update(
        execution_id,
        {"status": "running", "started_at": _now_iso()},
    )

    workflow = workflow_repo.get(ex["workflow_id"])
    if not workflow:
        execution_repo.update(
            execution_id,
            {"status": "failed", "error": "Workflow not found", "completed_at": _now_iso()},
        )
        return

    step_summaries: list[dict] = []
    step_started: dict[str, float] = {}

    def on_step_event(
        *,
        step_id: str,
        agent_slug: str,
        status: str,
        error: str | None = None,
    ) -> None:
        now = _now_iso()
        if status == "running":
            step_started[step_id] = time.monotonic()
            step_summaries.append(
                {
                    "step_id": step_id,
                    "agent": agent_slug,
                    "status": "running",
                    "started_at": now,
                }
            )
        else:
            for s in step_summaries:
                if s["step_id"] == step_id:
                    s["status"] = status
                    s["completed_at"] = now
                    if step_id in step_started:
                        s["duration_ms"] = int((time.monotonic() - step_started[step_id]) * 1000)
                    if error:
                        s["error"] = error
                    break
        execution_repo.update(execution_id, {"step_summaries": step_summaries})

    registry = AgentRegistry.load_builtin_agents()
    compiler = WorkflowCompiler(registry)
    definition = workflow["definition"]
    input_data = ex.get("input_data") or {}

    initial_state = {
        **input_data,
        "_execution_id": execution_id,
        "_workflow_id": workflow["_key"],
    }

    try:
        graph = compiler.compile(
            definition,
            input_data=input_data,
            on_step_event=on_step_event,
        )
        result = asyncio.run(graph.ainvoke(initial_state))
        output = truncate_output(dict(result))
        trace = _capture_langsmith()
        duration_ms = int((time.monotonic() - started) * 1000)
        execution_repo.update(
            execution_id,
            {
                "status": "completed",
                "output_data": output,
                "langsmith": trace,
                "step_summaries": step_summaries,
                "completed_at": _now_iso(),
                "duration_ms": duration_ms,
            },
        )
    except StepFailedError as e:
        duration_ms = int((time.monotonic() - started) * 1000)
        execution_repo.update(
            execution_id,
            {
                "status": "failed",
                "failed_step_id": e.step_id,
                "failed_agent_slug": e.agent_slug,
                "error": e.message,
                "step_summaries": step_summaries,
                "langsmith": _capture_langsmith(),
                "completed_at": _now_iso(),
                "duration_ms": duration_ms,
            },
        )
    except Exception as e:
        duration_ms = int((time.monotonic() - started) * 1000)
        execution_repo.update(
            execution_id,
            {
                "status": "failed",
                "error": str(e),
                "step_summaries": step_summaries,
                "langsmith": _capture_langsmith(),
                "completed_at": _now_iso(),
                "duration_ms": duration_ms,
            },
        )
