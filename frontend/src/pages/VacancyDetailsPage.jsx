import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import { useAuth } from "../context/AuthContext";

function formatSalary(min, max) {
  if (!min && !max) {
    return "Salary not specified";
  }
  if (min && max) {
    return `${min.toLocaleString()} - ${max.toLocaleString()} KZT`;
  }
  return `${(min || max).toLocaleString()} KZT`;
}

export default function VacancyDetailsPage() {
  const navigate = useNavigate();
  const { vacancyId } = useParams();
  const { user } = useAuth();
  const [vacancy, setVacancy] = useState(null);
  const [coverLetter, setCoverLetter] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    loadVacancy();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [vacancyId]);

  async function loadVacancy() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get(`/vacancies/${vacancyId}`);
      setVacancy(response.data);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load vacancy."));
    } finally {
      setLoading(false);
    }
  }

  async function handleApply(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setSuccess("");

    try {
      await api.post(`/vacancies/${vacancyId}/apply`, {
        cover_letter: coverLetter || null,
      });
      setSuccess("Application submitted.");
      setCoverLetter("");
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not submit application."));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete() {
    if (!window.confirm("Delete this vacancy?")) {
      return;
    }

    try {
      await api.delete(`/vacancies/${vacancyId}`);
      navigate("/dashboard/employer", { replace: true });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not delete vacancy."));
    }
  }

  if (loading) {
    return <div className="panel muted">Loading vacancy...</div>;
  }

  if (!vacancy) {
    return <div className="panel muted">Vacancy not found.</div>;
  }

  const isOwner = user?.role === "employer" && user?.id === vacancy.employer_id;

  return (
    <section className="page-stack">
      <div className="detail-hero panel">
        <div className="detail-hero-copy">
          <span className="eyebrow">{vacancy.employment_type}</span>
          <h1>{vacancy.title}</h1>
          <p>
            {vacancy.employer.company_name} • {vacancy.location} • {vacancy.category}
          </p>
        </div>
        <div className="detail-hero-meta">
          <strong>{formatSalary(vacancy.salary_min, vacancy.salary_max)}</strong>
          <span>{vacancy.applications_count} applications</span>
          {isOwner ? (
            <div className="inline-actions">
              <Link className="button" to={`/vacancies/${vacancy.id}/edit`}>
                Edit
              </Link>
              <button className="button button-danger" onClick={handleDelete} type="button">
                Delete
              </button>
            </div>
          ) : null}
        </div>
      </div>

      {error ? <div className="notice notice-error">{error}</div> : null}
      {success ? <div className="notice notice-success">{success}</div> : null}

      <div className="detail-grid">
        <article className="panel prose-panel">
          <h2>About this role</h2>
          <p>{vacancy.description}</p>

          <h3>Requirements</h3>
          <p>{vacancy.requirements || "Requirements were not specified."}</p>
        </article>

        <aside className="panel sidebar-panel">
          <h2>Company</h2>
          <p>{vacancy.employer.company_name}</p>
          <p>{vacancy.employer.location || "Location not specified"}</p>

          {user?.role === "student" ? (
            <form className="apply-form" onSubmit={handleApply}>
              <label htmlFor="cover_letter">Cover letter</label>
              <textarea
                id="cover_letter"
                onChange={(event) => setCoverLetter(event.target.value)}
                placeholder="Optional short motivation"
                rows="6"
                value={coverLetter}
              />
              <button className="button" disabled={submitting} type="submit">
                {submitting ? "Submitting..." : "Apply now"}
              </button>
            </form>
          ) : (
            <div className="muted-block">
              {user?.role === "employer"
                ? "Employers can review this vacancy and manage their own posts."
                : "Log in as a student to apply."}
            </div>
          )}
        </aside>
      </div>
    </section>
  );
}
