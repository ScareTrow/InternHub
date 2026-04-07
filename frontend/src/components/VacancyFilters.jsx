const CATEGORY_OPTIONS = [
  "",
  "Engineering",
  "Frontend",
  "Analytics",
  "DevOps",
  "QA",
  "Security",
  "Design",
];

export default function VacancyFilters({ filters, onChange, onSubmit, onReset }) {
  return (
    <form className="filters-grid panel" onSubmit={onSubmit}>
      <div className="field">
        <label htmlFor="title">Search</label>
        <input
          id="title"
          name="title"
          onChange={onChange}
          placeholder="Backend intern, analytics..."
          value={filters.title}
        />
      </div>

      <div className="field">
        <label htmlFor="category">Category</label>
        <select id="category" name="category" onChange={onChange} value={filters.category}>
          {CATEGORY_OPTIONS.map((option) => (
            <option key={option || "all"} value={option}>
              {option || "All categories"}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="location">Location</label>
        <input
          id="location"
          name="location"
          onChange={onChange}
          placeholder="Almaty, Remote..."
          value={filters.location}
        />
      </div>

      <div className="field">
        <label htmlFor="employment_type">Type</label>
        <select
          id="employment_type"
          name="employment_type"
          onChange={onChange}
          value={filters.employment_type}
        >
          <option value="">All types</option>
          <option value="internship">Internship</option>
          <option value="job">Job</option>
        </select>
      </div>

      <div className="filter-actions">
        <button className="button" type="submit">
          Apply filters
        </button>
        <button className="button button-secondary" onClick={onReset} type="button">
          Reset
        </button>
      </div>
    </form>
  );
}
