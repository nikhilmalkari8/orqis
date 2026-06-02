import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import AgentsListPage from "./pages/AgentsListPage";
import AgentDetailPage from "./pages/AgentDetailPage";
import WorkflowsListPage from "./pages/WorkflowsListPage";
import WorkflowDetailPage from "./pages/WorkflowDetailPage";
import ExecutionsListPage from "./pages/ExecutionsListPage";
import ExecutionDetailPage from "./pages/ExecutionDetailPage";

function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/agents"
            element={
              <PrivateRoute>
                <AgentsListPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/agents/:slug"
            element={
              <PrivateRoute>
                <AgentDetailPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/workflows"
            element={
              <PrivateRoute>
                <WorkflowsListPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/workflows/:id"
            element={
              <PrivateRoute>
                <WorkflowDetailPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/executions"
            element={
              <PrivateRoute>
                <ExecutionsListPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/executions/:id"
            element={
              <PrivateRoute>
                <ExecutionDetailPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
