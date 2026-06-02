from arango.database import StandardDatabase

from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    collection = "users"

    def get_by_email(self, email: str) -> dict | None:
        cursor = self.db.aql.execute(
            "FOR u IN users FILTER u.email == @email LIMIT 1 RETURN u",
            bind_vars={"email": email.lower()},
        )
        docs = list(cursor)
        if not docs:
            return None
        doc = docs[0]
        doc["id"] = doc["_key"]
        return doc

    def create(self, email: str, password_hash: str, display_name: str | None = None) -> dict:
        now = self.now_iso()
        return self.insert(
            {
                "email": email.lower(),
                "password_hash": password_hash,
                "display_name": display_name,
                "created_at": now,
                "updated_at": now,
                "is_active": True,
            }
        )
