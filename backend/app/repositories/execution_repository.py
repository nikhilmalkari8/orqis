from arango.database import StandardDatabase

from app.repositories.base import BaseRepository


class ExecutionRepository(BaseRepository):
    collection = "executions"

    def create(self, doc: dict) -> dict:
        now = self.now_iso()
        doc.setdefault("status", "pending")
        doc.setdefault("step_summaries", [])
        doc.setdefault("output_data", {})
        doc.setdefault("langsmith", {})
        doc["created_at"] = now
        doc["updated_at"] = now
        return self.insert(doc)

    def get_by_key(self, key: str, user_id: str | None = None) -> dict | None:
        doc = self.get(key)
        if doc is None:
            return None
        if user_id and doc.get("user_id") != user_id:
            return None
        return doc

    def list_by_user(
        self,
        user_id: str,
        *,
        workflow_id: str | None = None,
        agent_slug: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        filters = ["ex.user_id == @user_id"]
        bind: dict = {"user_id": user_id, "limit": min(limit, 100)}

        if workflow_id:
            filters.append("ex.workflow_id == @workflow_id")
            bind["workflow_id"] = workflow_id
        if status:
            filters.append("ex.status == @status")
            bind["status"] = status
        if agent_slug:
            filters.append("ex.step_summaries[*].agent ANY == @agent_slug")
            bind["agent_slug"] = agent_slug

        filter_expr = " AND ".join(filters)
        query = f"""
            FOR ex IN executions
              FILTER {filter_expr}
              SORT ex.created_at DESC
              LIMIT @limit
              RETURN ex
        """
        cursor = self.db.aql.execute(query, bind_vars=bind)
        return [_with_id(d) for d in cursor]

    def create_execution_edge(self, execution_key: str, workflow_key: str) -> None:
        edge_col = self.db.collection("execution_of_workflow")
        edge_col.insert(
            {"_from": f"executions/{execution_key}", "_to": f"workflows/{workflow_key}"},
            overwrite=True,
        )


def _with_id(doc: dict) -> dict:
    doc["id"] = doc["_key"]
    return doc
