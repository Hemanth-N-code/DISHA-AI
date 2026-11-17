// frontend/src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  register: (email: string, pass: string, name: string) => Promise<void>;
  logout: () => void;
  quickDemoLogin: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('disha_token'));
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadUser() {
      if (token) {
        try {
          const u = await api.auth.getMe();
          setUser(u);
        } catch (e) {
          console.warn('Session expired or invalid:', e);
          localStorage.removeItem('disha_token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    }
    loadUser();
  }, [token]);

  const login = async (email: string, pass: string) => {
    const res = await api.auth.login({ email, password: pass });
    localStorage.setItem('disha_token', res.access_token);
    setToken(res.access_token);
    const u = await api.auth.getMe();
    setUser(u);
  };

  const register = async (email: string, pass: string, name: string) => {
    const res = await api.auth.register({ email, password: pass, full_name: name });
    localStorage.setItem('disha_token', res.access_token);
    setToken(res.access_token);
    const u = await api.auth.getMe();
    setUser(u);
  };

  const logout = () => {
    localStorage.removeItem('disha_token');
    setToken(null);
    setUser(null);
  };

  const quickDemoLogin = async () => {
    // Tries to login with demo student, registers if not present
    const demoEmail = 'disha-ai@gmail.com';
    const demoPass = 'DishaDemo2026!';
    const demoName = 'Disha AI';
    try {
      await login(demoEmail, demoPass);
    } catch {
      await register(demoEmail, demoPass, demoName);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, quickDemoLogin }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}
