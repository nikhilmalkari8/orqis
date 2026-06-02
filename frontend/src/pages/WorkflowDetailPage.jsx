import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/client";

export default function WorkflowDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [workflow, setWorkflow] = useState(null);
  const [urls, setUrls] = useState("https://example.com/pricing");
  const [targetUrl, setTargetUrl] = useState("https://example.com");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/workflows/${id}`).then((r) => setWorkflow(r.data));
  }, [id]);

  const run = async () => {
    setRunning(true);
    setError("");
    try {
      let input_data = {};
      if (workflow?.slug === "qa-smoke") {
        input_data = { target_url: targetUrl, scenario: "Load homepage and verify title" };
      } else {
        input_data = {
          urls: urls.split(",").map((u) => u.trim()),
          email: "team@example.com",
        };
      }
      const { data } = await api.post(`/workflows/${id}/run`, { input_data });
      navigate(`/executions/${data.execution_id}`);
    } catch (e) {
      setError(e.response?.data?.error?.message || "Run failed");
    } finally {
      setRunning(false);
    }
  };

  if (!workflow) return <p>Loading…</p>;

  return (
    <div>
      <h1>{workflow.name}</h1>
      <p>
        <code>{workflow.slug}</code> · {workflow.definition?.steps?.length || 0} steps
      </p>
      <p>{workflow.description}</p>

      <div className="card">
        <h3>Run workflow</h3>
        {workflow.slug === "qa-smoke" ? (
          <>
            <label>Target URL</label>
            <input value={targetUrl} onChange={(e) => setTargetUrl(e.target.value)} />
          </>
        ) : (
          <>
            <label>URLs (comma-separated)</label>
            <input value={urls} onChange={(e) => setUrls(e.target.value)} />
          </>
        )}
        {error && <p className="error">{error}</p>}
        <button type="button" onClick={run} disabled={running}>
          {running ? "Starting…" : "Run now"}
        </button>
      </div>

      <h2>Definition</h2>
      <pre className="json">{JSON.stringify(workflow.definition, null, 2)}</pre>
    </div>
  );
}
