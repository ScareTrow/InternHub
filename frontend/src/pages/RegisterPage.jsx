import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const initialState = {
  email: "",
  password: "",
  role: "student",
  student_profile: {
    full_name: "",
    university: "",
    major: "",
    graduation_year: "",
    location: "",
    skills: "",
    bio: "",
  },
  employer_profile: {
    company_name: "",
    company_website: "",
    company_description: "",
    location: "",
  },
};

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, getApiErrorMessage } = useAuth();
  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleRootChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function handleStudentChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      student_profile: {
        ...current.student_profile,
        [name]: value,
      },
    }));
  }

  function handleEmployerChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      employer_profile: {
        ...current.employer_profile,
        [name]: value,
      },
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    const payload = {
      email: form.email,
      password: form.password,
      role: form.role,
      student_profile:
        form.role === "student"
          ? {
              ...form.student_profile,
              graduation_year: form.student_profile.graduation_year
                ? Number(form.student_profile.graduation_year)
                : null,
            }
          : null,
      employer_profile:
        form.role === "employer"
          ? {
              ...form.employer_profile,
              company_website: form.employer_profile.company_website || null,
            }
          : null,
    };

    try {
      const user = await register(payload);
      navigate(user.role === "employer" ? "/dashboard/employer" : "/dashboard/student", {
        replace: true,
      });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Could not create account."));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-layout register-layout">
      <div className="auth-copy">
        <span className="eyebrow">New workspace</span>
        <h1>Create a student or employer account.</h1>
        <p>
          InternHub keeps onboarding lightweight, but still captures the profile data
          needed for a believable team-project MVP.
        </p>
      </div>

      <form className="panel auth-form register-form" onSubmit={handleSubmit}>
        <div className="role-switch">
          <button
            className={form.role === "student" ? "role-pill role-pill-active" : "role-pill"}
            onClick={() => setForm((current) => ({ ...current, role: "student" }))}
            type="button"
          >
            Student
          </button>
          <button
            className={form.role === "employer" ? "role-pill role-pill-active" : "role-pill"}
            onClick={() => setForm((current) => ({ ...current, role: "employer" }))}
            type="button"
          >
            Employer
          </button>
        </div>

        <div className="field">
          <label htmlFor="register-email">Email</label>
          <input
            id="register-email"
            name="email"
            onChange={handleRootChange}
            required
            type="email"
            value={form.email}
          />
        </div>

        <div className="field">
          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            minLength="8"
            name="password"
            onChange={handleRootChange}
            required
            type="password"
            value={form.password}
          />
        </div>

        {form.role === "student" ? (
          <>
            <div className="field">
              <label htmlFor="full_name">Full name</label>
              <input
                id="full_name"
                name="full_name"
                onChange={handleStudentChange}
                required
                value={form.student_profile.full_name}
              />
            </div>
            <div className="field">
              <label htmlFor="university">University</label>
              <input
                id="university"
                name="university"
                onChange={handleStudentChange}
                required
                value={form.student_profile.university}
              />
            </div>
            <div className="field">
              <label htmlFor="major">Major</label>
              <input
                id="major"
                name="major"
                onChange={handleStudentChange}
                value={form.student_profile.major}
              />
            </div>
            <div className="field">
              <label htmlFor="graduation_year">Graduation year</label>
              <input
                id="graduation_year"
                name="graduation_year"
                onChange={handleStudentChange}
                type="number"
                value={form.student_profile.graduation_year}
              />
            </div>
            <div className="field">
              <label htmlFor="student-location">Location</label>
              <input
                id="student-location"
                name="location"
                onChange={handleStudentChange}
                value={form.student_profile.location}
              />
            </div>
            <div className="field">
              <label htmlFor="skills">Skills</label>
              <input
                id="skills"
                name="skills"
                onChange={handleStudentChange}
                placeholder="React, Python, SQL..."
                value={form.student_profile.skills}
              />
            </div>
            <div className="field field-span-2">
              <label htmlFor="student-bio">Bio</label>
              <textarea
                id="student-bio"
                name="bio"
                onChange={handleStudentChange}
                rows="4"
                value={form.student_profile.bio}
              />
            </div>
          </>
        ) : (
          <>
            <div className="field">
              <label htmlFor="company_name">Company name</label>
              <input
                id="company_name"
                name="company_name"
                onChange={handleEmployerChange}
                required
                value={form.employer_profile.company_name}
              />
            </div>
            <div className="field">
              <label htmlFor="company_website">Company website</label>
              <input
                id="company_website"
                name="company_website"
                onChange={handleEmployerChange}
                placeholder="https://company.com"
                value={form.employer_profile.company_website}
              />
            </div>
            <div className="field">
              <label htmlFor="employer-location">Location</label>
              <input
                id="employer-location"
                name="location"
                onChange={handleEmployerChange}
                value={form.employer_profile.location}
              />
            </div>
            <div className="field field-span-2">
              <label htmlFor="company_description">Company description</label>
              <textarea
                id="company_description"
                name="company_description"
                onChange={handleEmployerChange}
                rows="5"
                value={form.employer_profile.company_description}
              />
            </div>
          </>
        )}

        {error ? <div className="notice notice-error">{error}</div> : null}

        <button className="button" disabled={loading} type="submit">
          {loading ? "Creating..." : "Register"}
        </button>

        <p className="auth-footer">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </form>
    </section>
  );
}
