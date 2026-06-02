from arango.database import StandardDatabase

from app.core.agent_registry import AgentRegistry
from app.core.exceptions import NotFoundError, ValidationError
from app.core.workflow_compiler import WorkflowCompiler
from app.repositories.agent_repository import AgentRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowResponse,
    WorkflowSummary,
    WorkflowUpdate,
)
from app.services.workflow_edges import sync_workflow_agent_edges


class WorkflowService:
    def __init__(
        self,
        workflow_repo: WorkflowRepository,
        agent_repo: AgentRepository,
        db: StandardDatabase,
        registry: AgentRegistry | None = None,
    ):
        self.workflow_repo = workflow_repo
        self.agent_repo = agent_repo
        self.db = db
        self.registry = registry or AgentRegistry.load_builtin_agents()
        self.compiler = WorkflowCompiler(self.registry)

    def _to_response(self, doc: dict) -> WorkflowResponse:
        return WorkflowResponse(
            id=doc["id"],
            user_id=doc["user_id"],
            slug=doc["slug"],
            name=doc["name"],
            description=doc.get("description", ""),
            version=doc.get("version", 1),
            is_template=doc.get("is_template", False),
            definition=doc["definition"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )

    def list_workflows(self, user_id: str) -> list[WorkflowSummary]:
        result = []
        for doc in self.workflow_repo.list_by_user(user_id):
            steps = (doc.get("definition") or {}).get("steps") or []
            result.append(
                WorkflowSummary(
                    id=doc["id"],
                    slug=doc["slug"],
                    name=doc["name"],
                    description=doc.get("description", ""),
                    is_template=doc.get("is_template", False),
                    step_count=len(steps),
                    updated_at=doc["updated_at"],
                )
            )
        return result

    def get_workflow(self, user_id: str, workflow_id: str) -> WorkflowResponse:
        doc = self.workflow_repo.get_by_key(workflow_id, user_id)
        if not doc:
            raise NotFoundError("Workflow not found")
        return self._to_response(doc)

    def create(self, user_id: str, body: WorkflowCreate) -> WorkflowResponse:
        if self.workflow_repo.get_by_slug(body.slug, user_id):
            raise ValidationError(f"Workflow slug '{body.slug}' already exists")
        definition = body.definition.model_dump()
        errors = self.compiler.validate(definition)
        if errors:
            raise ValidationError("Invalid workflow definition", details={"errors": errors})

        doc = self.workflow_repo.create(
            {
                "user_id": user_id,
                "slug": body.slug,
                "name": body.name,
                "description": body.description,
                "is_template": body.is_template,
                "definition": definition,
            }
        )
        sync_workflow_agent_edges(self.db, doc["_key"], definition.get("steps") or [])
        return self._to_response(doc)

    def update(self, user_id: str, workflow_id: str, body: WorkflowUpdate) -> WorkflowResponse:
        doc = self.workflow_repo.get_by_key(workflow_id, user_id)
        if not doc:
            raise NotFoundError("Workflow not found")

        patch: dict = {}
        if body.name is not None:
            patch["name"] = body.name
        if body.description is not None:
            patch["description"] = body.description
        if body.is_template is not None:
            patch["is_template"] = body.is_template
        if body.definition is not None:
            definition = body.definition.model_dump()
            errors = self.compiler.validate(definition)
            if errors:
                raise ValidationError("Invalid workflow definition", details={"errors": errors})
            patch["definition"] = definition

        updated = self.workflow_repo.update_doc(workflow_id, patch)
        if "definition" in patch:
            sync_workflow_agent_edges(self.db, workflow_id, patch["definition"].get("steps") or [])
        return self._to_response(updated)

    def delete(self, user_id: str, workflow_id: str) -> None:
        doc = self.workflow_repo.get_by_key(workflow_id, user_id)
        if not doc:
            raise NotFoundError("Workflow not found")
        self.workflow_repo.delete(workflow_id)
