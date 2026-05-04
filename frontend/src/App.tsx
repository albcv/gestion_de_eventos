import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Login } from './pages/login';
import { Registro } from './pages/registro';
import { Inicio } from './pages/inicio';
import { Perfil } from './pages/perfil';
import { Navegación } from './components/Navegación';
import { PrivateRoute } from './components/PrivateRoute';
import { SubirTrabajo } from './pages/subirTrabajo';
import { AuthProvider, useAuth } from './components/Auth';
import { RevisarTrabajos } from './pages/revisarTrabajos.tsx';

function AppContent() {
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  const hideNavigationRoutes = ['/', '/login', '/registro'];
  const shouldShowNavigation = !hideNavigationRoutes.includes(location.pathname) && isAuthenticated;

  return (
    <div className="min-h-screen">
      {shouldShowNavigation && <Navegación />}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/inicio" element={<PrivateRoute><Inicio /></PrivateRoute>} />
        <Route path="/perfil" element={<PrivateRoute><Perfil /></PrivateRoute>} />
        <Route path="/subir-trabajo" element={<PrivateRoute><SubirTrabajo /></PrivateRoute>} />
        <Route path="/revisar-trabajos" element={<PrivateRoute><RevisarTrabajos /></PrivateRoute>} />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;