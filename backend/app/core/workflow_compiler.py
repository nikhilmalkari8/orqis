from collections.abc import Callable
from typing import Any

from langgraph.graph import END, StateGraph

from app.core.agent_registry import AgentRegistry
from app.core.exceptions import StepFailedError, ValidationError
from app.core.input_resolver import merge_step_inputs
from app.core.workflow_state import WorkflowState


class WorkflowCompiler:
    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def validate(self, definition: dict) -> list[str]:
        errors: list[str] = []
        if definition.get("schema_version") != "1.0":
            errors.append("definition.schema_version must be '1.0'")
        steps = definition.get("steps") or []
        if not steps:
            errors.append("definition.steps must not be empty")
        seen_ids: set[str] = set()
        for step in steps:
            sid = step.get("id")
            if not sid:
                errors.append("each step requires id")
                continue
            if sid in seen_ids:
                errors.append(f"duplicate step id: {sid}")
            seen_ids.add(sid)
            agent = step.get("agent")
            if not agent:
                errors.append(f"step {sid} requires agent")
            elif agent not in self.registry.slugs():
                errors.append(f"unknown agent slug: {agent}")
        return errors

    def compile(
        self,
        definition: dict,
        *,
        input_data: dict | None = None,
        on_step_event: Callable[..., None] | None = None,
    ) -> Any:
        errors = self.validate(definition)
        if errors:
            raise ValidationError("Invalid workflow definition", details={"errors": errors})

        steps = definition["steps"]
        graph = StateGraph(WorkflowState)
        base_inputs = input_data or {}

        for step in steps:
            step_id = step["id"]
            agent_slug = step["agent"]
            runner = self.registry.get(agent_slug)
            step_config = step.get("config") or {}

            async def node_fn(
                state: WorkflowState,
                _step=step,
                _step_id=step_id,
                _agent_slug=agent_slug,
                _runner=runner,
                _config=step_config,
            ) -> WorkflowState:
                if on_step_event:
                    on_step_event(
                        step_id=_step_id,
                        agent_slug=_agent_slug,
                        status="running",
                    )
                working = merge_step_inputs(_step, dict(state), base_inputs)
                working["_current_step_id"] = _step_id
                working["_step_config"] = _config
                try:
                    result = await _runner(working)
                    if on_step_event:
                        on_step_event(
                            step_id=_step_id,
                            agent_slug=_agent_slug,
                            status="completed",
                        )
                    return result
                except StepFailedError:
                    raise
                except Exception as e:
                    if on_step_event:
                        on_step_event(
                            step_id=_step_id,
                            agent_slug=_agent_slug,
                            status="failed",
                            error=str(e),
                        )
                    raise StepFailedError(_step_id, _agent_slug, str(e)) from e

            graph.add_node(step_id, node_fn)

        graph.set_entry_point(steps[0]["id"])
        for i in range(len(steps) - 1):
            graph.add_edge(steps[i]["id"], steps[i + 1]["id"])
        graph.add_edge(steps[-1]["id"], END)

        return graph.compile()
