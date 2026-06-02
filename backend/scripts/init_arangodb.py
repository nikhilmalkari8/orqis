#!/usr/bin/env python3
"""Initialize ArangoDB collections, indexes, and graph for Orqis MVP."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arango import ArangoClient

from app.config import get_settings

DOC_COLLECTIONS = ["users", "agents", "workflows", "executions"]
EDGE_COLLECTIONS = ["workflow_uses_agent", "execution_of_workflow"]


def main() -> None:
    settings = get_settings()
    client = ArangoClient(hosts=settings.arango_url)
    sys_db = client.db("_system", username=settings.arango_user, password=settings.arango_password)

    if not sys_db.has_database(settings.arango_db):
        sys_db.create_database(settings.arango_db)
        print(f"Created database: {settings.arango_db}")

    db = client.db(
        settings.arango_db,
        username=settings.arango_user,
        password=settings.arango_password,
    )

    for name in DOC_COLLECTIONS:
        if not db.has_collection(name):
            db.create_collection(name)
            print(f"Created collection: {name}")

    for name in EDGE_COLLECTIONS:
        if not db.has_collection(name):
            db.create_collection(name, edge=True)
            print(f"Created edge collection: {name}")

    if not db.has_graph("orqis_graph"):
        db.create_graph(
            "orqis_graph",
            edge_definitions=[
                {
                    "edge_collection": "workflow_uses_agent",
                    "from_vertex_collections": ["workflows"],
                    "to_vertex_collections": ["agents"],
                },
                {
                    "edge_collection": "execution_of_workflow",
                    "from_vertex_collections": ["executions"],
                    "to_vertex_collections": ["workflows"],
                },
            ],
        )
        print("Created graph: orqis_graph")

    _ensure_index(db, "users", ["email"], unique=True)
    _ensure_index(db, "agents", ["slug"], unique=True)
    _ensure_index(db, "workflows", ["user_id", "slug"], unique=True)
    _ensure_index(db, "workflows", ["user_id"])
    _ensure_index(db, "executions", ["workflow_id"])
    _ensure_index(db, "executions", ["user_id"])
    _ensure_index(db, "executions", ["status"])
    _ensure_index(db, "executions", ["created_at"])

    print("ArangoDB initialization complete.")


def _ensure_index(db, collection: str, fields: list[str], unique: bool = False) -> None:
    col = db.collection(collection)
    name = f"idx_{collection}_{'_'.join(fields)}"
    existing = {idx["name"] for idx in col.indexes()}
    if name in existing:
        return
    if unique:
        col.add_hash_index(fields=fields, unique=True, name=name)
    else:
        col.add_persistent_index(fields=fields, name=name)
    print(f"Created index {name} on {collection}")


if __name__ == "__main__":
    main()
