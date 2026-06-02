from app.core.agent_registry import AgentRegistry


def test_loads_all_builtin_slugs():
    registry = AgentRegistry.load_builtin_agents()
    slugs = set(registry.slugs())
    assert "browser-agent" in slugs
    assert "extractor" in slugs
    assert "analyzer" in slugs
    assert "qa-tester" in slugs
