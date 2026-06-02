from typing import Any, TypedDict


class WorkflowState(TypedDict, total=False):
    urls: list[str]
    email: str
    browser_task: str
    target_url: str
    scenario: str
    raw_content: str | dict[Any, Any]
    structured_data: dict[str, Any]
    analysis: str
    report: str
    qa_result: dict[str, Any]
    _execution_id: str
    _workflow_id: str
    _current_step_id: str
    _step_config: dict[str, Any]
