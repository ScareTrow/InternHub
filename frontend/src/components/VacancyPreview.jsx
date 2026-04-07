import { Link } from "react-router-dom";

function formatSalary(min, max) {
  if (!min && !max) {
    return "Salary not specified";
  }
  if (min && max) {
    return `${min.toLocaleString()} - ${max.toLocaleString()} KZT`;
  }
  return `${(min || max).toLocaleString()} KZT`;
}

export default function VacancyPreview({ vacancy, actionSlot = null }) {
  return (
    <article className="vacancy-row panel">
      <div className="vacancy-row-main">
        <div className="vacancy-row-meta">
          <span className="badge">{vacancy.employment_type}</span>
          <span>{vacancy.category}</span>
          <span>{vacancy.location}</span>
        </div>

        <div className="vacancy-row-heading">
          <div>
            <h3>{vacancy.title}</h3>
            <p>
              {vacancy.employer.company_name}
              {vacancy.employer.location ? ` • ${vacancy.employer.location}` : ""}
            </p>
          </div>
          <strong>{formatSalary(vacancy.salary_min, vacancy.salary_max)}</strong>
        </div>

        <p className="vacancy-row-description">{vacancy.description}</p>
      </div>

      <div className="vacancy-row-actions">
        {actionSlot}
        <Link className="button button-secondary" to={`/vacancies/${vacancy.id}`}>
          Open
        </Link>
      </div>
    </article>
  );
}
