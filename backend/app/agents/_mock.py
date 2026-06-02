"""Mock agent responses when MOCK_AGENTS=true (default for local dev)."""

from app.core.workflow_state import WorkflowState


def mock_browser(state: WorkflowState) -> WorkflowState:
    urls = state.get("urls") or [state.get("target_url", "https://example.com")]
    return {
        **state,
        "raw_content": f"[mock] Scraped content from {urls}",
    }


def mock_extractor(state: WorkflowState) -> WorkflowState:
    raw = state.get("raw_content", "")
    return {
        **state,
        "structured_data": {
            "source": "mock",
            "summary": str(raw)[:500],
            "items": [{"name": "Pro Plan", "price": 99}],
        },
    }


def mock_analyzer(state: WorkflowState) -> WorkflowState:
    data = state.get("structured_data", {})
    return {
        **state,
        "analysis": f"[mock] Analysis complete. Keys: {list(data.keys())}",
    }


def mock_reporter(state: WorkflowState) -> WorkflowState:
    return {
        **state,
        "report": f"[mock] Report:\n{state.get('analysis', 'No analysis')}",
    }


def mock_qa(state: WorkflowState) -> WorkflowState:
    url = state.get("target_url") or (state.get("urls") or ["https://example.com"])[0]
    scenario = state.get("scenario", "smoke test")
    return {
        **state,
        "qa_result": {
            "passed": True,
            "url": url,
            "scenario": scenario,
            "message": "[mock] QA scenario passed",
        },
    }
