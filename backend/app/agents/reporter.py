from app.agents._mock import mock_reporter
from app.config import get_settings
from app.core.workflow_state import WorkflowState

SLUG = "reporter"


async def run(state: WorkflowState) -> WorkflowState:
    settings = get_settings()
    if settings.mock_agents:
        return mock_reporter(state)

    import litellm

    analysis = state.get("analysis", "")
    response = await litellm.acompletion(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Format this analysis as a concise markdown report:\n{analysis}",
            }
        ],
    )
    content = response.choices[0].message.content or ""
    return {**state, "report": content}
