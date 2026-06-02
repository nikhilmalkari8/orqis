import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api/client";
import StatusBadge from "../components/StatusBadge";

export default function ExecutionDetailPage() {
  const { id } = useParams();
  const [ex, setEx] = useState(null);

  const load = () => api.get(`/executions/${id}`).then((r) => setEx(r.data));

  useEffect(() => {
    load();
    const t = setInterval(() => {
      if (ex?.status === "pending" || ex?.status === "running") load();
    }, 2000);
    return () => clearInterval(t);
  }, [id, ex?.status]);

  if (!ex) return <p>Loading…</p>;

  const traceUrl = ex.langsmith?.trace_url;

  return (
    <div>
      <h1>
        Execution <StatusBadge status={ex.status} />
      </h1>
      <p>
        Workflow: <Link to={`/workflows/${ex.workflow_id}`}>{ex.workflow_slug}</Link>
      </p>
      {ex.failed_step_id && (
        <p className="error">
          Failed at step <code>{ex.failed_step_id}</code>
          {ex.failed_agent_slug && (
            <>
              {" "}
              (agent <code>{ex.failed_agent_slug}</code>)
            </>
          )}
          {ex.error && <> — {ex.error}</>}
        </p>
      )}
      {traceUrl && (
        <p>
          <a href={traceUrl} target="_blank" rel="noreferrer" className="btn">
            Open in LangSmith
          </a>
        </p>
      )}

      <h2>Steps</h2>
      <table>
        <thead>
          <tr>
            <th>Step</th>
            <th>Agent</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>
          {(ex.step_summaries || []).map((s) => (
            <tr key={s.step_id}>
              <td>
                <code>{s.step_id}</code>
              </td>
              <td>
                <Link to={`/agents/${s.agent}`}>{s.agent}</Link>
              </td>
              <td>
                <StatusBadge status={s.status} />
              </td>
              <td>{s.duration_ms != null ? `${s.duration_ms}ms` : "—"}</td>
              <td>{s.error || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Input</h2>
      <pre className="json">{JSON.stringify(ex.input_data, null, 2)}</pre>
      <h2>Output</h2>
      <pre className="json">{JSON.stringify(ex.output_data, null, 2)}</pre>
    </div>
  );
}
