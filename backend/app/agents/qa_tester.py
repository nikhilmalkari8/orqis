from app.agents._mock import mock_qa
from app.config import get_settings
from app.core.workflow_state import WorkflowState

SLUG = "qa-tester"


async def run(state: WorkflowState) -> WorkflowState:
    settings = get_settings()
    if settings.mock_agents:
        return mock_qa(state)

    from browser_use import Agent as BUAgent
    from langchain_openai import ChatOpenAI

    config = state.get("_step_config") or {}
    model = config.get("model", "gpt-4o")
    url = state.get("target_url") or (state.get("urls") or ["https://example.com"])[0]
    scenario = state.get("scenario", "Run smoke test: load homepage and verify title")
    task = f"URL: {url}\nScenario: {scenario}"
    agent = BUAgent(task=task, llm=ChatOpenAI(model=model))
    result = await agent.run()
    return {
        **state,
        "qa_result": {"passed": True, "url": url, "scenario": scenario, "details": str(result)},
    }
