import { Link, NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const studentLinks = [
  { to: "/", label: "Vacancies" },
  { to: "/dashboard/student", label: "Dashboard" },
  { to: "/applications/my", label: "My applications" },
];

const employerLinks = [
  { to: "/", label: "Vacancies" },
  { to: "/dashboard/employer", label: "Dashboard" },
  { to: "/vacancies/new", label: "New vacancy" },
];

export default function AppLayout() {
  const { isAuthenticated, logout, user } = useAuth();
  const links =
    user?.role === "employer"
      ? employerLinks
      : user?.role === "student"
        ? studentLinks
        : [{ to: "/", label: "Vacancies" }];

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link className="brand" to="/">
          <span className="brand-mark">IH</span>
          <span>
            <strong>InternHub</strong>
            <small>Student internship and job platform</small>
          </span>
        </Link>

        <nav className="topnav">
          {links.map((link) => (
            <NavLink
              key={link.to}
              className={({ isActive }) =>
                isActive ? "nav-link nav-link-active" : "nav-link"
              }
              to={link.to}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="topbar-actions">
          {isAuthenticated ? (
            <>
              <div className="user-chip">
                <span>{user?.email}</span>
                <small>{user?.role}</small>
              </div>
              <button className="button button-secondary" onClick={logout} type="button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link className="button button-secondary" to="/login">
                Login
              </Link>
              <Link className="button" to="/register">
                Register
              </Link>
            </>
          )}
        </div>
      </header>

      <main className="page-shell">
        <Outlet />
      </main>
    </div>
  );
}
