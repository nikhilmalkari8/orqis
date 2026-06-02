from app.agents._mock import mock_extractor
from app.config import get_settings
from app.core.workflow_state import WorkflowState

SLUG = "extractor"


async def run(state: WorkflowState) -> WorkflowState:
    settings = get_settings()
    if settings.mock_agents:
        return mock_extractor(state)

    import instructor
    from openai import OpenAI
    from pydantic import BaseModel, Field

    class ExtractedItem(BaseModel):
        name: str
        price: float | None = None

    class ExtractedData(BaseModel):
        summary: str
        items: list[ExtractedItem] = Field(default_factory=list)

    client = instructor.from_openai(OpenAI())
    raw = str(state.get("raw_content", ""))
    data = client.chat.completions.create(
        model="gpt-4o",
        response_model=ExtractedData,
        messages=[
            {
                "role": "user",
                "content": f"Extract structured pricing/features from:\n{raw[:8000]}",
            }
        ],
    )
    return {**state, "structured_data": data.model_dump()}
