from arango.database import StandardDatabase

from app.repositories.agent_repository import AgentRepository


def sync_workflow_agent_edges(db: StandardDatabase, workflow_key: str, steps: list[dict]) -> None:
    """Replace workflow_uses_agent edges for a workflow."""
    edge_col = db.collection("workflow_uses_agent")
    workflow_ref = f"workflows/{workflow_key}"

    cursor = db.aql.execute(
        """
        FOR e IN workflow_uses_agent
          FILTER e._from == @from
          REMOVE e IN workflow_uses_agent
        """,
        bind_vars={"from": workflow_ref},
    )
    list(cursor)  # consume

    agent_repo = AgentRepository(db)
    for order, step in enumerate(steps):
        slug = step.get("agent")
        if not slug:
            continue
        agent = agent_repo.get_by_slug(slug)
        if not agent:
            continue
        edge_col.insert(
            {
                "_from": workflow_ref,
                "_to": f"agents/{agent['_key']}",
                "step_id": step.get("id"),
                "step_order": order,
                "agent_slug": slug,
                "config_snapshot": step.get("config") or {},
            }
        )
