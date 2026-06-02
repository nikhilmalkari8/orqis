from arango import ArangoClient
from arango.database import StandardDatabase

from app.config import Settings, get_settings

_client: ArangoClient | None = None
_db: StandardDatabase | None = None


def get_arango_client(settings: Settings | None = None) -> ArangoClient:
    global _client
    settings = settings or get_settings()
    if _client is None:
        _client = ArangoClient(hosts=settings.arango_url)
    return _client


def get_db(settings: Settings | None = None) -> StandardDatabase:
    global _db
    settings = settings or get_settings()
    if _db is None:
        client = get_arango_client(settings)
        sys_db = client.db("_system", username=settings.arango_user, password=settings.arango_password)
        if not sys_db.has_database(settings.arango_db):
            sys_db.create_database(settings.arango_db)
        _db = client.db(
            settings.arango_db,
            username=settings.arango_user,
            password=settings.arango_password,
        )
    return _db


def close_db() -> None:
    global _client, _db
    _client = None
    _db = None
