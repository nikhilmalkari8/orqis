from arango.database import StandardDatabase

from app.repositories.base import BaseRepository


class AgentRepository(BaseRepository):
    collection = "agents"

    def get_by_slug(self, slug: str) -> dict | None:
        cursor = self.db.aql.execute(
            "FOR a IN agents FILTER a.slug == @slug LIMIT 1 RETURN a",
            bind_vars={"slug": slug},
        )
        docs = list(cursor)
        if not docs:
            return None
        doc = docs[0]
        doc["id"] = doc["_key"]
        return doc

    def list_active(self) -> list[dict]:
        cursor = self.db.aql.execute(
            "FOR a IN agents FILTER a.status == 'active' SORT a.name RETURN a"
        )
        result = []
        for doc in cursor:
            doc["id"] = doc["_key"]
            result.append(doc)
        return result

    def upsert_by_slug(self, doc: dict) -> dict:
        existing = self.get_by_slug(doc["slug"])
        now = self.now_iso()
        if existing:
            doc["_key"] = existing["_key"]
            doc["updated_at"] = now
            self.col.update(doc)
            return self.get(existing["_key"])  # type: ignore
        doc["created_at"] = now
        doc["updated_at"] = now
        return self.insert(doc)
