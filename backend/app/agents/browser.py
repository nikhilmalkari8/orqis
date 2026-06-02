from app.agents._mock import mock_browser
from app.config import get_settings
from app.core.workflow_state import WorkflowState

SLUG = "browser-agent"


async def run(state: WorkflowState) -> WorkflowState:
    settings = get_settings()
    if settings.mock_agents:
        return mock_browser(state)

    from browser_use import Agent as BUAgent
    from langchain_openai import ChatOpenAI

    config = state.get("_step_config") or {}
    model = config.get("model", "gpt-4o")
    urls = state.get("urls") or []
    task = state.get("browser_task") or f"Extract main content from: {urls}"
    agent = BUAgent(task=task, llm=ChatOpenAI(model=model))
    result = await agent.run()
    return {**state, "raw_content": str(result)}
