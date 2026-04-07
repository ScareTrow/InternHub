export default function EmptyState({ title, description, action = null }) {
  return (
    <div className="panel empty-state">
      <h3>{title}</h3>
      <p>{description}</p>
      {action}
    </div>
  );
}
