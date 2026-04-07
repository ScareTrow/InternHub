import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import EmployerDashboardPage from "./pages/EmployerDashboardPage";
import LoginPage from "./pages/LoginPage";
import MyApplicationsPage from "./pages/MyApplicationsPage";
import RegisterPage from "./pages/RegisterPage";
import StudentDashboardPage from "./pages/StudentDashboardPage";
import VacancyDetailsPage from "./pages/VacancyDetailsPage";
import VacancyFormPage from "./pages/VacancyFormPage";
import VacancyListPage from "./pages/VacancyListPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<VacancyListPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/vacancies/:vacancyId" element={<VacancyDetailsPage />} />

        <Route element={<ProtectedRoute allowedRoles={["student"]} />}>
          <Route path="/dashboard/student" element={<StudentDashboardPage />} />
          <Route path="/applications/my" element={<MyApplicationsPage />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["employer"]} />}>
          <Route path="/dashboard/employer" element={<EmployerDashboardPage />} />
          <Route path="/vacancies/new" element={<VacancyFormPage mode="create" />} />
          <Route path="/vacancies/:vacancyId/edit" element={<VacancyFormPage mode="edit" />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
