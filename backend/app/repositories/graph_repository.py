from arango.database import StandardDatabase


class GraphRepository:
    def __init__(self, db: StandardDatabase):
        self.db = db

    def workflows_using_agent(self, agent_slug: str) -> list[dict]:
        cursor = self.db.aql.execute(
            """
            FOR agent IN agents
              FILTER agent.slug == @agent_slug
              FOR v, e IN 1..1 INBOUND agent workflow_uses_agent
                RETURN {
                  workflow_id: v._key,
                  slug: v.slug,
                  name: v.name,
                  step_id: e.step_id,
                  step_order: e.step_order
                }
            """,
            bind_vars={"agent_slug": agent_slug},
        )
        return list(cursor)

    def agent_stats(self, agent_slug: str, since_iso: str) -> dict:
        cursor = self.db.aql.execute(
            """
            LET runs = (
              FOR ex IN executions
                FILTER ex.step_summaries[*].agent ANY == @agent_slug
                FILTER ex.created_at >= @since
                RETURN ex
            )
            LET total = LENGTH(runs)
            LET completed = LENGTH(FOR r IN runs FILTER r.status == 'completed' RETURN 1)
            LET failed = LENGTH(FOR r IN runs FILTER r.status == 'failed' RETURN 1)
            LET last = FIRST(
              FOR r IN runs
                SORT r.created_at DESC
                LIMIT 1
                RETURN r
            )
            RETURN {
              total_runs: total,
              completed: completed,
              failed: failed,
              success_rate: total > 0 ? completed / total : 0,
              last_run_at: last != null ? last.started_at : null,
              last_status: last != null ? last.status : null
            }
            """,
            bind_vars={"agent_slug": agent_slug, "since": since_iso},
        )
        results = list(cursor)
        if results:
            return results[0]
        return {
            "total_runs": 0,
            "completed": 0,
            "failed": 0,
            "success_rate": 0.0,
            "last_run_at": None,
            "last_status": None,
        }
