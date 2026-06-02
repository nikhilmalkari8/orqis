from app.agents._mock import mock_analyzer
from app.config import get_settings
from app.core.workflow_state import WorkflowState

SLUG = "analyzer"


async def run(state: WorkflowState) -> WorkflowState:
    settings = get_settings()
    if settings.mock_agents:
        return mock_analyzer(state)

    import litellm

    config = state.get("_step_config") or {}
    model = config.get("model", "gpt-4o")
    structured = state.get("structured_data", {})
    response = await litellm.acompletion(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this competitor data and provide executive insights:\n{structured}",
            }
        ],
    )
    content = response.choices[0].message.content or ""
    return {**state, "analysis": content}
