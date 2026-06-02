import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api/client";
import StatusBadge from "../components/StatusBadge";

export default function AgentDetailPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get(`/agents/${slug}`)
      .then((r) => setData(r.data))
      .catch((e) => setError(e.response?.data?.error?.message || "Not found"));
  }, [slug]);

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p>Loading…</p>;

  const { agent, workflows_using, stats, recent_executions } = data;

  return (
    <div>
      <h1>{agent.name}</h1>
      <p>
        <code>{agent.slug}</code> · v{agent.version} · {agent.implementation.framework}
      </p>
      <p>{agent.description}</p>

      <div className="card">
        <h3>Stats (30 days)</h3>
        <p>
          Runs: {stats.total_runs} · Success rate: {(stats.success_rate * 100).toFixed(0)}% · Last:{" "}
          {stats.last_status || "—"}
        </p>
      </div>

      <h2>Used in workflows</h2>
      {workflows_using.length === 0 ? (
        <p>Not used in any workflow yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Step</th>
              <th>Order</th>
            </tr>
          </thead>
          <tbody>
            {workflows_using.map((w) => (
              <tr key={`${w.workflow_id}-${w.step_id}`}>
                <td>
                  <Link to={`/workflows/${w.workflow_id}`}>{w.name}</Link>
                </td>
                <td>
                  <code>{w.step_id}</code>
                </td>
                <td>{w.step_order}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h2>Recent executions</h2>
      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Status</th>
            <th>Trace</th>
          </tr>
        </thead>
        <tbody>
          {recent_executions.map((ex) => (
            <tr key={ex.execution_id}>
              <td>
                <Link to={`/executions/${ex.execution_id}`}>{ex.workflow_slug}</Link>
              </td>
              <td>
                <StatusBadge status={ex.status} />
              </td>
              <td>
                {ex.langsmith_trace_url ? (
                  <a href={ex.langsmith_trace_url} target="_blank" rel="noreferrer">
                    LangSmith
                  </a>
                ) : (
                  "—"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Schemas</h2>
      <h3>Input</h3>
      <pre className="json">{JSON.stringify(agent.input_schema, null, 2)}</pre>
      <h3>Output</h3>
      <pre className="json">{JSON.stringify(agent.output_schema, null, 2)}</pre>
      <h3>Config</h3>
      <pre className="json">{JSON.stringify(agent.config_schema, null, 2)}</pre>
    </div>
  );
}
