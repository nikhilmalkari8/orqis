import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function AgentsListPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/agents").then((r) => setItems(r.data.items || []));
  }, []);

  return (
    <div>
      <h1>Agents</h1>
      <p>First-party agents registered on Orqis. Reuse them across workflows.</p>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Slug</th>
            <th>Framework</th>
            <th>Category</th>
            <th>Version</th>
          </tr>
        </thead>
        <tbody>
          {items.map((a) => (
            <tr key={a.slug}>
              <td>
                <Link to={`/agents/${a.slug}`}>{a.name}</Link>
              </td>
              <td>
                <code>{a.slug}</code>
              </td>
              <td>{a.framework}</td>
              <td>{a.category}</td>
              <td>{a.version}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
