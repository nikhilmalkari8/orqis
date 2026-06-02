class OrqisError(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: dict | None = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(OrqisError):
    def __init__(self, message: str = "Resource not found", details: dict | None = None):
        super().__init__(message, code="NOT_FOUND", details=details)


class ValidationError(OrqisError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class AgentNotFoundError(NotFoundError):
    def __init__(self, slug: str):
        super().__init__(f"Agent '{slug}' is not registered.", details={"slug": slug})
        self.code = "AGENT_NOT_FOUND"


class UnauthorizedError(OrqisError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, code="UNAUTHORIZED")


class StepFailedError(OrqisError):
    def __init__(self, step_id: str, agent_slug: str, message: str = "Step failed"):
        super().__init__(message, code="EXECUTION_STEP_FAILED", details={"step_id": step_id, "agent_slug": agent_slug})
        self.step_id = step_id
        self.agent_slug = agent_slug
