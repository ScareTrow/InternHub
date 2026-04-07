import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import EmptyState from "../components/EmptyState";
import VacancyFilters from "../components/VacancyFilters";
import VacancyPreview from "../components/VacancyPreview";
import { useAuth } from "../context/AuthContext";

const defaultFilters = {
  title: "",
  category: "",
  location: "",
  employment_type: "",
};

function cleanParams(filters, page) {
  return Object.fromEntries(
    Object.entries({
      ...filters,
      page,
      page_size: 6,
    }).filter(([, value]) => value !== "" && value !== null && value !== undefined),
  );
}

export default function VacancyListPage() {
  const { user } = useAuth();
  const [formFilters, setFormFilters] = useState(defaultFilters);
  const [appliedFilters, setAppliedFilters] = useState(defaultFilters);
  const [vacancies, setVacancies] = useState([]);
  const [meta, setMeta] = useState({ page: 1, pages: 1, total: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadVacancies(appliedFilters, meta.page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [appliedFilters, meta.page]);

  async function loadVacancies(filters, page) {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/vacancies", {
        params: cleanParams(filters, page),
      });
      setVacancies(response.data.items);
      setMeta(response.data.meta);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load vacancies."));
    } finally {
      setLoading(false);
    }
  }

  function handleFilterChange(event) {
    const { name, value } = event.target;
    setFormFilters((current) => ({ ...current, [name]: value }));
  }

  function handleFilterSubmit(event) {
    event.preventDefault();
    setAppliedFilters(formFilters);
    setMeta((current) => ({ ...current, page: 1 }));
  }

  function handleReset() {
    setFormFilters(defaultFilters);
    setAppliedFilters(defaultFilters);
    setMeta((current) => ({ ...current, page: 1 }));
  }

  function changePage(nextPage) {
    setMeta((current) => ({ ...current, page: nextPage }));
  }

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <span className="eyebrow">Open roles</span>
          <h1>Find internships and early-career jobs built for students.</h1>
          <p>
            Search by title, category, location, or role type. Employers can switch to
            dashboard mode and publish openings directly.
          </p>
        </div>
        {user?.role === "employer" ? (
          <Link className="button" to="/vacancies/new">
            Create vacancy
          </Link>
        ) : null}
      </div>

      <VacancyFilters
        filters={formFilters}
        onChange={handleFilterChange}
        onReset={handleReset}
        onSubmit={handleFilterSubmit}
      />

      {error ? <div className="notice notice-error">{error}</div> : null}

      {loading ? (
        <div className="panel muted">Loading vacancies...</div>
      ) : vacancies.length === 0 ? (
        <EmptyState
          title="No vacancies found"
          description="Try changing your filters or clear them to see more results."
        />
      ) : (
        <>
          <div className="list-stack">
            {vacancies.map((vacancy) => (
              <VacancyPreview key={vacancy.id} vacancy={vacancy} />
            ))}
          </div>

          <div className="pagination-row panel">
            <span>
              Page {meta.page} of {meta.pages} • {meta.total} total vacancies
            </span>
            <div className="inline-actions">
              <button
                className="button button-secondary"
                disabled={meta.page <= 1}
                onClick={() => changePage(meta.page - 1)}
                type="button"
              >
                Previous
              </button>
              <button
                className="button button-secondary"
                disabled={meta.page >= meta.pages}
                onClick={() => changePage(meta.page + 1)}
                type="button"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </section>
  );
}
