import { useEffect, useState } from "react";

const DEFAULT_VALUES = {
  title: "",
  category: "Engineering",
  location: "",
  employment_type: "internship",
  description: "",
  requirements: "",
  salary_min: "",
  salary_max: "",
  is_active: true,
};

function normalizeInitialValues(initialValues) {
  return {
    ...DEFAULT_VALUES,
    ...initialValues,
    salary_min: initialValues?.salary_min ?? "",
    salary_max: initialValues?.salary_max ?? "",
  };
}

export default function VacancyForm({
  initialValues,
  loading,
  error,
  submitLabel,
  onSubmit,
}) {
  const [form, setForm] = useState(normalizeInitialValues(initialValues));

  useEffect(() => {
    setForm(normalizeInitialValues(initialValues));
  }, [initialValues]);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit({
      ...form,
      salary_min: form.salary_min === "" ? null : Number(form.salary_min),
      salary_max: form.salary_max === "" ? null : Number(form.salary_max),
    });
  }

  return (
    <form className="panel form-grid" onSubmit={handleSubmit}>
      <div className="field field-span-2">
        <label htmlFor="title">Title</label>
        <input id="title" name="title" onChange={handleChange} required value={form.title} />
      </div>

      <div className="field">
        <label htmlFor="category">Category</label>
        <input
          id="category"
          name="category"
          onChange={handleChange}
          required
          value={form.category}
        />
      </div>

      <div className="field">
        <label htmlFor="location">Location</label>
        <input
          id="location"
          name="location"
          onChange={handleChange}
          required
          value={form.location}
        />
      </div>

      <div className="field">
        <label htmlFor="employment_type">Type</label>
        <select
          id="employment_type"
          name="employment_type"
          onChange={handleChange}
          value={form.employment_type}
        >
          <option value="internship">Internship</option>
          <option value="job">Job</option>
        </select>
      </div>

      <div className="field checkbox-field">
        <label htmlFor="is_active">Active</label>
        <input
          checked={form.is_active}
          id="is_active"
          name="is_active"
          onChange={handleChange}
          type="checkbox"
        />
      </div>

      <div className="field">
        <label htmlFor="salary_min">Salary min</label>
        <input
          id="salary_min"
          min="0"
          name="salary_min"
          onChange={handleChange}
          type="number"
          value={form.salary_min}
        />
      </div>

      <div className="field">
        <label htmlFor="salary_max">Salary max</label>
        <input
          id="salary_max"
          min="0"
          name="salary_max"
          onChange={handleChange}
          type="number"
          value={form.salary_max}
        />
      </div>

      <div className="field field-span-2">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          onChange={handleChange}
          required
          rows="7"
          value={form.description}
        />
      </div>

      <div className="field field-span-2">
        <label htmlFor="requirements">Requirements</label>
        <textarea
          id="requirements"
          name="requirements"
          onChange={handleChange}
          rows="5"
          value={form.requirements}
        />
      </div>

      {error ? <div className="notice notice-error">{error}</div> : null}

      <div className="form-actions field-span-2">
        <button className="button" disabled={loading} type="submit">
          {loading ? "Saving..." : submitLabel}
        </button>
      </div>
    </form>
  );
}
