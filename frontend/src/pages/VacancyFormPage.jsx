import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api, { getApiErrorMessage } from "../api/client";
import VacancyForm from "../components/VacancyForm";

export default function VacancyFormPage({ mode }) {
  const navigate = useNavigate();
  const { vacancyId } = useParams();
  const [initialValues, setInitialValues] = useState(null);
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (mode === "edit" && vacancyId) {
      loadVacancy();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, vacancyId]);

  async function loadVacancy() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get(`/vacancies/${vacancyId}`);
      setInitialValues(response.data);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not load vacancy."));
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(payload) {
    setSaving(true);
    setError("");
    try {
      const response =
        mode === "edit"
          ? await api.put(`/vacancies/${vacancyId}`, payload)
          : await api.post("/vacancies", payload);
      navigate(`/vacancies/${response.data.id}`, { replace: true });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not save vacancy."));
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <div className="panel muted">Loading vacancy form...</div>;
  }

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <span className="eyebrow">Employer tools</span>
          <h1>{mode === "edit" ? "Edit vacancy" : "Create vacancy"}</h1>
          <p>Manage vacancy details, hiring scope, and publishing status.</p>
        </div>
      </div>

      <VacancyForm
        error={error}
        initialValues={initialValues}
        loading={saving}
        onSubmit={handleSubmit}
        submitLabel={mode === "edit" ? "Update vacancy" : "Publish vacancy"}
      />
    </section>
  );
}
