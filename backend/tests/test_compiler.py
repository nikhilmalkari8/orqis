import pytest

from app.core.agent_registry import AgentRegistry
from app.core.workflow_compiler import WorkflowCompiler


@pytest.fixture
def compiler():
    return WorkflowCompiler(AgentRegistry.load_builtin_agents())


def test_validate_rejects_empty_steps(compiler):
    errors = compiler.validate({"schema_version": "1.0", "steps": []})
    assert any("empty" in e for e in errors)


def test_validate_unknown_agent(compiler):
    errors = compiler.validate(
        {
            "schema_version": "1.0",
            "steps": [{"id": "a", "agent": "nonexistent"}],
        }
    )
    assert any("unknown agent" in e for e in errors)


def test_compile_builds_graph(compiler):
    definition = {
        "schema_version": "1.0",
        "steps": [
            {"id": "scrape", "agent": "browser-agent"},
            {"id": "extract", "agent": "extractor"},
        ],
    }
    graph = compiler.compile(definition, input_data={"urls": ["https://example.com"]})
    assert graph is not None
