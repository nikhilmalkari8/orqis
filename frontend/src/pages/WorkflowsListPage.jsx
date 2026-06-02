import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function WorkflowsListPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/workflows").then((r) => setItems(r.data || []));
  }, []);

  return (
    <div>
      <h1>Workflows</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Slug</th>
            <th>Steps</th>
            <th>Template</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          {items.map((w) => (
            <tr key={w.id}>
              <td>
                <Link to={`/workflows/${w.id}`}>{w.name}</Link>
              </td>
              <td>
                <code>{w.slug}</code>
              </td>
              <td>{w.step_count}</td>
              <td>{w.is_template ? "Yes" : "No"}</td>
              <td>{w.updated_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
