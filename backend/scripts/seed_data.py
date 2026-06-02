#!/usr/bin/env python3
"""Seed agents, dev user, and template workflows."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import get_settings
from app.core.security import hash_password
from app.db.arango import get_db
from app.repositories.agent_repository import AgentRepository
from app.repositories.user_repository import UserRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.seed.agents import AGENT_SEED_DATA, WORKFLOW_SEED_TEMPLATES
from app.services.workflow_edges import sync_workflow_agent_edges
from scripts.init_arangodb import main as init_db


def main() -> None:
    init_db()
    settings = get_settings()
    db = get_db()
    agent_repo = AgentRepository(db)
    user_repo = UserRepository(db)
    workflow_repo = WorkflowRepository(db)

    for agent in AGENT_SEED_DATA:
        agent_repo.upsert_by_slug(agent)
        print(f"Seeded agent: {agent['slug']}")

    user_id = None
    if settings.seed_dev_user:
        existing = user_repo.get_by_email(settings.dev_user_email)
        if existing:
            user_id = existing["_key"]
            print(f"Dev user exists: {settings.dev_user_email}")
        else:
            user = user_repo.create(
                settings.dev_user_email,
                hash_password(settings.dev_user_password),
                display_name="Dev User",
            )
            user_id = user["_key"]
            print(f"Created dev user: {settings.dev_user_email} / {settings.dev_user_password}")

    if user_id:
        for wf in WORKFLOW_SEED_TEMPLATES:
            existing = workflow_repo.get_by_slug(wf["slug"], user_id)
            if existing:
                print(f"Workflow exists: {wf['slug']}")
                continue
            doc = workflow_repo.create(
                {
                    "user_id": user_id,
                    "slug": wf["slug"],
                    "name": wf["name"],
                    "description": wf["description"],
                    "is_template": wf["is_template"],
                    "definition": wf["definition"],
                }
            )
            sync_workflow_agent_edges(db, doc["_key"], wf["definition"]["steps"])
            print(f"Seeded workflow: {wf['slug']}")

    print("Seed complete.")


if __name__ == "__main__":
    main()
