import { createContext, useContext, useEffect, useState } from "react";

import api, { TOKEN_STORAGE_KEY, getApiErrorMessage } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_STORAGE_KEY));
  const [user, setUser] = useState(null);
  const [isReady, setIsReady] = useState(false);

  async function fetchCurrentUser(activeToken = token) {
    if (!activeToken) {
      setUser(null);
      setIsReady(true);
      return null;
    }

    try {
      const response = await api.get("/auth/me", {
        headers: { Authorization: `Bearer ${activeToken}` },
      });
      setUser(response.data);
      return response.data;
    } catch (error) {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      setToken(null);
      setUser(null);
      throw error;
    } finally {
      setIsReady(true);
    }
  }

  useEffect(() => {
    fetchCurrentUser().catch(() => {
      setIsReady(true);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function login({ email, password }) {
    const payload = new URLSearchParams();
    payload.set("username", email);
    payload.set("password", password);

    const response = await api.post("/auth/login", payload, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const nextToken = response.data.access_token;
    localStorage.setItem(TOKEN_STORAGE_KEY, nextToken);
    setToken(nextToken);
    const currentUser = await fetchCurrentUser(nextToken);
    return currentUser;
  }

  async function register(payload) {
    await api.post("/auth/register", payload);
    return login({ email: payload.email, password: payload.password });
  }

  function logout() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isReady,
        isAuthenticated: Boolean(token && user),
        login,
        register,
        logout,
        refreshUser: fetchCurrentUser,
        getApiErrorMessage,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
