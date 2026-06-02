from collections.abc import Awaitable, Callable

from app.core.exceptions import AgentNotFoundError
from app.core.workflow_state import WorkflowState

AgentRunner = Callable[[WorkflowState], Awaitable[WorkflowState]]


class AgentRegistry:
    def __init__(self) -> None:
        self._runners: dict[str, AgentRunner] = {}

    def register(self, slug: str, runner: AgentRunner) -> None:
        self._runners[slug] = runner

    def get(self, slug: str) -> AgentRunner:
        if slug not in self._runners:
            raise AgentNotFoundError(slug)
        return self._runners[slug]

    def slugs(self) -> list[str]:
        return list(self._runners.keys())

    @classmethod
    def load_builtin_agents(cls) -> "AgentRegistry":
        from app.agents import analyzer, browser, extractor, qa_tester, reporter

        registry = cls()
        registry.register("browser-agent", browser.run)
        registry.register("extractor", extractor.run)
        registry.register("analyzer", analyzer.run)
        registry.register("reporter", reporter.run)
        registry.register("qa-tester", qa_tester.run)
        return registry
