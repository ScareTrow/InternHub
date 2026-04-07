import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import EmptyState from "../components/EmptyState";

export default function MyApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadApplications();
  }, []);

  async function loadApplications() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/applications/me");
      setApplications(response.data);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load applications."));
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="panel muted">Loading applications...</div>;
  }

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <span className="eyebrow">My applications</span>
          <h1>Track every application in one place.</h1>
          <p>Review where you applied, current status, and vacancy details.</p>
        </div>
      </div>

      {error ? <div className="notice notice-error">{error}</div> : null}

      {applications.length === 0 ? (
        <EmptyState
          title="No applications submitted"
          description="Start from the vacancy list and apply to roles that match your skills."
          action={
            <Link className="button" to="/">
              Browse vacancies
            </Link>
          }
        />
      ) : (
        <div className="list-stack">
          {applications.map((application) => (
            <article className="panel application-row" key={application.id}>
              <div>
                <h3>{application.vacancy.title}</h3>
                <p>
                  {application.vacancy.employer_name} • {application.vacancy.location}
                </p>
              </div>
              <div className="application-row-side">
                <span className="badge">{application.status}</span>
                <Link className="button button-secondary" to={`/vacancies/${application.vacancy.id}`}>
                  View vacancy
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
