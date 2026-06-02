import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="layout">
      <nav className="nav">
        <Link to="/" className="brand">
          Orqis
        </Link>
        <Link to="/agents">Agents</Link>
        <Link to="/workflows">Workflows</Link>
        <Link to="/executions">Executions</Link>
        {user && (
          <>
            <span style={{ color: "#64748b", fontSize: "0.875rem" }}>{user.email}</span>
            <button type="button" className="secondary" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </nav>
      {children}
    </div>
  );
}
