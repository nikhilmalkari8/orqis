from arango.database import StandardDatabase

from app.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository):
    collection = "workflows"

    def list_by_user(self, user_id: str) -> list[dict]:
        cursor = self.db.aql.execute(
            """
            FOR w IN workflows
              FILTER w.user_id == @user_id
              SORT w.updated_at DESC
              RETURN w
            """,
            bind_vars={"user_id": user_id},
        )
        return [_with_id(d) for d in cursor]

    def get_by_key(self, key: str, user_id: str | None = None) -> dict | None:
        doc = self.get(key)
        if doc is None:
            return None
        if user_id and doc.get("user_id") != user_id:
            return None
        return doc

    def get_by_slug(self, slug: str, user_id: str) -> dict | None:
        cursor = self.db.aql.execute(
            """
            FOR w IN workflows
              FILTER w.user_id == @user_id AND w.slug == @slug
              LIMIT 1
              RETURN w
            """,
            bind_vars={"user_id": user_id, "slug": slug},
        )
        docs = list(cursor)
        if not docs:
            return None
        return _with_id(docs[0])

    def create(self, doc: dict) -> dict:
        now = self.now_iso()
        doc.setdefault("version", 1)
        doc.setdefault("status", "active")
        doc["created_at"] = now
        doc["updated_at"] = now
        return self.insert(doc)

    def update_doc(self, key: str, patch: dict) -> dict:
        return self.update(key, patch)


def _with_id(doc: dict) -> dict:
    doc["id"] = doc["_key"]
    return doc
