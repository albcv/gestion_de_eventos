import { createContext, useContext, useState, useEffect} from 'react';
import type {ReactNode} from 'react';
import { fetchCsrfCookie } from '../api/auth';
import axios from '../api/axios';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  login: (userData: any) => void;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    try {
      await fetchCsrfCookie();
      const response = await axios.get('/perfil/');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = (userData: any) => {
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  if (loading) return null; // Evita renderizar hijos hasta terminar la verificación

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};