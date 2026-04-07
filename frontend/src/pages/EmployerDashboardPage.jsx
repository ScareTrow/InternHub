import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import EmptyState from "../components/EmptyState";
import VacancyPreview from "../components/VacancyPreview";
import { useAuth } from "../context/AuthContext";

export default function EmployerDashboardPage() {
  const { user } = useAuth();
  const [vacancies, setVacancies] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    setLoading(true);
    setError("");
    try {
      const [vacanciesResponse, applicationsResponse] = await Promise.all([
        api.get("/vacancies/me/list"),
        api.get("/applications/employer"),
      ]);
      setVacancies(vacanciesResponse.data);
      setApplications(applicationsResponse.data);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load employer dashboard."));
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="panel muted">Loading dashboard...</div>;
  }

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <span className="eyebrow">Employer dashboard</span>
          <h1>{user?.employer_profile?.company_name || user?.email}</h1>
          <p>{user?.employer_profile?.company_description || "Manage open hiring activity."}</p>
        </div>
        <Link className="button" to="/vacancies/new">
          Create vacancy
        </Link>
      </div>

      {error ? <div className="notice notice-error">{error}</div> : null}

      <div className="metrics-grid">
        <div className="panel metric">
          <span>Published vacancies</span>
          <strong>{vacancies.length}</strong>
        </div>
        <div className="panel metric">
          <span>Total applications</span>
          <strong>{applications.length}</strong>
        </div>
        <div className="panel metric">
          <span>HQ</span>
          <strong>{user?.employer_profile?.location || "Remote"}</strong>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="section-heading">
            <h2>Your vacancies</h2>
          </div>
          {vacancies.length === 0 ? (
            <EmptyState
              title="No vacancies yet"
              description="Create the first role to start collecting student applications."
              action={
                <Link className="button" to="/vacancies/new">
                  Create vacancy
                </Link>
              }
            />
          ) : (
            <div className="list-stack">
              {vacancies.map((vacancy) => (
                <VacancyPreview
                  key={vacancy.id}
                  actionSlot={
                    <Link className="button" to={`/vacancies/${vacancy.id}/edit`}>
                      Edit
                    </Link>
                  }
                  vacancy={vacancy}
                />
              ))}
            </div>
          )}
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Recent applicants</h2>
          </div>
          {applications.length === 0 ? (
            <EmptyState
              title="No applications yet"
              description="Applications will appear here as soon as students start applying."
            />
          ) : (
            <div className="compact-list">
              {applications.slice(0, 8).map((application) => (
                <div className="compact-row" key={application.id}>
                  <div>
                    <strong>{application.student.full_name}</strong>
                    <p>
                      {application.vacancy.title} • {application.student.university}
                    </p>
                  </div>
                  <span className="badge">{application.status}</span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </section>
  );
}
