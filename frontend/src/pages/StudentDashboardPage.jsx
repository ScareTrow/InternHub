import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import EmptyState from "../components/EmptyState";
import VacancyPreview from "../components/VacancyPreview";
import { useAuth } from "../context/AuthContext";

export default function StudentDashboardPage() {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    setLoading(true);
    setError("");
    try {
      const [applicationsResponse, vacanciesResponse] = await Promise.all([
        api.get("/applications/me"),
        api.get("/vacancies", { params: { page_size: 4 } }),
      ]);
      setApplications(applicationsResponse.data);
      setVacancies(vacanciesResponse.data.items);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load dashboard."));
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
          <span className="eyebrow">Student dashboard</span>
          <h1>{user?.student_profile?.full_name || user?.email}</h1>
          <p>
            {user?.student_profile?.university}
            {user?.student_profile?.major ? ` • ${user.student_profile.major}` : ""}
          </p>
        </div>
        <Link className="button" to="/applications/my">
          View all applications
        </Link>
      </div>

      {error ? <div className="notice notice-error">{error}</div> : null}

      <div className="metrics-grid">
        <div className="panel metric">
          <span>Applications</span>
          <strong>{applications.length}</strong>
        </div>
        <div className="panel metric">
          <span>Graduation year</span>
          <strong>{user?.student_profile?.graduation_year || "N/A"}</strong>
        </div>
        <div className="panel metric">
          <span>Location</span>
          <strong>{user?.student_profile?.location || "Flexible"}</strong>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="section-heading">
            <h2>Recent applications</h2>
          </div>
          {applications.length === 0 ? (
            <EmptyState
              title="No applications yet"
              description="Browse open roles and submit your first application."
            />
          ) : (
            <div className="compact-list">
              {applications.slice(0, 5).map((application) => (
                <div className="compact-row" key={application.id}>
                  <div>
                    <strong>{application.vacancy.title}</strong>
                    <p>
                      {application.vacancy.employer_name} • {application.vacancy.location}
                    </p>
                  </div>
                  <span className="badge">{application.status}</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Suggested vacancies</h2>
            <Link to="/">See all</Link>
          </div>
          <div className="list-stack">
            {vacancies.slice(0, 3).map((vacancy) => (
              <VacancyPreview key={vacancy.id} vacancy={vacancy} />
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}
