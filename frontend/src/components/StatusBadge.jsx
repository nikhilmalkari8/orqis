export default function StatusBadge({ status }) {
  const cls = `badge badge-${status || "pending"}`;
  return <span className={cls}>{status}</span>;
}
