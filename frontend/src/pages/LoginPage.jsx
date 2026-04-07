import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, getApiErrorMessage } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const user = await login(form);
      const fallbackPath =
        user.role === "employer" ? "/dashboard/employer" : "/dashboard/student";
      navigate(location.state?.from?.pathname || fallbackPath, { replace: true });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not sign in."));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-layout">
      <div className="auth-copy">
        <span className="eyebrow">InternHub access</span>
        <h1>Sign in and continue your hiring workflow.</h1>
        <p>
          Students can track applications. Employers can manage vacancies and review
          incoming candidates.
        </p>
      </div>

      <form className="panel auth-form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            onChange={handleChange}
            required
            type="email"
            value={form.email}
          />
        </div>

        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            onChange={handleChange}
            required
            type="password"
            value={form.password}
          />
        </div>

        {error ? <div className="notice notice-error">{error}</div> : null}

        <button className="button" disabled={loading} type="submit">
          {loading ? "Signing in..." : "Login"}
        </button>

        <p className="auth-footer">
          No account yet? <Link to="/register">Create one</Link>
        </p>
      </form>
    </section>
  );
}
