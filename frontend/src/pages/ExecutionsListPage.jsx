import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import StatusBadge from "../components/StatusBadge";

export default function ExecutionsListPage() {
  const [items, setItems] = useState([]);
  const [agent, setAgent] = useState("");

  const load = () => {
    const params = { limit: 50 };
    if (agent) params.agent = agent;
    api.get("/executions", { params }).then((r) => setItems(r.data || []));
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <h1>Executions</h1>
      <div style={{ marginBottom: "1rem" }}>
        <label>Filter by agent slug </label>
        <input
          style={{ display: "inline-block", width: "200px", margin: 0 }}
          value={agent}
          onChange={(e) => setAgent(e.target.value)}
          placeholder="browser-agent"
        />
        <button type="button" onClick={load} style={{ marginLeft: "0.5rem" }}>
          Apply
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Status</th>
            <th>Failed step</th>
            <th>Duration</th>
            <th>Trace</th>
          </tr>
        </thead>
        <tbody>
          {items.map((ex) => (
            <tr key={ex.id}>
              <td>
                <Link to={`/executions/${ex.id}`}>{ex.workflow_slug}</Link>
              </td>
              <td>
                <StatusBadge status={ex.status} />
              </td>
              <td>{ex.failed_step_id || "—"}</td>
              <td>{ex.duration_ms != null ? `${ex.duration_ms}ms` : "—"}</td>
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
    </div>
  );
}
