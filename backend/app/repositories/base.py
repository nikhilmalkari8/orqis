import uuid
from datetime import datetime, timezone

from arango.database import StandardDatabase


class BaseRepository:
    collection: str

    def __init__(self, db: StandardDatabase):
        self.db = db
        self.col = db.collection(self.collection)

    @staticmethod
    def new_key() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def get(self, key: str) -> dict | None:
        doc = self.col.get(key)
        if doc is None:
            return None
        doc["id"] = doc["_key"]
        return doc

    def insert(self, doc: dict) -> dict:
        if "_key" not in doc:
            doc["_key"] = self.new_key()
        meta = self.col.insert(doc)
        doc["_key"] = meta["_key"]
        doc["id"] = meta["_key"]
        return doc

    def update(self, key: str, patch: dict) -> dict:
        patch["updated_at"] = self.now_iso()
        self.col.update({"_key": key, **patch}, merge=True)
        return self.get(key)  # type: ignore

    def delete(self, key: str) -> None:
        self.col.delete(key)
