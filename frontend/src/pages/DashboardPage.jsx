import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import StatusBadge from "../components/StatusBadge";

export default function DashboardPage() {
  const [agents, setAgents] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [executions, setExecutions] = useState([]);

  useEffect(() => {
    Promise.all([
      api.get("/agents"),
      api.get("/workflows"),
      api.get("/executions", { params: { limit: 5 } }),
    ]).then(([a, w, e]) => {
      setAgents(a.data.items || []);
      setWorkflows(w.data || []);
      setExecutions(e.data || []);
    });
  }, []);

  const failures = executions.filter((x) => x.status === "failed").length;

  return (
    <div>
      <h1>Dashboard</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
        <div className="card">
          <h3>Agents</h3>
          <p style={{ fontSize: "2rem", margin: 0 }}>{agents.length}</p>
          <Link to="/agents">View agents →</Link>
        </div>
        <div className="card">
          <h3>Workflows</h3>
          <p style={{ fontSize: "2rem", margin: 0 }}>{workflows.length}</p>
          <Link to="/workflows">View workflows →</Link>
        </div>
        <div className="card">
          <h3>Recent failures</h3>
          <p style={{ fontSize: "2rem", margin: 0 }}>{failures}</p>
          <Link to="/executions">View runs →</Link>
        </div>
      </div>
      <h2>Recent executions</h2>
      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Status</th>
            <th>Started</th>
          </tr>
        </thead>
        <tbody>
          {executions.map((ex) => (
            <tr key={ex.id}>
              <td>
                <Link to={`/executions/${ex.id}`}>{ex.workflow_slug}</Link>
              </td>
              <td>
                <StatusBadge status={ex.status} />
              </td>
              <td>{ex.started_at || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
